from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "project_text_bundle.md"

INCLUDE_SUFFIX = {".py", ".md", ".txt", ".log", ".json", ".example", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".csv"}
EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv"}
EXCLUDE_FILES = {"project_text_bundle.md"}


def should_include(path: Path) -> bool:
    if any(p in EXCLUDE_DIRS for p in path.parts):
        return False
    if path.name in EXCLUDE_FILES:
        return False
    if path.suffix in INCLUDE_SUFFIX:
        return True
    if path.name in {"requirements.txt", ".env.example"}:
        return True
    return False


def build_bundle() -> str:
    lines = [
        "# AI4E-ResearchPilot 文本归档",
        "",
        "该文档用于在不支持二进制文件传输的环境中，以纯文本/Markdown方式共享项目源码。",
        "",
    ]

    files = [p for p in ROOT.rglob("*") if p.is_file() and should_include(p)]
    files.sort(key=lambda x: x.as_posix())

    for fp in files:
        rel = fp.relative_to(ROOT).as_posix()
        try:
            content = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = fp.read_text(encoding="latin-1", errors="replace")

        lines.extend([
            f"## `{rel}`",
            "",
            "```text",
            content.rstrip("\n"),
            "```",
            "",
        ])

    return "\n".join(lines)


if __name__ == "__main__":
    OUT.write_text(build_bundle(), encoding="utf-8")
    print(f"written: {OUT}")
