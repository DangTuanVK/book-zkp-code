#!/usr/bin/env python3
"""Trích các khối mã Python trong sách "Chứng minh mà không tiết lộ".

Đọc thứ tự chương từ main.tex của sách, đánh số mã nguồn đúng như LaTeX
(bộ đếm `listing` theo chương, đếm mọi ngôn ngữ), ghi mỗi khối Python ra
chXX/ma_nguon_X_YY_<ten>.py và lập manifest.json cho run_all.py.

Cách dùng:  python3 extract.py [đường_dẫn_thư_mục_sách]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent / "book-zkp"
DEPS_FILE = HERE / "deps.json"   # khai báo phụ thuộc giữa các mã nguồn


def slugify(caption, max_words=5):
    """Tên file ngắn từ caption: bỏ lệnh LaTeX, bỏ dấu, nối bằng '_'."""
    s = re.sub(r"\$[^$]*\$", " ", caption)            # bỏ công thức
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", s)  # bỏ lệnh LaTeX
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    words = re.findall(r"[A-Za-z0-9]+", s.lower())
    return "_".join(words[:max_words]) or "ma_nguon"


def plain(caption):
    """Caption LaTeX -> văn bản thường (cho chú thích code và báo cáo)."""
    s = caption
    for a, b in [(r"\\mathbb\{F\}", "F"), (r"\\mathbb\{Z\}", "Z"), (r"\\text\{([^}]*)\}", r"\1"),
                 (r"\\texttt\{([^}]*)\}", r"\1"), (r"\\emph\{([^}]*)\}", r"\1"),
                 (r"\\gamma", "gamma"), (r"\\delta", "delta"), (r"\\neq", "!="),
                 (r"\\times", "x"), (r"\\to", "->"), (r"\$", ""), (r"[{}]", ""),
                 (r"--", "-"), (r"\\", "")]:
        s = re.sub(a, b, s)
    return re.sub(r"\s+", " ", s).strip()


def _strip(seg):
    out = []
    for line in seg.split("\n"):
        m = re.search(r"(?<!\\)%", line)
        out.append(line[:m.start()] if m else line)
    return "\n".join(out)


def strip_comments(tex):
    """Xóa chú thích LaTeX (%) ngoài các khối minted; giữ nguyên số dòng
    và giữ nguyên nội dung code (toán tử % của Python)."""
    parts, pos = [], 0
    for m in re.finditer(r"\\begin\{minted\}.*?\\end\{minted\}", tex, re.S):
        parts.append(_strip(tex[pos:m.start()]))
        parts.append(m.group(0))
        pos = m.end()
    parts.append(_strip(tex[pos:]))
    return "".join(parts)


def chapter_files():
    main = (BOOK / "main.tex").read_text(encoding="utf-8")
    main = strip_comments(main)
    mainmatter = main[main.index("\\mainmatter"):main.index("\\appendix")]
    chapters = re.findall(r"\\include\{chapters/(ch\d+)/main\}", mainmatter)
    return [(i + 1, BOOK / "chapters" / c / "main.tex") for i, c in enumerate(chapters)]


def page_numbers():
    """Số trang của từng mã nguồn, lấy từ main.lol (nếu đã build)."""
    lol = BOOK / "main.lol"
    pages = {}
    if lol.exists():
        for m in re.finditer(r"\\numberline \{([\d.]+)\}.*?\}\}\{(\d+)\}",
                             lol.read_text(encoding="utf-8")):
            pages[m.group(1)] = int(m.group(2))
    return pages


ENV_RE = re.compile(
    r"\\begin\{listing\}|\\end\{listing\}"
    r"|\\begin\{minted\}(?:\[[^\]]*\])?\{(?P<lang>[a-z]+)\}\n(?P<code>.*?)\\end\{minted\}",
    re.S)


def extract_chapter(chap_no, path):
    tex = strip_comments(path.read_text(encoding="utf-8"))
    blocks, number, in_listing, last_id, suffix = [], 0, False, None, 0
    for m in ENV_RE.finditer(tex):
        tok = m.group(0)
        if tok.startswith("\\begin{listing}"):
            number += 1
            in_listing = True
            suffix = 0
            continue
        if tok.startswith("\\end{listing}"):
            in_listing = False
            continue
        if m.group("lang") != "python":
            continue
        line = tex[:m.start()].count("\n") + 1
        after = tex[m.end():m.end() + 1500]
        if in_listing:
            num = f"{chap_no}.{number}"
            ident = f"{chap_no}_{number:02d}"
            cap = re.search(r"\\caption\{((?:[^{}]|\{[^{}]*\})*)\}", after)
            caption = cap.group(1) if cap else ""
        else:
            # Khối không có số: phần nối tiếp của mã nguồn ngay trước
            suffix += 1
            letter = "bcdefg"[suffix - 1]
            num = f"{chap_no}.{number}{letter}"
            ident = f"{chap_no}_{number:02d}{letter}"
            caption = "(phần nối tiếp của Mã nguồn %d.%d)" % (chap_no, number)
        # "Kết quả chạy" in trong sách (nếu có), ngay sau listing
        expected = None
        tail = after[after.find("\\end{listing}") + 13:] if in_listing else after
        em = re.match(r"\s*(?:Kết quả chạy[^\n]*\n)\s*\\begin\{minted\}(?:\[[^\]]*\])?\{text\}\n(.*?)\\end\{minted\}",
                      tail, re.S)
        if em:
            expected = em.group(1)
        blocks.append(dict(id=ident, number=num, chapter=chap_no,
                           caption=caption, tex=str(path.relative_to(BOOK)),
                           line=line, code=m.group("code"), expected=expected))
        last_id = ident
    return blocks


def header_lines(b, page, deps, by_id):
    cap = plain(b["caption"])
    h = [f"# Mã nguồn {b['number']} - {cap}",
         f"# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), "
         f"Chương {b['chapter']}" + (f", trang {page}" if page else ""),
         f"# Trích tự động từ {b['tex']} (dòng {b['line']}) bằng extract.py; "
         f"không sửa tay file này."]
    if deps:
        h.append("")
        h.append("# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ "
                 + ", ".join("Mã nguồn " + by_id[d]["number"] for d in deps) + " ---")
        h.append("import contextlib as _ctx, io as _io")
        h.append("with _ctx.redirect_stdout(_io.StringIO()):")
        for d in deps:
            h.append(f"    from {Path(by_id[d]['file']).stem} import *  # noqa")
        h.append("# --- Hết phần thêm ---")
    return h


def main():
    deps_all = json.loads(DEPS_FILE.read_text(encoding="utf-8")) if DEPS_FILE.exists() else {}
    pages = page_numbers()
    blocks = []
    for chap_no, path in chapter_files():
        blocks += extract_chapter(chap_no, path)
    by_id = {}
    for b in blocks:
        base = b["number"].rstrip("bcdefg")
        slug = slugify(b["caption"]) if not b["number"][-1].isalpha() else \
            slugify(by_id[f"{b['chapter']}_{int(base.split('.')[1]):02d}"]["caption"]) + "_tiep"
        b["file"] = f"ch{b['chapter']:02d}/ma_nguon_{b['id']}_{slug}.py"
        b["page"] = pages.get(base)
        b["deps"] = deps_all.get(b["id"], [])
        b["title"] = plain(b["caption"])
        by_id[b["id"]] = b
    for b in blocks:
        out = HERE / b["file"]
        out.parent.mkdir(parents=True, exist_ok=True)
        text = "\n".join(header_lines(b, b["page"], b["deps"], by_id)) + "\n\n" + b["code"]
        out.write_text(text, encoding="utf-8")
    manifest = [{k: v for k, v in b.items() if k != "code"} for b in blocks]
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    print(f"Đã trích {len(blocks)} khối Python từ {BOOK}")


if __name__ == "__main__":
    main()
