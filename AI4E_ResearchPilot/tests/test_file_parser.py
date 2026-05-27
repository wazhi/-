from io import BytesIO
from src.file_parser import parse_uploaded_files

class UF:
    def __init__(self,name,data): self.name=name; self._data=data
    def getvalue(self): return self._data

def test_parse_txt_file():
    r = parse_uploaded_files([UF("a.txt", b"hello battery")])
    assert r["total_chars"] > 0
    assert any("hello" in t for t in r["texts"])
