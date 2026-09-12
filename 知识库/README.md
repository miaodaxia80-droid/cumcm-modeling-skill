# 知识库索引

建模方法论 / 求解清单 / 题型矩阵。与 `SKILL.md` 流程配合使用。

## 使用约定

- 拆题顺序：先 `modeling-core.md` 形式化（问题五分类 + 最小模型说明表）→ `打穿短表.md` 索引 → 对得上再打开对应模块看细节。文件不长就整篇开；超长篇可先开点名节，不够就继续开。**禁止每题通读本目录**
- 磁盘有 `*数模经验.md` 才开专篇，没有不算缺
- 短表和任何模块都不是上限。每题仍过全问闭环；检验认 `result-check.md` 两级检验 + 独立验证证据菜单，不是只写一句「做了灵敏度分析」。表上没有的打法照样用
- 方便和产出优先；省 token 是顺带，不挡开模块
- 短表点名的打法用标题搜。有指针的肥篇只留实战要点 + 指针段
- 与 rules 冲突时 **以 rules 为准**（完成度 `modeling-value`；论文格式 `paper-format`；节奏 `contest-workflow`）
- **本库只管「这个模型怎么建怎么算」；做不做、做几问、先做哪问、论文怎么写，全在 rules**

## 文件清单

| 文件 | 说明 |
|------|------|
| `modeling-core.md` | 通用建模核心：形式化链条、五先决判断、可识别性快检、复杂度闸（每问开算前必过） |
| `打穿短表.md` | 题型信号 → 打法索引（一行/指针；正文仍在各模块） |
| `uncertainty-and-identifiability.md` | 不确定性：CI、bootstrap、误差传播、Sobol/Morris、预测区间、鲁棒决策 |
| `data-cleaning.md` | 数据读取、清洗、缺失机制、异常、特征构造（数据题第一站） |
| `op-models.md` | 优化：LP/MIP、动态规划、启发式、多目标、不确定结构（§六b）、解验收（§六c） |
| `eval-models.md` | 评价：权重来源判定、TOPSIS/模糊/灰色/DEA、排名稳定性、稳健代码模板 |
| `predict-models.md` | 预测：回归、ARIMA、灰色 GM(1,1)、神经网络、组合预测、选型检查单 |
| `stat-models.md` | 统计：检验、方差、相关、聚类、PCA、抽样 |
| `ml-models.md` | 机器学习：树模型、交叉验证、调参、可解释性 |
| `diff-models.md` | 微分方程：人口/传染病/SIR/捕食/稳定性/数值解 |
| `numerical-models.md` | 数值建模链：方程组、PDE/差分、网格收敛、逆问题、参数校准（A 题底座） |
| `graph-models.md` | 图论：最短路、最小树、最大流、选址、匹配 |
| `sim-models.md` | 仿真：蒙特卡洛（序贯停止）、排队论、元胞自动机 |
| `signal-models.md` | 信号：FFT、小波、滤波、周期检测、特征提取、时频 |
| `spatial-models.md` | 空间：投影距离、插值、Moran's I、空间回归、覆盖选址 |
| `control-models.md` | 控制与序列决策：DP、最优控制、MDP、PID/LQR/MPC |
| `phys-geo-models.md` | 物理/几何/概率经典建模（A 题常见底座） |
| `result-check.md` | 检验：两级检验、独立验证证据菜单、灵敏度范围纪律、基线对比 |
| `plot-spec.md` | 图表规范与每题出图清单 |
| `abstract-writing.md` | 摘要 8 要素写法（评审第一关，单篇最高优先） |
| `paper-template.md` | 论文骨架 + LaTeX 模板 + 提交清单 |
| `solver-toolkit.md` | Python/求解器/环境/依赖/报错处置/求解器级证据 |

**合计：22 个知识文件**（不含本 README）。论文版式不在本库：见 `rules/paper-format.md`。完成度只认 rules，本库不定级。
