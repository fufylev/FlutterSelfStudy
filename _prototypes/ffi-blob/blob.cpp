#include <cstdint>
#include <cmath>
#include <vector>

namespace {
struct P { double x, y; };

const P kBlob[13] = {{.45,.05},{.75,0},{1,.3},{.95,.55},{.9,.85},{.7,1},{.45,.95},
                     {.15,.9},{0,.75},{.05,.45},{.1,.15},{.2,.08},{.45,.05}};
const P kDrop[13] = {{.5,.02},{.62,.25},{.92,.42},{.92,.65},{.92,.88},{.73,1},{.5,1},
                     {.27,1},{.08,.88},{.08,.65},{.08,.42},{.38,.25},{.5,.02}};

// Контур при прогрессе t: интерполяция 13 точек и разбиение кривых Безье на отрезки
std::vector<P> outline(double t, int w, int h) {
  P c[13];
  for (int i = 0; i < 13; ++i)
    c[i] = {(kBlob[i].x + (kDrop[i].x - kBlob[i].x) * t) * w, (kBlob[i].y + (kDrop[i].y - kBlob[i].y) * t) * h};
  std::vector<P> poly{c[0]};
  for (int s = 1; s < 13; s += 3) {
    const P a = poly.back(), b = c[s], d = c[s + 1], e = c[s + 2];
    for (int k = 1; k <= 24; ++k) {
      const double u = k / 24.0, v = 1 - u;
      poly.push_back({v*v*v*a.x + 3*v*v*u*b.x + 3*v*u*u*d.x + u*u*u*e.x,
                      v*v*v*a.y + 3*v*v*u*b.y + 3*v*u*u*d.y + u*u*u*e.y});
    }
  }
  return poly;
}

// Точка внутри многоугольника? (правило чётности пересечений)
bool inside(const std::vector<P>& poly, double x, double y) {
  bool in = false;
  for (size_t i = 0, j = poly.size() - 1; i < poly.size(); j = i++) {
    if ((poly[i].y > y) != (poly[j].y > y) &&
        x < (poly[j].x - poly[i].x) * (y - poly[i].y) / (poly[j].y - poly[i].y) + poly[i].x)
      in = !in;
  }
  return in;
}
}  // namespace

extern "C" {

// Нарисовать кнопку в буфер RGBA размером w × h (4 подвыборки на пиксель — сглаживание краёв)
void blob_render(double t, int32_t w, int32_t h, uint8_t* rgba) {
  const auto poly = outline(t, w, h);
  for (int y = 0; y < h; ++y) {
    for (int x = 0; x < w; ++x) {
      int hits = 0;
      for (int sy = 0; sy < 2; ++sy)
        for (int sx = 0; sx < 2; ++sx)
          hits += inside(poly, x + 0.25 + 0.5 * sx, y + 0.25 + 0.5 * sy);
      uint8_t* px = rgba + 4 * (y * w + x);
      const double a = hits / 4.0;  // доля покрытия → прозрачность (premultiplied alpha)
      px[0] = static_cast<uint8_t>(0x3F * a);
      px[1] = static_cast<uint8_t>(0x51 * a);
      px[2] = static_cast<uint8_t>(0xB5 * a);
      px[3] = static_cast<uint8_t>(255 * a);
    }
  }
}

// Попала ли точка нажатия в фигуру
int32_t blob_contains(double t, int32_t w, int32_t h, double x, double y) {
  return inside(outline(t, w, h), x, y) ? 1 : 0;
}
}
