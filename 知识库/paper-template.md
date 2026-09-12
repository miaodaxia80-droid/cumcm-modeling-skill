# 论文骨架与模板（paper-template）

> 本篇给「可直接开工」的骨架：LaTeX 模板 + 章节内容清单 + 终检清单。版式细则（字体/匿名/落盘）只认 `rules/paper-format.md`。

## 一、章节骨架（每章干什么）

```
标题 + 题号
摘要页            ← abstract-writing.md 8 要素
一、问题重述       背景一句 + 问题本质一段（≤1 页）
二、问题分析       每问思路一段 + 总体技术路线流程图（必出）
三、模型假设       编号列表：假设 + 一句理由；强假设标注
四、符号说明       三列表：符号/含义/单位
五、模型建立与求解  5.1 问题一 … 5.k 问题 k（主体）
                   每问：模型推导 → 求解方法 → 结果表图 → 独立验证证据对照
六、模型的检验      两级检验的全文部分：灵敏度 + 误差 + 稳健性（result-check）
七、模型评价与推广  优点 2~3 / 缺点 1~2（诚实）/ 推广 1~2 句
参考文献           GB/T 7714；真实可核；5~12 条
附录 A 核心代码     真实运行版 + 注释；附录 B 补充数据/图
```

**写作顺序**：先 5 章（逐问闭环时同步写）→ 二、三章 → 六章检验 → 一章重述 → 摘要 → 七章评价 → 参考文献与附录。**摘要在最后写、最优先打磨。**

## 二、LaTeX 模板（国赛中文版）

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[UTF8]{ctex}           % 中文
\usepackage{geometry,amsmath,amssymb,graphicx,booktabs,caption,indentfirst}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}
\usepackage[numbers,sort&compress]{natbib}   % 引用
\linespread{1.5}

\title{\textbf{基于 XX 与 XX 的 XX 问题研究}}
\author{}                          % 匿名：不写姓名/学校/队号
\date{}

\begin{document}
\maketitle
\begin{center}{\large\textbf{摘\quad 要}}\end{center}
% 8 要素摘要（逐问模型名+数字）
\noindent\textbf{关键词：} XX；XX；XX
\newpage
\section{问题重述} ...
\section{问题分析} ... % 含流程图 \includegraphics
\section{模型假设} \begin{enumerate}...\end{enumerate}
\section{符号说明} \begin{table}...\end{table}
\section{模型建立与求解}
\subsection{问题一的模型建立与求解} ... % 公式 equation + 表 + 图
\section{模型检验} ...
\section{模型评价与推广} ...
\begin{thebibliography}{9}
\bibitem{ref1} 作者. 题名[J]. 刊名, 年, 卷(期): 页码.
\end{thebibliography}
\appendix \section{核心代码} ... % lstinputlisting 或 verbatim
\end{document}
```

- 公式编号：`\begin{equation}` 自动编号，正文 `\eqref` 引用
- 图表：`figure`/`table` 环境 + `\caption`，位置 `[htbp]`
- 代码：`\usepackage{listings}` + `\lstinputlisting`
- 编译：XeLaTeX（中文必用）；编译报错先查宏包与字体

## 三、Word 交付（用户点名时）

- 样式：正文宋体小四 1.5 倍行距；标题黑体；西文 Times New Roman
- 公式用 Word 公式编辑器/MathType；编号右侧
- 图表插入后居中，题注用交叉引用
- 匿名自查同 LaTeX 版

## 四、终检清单（交稿前逐条过 · 硬）

**反造假红线（详见 SKILL.md）**
- [ ] 论文每个数字可溯源到 `结果/q*/summary_q*.md`？
- [ ] 附录代码 = 真实运行版（能一键复跑出结果）？
- [ ] 所有图来自真实数据？
- [ ] 参考文献全部真实可核？
- [ ] 摘要每问有数字？

**数字一致性**
- [ ] 摘要 = 正文 = 图表 = 结果文件，四处一致？
- [ ] 全文有效位/千分位格式统一？

**格式**
- [ ] 摘要单独一页；关键词 3~8 个？
- [ ] 图表全部有编号、有题注、被正文引用？
- [ ] 公式编号连续且被引用？
- [ ] 匿名：全文搜索姓名/学校/地区/「我校」→ 零命中？
- [ ] 字体字号行距符合规范？
- [ ] 参考文献 GB/T 7714 格式统一？

**提交包**
- [ ] PDF 编译成功且页数合理？
- [ ] 文件名按当年要求（题号等）？
- [ ] 支撑材料 zip：代码 + 数据 + 说明 README？
- [ ] MD5 计算并登记（提交系统要求时）？

## 五、常见坑

- 摘要写完才想起来某问没做 → 终检先于摘要打磨（先勾完成度）
- LaTeX 编译报错硬扛 → 先最小化复现（注释掉一半定位）
- 引用文献格式五花八门 → 统一 thebibliography
- 附录代码不带注释、正文结果找不到对应代码段 → 代码段前加注释「对应正文 5.2」
- 忘记删作者信息占位符

**一句话：** 骨架照表、写作顺序先五后摘、终检清单逐条过、匿名与数字一致性两道闸谁也不省。
