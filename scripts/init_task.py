#!/usr/bin/env python3
"""init_task.py — 数模任务根初始化（task-folder.md 标准七件套）

用法：
    python init_task.py "C题_垃圾清运优化"                    # 在当前目录下建任务根
    python init_task.py "C题_垃圾清运优化" --path ~/Desktop   # 指定父目录（默认当前目录；用户指定 > 工作区 > 桌面由调用方决定）

行为：建 题目/数据/代码/结果/论文/提交 六夹 + README.md + 进度.md + 代码/README.md + requirements.txt。
已存在的文件/夹不覆盖，只补缺失项（续跑安全）。
"""
import argparse
import sys
from pathlib import Path

PROGRESS_TEMPLATE = """# {name} 数模进度

> 续跑先读本文件；每问状态：pending / doing / 收口 / 卡点。收口唯一标准 = rules/contest-workflow.md §2 收口表。

## 模式与口径
- 模式：做题（练习/比赛：___）  赛事：___  截止：___
- 数据口径登记：每问标 official / assumption / synthetic-demo（demo 结果禁止进论文）

## 拆题（粗路线：只到候选模型；详细建模轮到该问才做）
| 问 | 要什么 | 输入 | 输出 | 依赖 | 候选模型 | 口径 | 状态 |
|----|--------|------|------|------|----------|------|------|
| q1 |  |  |  |  |  |  | pending |

## 数据摸底
（表名/行数/列/缺失一眼登记；数据字典逐列：类型+含义+样值）

## 约束清单（题面逐条编号 + 常识隐含）
| # | 约束 | 来源（题面/常识/假设） |

## 假设清单
| # | 假设 | 理由 | 影响哪问 |

## 结果登记
| 文件 | 供谁用 |
|-------|--------|

## 卡点记录
（问题 + 换过什么路线 + 结论）
"""

README_TEMPLATE = """# {name}

数模竞赛任务根。目录结构：

```
题目/   题面原文 + 官方附件（只读，禁止改写）
进度.md 状态闸 —— 续跑/压缩后先读它
数据/   清洗后的衍生数据集（可由 代码/ 一键复现）
代码/   分问脚本 + requirements.txt + README（运行顺序）
结果/   q{{i}}/result_q*.csv + summary_q*.md + figs/（论文数字唯一来源）
论文/   草稿.md → 终稿 + PDF
提交/   PDF + MD5 + 支撑材料 zip
```

**续跑说明：先读 `进度.md`，从最近未收口的问接着做，禁止凭会话记忆继续。**
论文数字只能从 `结果/q*/summary_q*.md` 抄（四处同源闸）。
"""

CODE_README_TEMPLATE = """# 代码运行顺序

1. `clean_*.py` — 清洗：读 题目/原件 → 写 数据/clean_*.csv
2. `q1_*.py` … — 按问求解：读 数据/ → 写 结果/q*/
3. 全部脚本可独立复跑；随机种子已固定；输出路径一律指向 任务根/结果/

> 运行环境：`pip install -r requirements.txt`
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="数模任务根初始化")
    ap.add_argument("name", help="任务根名（如 C题_垃圾清运优化）")
    ap.add_argument("--path", default=".", help="父目录（默认当前目录）")
    args = ap.parse_args()

    root = Path(args.path).expanduser() / args.name
    root.mkdir(parents=True, exist_ok=True)
    for sub in ("题目", "数据", "代码", "结果", "论文", "提交"):
        (root / sub).mkdir(exist_ok=True)

    files = {
        root / "README.md": README_TEMPLATE.format(name=args.name),
        root / "进度.md": PROGRESS_TEMPLATE.format(name=args.name),
        root / "代码" / "README.md": CODE_README_TEMPLATE,
        root / "代码" / "requirements.txt": "numpy\npandas\nscipy\nmatplotlib\n",
    }
    for path, content in files.items():
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            print(f"  + {path.relative_to(root)}")
        else:
            print(f"  = {path.relative_to(root)}（已存在，未覆盖）")

    # 桌面根零散文件检查（task-folder.md §2.7）
    print(f"任务根就绪：{root}")
    print("下一步：题面+附件放 题目/（只读）→ 填 进度.md 拆题表 → 开算")
    return 0


if __name__ == "__main__":
    sys.exit(main())
