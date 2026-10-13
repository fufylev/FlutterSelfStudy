import 'dart:ffi';
import 'dart:ui' as ui;

import 'package:ffi/ffi.dart';
import 'package:flutter/material.dart';

// Сигнатуры C-функций и их Dart-аналоги
typedef _RenderC = Void Function(Double t, Int32 w, Int32 h, Pointer<Uint8> rgba);
typedef _RenderDart = void Function(double t, int w, int h, Pointer<Uint8> rgba);
typedef _ContainsC = Int32 Function(Double t, Int32 w, Int32 h, Double x, Double y);
typedef _ContainsDart = int Function(double t, int w, int h, double x, double y);

/// Обёртка над нативной библиотекой: C++ рисует кнопку в буфер пикселей
class NativeBlob {
  NativeBlob(DynamicLibrary lib)
      : _render = lib.lookupFunction<_RenderC, _RenderDart>('blob_render'),
        _contains = lib.lookupFunction<_ContainsC, _ContainsDart>('blob_contains');

  final _RenderDart _render;
  final _ContainsDart _contains;

  /// Отрисовать форму при прогрессе t и превратить пиксели в ui.Image
  Future<ui.Image> render(double t, int size) async {
    final buffer = calloc<Uint8>(size * size * 4); // нативная память: освобождать вручную
    try {
      _render(t, size, size, buffer);
      final pixels = buffer.asTypedList(size * size * 4);
      final immutable = await ui.ImmutableBuffer.fromUint8List(pixels); // копия в память движка
      final descriptor = ui.ImageDescriptor.raw(
        immutable,
        width: size,
        height: size,
        pixelFormat: ui.PixelFormat.rgba8888,
      );
      final codec = await descriptor.instantiateCodec();
      return (await codec.getNextFrame()).image;
    } finally {
      calloc.free(buffer);
    }
  }

  bool contains(double t, int size, Offset p) => _contains(t, size, size, p.dx, p.dy) == 1;
}

class NativeBlobButton extends StatefulWidget {
  const NativeBlobButton({super.key, required this.native, required this.onPressed});

  final NativeBlob native;
  final VoidCallback onPressed;

  @override
  State<NativeBlobButton> createState() => _NativeBlobButtonState();
}

class _NativeBlobButtonState extends State<NativeBlobButton> with SingleTickerProviderStateMixin {
  static const _size = 120;
  late final _controller = AnimationController(vsync: this, duration: const Duration(milliseconds: 700))
    ..addListener(_draw);
  late final _progress = CurvedAnimation(parent: _controller, curve: Curves.elasticOut);
  ui.Image? _image;

  @override
  void initState() {
    super.initState();
    _draw();
  }

  // На каждом тике просим C++ нарисовать новый кадр
  Future<void> _draw() async {
    final image = await widget.native.render(_progress.value, _size);
    if (!mounted) return image.dispose();
    setState(() {
      _image?.dispose();
      _image = image;
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _image?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => GestureDetector(
        onTapUp: (details) {
          if (!widget.native.contains(_progress.value, _size, details.localPosition)) return; // мимо фигуры
          _controller.isForwardOrCompleted ? _controller.reverse() : _controller.forward();
          widget.onPressed();
        },
        child: SizedBox.square(dimension: _size.toDouble(), child: RawImage(image: _image)),
      );
}
