from __future__ import annotations

from io import BytesIO
from zipfile import ZipFile
from typing import Any

import pandas as pd
from docx import Document
from pypdf import PdfReader

MAX_TEXT_CHARS = 12000
MAX_TABLE_ROWS = 8
KEY_FILES = {
    "readme.md",
    "requirements.txt",
    "train.py",
    "main.py",
    "config.py",
    "model.py",
    "dataset.py",
    "data.py",
    "evaluate.py",
    "test.py",
}


def _safe_decode(raw: bytes) -> str:
    for enc in ("utf-8", "gbk", "latin-1"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return ""


def _clip(text: str, limit: int = MAX_TEXT_CHARS) -> str:
    return text[:limit]


def parse_uploaded_files(uploaded_files) -> dict[str, Any]:
    result = {
        "texts": [],
        "file_summaries": [],
        "code_files": [],
        "zip_tree": "",
        "total_chars": 0,
        "python_file_count": 0,
        "has_pdf": False,
        "has_docx": False,
        "has_zip": False,
        "has_log": False,
        "uploaded_count": len(uploaded_files or []),
    }
    if not uploaded_files:
        return result

    for f in uploaded_files:
        name = f.name.lower()
        raw = f.getvalue()
        suffix = name.rsplit(".", 1)[-1] if "." in name else ""

        if suffix == "pdf":
            result["has_pdf"] = True
            reader = PdfReader(BytesIO(raw))
            text = "\n".join((p.extract_text() or "") for p in reader.pages)
            text = _clip(text)
            result["texts"].append(text)
            result["file_summaries"].append(f"PDF:{f.name} 字符数={len(text)}")
        elif suffix == "docx":
            result["has_docx"] = True
            doc = Document(BytesIO(raw))
            text = _clip("\n".join(p.text for p in doc.paragraphs if p.text.strip()))
            result["texts"].append(text)
            result["file_summaries"].append(f"DOCX:{f.name} 段落字符数={len(text)}")
        elif suffix in {"txt", "md", "log", "py"}:
            text = _clip(_safe_decode(raw))
            if suffix == "log":
                result["has_log"] = True
            if suffix == "py":
                result["python_file_count"] += 1
                result["code_files"].append(f.name)
            result["texts"].append(text)
            result["file_summaries"].append(f"文本:{f.name} 字符数={len(text)}")
        elif suffix == "csv":
            df = pd.read_csv(BytesIO(raw), nrows=MAX_TABLE_ROWS)
            snippet = f"CSV:{f.name} 列={list(df.columns)}\n{df.head(MAX_TABLE_ROWS).to_markdown(index=False)}"
            result["texts"].append(_clip(snippet))
            result["file_summaries"].append(f"CSV:{f.name} 行预览={len(df)}")
        elif suffix == "xlsx":
            df = pd.read_excel(BytesIO(raw), nrows=MAX_TABLE_ROWS)
            snippet = f"XLSX:{f.name} 列={list(df.columns)}\n{df.head(MAX_TABLE_ROWS).to_markdown(index=False)}"
            result["texts"].append(_clip(snippet))
            result["file_summaries"].append(f"XLSX:{f.name} 行预览={len(df)}")
        elif suffix == "zip":
            result["has_zip"] = True
            with ZipFile(BytesIO(raw)) as zf:
                names = sorted([n for n in zf.namelist() if not n.endswith("/")])
                result["zip_tree"] = "\n".join(names[:200])
                result["python_file_count"] += sum(1 for n in names if n.endswith(".py"))
                for n in names:
                    lower = n.lower().split("/")[-1]
                    if n.endswith(".py"):
                        result["code_files"].append(n)
                    if lower in KEY_FILES:
                        content = _clip(_safe_decode(zf.read(n)))
                        result["texts"].append(f"[{n}]\n{content}")
                        result["file_summaries"].append(f"ZIP关键文件:{n}")
        else:
            result["file_summaries"].append(f"暂不解析:{f.name}")

    result["total_chars"] = sum(len(t) for t in result["texts"])
    return result
