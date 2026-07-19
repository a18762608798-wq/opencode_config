# Grover 搜索算法的量子加速原理

**Date**: 2026-07-19 12:00
**Category**: Theory/Quantum Computing
**Tags**: #grover #quantum-algorithm #amplitude-amplification #quantum-interference

## Background
问答讨论了量子计算相较经典计算的速度优势，以 Grover 搜索算法为具体例子。

## Content
Grover 搜索算法是量子加速的经典案例：经典搜索无序数据库需要 O(N) 次查询，而 Grover 算法仅需 O(√N) 次查询。

算法核心步骤如下：
1. **初始化**：用 Hadamard 门将 n 个量子比特制备为所有 N=2ⁿ 个状态的等权叠加。
2. **Grover 迭代**（反复执行约 π√N/4 次）：
   - **Oracle 操作**：翻转目标态 |ω⟩ 的相位（标记正确答案）。
   - **扩散算子**（Diffusion operator）：将所有状态的振幅绕平均振幅进行翻转。
3. 经过足够次数的迭代后，目标态的振幅趋近于 1，测量时以极高概率获得正确答案。

量子加速的本质在于**量子干涉**：通过精心设计的幺正操作，让错误答案对应的振幅发生相消干涉而减小，让正确答案的振幅发生相长干涉而增大。这种全局性的振幅操控能力是经典计算无法实现的。

## Key Points
- Grover 算法实现二次加速 O(N) → O(√N)，而非指数加速
- 核心是振幅放大（amplitude amplification）技术
- Oracle 负责相位翻转，扩散算子实现"关于平均的反演"
- 量子干涉是实现振幅操控的底层物理机制
- Grover 算法不需要量子纠缠即可运行
