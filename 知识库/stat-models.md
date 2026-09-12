# 统计分析（stat-models）

> 对得上：显著性、差异比较、相关性、抽样、聚类、降维、假设检验。
> 主线：数据形态 → 选检验 → 报统计量+p 值+效应量 → 可视化。

## 一、检验选择表（先判数据类型与分布）

| 问题 | 前提 | 用 |
|------|------|-----|
| 两组均值比较 | 正态、方差齐 | 双样本 t 检验；方差不齐用 Welch |
| 两组均值比较 | 非正态/小样本 | Mann-Whitney U |
| 配对前后比较 | 差值正态 | 配对 t；否则 Wilcoxon 符号秩 |
| 多组比较 | 正态、方差齐 | 单因素 ANOVA + 事后检验（Tukey HSD）；非参数用 Kruskal-Wallis |
| 比例/分类关联 | 频数表 | 卡方检验（期望频数<5 → Fisher 精确） |
| 两变量线性相关 | 近似正态 | Pearson r（**显著性 + r 值都报**）；否则 Spearman |
| 分布拟合 | — | KS 检验 / 卡方拟合优度 |
| 正态性 | — | Shapiro-Wilk（小样本）/ D'Agostino |

**纪律**：检验前提（正态性、方差齐性）必须先查并写一句；只报 p 值不报效应量（r、Cohen's d、η²）= 扣分。

## 二、多元统计

| 手法 | 用途 | 要点 |
|------|------|------|
| PCA | 高维降维/去共线 | 标准化后做；累计方差 ≥85% 定主成分个数；载荷矩阵解释成分含义 |
| 因子分析 | 找潜在维度 | 旋转（varimax）+ 因子载荷解释 |
| 系统聚类 | 小样本分层 | 树状图 + 手肘/轮廓系数定簇数 |
| K-means | 大样本分群 | 手肘法（SSE）+ 轮廓系数；标准化必须 |
| 判别分析/Logistic | 已有类别找规则 | 混淆矩阵验证 |
| 抽样调查推断 | 问卷/样本推总体 | 简单随机/分层抽样公式，置信区间（比例 z 区间），样本量论证 |

## 三、方差分析延伸

两因素 ANOVA + 交互项 → 主效应图（interaction plot）；重复测量用重复测量 ANOVA。

## 四、常见坑（假点）

- 没查正态性直接 t/ANOVA
- 卡方用在期望频数 <5 的格子
- 相关 ≠ 因果：正文写「A 导致 B」而只算了 Pearson r
- PCA 忘了标准化（量纲大的变量吞掉全部方差）
- K-means 不标准化
- 多重比较不校正（跑 20 个检验按 0.05 挑显著的）→ Bonferroni 校正或事先定主检验

## 五、实现要点

```python
from scipy import stats
t, p = stats.ttest_ind(a, b, equal_var=False)      # Welch t
H, p = stats.kruskal(*groups)                      # 非参数多组
chi2, p, dof, exp = stats.chi2_contingency(tab)    # 卡方
from sklearn.decomposition import PCA; from sklearn.preprocessing import StandardScaler
Z = StandardScaler().fit_transform(X); pcs = PCA(0.85).fit(Z)   # 保留 85% 方差
```

## 六、论文里写什么

1. 分析对象与样本量一句
2. 前提检验一句（「经 Shapiro-Wilk 检验，p=…，不拒绝正态」）
3. 检验结果表（方法、统计量、p 值、效应量、结论）
4. 一张可视化（箱线图组间对比 / 相关热力图 / 碎石图）

**一句话：** 前提先行、检验选对、统计量+p 值+效应量三件套、可视化配套；相关不写因果。
