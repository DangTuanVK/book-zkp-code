#!/usr/bin/env python3
"""Tìm phụ thuộc giữa các mã nguồn và ghi vào deps.json.

Chạy từng mã nguồn; nếu gặp NameError, tìm mã nguồn đứng trước (ưu tiên cùng
chương, gần nhất) có định nghĩa tên đó, thêm vào deps.json, trích lại và chạy
lại cho đến khi hết NameError. Dùng một lần khi lập thư mục, hoặc khi sách
thêm mã nguồn mới.

Cách dùng:  micromamba run -n zkpbook python resolve_deps.py
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPS = HERE / "deps.json"


def defines(code, name):
    n = re.escape(name)
    pats = [rf"^(?:def|class)\s+{n}\b", rf"^{n}\s*(?:,[^=\n]*)?=", rf"^[\w\s,]*\b{n}\b[\w\s,]*=[^=]",
            rf"^import\s+(?:[\w.]+\s*,\s*)*{n}\b", rf"^from\s+\S+\s+import\s+.*\b{n}\b",
            rf"^for\s+(?:[\w\s,]*\b){n}\b"]
    return any(re.search(p, code, re.M) for p in pats)


def run(b):
    env = dict(os.environ, PYTHONHASHSEED="0",
               PYTHONPATH=os.pathsep.join(str(p) for p in sorted(HERE.glob("ch[0-9]*"))))
    path = HERE / b["file"]
    p = subprocess.run([sys.executable, path.name], cwd=path.parent, env=env,
                       capture_output=True, text=True, timeout=900)
    return p.returncode, p.stderr


def main():
    deps = json.loads(DEPS.read_text()) if DEPS.exists() else {}
    for _ in range(15):
        subprocess.run([sys.executable, str(HERE / "extract.py")], check=True,
                       stdout=subprocess.DEVNULL)
        manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
        changed = False
        for i, b in enumerate(manifest):
            rc, err = run(b)
            m = re.search(r"NameError: name '(\w+)' is not defined", err)
            if rc == 0 or not m:
                continue
            name = m.group(1)
            earlier = manifest[:i]
            cands = [e for e in reversed(earlier) if e["chapter"] == b["chapter"]] + \
                    [e for e in reversed(earlier) if e["chapter"] != b["chapter"]]
            for e in cands:
                code = (HERE / e["file"]).read_text(encoding="utf-8")
                if defines(code, name):
                    lst = deps.setdefault(b["id"], [])
                    if e["id"] not in lst:
                        lst.append(e["id"])
                        print(f"{b['number']}: thiếu '{name}' -> dùng Mã nguồn {e['number']}")
                        changed = True
                    break
            else:
                print(f"{b['number']}: thiếu '{name}', không tìm thấy định nghĩa")
        DEPS.write_text(json.dumps(deps, indent=1, sort_keys=True) + "\n")
        if not changed:
            break
    subprocess.run([sys.executable, str(HERE / "extract.py")], check=True)


if __name__ == "__main__":
    main()
