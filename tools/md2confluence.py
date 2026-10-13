#!/usr/bin/env python3
"""Конвертирует страницы базы знаний (Markdown) в Confluence Wiki Markup.

Результат кладётся в `_build/confluence/<раздел>/<страница>.txt` вместе с PNG диаграмм.
Вставка в Confluence: Insert markup (Ctrl/Cmd+Shift+D) → Confluence Wiki → вставить текст.

Поддерживается только тот набор Markdown, который мы используем на страницах:
заголовки, абзацы, списки (вложенные через 2 пробела), таблицы, блоки кода, цитаты-панели
(ℹ️ / ⚠️ / 💡 / ✍️ / 🖼️), картинки ![подпись](diagrams/x.png) отдельной строкой, <details>/<summary>, ---,
**жирный**, *курсив*, `код`, [ссылки](url).

README.md конвертируется до раздела «## 🛠» — дальше идёт часть только для GitHub.

Использование:
    tools/md2confluence.py                 # все страницы
    tools/md2confluence.py path/to/page.md # отдельные страницы
    tools/md2confluence.py --dart-lang java  # если Confluence не знает язык dart
"""
from __future__ import annotations  # аннотации вида `str | None` на Python 3.9 (системный python3 macOS)

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_build" / "confluence"

SPECIAL = re.compile(r"([\\*_!|^+~-])")

# Скобки и «?» пишем HTML-кодами, а не через «\»: сочетания вроде {{\{\}}} (три «}» подряд)
# и {{??}} (?? — разметка цитаты) роняют конвертер Confluence с ошибкой 500.
ENTITIES = {"{": "&#123;", "}": "&#125;", "[": "&#91;", "]": "&#93;", "?": "&#63;"}

PANELS = {
    "ℹ️": "info",
    "⚠️": "warning",
    "💡": "tip",
    "✍️": "note",
}


def escape(text: str) -> str:
    text = SPECIAL.sub(r"\\\1", text)
    return "".join(ENTITIES.get(ch, ch) for ch in text)


def inline(text: str) -> str:
    """Markdown inline → wiki markup."""
    out = []
    pos = 0
    pattern = re.compile(
        r"`([^`]+)`"                      # 1 inline code
        r"|\[([^\]]+)\]\(([^)]+)\)"       # 2,3 link
        r"|\*\*(.+?)\*\*"                 # 4 bold
        r"|(?<![\w*])\*(?!\s)(.+?)\*(?!\w)"  # 5 italic
    )
    for m in pattern.finditer(text):
        out.append(escape(text[pos:m.start()]))
        if m.group(1) is not None:
            out.append("{{" + escape(m.group(1)) + "}}")
        elif m.group(2) is not None:
            out.append("[" + inline(m.group(2)).replace("|", "\\|") + "|" + m.group(3) + "]")
        elif m.group(4) is not None:
            out.append("*" + inline(m.group(4)) + "*")
        else:
            out.append("_" + inline(m.group(5)) + "_")
        pos = m.end()
    out.append(escape(text[pos:]))
    return "".join(out)


def split_row(line: str) -> list[str]:
    cells, buf, in_code = [], "", False
    for ch in line.strip().strip("|"):
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append(buf.strip())
            buf = ""
        else:
            buf += ch
    cells.append(buf.strip())
    return cells


# Языки, которые подсвечивает Confluence пользователя (макрос Code Block):
# actionscript3, applescript, bash, csharp, cpp, css, coldfusion, delphi, diff, erlang, groovy, xml (HTML и XML),
# java, javafx, javascript, php, perl, text, powershell, python, ruby, sql, sass, scala, vb, yaml.
# Dart, Kotlin, Swift, Objective-C не поддерживаются — подставляем ближайший по синтаксису язык.
LANG_MAP = {
    "kotlin": "java", "kt": "java", "kts": "java",          # классы, аннотации, строки — как в Java
    "swift": "javascript",                                    # let/var, class, import, switch/case
    "objective-c": "cpp", "objc": "cpp", "objectivec": "cpp", "c": "cpp", "c++": "cpp", "h": "cpp", "m": "cpp",
    "groovy": "groovy", "gradle": "groovy",                   # build.gradle на Groovy DSL
    "xml": "xml", "html": "xml", "plist": "xml",              # AndroidManifest.xml, Info.plist
    "json": "javascript", "yml": "yaml",
    "sh": "bash", "shell": "bash", "zsh": "bash", "console": "bash",
    "ruby": "ruby", "podfile": "ruby",                        # Podfile — это Ruby
}


def code_lang(lang: str, dart_lang: str) -> str | None:
    lang = lang.strip().lower()
    if lang in ("", "text", "gitignore", "plaintext", "protobuf", "proto", "cmake"):
        return None
    if lang == "dart":
        return dart_lang
    return LANG_MAP.get(lang, lang)


def convert(md: str, dart_lang: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    para: list[str] = []
    i = 0

    def flush():
        if para:
            out.append(inline(" ".join(s.strip() for s in para)))
            out.append("")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # H1 — это заголовок страницы в Confluence, в тело не переносим
        if line.startswith("# "):
            i += 1
            continue

        if not stripped:
            flush()
            i += 1
            continue

        # Блок кода
        if stripped.startswith("```"):
            flush()
            lang = code_lang(stripped[3:], dart_lang)
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            if lang:
                out.append(f"{{code:language={lang}|linenumbers=false}}")
                out.extend(body)
                out.append("{code}")
            else:
                out.append("{noformat}")
                out.extend(body)
                out.append("{noformat}")
            out.append("")
            continue

        # <details> / <summary>
        if stripped == "<details>":
            flush()
            title = "Ответы"
            if i + 1 < len(lines):
                m = re.match(r"\s*<summary>(.*)</summary>", lines[i + 1])
                if m:
                    title = m.group(1).strip()
                    i += 1
            out.append("{expand:" + escape(title) + "}")
            i += 1
            continue
        if stripped == "</details>":
            flush()
            out.append("{expand}")
            out.append("")
            i += 1
            continue

        # Заголовки
        m = re.match(r"(#{2,6})\s+(.*)", line)
        if m:
            flush()
            level = len(m.group(1))
            out.append(f"h{level}. {inline(m.group(2))}")
            out.append("")
            i += 1
            continue

        # Горизонтальная линия
        if re.fullmatch(r"-{3,}", stripped):
            flush()
            out.append("----")
            out.append("")
            i += 1
            continue

        # Таблица
        if stripped.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            header, body = rows[0], rows[2:] if len(rows) > 1 and re.fullmatch(r"[\s|:\-]+", rows[1]) else rows[1:]
            out.append("||" + "||".join(inline(c) or " " for c in split_row(header)) + "||")
            for r in body:
                out.append("|" + "|".join(inline(c) or " " for c in split_row(r)) + "|")
            out.append("")
            continue

        # Картинка отдельной строкой: ![подпись](diagrams/x.png) → вложение страницы x.png
        m = re.fullmatch(r"!\[[^\]]*\]\((?:[^)]*/)?([^/)]+\.png)\)", stripped)
        if m:
            flush()
            out.append(f"!{m.group(1)}|border=1!")
            out.append("")
            i += 1
            continue

        # Цитата / панель
        if stripped.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            text = " ".join(q for q in quote if q)
            if text.startswith("🖼️"):
                img = re.search(r"`([^`]+\.png)`", text)
                if img:
                    out.append(f"!{img.group(1)}|border=1!")
                    out.append("")
                    continue
            panel = next((p for e, p in PANELS.items() if text.startswith(e)), None)
            if panel:
                out.append("{" + panel + "}")
                out.append(inline(text))
                out.append("{" + panel + "}")
            else:
                out.append("{quote}")
                out.append(inline(text))
                out.append("{quote}")
            out.append("")
            continue

        # Списки
        m = re.match(r"(\s*)([-*]|\d+\.)\s+(.*)", line)
        if m:
            flush()
            while i < len(lines):
                m = re.match(r"(\s*)([-*]|\d+\.)\s+(.*)", lines[i])
                if not m:
                    break
                depth = len(m.group(1)) // 2 + 1
                marker = ("*" if m.group(2) in "-*" else "#") * depth
                text = m.group(3)
                i += 1
                # строки-продолжения пункта (с отступом, но не новый пункт)
                while (
                    i < len(lines)
                    and lines[i].startswith("  ")
                    and lines[i].strip()
                    and not re.match(r"\s*([-*]|\d+\.)\s+", lines[i])
                ):
                    text += " " + lines[i].strip()
                    i += 1
                out.append(f"{marker} {inline(text)}")
            out.append("")
            continue

        para.append(line)
        i += 1

    flush()
    return "\n".join(out).rstrip() + "\n"


def pages(args: list[str]) -> list[Path]:
    if args:
        return [Path(a).resolve() for a in args]
    result = [ROOT / "README.md"]
    for section in sorted(ROOT.glob("[0-9][0-9]-*")):
        result.extend(sorted(section.glob("*.md")))
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--dart-lang", default="java", help="язык подсветки для dart-блоков (dart, java, …)")
    a = ap.parse_args()

    for page in pages(a.files):
        source = page.read_text(encoding="utf-8")
        if page.name == "README.md":
            source = source.split("\n## 🛠")[0]  # хвост README — только для GitHub
        if not page.name.startswith("_") and "📝 Запланировано" in source and not a.files:
            continue  # заглушки ещё не написанных тем
        rel = page.relative_to(ROOT)
        target = OUT / rel.with_suffix(".txt")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(convert(source, a.dart_lang), encoding="utf-8")
        diagrams = page.parent / "diagrams"
        prefix = page.stem + "--"
        for png in diagrams.glob(prefix + "*.png") if diagrams.exists() else []:
            shutil.copy2(png, target.parent / png.name)
        print(f"→ {target.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
