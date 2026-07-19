# 变分量子本征求解器（VQE）原理

## 背景/动机

经典计算机模拟量子体系随比特数指数增长（$2^N$ 维希尔伯特空间），无法处理大规模系统的哈密顿量对角化问题。VQE 是一种混合量子-经典算法，利用量子计算机制备参数化量子态，经典优化器在外部调参，逼近体系基态能量。

## 核心内容

### 算法框架

VQE 基于变分原理：对于任意归一化试探波函数 $|\psi(\theta)\rangle$，有

$$
\langle H \rangle = \langle \psi(\theta) | H | \psi(\theta) \rangle \geq E_0
$$

等号仅当 $|\psi(\theta)\rangle$ 为真实基态时成立。因此只需在量子计算机上制备 $|\psi(\theta)\rangle$，估计期望值 $\langle H \rangle$，再用经典优化器调参使期望最小化。

### 哈密顿量拆分为 Pauli 串

由于量子计算机只能直接测量计算基（Pauli-Z 基），需要将 $H$ 在 Pauli 基下展开：

$$
H = \sum_i c_i P_i, \quad P_i \in \{I, X, Y, Z\}^{\otimes N}
$$

通过线性性质，只需分别估计每个 Pauli 串的期望值再加权求和：

$$
\langle H \rangle = \sum_i c_i \langle P_i \rangle
$$

实际 Qiskit 工作流中，`SparsePauliOp` 负责存储这些 Pauli 串及其系数。每个 $P_i$ 的期望值通过在不同测量基下采样得到——对于非 Z 的 Pauli 矩阵（如 X、Y），需要在测量前添加相应的旋转门（$H$ 或 $S^\dagger H$）进行基变换。

### 对易分组优化的意义

由于全部 $4^N - 1$ 个 Pauli 串中，相互逐比特对易的串可共享同一组测量基，通过分组可大幅减少 measurement settings 数量。这在 VQE 每次期望估计的迭代中对电路运行效率至关重要。

### Ansatz 电路设计：UCCSD

UCCSD（Unitary Coupled Cluster Singles and Doubles）是一种受量子化学启发的 ansatz 构造方法：

1. **出发点**：以 Hartree-Fock 态（如 $|1100\rangle$，即较低能轨道占据）作为参考态
2. **激发算符**：构造单激发算符 $T_1$ 和双激发算符 $T_2$，描述电子从占据轨道向虚轨道的跃迁
3. **幺正化**：取 $T - T^\dagger$ 的指数形式得到幺正算符：

$$
U(\theta) = e^{T(\theta) - T^\dagger(\theta)}
$$

4. **Trotter 分解**：由于指数中各项不对易，实际电路中通过 Trotter 近似分解为一系列 Pauli 旋转门的乘积。

> UCCSD 的优势在于参数数量可控（由激发级别和分子轨道数决定），且 ansatz 在化学相关子空间中表达力强。

## 关键公式

VQE 迭代目标：

$$
\theta^* = \arg\min_\theta \sum_i c_i \langle 0 | U^\dagger(\theta) P_i U(\theta) | 0 \rangle
$$

其中 $U(\theta)$ 为 ansatz 参数化电路。

## 注意事项/常见误区

- VQE 是启发式算法，不保证收敛到全局最优——局部极小值和 barren plateau 是主要困难
- UCCSD 的 Trotter 步数需权衡精度与电路深度（Trotter 误差 vs. 噪声容忍度）
- 实际 VQE 中，Pauli 串数量随分子规模快速增长，分组策略和 shot 数分配策略直接决定收敛效率
