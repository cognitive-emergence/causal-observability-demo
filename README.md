---
title: 因果可观测性演示
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.20.0
app_file: app.py
pinned: false
---

# 因果可观测性演示

**Causal Observability Gap — Finite-Model Determinability Checker**

基于论文 *"A Theory of Target-Fact Determinability in Finite Causal Event Systems"* 的有限模型检验算法交互演示。

---

## 核心定理

&gt; **D is determinable from Ω ⟺ D is constant on every Ω-equivalence class.**

该定理划定了问责的数学边界：若观察函数 Ω 不够丰富，导致不同目标的配置落在同一观察等价类中，则任何审计程序都无法零误差确定目标事实。

---

## 功能

本 Space 实现了论文 **Appendix D** 的 `CheckDeterminability` 算法：

- **输入**：有限配置族 `F`（JSON）、观察函数 `Ω`（可见属性列表）、目标函数 `D`（目标属性键）
- **输出**：
  - `Determined` + 决策表 `δ`（审计可行）
  - `NotDetermined` + 反例对 `(C₁, C₂)`（审计不可行，需细化观察或限制配置族）

预置了论文 **Section 10.2** 的 LLM 代理审计案例（8 个配置），可直接复现从 Ω₀ 到 Ωₜ,ᵥ,ₕ 的观察细化演进。

---

## 快速实验

依次在"观察函数"输入框中尝试：

1. `output` —— 仅看最终输出（Ω₀）→ **NotDetermined**
2. `output,tool_type` —— 加入工具类型（Ωₜ）→ **NotDetermined**
3. `output,tool_type,has_verification` —— 加入验证标志（Ωₜ,ᵥ）→ **NotDetermined**
4. `output,tool_type,has_verification,verif_hash` —— 加入防篡改哈希（Ωₜ,ᵥ,ₕ）→ **Determined**

---

## 与 JEP 的关系

JEP（Judgment · Delegation · Termination · Verification）四原语问责协议的核心层，正是基于该数学定理推导出的**最小稳定记录语法**。四原语的作用是通过强制记录关键状态转换，人为打破 Ω-等价类中的目标歧义，使审计目标在数学上变为可确定。

---

## 论文与代码

- 数学基础论文（第二篇）：*A Theory of Target-Fact Determinability in Finite Causal Event Systems*
- 协议架构论文（第一篇）：*Judgment, Delegation, Termination, Verification: A Minimal Grammar for AI Accountability*
- 论文 PDF 与评估语料见 Dataset：[cognitiveemergencelab/jep-papers-and-corpus](https://huggingface.co/datasets/cognitiveemergencelab/jep-papers-and-corpus)

---

## 许可证

Apache-2.0

---

## 作者

Cognitive Emergence Lab / Human Judgment Systems Foundation 