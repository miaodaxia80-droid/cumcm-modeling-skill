# 求解器与代码工具链（solver-toolkit）

> 对得上：任何求解落地——选库、装环境、报错处置、复现保障。
> 原则：**首选开源免费可复现**；环境一句话能装好；代码可一键复跑。

## 一、环境基线（Python 优先）

```bash
conda create -n mcm python=3.11 numpy pandas scipy matplotlib -y
pip install statsmodels scikit-learn pulp networkx openpyxl sympy deap shap xgboost
# LaTeX 编译：TeX Live / MacTeX（XeLaTeX）
```

- 依赖锁：`代码/requirements.txt`（`pip freeze` 导出）随附录提交
- 所有脚本头部注释：输入文件 → 输出文件 → 运行顺序
- **固定种子**：`np.random.default_rng(42)`；任何随机过程可复现

## 二、库选型速查

| 任务 | 首选 | 备选 |
|------|------|------|
| LP/MIP | pulp（自带 CBC，零配置） | scipy.linprog（纯 LP）、gurobipy（要 license，学术免费） |
| 非线性优化 | scipy.optimize.minimize | 差分进化 differential_evolution、optuna |
| ODE | scipy.integrate.solve_ivp | odeint；刚性换 method="Radau"/"BDF" |
| 参数拟合 | scipy.optimize.curve_fit | lmfit、least_squares |
| 时间序列 | statsmodels（ARIMA/季节分解） | pmdarima（auto_arima）、prophet |
| 机器学习 | scikit-learn | xgboost、lightgbm |
| 排队/仿真 | numpy 自写 / simpy | simpy（离散事件） |
| 图论 | networkx | scipy.sparse.csgraph（快） |
| 表格处理 | pandas + openpyxl | polars（百万行快） |
| 统计检验 | scipy.stats | statsmodels |
| 聚类/降维 | scikit-learn | — |
| 中文画图 | matplotlib + 字体配置 | — |

## 三、报错处置表（高频翻车）

| 报错/症状 | 处置 |
|-----------|------|
| ModuleNotFoundError | 先 `pip install`；无外网 → 检查 conda/本地已有；都无 → 手写等价实现（小规模可行） |
| **CBC timeLimit 假收敛**：变体约束更松但利润更低、或与基准不可比 | 未收敛伪影（实测：120s 报 Optimal 但利润虚低 12%，TL=240 重跑恢复单调 +2.3%）。处置：提高时限/缩规模/gapRel 收紧后重解；对照时先验「放宽约束单调性」 |
| pulp 状态 Optimal 但重算 ≠ 目标值 | 线性化约束漏写（如超额 z 忘了 z ≥ Q−D）或核算口径与模型不一致（聚合口径，见 op-models §3.2）；先查约束清单再怀疑求解器 |
| 中文画图乱码 | 配 font.sans-serif（Songti SC/SimHei/Noto Sans CJK SC）+ unicode_minus=False |
| Gurobi license 报错 | 直接换 pulp（CBC）——不要为 license 停工 |
| MIP 跑不完 | ① 缩小算例验证模型正确 ② timeLimit + 输出 gap ③ 换启发式 |
| solve_ivp 发散/失败 | 查量纲、换刚性方法（BDF）、调步长 t_eval |
| curve_fit 不收敛 | 加 bounds、换初值（多起点）、换 least_squares(loss="soft_l1") |
| Infeasible（不可行） | 约束冲突：逐条注释定位；放宽（软约束+罚项） |
| Excel 读取错 | openpyxl 引擎指定；多 sheet 用 sheet_name=None 全读 |
| pandas merge 行数暴涨 | 键不唯一 → 先 drop_duplicates 或 validate="one_to_one" |
| 内存爆 | 分块读取 chunksize、降 dtype（float32）、只读需要的列 |

## 三b、求解器级证据清单（优化/方程解的验收记录，落 `结果/q*/solver_log.md`）

「状态 Optimal」只是及格线。能保存的都保存，论文与终检抽查用：

| 证据 | 怎么拿 |
|------|--------|
| primal objective + best bound + **gap** | pulp：`prob.solutionTime`；gurobipy：`objVal/objBound/MIPGap`；CBC 经 `msg=1` 日志读 |
| 最大约束违反量 / 整数违反量 | 解逐条代回约束算残差（自写检查函数，也在 `verify_task.py` 抽查范围） |
| 目标值独立重算 | 用解的数值重新算一遍目标（独立核算函数），必须与求解器目标一致（口径不一致 = `op-models.md` §3.2 类 bug） |
| 求解时间 / 求解器版本 / 随机种子 | 时间 `prob.solutionTime`；版本 `pulp.__version__` 等；种子固定（§一） |
| 原始日志 | 求解器 `logPath` 或重定向 stdout 存 `结果/q*/` |
| 关键约束逐项审计 | 最紧的 3~5 条约束：松弛量 = 0 的（顶边界）列出并解释合理性（`result-check.md` §四边界检查） |
| 不可行时冲突定位 | 逐条注释法；或 gurobi `computeIIS` / CBC IIS → 冲突约束集写进卡点记录 |
| KKT/对偶抽查（凸问题） | 对偶变量（影子价格）符号与经济含义一致；对偶间隙 ≈ 0 |

## 四、代码组织规范（附录可复现）

```
代码/
  README.md        ← 运行顺序：1) clean.py 2) q1_model.py 3) q2_...
  requirements.txt
  common.py        ← 读数据/画图/存结果的公共函数（路径常量指到任务根）
  clean_*.py  q1_*.py  q2_*.py ...
```

- 每个脚本：`if __name__ == "__main__":` 入口 + 顶部注释（做什么、产出什么文件）
- 输出全部写到 `结果/q*/`，路径用 `pathlib.Path(__file__).parent` 相对化（换机器可跑）
- 硬编码路径 = 禁止（换机器即断）
- 长运算打印进度（print 每 10%），方便长跑观察

## 五、精度与效率

- 数值统一 float64；比较用容差（`np.isclose`）不比精确相等
- 循环能向量化就向量化（numpy 广播）；10⁶ 级循环先试向量化再谈 numba
- 求解器时间盒：单问求解 ≤ 10~30 分钟（练习模式）；跑不完 → 缩规模/换启发式
- 结果四舍五入进论文（2~4 位有效数字），但结果文件保留全精度

## 六、复现闸（终检前）

- [ ] `代码/README.md` 按顺序跑一遍，能复现 `结果/` 全部数字？
- [ ] 随机种子固定？
- [ ] 无硬编码绝对路径？
- [ ] requirements.txt 与实际环境一致？

**一句话：** Python 全家桶 + pulp 兜底求解器、种子固定、路径相对化、一键复跑复现闸；报错按处置表换线不停工。
