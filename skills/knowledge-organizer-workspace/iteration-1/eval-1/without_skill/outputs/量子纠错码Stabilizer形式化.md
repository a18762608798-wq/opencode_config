# 量子纠错码 Stabilizer 形式化

## 背景/动机

量子信息极易受退相干和噪声的影响，需要量子纠错码（QECC）来保护逻辑量子态。Stabilizer 形式化是描述一大类量子纠错码的统一数学框架，涵盖了表面码、色码、Shor 码、Steane 码等几乎所有重要的 QECC 构造。

## 核心内容

### Pauli 群

$n$ 量子比特上的 Pauli 群 $\mathcal{P}_n$ 由所有 $n$ 重张量积的 Pauli 矩阵组成（含相位因子 $\pm 1, \pm i$）：

$$
\mathcal{P}_n = \{c \cdot P_1 \otimes P_2 \otimes \cdots \otimes P_n \mid P_i \in \{I, X, Y, Z\}, \; c \in \{\pm 1, \pm i\}\}
$$

任意两个 Pauli 算符要么对易，要么反对易。这是 stabilizer 纠错码成立的基础。

### Stabilizer 群

一个 $[[n, k, d]]$ 量子码的 stabilizer 群 $\mathcal{S}$ 是 $\mathcal{P}_n$ 的一个 Abel 子群，满足 $-I \notin \mathcal{S}$。它由 $n-k$ 个独立的生成元 $\{g_1, g_2, \ldots, g_{n-k}\}$ 生成：

$$
\mathcal{S} = \langle g_1, g_2, \ldots, g_{n-k} \rangle
$$

每个生成元 $g_i \in \mathcal{P}_n$ 且 $g_i^2 = I$，所有生成元相互对易。

### 码空间

码空间 $\mathcal{C}$ 是所有 stabilizer 算符的 $+1$ 共同本征空间：

$$
\mathcal{C} = \{|\psi\rangle \mid g_i |\psi\rangle = +|\psi\rangle, \; \forall i = 1, \ldots, n-k\}
$$

$\mathcal{C}$ 的维数为 $2^k$，编码 $k$ 个逻辑量子比特。

### 逻辑算符

逻辑 $X$ 和逻辑 $Z$ 算符 $\bar{X}_j, \bar{Z}_j$（$j = 1, \ldots, k$）满足：

- 与所有 stabilizer 生成元对易（将码空间映射到自身）
- $\bar{X}_j \bar{Z}_j = -\bar{Z}_j \bar{X}_j$（在同一逻辑比特上反对易）
- 不同逻辑比特上的算符相互对易

### 错误检测：Syndrome 测量

对于 Pauli 错误 $E \in \mathcal{P}_n$，测量每个 stabilizer 生成元 $g_i$ 得到 syndrome 比特 $s_i$：

$$
s_i = 
\begin{cases}
+1, & \text{若 } [E, g_i] = 0 \\
-1, & \text{若 } \{E, g_i\} = 0
\end{cases}
$$

Syndrome 向量 $\mathbf{s} = (s_1, \ldots, s_{n-k})$ 用于识别错误，且不扰动编码态（因为测量的是 $+1/-1$ 本征空间投影）。

### 错误纠正条件

一个码可以纠正错误集 $\mathcal{E}$ 的充要条件是：对任意 $E_a, E_b \in \mathcal{E}$，

$$
E_a^\dagger E_b \in \mathcal{S} \quad \text{或} \quad E_a^\dagger E_b \notin N(\mathcal{S})
$$

其中 $N(\mathcal{S})$ 是 $\mathcal{S}$ 在 $\mathcal{P}_n$ 中的正规化子。

### 逻辑错误率随码距的指数抑制

码距 $d$ 定义为逻辑算符的最小 Pauli 权重：

$$
d = \min_{P \in N(\mathcal{S}) \setminus \mathcal{S}} \text{wt}(P)
$$

长度为 $d$ 的量子纠错码可以纠正任意 $\lfloor (d-1)/2 \rfloor$ 个错误。

对于物理错误率为 $p$ 的独立同分布噪声，逻辑错误率 $p_L$ 满足：

$$
p_L \propto \left(\frac{p}{p_\text{th}}\right)^{d/2}
$$

其中 $p_\text{th}$ 是纠错阈值。这意味着当物理错误率低于阈值时，逻辑错误率随码距 $d$ 的增加呈**指数级下降**——这是量子纠错可行的理论保证。

## 常见误区

- Stabilizer 生成元不一定对所有 Paoli 错误都检测到反对易——它们只对不与其对易的错误产生 $-1$ syndrome。完全确定错误需要足够多的生成元。
- $[[n, k, d]]$ 中的 $d$ 是**逻辑算符的最小权重**，不是生成元的最小权重。
- 码距越大虽然保护越强，但物理量子比特数通常以 $O(d^2)$ 增长（对于表面码等拓扑码），工程代价随码距平方增长。
