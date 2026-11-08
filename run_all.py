#!/usr/bin/env python3
"""Chạy mọi mã nguồn Python của sách, lưu kết quả và so với sách.

Cách dùng:
    micromamba run -n zkpbook python run_all.py           # chạy tất cả
    micromamba run -n zkpbook python run_all.py 2_08 4_06 # chạy vài mã nguồn

Kết quả: ket_qua/chXX/ma_nguon_X_YY.txt (stdout + stderr) và ket_qua/BAO_CAO.md.
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "ket_qua"
TIMEOUT = 900  # giây cho mỗi mã nguồn


def normalize(text):
    return [line.rstrip() for line in text.strip("\n").split("\n")]


def compare(actual, expected):
    """Trả về danh sách dòng lệch (số dòng, sách, thực tế)."""
    a, e = normalize(actual), normalize(expected)
    diffs = []
    for i in range(max(len(a), len(e))):
        la = a[i] if i < len(a) else "<không có>"
        le = e[i] if i < len(e) else "<không có>"
        if la != le:
            diffs.append((i + 1, le, la))
    return diffs


STDOUT = {}   # stdout theo id, dùng cho khối nối tiếp (hậu tố b, c...)


def run_one(b):
    path = HERE / b["file"]
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONIOENCODING="utf-8",
               PYTHONPATH=os.pathsep.join(str(p) for p in sorted(HERE.glob("ch[0-9]*"))))
    before = set(path.parent.iterdir())
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, path.name], cwd=path.parent, env=env,
                           capture_output=True, text=True, timeout=TIMEOUT)
        rc, stdout, stderr = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as ex:
        rc, stdout, stderr = "timeout", ex.stdout or "", f"Quá {TIMEOUT} giây"
        stdout = stdout.decode() if isinstance(stdout, bytes) else stdout
    dt = time.time() - t0
    STDOUT[b["id"]] = stdout
    res = OUT / f"ch{b['chapter']:02d}" / f"ma_nguon_{b['id']}.txt"
    res.parent.mkdir(parents=True, exist_ok=True)
    body = (f"# Mã nguồn {b['number']}: {b['file']}\n"
            f"# Lệnh: python {path.name}   (mã thoát: {rc}, {dt:.1f} s)\n\n{stdout}")
    if stderr.strip():
        body += f"\n# --- stderr ---\n{stderr}"
    # File do mã nguồn tạo ra (json, onnx...) -> chuyển vào thư mục kết quả
    created = [f for f in path.parent.iterdir()
               if f not in before and f.name != "__pycache__"]
    if created:
        dest = res.parent / f"ma_nguon_{b['id']}_tep"
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        for f in created:
            shutil.move(str(f), dest / f.name)
        body += "\n# --- File tạo ra (đã chuyển vào " + dest.name + "/): " + \
                ", ".join(sorted(f.name for f in created)) + "\n"
    res.write_text(body, encoding="utf-8")
    if rc != 0:
        status = "TIMEOUT" if rc == "timeout" else "LỖI"
        diffs = None
    elif b.get("expected"):
        diffs = compare(stdout, b["expected"])
        base = b["id"].rstrip("bcdefg")
        if diffs and base != b["id"] and base in STDOUT:
            # Sách in chung kết quả của mã nguồn gốc và phần nối tiếp
            for sep in ("\n", "\n\n"):
                if not compare(STDOUT[base].rstrip("\n") + sep + stdout, b["expected"]):
                    diffs = []
                    break
        status = "KHỚP SÁCH" if not diffs else "LỆCH SÁCH"
    else:
        diffs, status = None, "CHẠY ĐƯỢC"
    return dict(status=status, rc=rc, seconds=dt, diffs=diffs, stderr=stderr,
                result=str(res.relative_to(HERE)))


def main():
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    only = set(sys.argv[1:])
    rows = []
    for b in manifest:
        if only and b["id"] not in only:
            continue
        r = run_one(b)
        rows.append((b, r))
        print(f"{b['number']:>6}  {r['status']:<10} {r['seconds']:6.1f}s  {b['file']}")
    if only:
        return
    # Báo cáo
    counts = {}
    for _, r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines = ["# Báo cáo chạy mã nguồn Python của sách", "",
             f"Python {sys.version.split()[0]}; {len(rows)} mã nguồn: "
             + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + ".", "",
             "Trạng thái: **KHỚP SÁCH** (chạy được và kết quả trùng với \"Kết quả chạy\" in trong "
             "sách), **CHẠY ĐƯỢC** (sách không in kết quả), **LỆCH SÁCH**, **LỖI**, **TIMEOUT**.", "",
             "| Mã nguồn | Trang | Nội dung | Trạng thái | Thời gian | Kết quả |",
             "|---|---|---|---|---|---|"]
    for b, r in rows:
        cap = b["title"].replace("|", "/")
        lines.append(f"| {b['number']} | {b.get('page') or ''} | {cap} | {r['status']} | "
                     f"{r['seconds']:.1f} s | [{Path(r['result']).name}]({r['result'][len('ket_qua/'):]}) |")
    problems = [(b, r) for b, r in rows if r["status"] not in ("KHỚP SÁCH", "CHẠY ĐƯỢC")]
    if problems:
        lines += ["", "## Chi tiết các mã nguồn có vấn đề", ""]
        for b, r in problems:
            lines.append(f"### Mã nguồn {b['number']} ({r['status']})")
            if r["diffs"]:
                for n, le, la in r["diffs"][:15]:
                    lines.append(f"- dòng {n}: sách `{le}` / thực tế `{la}`")
            if r["stderr"].strip():
                lines.append("```\n" + "\n".join(r["stderr"].strip().split("\n")[-8:]) + "\n```")
            lines.append("")
    (OUT / "BAO_CAO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n" + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
