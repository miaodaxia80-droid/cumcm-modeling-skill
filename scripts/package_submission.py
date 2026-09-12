#!/usr/bin/env python3
"""package_submission.py — 生成提交包（Phase 6 末尾）

用法：
    python package_submission.py --root ~/Desktop/C题_垃圾清运优化_数模竞赛
    python package_submission.py --root ... --pdf 论文/终稿.pdf      # PDF 不止一个时点名

行为：
  1. 打包 代码/ + 结果/ + 数据/ → 提交/支撑材料.zip（排除 题目/ 官方原件、__pycache__、.DS_Store）
  2. 生成 提交/支撑材料文件列表.txt
  3. 计算 PDF 与 zip 的 MD5 → 提交/MD5.txt
  4. 生成 提交/提交清单.md（核对清单：文件、大小、MD5、提交前人工核对项）
"""
import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

EXCLUDE = {"__pycache__", ".DS_Store", ".ipynb_checkpoints"}


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="数模提交包生成")
    ap.add_argument("--root", required=True)
    ap.add_argument("--pdf", default=None, help="论文 PDF（默认取 论文/ 下唯一 PDF）")
    ap.add_argument("--zip-name", default="支撑材料.zip")
    args = ap.parse_args()
    root = Path(args.root).expanduser()
    if not root.exists():
        print(f"任务根不存在：{root}")
        return 1
    out = root / "提交"
    out.mkdir(exist_ok=True)

    # 1 PDF
    if args.pdf:
        pdf = root / args.pdf
    else:
        pdfs = list((root / "论文").glob("*.pdf"))
        pdf = pdfs[0] if len(pdfs) == 1 else None
        if pdf is None:
            print(f"论文/ 下有 {len(pdfs)} 个 PDF，用 --pdf 点名一个")
            return 1
    if not pdf.exists():
        print(f"PDF 不存在：{pdf}")
        return 1

    # 2 支撑材料 zip
    zip_path = out / args.zip_name
    members = []
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for sub in ("代码", "结果", "数据"):
            base = root / sub
            if not base.is_dir():
                continue
            for p in sorted(base.rglob("*")):
                if p.is_file() and not (set(p.parts) & EXCLUDE or p.name in EXCLUDE):
                    z.write(p, p.relative_to(root))
                    members.append(str(p.relative_to(root)))
    (out / "支撑材料文件列表.txt").write_text(
        "\n".join(members) + f"\n\n共 {len(members)} 个文件\n", encoding="utf-8")

    # 3 MD5
    pdf_md5, zip_md5 = md5_of(pdf), md5_of(zip_path)
    (out / "MD5.txt").write_text(
        f"{pdf_md5}  {pdf.name}\n{zip_md5}  {args.zip_name}\n", encoding="utf-8")

    # 4 提交清单
    checklist = f"""# 提交清单（{root.name}）

| 文件 | 大小 | MD5 |
|------|------|-----|
| {pdf.name} | {pdf.stat().st_size/1e6:.2f} MB | `{pdf_md5}` |
| {args.zip_name} | {zip_path.stat().st_size/1e6:.2f} MB | `{zip_md5}` |

支撑材料 {len(members)} 个文件（代码/结果/数据），官方附件原件未包含（按当年要求核对是否需附）。

## 提交前人工核对
- [ ] PDF 打开正常、页数/命名符合当年要求
- [ ] MD5 已按官网提交口录入并核对
- [ ] 支撑材料内无 题目/ 官方原件、无 demo_ 演示结果混入
- [ ] 附录代码与 结果/ 数字对应（已跑 verify_task.py，FAIL 清零）
"""
    (out / "提交清单.md").write_text(checklist, encoding="utf-8")

    print(f"PDF:  {pdf.name}  {pdf_md5}")
    print(f"ZIP:  {args.zip_name}  {zip_md5}  ({len(members)} 文件)")
    print(f"输出目录：{out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
