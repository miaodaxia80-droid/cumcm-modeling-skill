# 综合评价建模（eval-models）

> 对得上：方案择优、排名、指标体系、绩效评价、「哪个更好」。
> 主线：指标体系 → **权重来源判定** → 聚合 → 排序 → 检验（排名稳定性）。

## 一、指标体系（先建体系再谈方法）

```
题面给的指标 + 从数据里补的指标 → 分层（目标层/准则层/指标层）
每个指标登记：方向（效益型↑/成本型↓）、量纲、是否有数据支撑
无数据的指标 → 造代理指标（有依据的）或删；别放"拍脑袋指标"
```

**方向处理**：成本型正向化（取负/取倒数）后再归一化；**标准化**：z-score 或 min-max（评价内常用 min-max 到 [0,1]）。高相关指标（|r|>0.9）先合并或 PCA，否则后续熵权/加权重复计权。

## 二、赋权：先问权重从哪来（禁止默认「熵权 + AHP 各 0.5」）

| 权重来源（先判断题面给的是哪种） | 方法 | 纪律 |
|------|------|------|
| 有真实决策者/专家两两判断 | **AHP** | 判断矩阵必须来自真实偏好（队内按业务依据讨论定标度），**禁止 Agent 编造判断矩阵**；一致性 CR = CI/RI < 0.10，不过就调矩阵；正文交代判断依据 |
| 只有数据矩阵、无任何偏好信息 | **熵权 / CRITIC / 变异系数** | 数据离散度 ≠ 指标真实重要性，正文表述为「数据信息量权重」；作为客观参考 |
| 题面要求主客观结合 | 组合权重 w = α·w_主 + (1−α)·w_客 | **α 不写死 0.5**：给 α∈{0.3, 0.5, 0.7} 三档对比排名稳定性，正文写明选取依据（或按「主客观权重可信度」论证） |
| 多投入多产出效率评价 | **DEA** | CCR/BCC 模型，输出效率值与有效单元 |
| 权重高度不确定 / 要结论站得住 | **鲁棒排序** | 权重可行域内 Monte Carlo 采样 → 排名区间 + top-k 稳定概率（`uncertainty-and-identifiability.md`） |

## 三、聚合排序：按决策结构选，不全塞 TOPSIS

| 决策结构 | 方法 | 要点 |
|------|------|------|
| 补偿型（指标可互相弥补），方案较多 | **TOPSIS**（常用默认） | 贴近度 C_i = D_i⁻/(D_i⁺ + D_i⁻)；注意对归一化方法敏感、加无关方案可能秩逆转（§四检验） |
| 有等级评定（优/良/中/差） | 模糊综合评价 | 隶属度函数（三角形/梯形）+ 模糊算子合成 |
| 小样本、与参照序列比 | 灰色关联分析 | 关联系数 → 关联度排序；可与 TOPSIS 互验 |
| 存在不可补偿门槛（某项太差即一票否决） | **ELECTRE / PROMETHEE** | 级别高于关系；门槛参数须有依据 |
| 有明确效用函数/偏好结构 | MAUT | 效用函数逐指标定 + 加权 |
| 数据弱、只要排序 | 秩和比 RSR | 说服力弱，当辅助 |

**TOPSIS 注意**：正负理想解受离群方案影响；指标强相关时距离重复计权——先做 §一 的共线处理。

## 四、检验（评价类必须做：排名稳定性）

| 检验 | 做法 |
|------|------|
| 权重敏感性 | 权重在其可行域内扰动（默认 ±10% 起步，`result-check.md` §二）→ 排名前 3 是否翻盘；出「排名稳定性」结论 |
| 组合权重 α 敏感性 | α 取三档对比排序是否一致（主客观组合时必做） |
| 方法互验 | 换一种聚合（如熵权-灰色关联）排名对比，Spearman 相关系数/一致性——**一致只能写「排名接近」，不自动等于「稳健」**（`result-check.md` §三） |
| 秩逆转检验 | 增/删一个方案重排，看原方案名次是否漂移（TOPSIS 已知缺陷，点名交代） |
| top-k 稳定概率 | 权重 Monte Carlo 采样下前 k 名保持不变的概率（鲁棒排序时给） |
| 合理性对照 | 前后名差距可解释（第一名为什么高：哪些指标拉动） |
| 聚类辅助（可选） | 评价对象先聚类分层，再看层内排名——展示结构 |

## 五、常见坑（假点）

- 全部指标同向化之前就加权 → 成本型指标把结果带反
- Agent 自己编 AHP 判断矩阵 → 判断不是真实偏好，「假设合理性」扣分（比不做 AHP 更糟）
- 「客观权重 + 主观权重各 0.5」无依据 → α 必须给论证或敏感性
- 熵权被当「指标重要性」解释 → 它只反映样本离散度
- 指标间强共线（GDP 与财政收入之类）没处理 → 熵权被扭曲；先看相关矩阵
- 排名出来了不解释为什么 → 「表述清晰度」扣分；必须给前几名的拉动因子
- 「两种方法排名一致」写成「模型稳健」→ 只能写「排名接近」（同源风险，`result-check.md` §三）

## 六、实现模板（熵权-TOPSIS 稳健版，含自检）

常数列/全零列/缺失/非数值/正负指标/分母为零/并列名次全部处理（直接 `python 知识库模板` 里的 `__main__` 自检可验）：

```python
import numpy as np, pandas as pd

def entropy_topsis(csv_path, benefit=None):
    """熵权-TOPSIS 稳健版。benefit: 长度=列数的 bool 列表（True=效益型）；None=全效益型。
    处理：非数值值报错、缺失中位数填、常数列权重归零、全零列护栏、成本型正向化、零距离护栏、并列名次。"""
    X = pd.read_csv(csv_path)
    for col in X.columns:                                   # 只拦「转不成数值的非空值」；NaN 走下面的填充
        if not pd.api.types.is_numeric_dtype(X[col]):
            coerced = pd.to_numeric(X[col], errors="coerce")
            bad = coerced.isna() & X[col].notna()
            assert not bad.any(), f"列 {col} 含无法数值化的值：先清洗（data-cleaning.md），不要硬算"
            X[col] = coerced
    X = X.fillna(X.median())                               # 缺失兜底（正常应已在清洗期处理）
    Xv = X.to_numpy(float)
    if benefit is not None:                                # 成本型 → 取倒数正向化（零值护栏）
        Xv[:, ~np.asarray(benefit, bool)] = 1.0 / np.where(Xv[:, ~np.asarray(benefit, bool)] == 0, 1e-12, Xv[:, ~np.asarray(benefit, bool)])
    rng = Xv.max(0) - Xv.min(0)
    const = rng < 1e-12                                    # 常数列：无区分度
    safe_rng = np.where(const, 1.0, rng)
    Xn = (Xv - Xv.min(0)) / safe_rng                       # min-max；常数列 → 全 0（不产生 NaN）
    col_sum = Xn.sum(0)
    P = Xn / np.where(col_sum == 0, 1.0, col_sum)          # 全零列分母护栏
    e = -(P * np.log(P + 1e-12)).sum(0) / np.log(max(len(X), 2))
    w = (1 - e) / max((1 - e).sum(), 1e-12)
    w = np.where(const, 0.0, w)                            # 常数列权重归零
    ws = w.sum()
    w = w / ws if ws > 1e-12 else np.full(w.shape, 1.0 / w.size)  # 全常数列兜底：等权（本就无区分度，正文须交代）
    V = Xn * w
    Dp = np.sqrt(((V - V.max(0))**2).sum(1)); Dn = np.sqrt(((V - V.min(0))**2).sum(1))
    C = Dn / np.maximum(Dp + Dn, 1e-12)                    # 单一方案/零距离护栏
    return pd.DataFrame({"得分": C.round(4),
                         "名次": pd.Series(C).rank(ascending=False, method="min").astype(int)})

if __name__ == "__main__":
    # 最小自检：常数列不产生 NaN 且权重为 0；非数值列被拦截；并列名次正确
    pd.DataFrame({"a": [1, 2, 3], "b": [5, 5, 5]}).to_csv("_t1.csv", index=False)
    assert not entropy_topsis("_t1.csv").isna().any().any()
    pd.DataFrame({"a": [1, "x", 3]}).to_csv("_t2.csv", index=False)
    try:
        entropy_topsis("_t2.csv"); raise SystemExit("非数值列未被拦截")
    except AssertionError:
        pass
    pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 1]}).to_csv("_t3.csv", index=False)
    assert entropy_topsis("_t3.csv")["名次"].tolist() == [2, 2, 1]   # 前两行相同 → 并列 2
    print("self-test OK")
```

## 七、论文里写什么

1. 指标体系表（层级 + 方向 + 来源）
2. **权重来源判定一段**（为什么用这种赋权）+ 权重表（CR 值/α 敏感性，如适用）
3. 聚合公式 + **完整排名表**（对象 × 得分 × 名次，含并列）
4. 一张核心图（排名条形图 / 雷达图 / 帕累托图）
5. 排名稳定性结论（权重扰动、α 档位、方法互验——措辞按 `result-check.md` §三 纪律）

**一句话：** 指标分层正向化、权重先问来源（真实判断才 AHP、纯数据才熵权、组合必做 α 敏感性）、聚合按决策结构选、排名稳定性检验到 top-k、方法一致只写「接近」不写「稳健」。
