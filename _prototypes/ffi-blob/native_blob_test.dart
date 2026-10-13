import 'dart:ffi' show DynamicLibrary;
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:oopcheck/anim/native_blob.dart';

void main() {
  final native = NativeBlob(DynamicLibrary.open('native/libblob.dylib'));

  testWidgets('C++ рисует кадры', (tester) async {
    tester.view.physicalSize = const Size(900, 200);
    tester.view.devicePixelRatio = 1;
    final images = <ui.Image>[];
    await tester.runAsync(() async {
      for (final t in [0.0, 0.25, 0.5, 0.75, 1.0]) {
        images.add(await native.render(t, 120));
      }
    });
    final key = GlobalKey();
    await tester.pumpWidget(RepaintBoundary(key: key, child: ColoredBox(color: Colors.white,
      child: Row(mainAxisSize: MainAxisSize.min, textDirection: TextDirection.ltr, children: [
        for (final image in images) SizedBox(width: 170, height: 170, child: Center(child: RawImage(image: image))),
      ]))));
    await tester.runAsync(() async {
      final boundary = key.currentContext!.findRenderObject()! as RenderRepaintBoundary;
      final png = await (await boundary.toImage(pixelRatio: 1.5)).toByteData(format: ui.ImageByteFormat.png);
      File('native/frames.png').writeAsBytesSync(png!.buffer.asUint8List());
    });
    print('OUT кадров отрисовано на C++: ${images.length}, размер ${images.first.width}×${images.first.height}');
  });

  testWidgets('кнопка и нажатия', (tester) async {
    var taps = 0;
    await tester.runAsync(() async {
      await tester.pumpWidget(MaterialApp(home: Center(child: NativeBlobButton(native: native, onPressed: () => taps++))));
      await Future<void>.delayed(const Duration(milliseconds: 50));
    });
    await tester.pump();
    final origin = tester.getTopLeft(find.byType(NativeBlobButton));
    await tester.tapAt(origin + const Offset(4, 4));
    await tester.tapAt(origin + const Offset(60, 60));
    print('OUT нажатий: $taps (угол мимо фигуры не считается)');
    final image = tester.widget<RawImage>(find.byType(RawImage)).image;
    print('OUT на экране изображение от C++: ${image != null}');
  });
}
