#!/usr/bin/env python3
"""verify_task.py — 数模任务根自动验收（Phase 6 终检 / 每问收口后抽查）

用法：
    python verify_task.py --root ~/Desktop/C题_垃圾清运优化_数模竞赛

检查项（PASS/WARN/FAIL，FAIL 使退出码为 1）：
  1. 七件套结构 + 进度.md 存在且有拆题表
  2. 已收口问的结果三件套齐全（result csv + summary md + figs 图）
  3. 结果/数据 CSV 无 NaN/Inf 空洞
  4. 数字溯源：summary_q*.md 的数字出现在论文草稿/终稿中
  5. 匿名扫描：论文中出现 我校/我们学校/我们学院/姓名类标记 → FAIL
  6. PDF 页数与大小（--max-pages 默认 50，--max-mb 默认 20）
  7. 代码语法可编译（py_compile）+ 随机模块使用但未固定种子 → WARN
  8. demo_ 前缀结果文件清单（提示：禁止进论文）
"""
import argparse
import csv
import py_compile
import re
import sys
from pathlib import Path

NUM_RE = re.compile(r"\d[\d,\s]*(?:\.\d+)?")
STATUS_RE = re.compile(r"\b(pending|doing|收口|卡点)\b")
ANON_HARD = ("我校", "我们学校", "我们学院", "指导教师", "指导老师")
ANON_SOFT = ("大学", "学院", "学校", "队号小明")


def check(name: str, level: str, detail: str = "") -> tuple[str, str, str]:
    print(f"[{level:^4}] {name}" + (f" — {detail}" if detail else ""))
    return name, level, detail


def main() -> int:
    ap = argparse.ArgumentParser(description="数模任务根自动验收")
    ap.add_argument("--root", required=True)
    ap.add_argument("--max-pages", type=int, default=50)
    ap.add_argument("--max-mb", type=int, default=20)
    args = ap.parse_args()
    root = Path(args.root).expanduser()
    if not root.exists():
        print(f"任务根不存在：{root}")
        return 1

    fails, warns = [], []

    def record(name: str, level: str, detail: str = "") -> None:
        print(f"[{level:^4}] {name}" + (f" — {detail}" if detail else ""))
        if level == "FAIL":
            fails.append(name)
        elif level == "WARN":
            warns.append(name)

    # 1 结构
    missing = [d for d in ("题目", "数据", "代码", "结果", "论文") if not (root / d).is_dir()]
    prog = root / "进度.md"
    if missing or not prog.exists():
        record("结构七件套", "FAIL", f"缺 {missing + (['进度.md'] if not prog.exists() else [])}")
    else:
        text = prog.read_text(encoding="utf-8")
        statuses = STATUS_RE.findall(text)
        if "|" not in text or "q1" not in text:
            record("进度.md 拆题表", "FAIL", "没有拆题表或无 q1 行")
        else:
            record("结构 + 拆题表", "PASS", f"状态统计: {dict((s, statuses.count(s)) for s in set(statuses)) or '空'}")

    # 2 收口问的结果三件套
    qdirs = sorted((root / "结果").glob("q*")) if (root / "结果").is_dir() else []
    if not qdirs:
        record("结果目录", "WARN", "结果/q* 还没有任何问的结果")
    for qd in qdirs:
        miss = []
        if not list(qd.glob("*.csv")) and not list(qd.glob("*.json")):
            miss.append("result csv")
        if not list(qd.glob("summary*.md")):
            miss.append("summary md")
        figs = qd / "figs"
        if not figs.is_dir() or not list(figs.glob("*.png")):
            miss.append("figs 图")
        record(f"{qd.name} 三件套", "FAIL" if miss else "PASS", "缺 " + "、".join(miss) if miss else "")

    # 3 CSV NaN/Inf
    bad_cells = 0
    for csvf in list(root.rglob("结果/**/*.csv")) + list(root.rglob("数据/*.csv")):
        with open(csvf, newline="", encoding="utf-8", errors="replace") as f:
            for row in csv.reader(f):
                bad_cells += sum(1 for c in row if c.strip().lower() in {"nan", "inf", "-inf", "infinity", "-infinity"})
    record("CSV NaN/Inf 扫描", "FAIL" if bad_cells else "PASS", f"{bad_cells} 个空洞" if bad_cells else "")

    # 4 数字溯源：summary 数字 → 论文
    papers = [p for pat in ("*.md", "*.tex") for p in (root / "论文").glob(pat)]
    paper_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in papers) if papers else ""
    if not paper_text:
        record("数字溯源", "WARN", "论文/ 还没有草稿或终稿")
    else:
        norm = lambda s: re.sub(r"[\s,]", "", s)
        pt = norm(paper_text)
        missing_nums = []
        for sm in root.rglob("结果/q*/summary*.md"):
            for raw in NUM_RE.findall(sm.read_text(encoding="utf-8")):
                n = norm(raw)
                if len(n) >= 2 and "." in n and n not in pt:   # 只查带小数点的关键数值
                    missing_nums.append(f"{sm.parent.name}:{raw}")
        record("数字溯源", "FAIL" if missing_nums else "PASS", f"论文中找不到: {missing_nums[:8]}" if missing_nums else "summary 小数全部可溯源")

    # 5 匿名扫描
    anon_hits = []
    for p in papers:
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if any(k in line for k in ANON_HARD):
                anon_hits.append(f"{p.name}:{i}")
            elif any(k in line for k in ANON_SOFT) and "参考" not in line and "[" not in line:
                warns.append(f"匿名(soft)") if "匿名(soft)" not in warns else None
                anon_hits.append(f"{p.name}:{i}(soft)")
    record("匿名硬扫描", "FAIL" if any("(soft)" not in h for h in anon_hits) else ("WARN" if anon_hits else "PASS"),
           "; ".join(anon_hits[:6]) if anon_hits else "")

    # 6 PDF
    for pdf in (root / "论文").glob("*.pdf"):
        mb = pdf.stat().st_size / 1e6
        raw = pdf.read_bytes()
        pages = len(re.findall(rb"/Type\s*/Page[^s]", raw))
        ok = mb <= args.max_mb and pages <= args.max_pages
        record(f"PDF {pdf.name}", "PASS" if ok else "FAIL", f"{pages} 页 / {mb:.1f} MB（上限 {args.max_pages} 页 / {args.max_mb} MB）")
    if not list((root / "论文").glob("*.pdf")):
        record("PDF", "WARN", "还没有终稿 PDF")

    # 7 代码
    for py in (root / "代码").rglob("*.py"):
        try:
            py_compile.compile(str(py), doraise=True)
        except py_compile.PyCompileError as e:
            record(f"代码 {py.name}", "FAIL", str(e).splitlines()[0])
            continue
        src = py.read_text(encoding="utf-8", errors="replace")
        uses_rand = re.search(r"np\.random|random\.|sample\(|shuffle", src)
        has_seed = re.search(r"seed|default_rng", src)
        if uses_rand and not has_seed:
            record(f"代码 {py.name}", "WARN", "用了随机但未固定种子")
    record("代码扫描", "PASS", f"{len(list((root / '代码').rglob('*.py')))} 个文件语法通过" if not any("代码" in f for f in fails) else "")

    # 8 demo 清单
    demos = [str(p.relative_to(root)) for p in root.rglob("结果/**/demo_*")]
    record("demo 数据清单", "PASS", "；".join(demos) + "（禁止进论文）" if demos else "无 demo 文件")

    print("\n==== 汇总 ====")
    print(f"FAIL {len(fails)} | WARN {len(warns)}")
    if fails:
        print("FAIL 项：", "、".join(dict.fromkeys(fails)))
    if warns:
        print("WARN 项：", "、".join(dict.fromkeys(warns)))
    print("结论：", "有 FAIL，先修再交" if fails else "无 FAIL；WARN 逐条人工确认")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
