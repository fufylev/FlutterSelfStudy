import 'dart:ui';

// Обе формы — одинаковый набор точек: старт + 4 кривые Безье (по 3 точки). Координаты в долях 0…1
const _blob = [
  Offset(.45, .05), Offset(.75, 0), Offset(1, .3), Offset(.95, .55), Offset(.9, .85), Offset(.7, 1), Offset(.45, .95),
  Offset(.15, .9), Offset(0, .75), Offset(.05, .45), Offset(.1, .15), Offset(.2, .08), Offset(.45, .05),
];
const _drop = [
  Offset(.5, .02), Offset(.62, .25), Offset(.92, .42), Offset(.92, .65), Offset(.92, .88), Offset(.73, 1), Offset(.5, 1),
  Offset(.27, 1), Offset(.08, .88), Offset(.08, .65), Offset(.08, .42), Offset(.38, .25), Offset(.5, .02),
];

/// Форма при прогрессе t: 0 — клякса, 1 — капля. Каждая точка интерполируется отдельно
Path blobPath(Size size, double t) {
  final p = [for (var i = 0; i < 13; i++) Offset.lerp(_blob[i], _drop[i], t)!.scale(size.width, size.height)];
  final path = Path()..moveTo(p[0].dx, p[0].dy);
  for (var i = 1; i < 13; i += 3) {
    path.cubicTo(p[i].dx, p[i].dy, p[i + 1].dx, p[i + 1].dy, p[i + 2].dx, p[i + 2].dy);
  }
  return path..close();
}
