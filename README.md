# 因果可观测性演示

**Causal Observability Gap — Finite-Model Determinability Checker**

基于论文 *"A Theory of Target-Fact Determinability in Finite Causal Event Systems"* 的有限模型检验算法交互演示。

## 核心定理

&gt; **D is determinable from Ω ⟺ D is constant on every Ω-equivalence class.**

## 快速实验

依次在"观察函数"输入框中尝试：

1. `output` → **NotDetermined**
2. `output,tool_type` → **NotDetermined**
3. `output,tool_type,has_verification` → **NotDetermined**
4. `output,tool_type,has_verification,verif_hash` → **Determined**

## 与 JEP 的关系

JEP（Judgment · Delegation · Termination · Verification）四原语问责协议的核心层，正是基于该数学定理推导出的**最小稳定记录语法**。

## 许可证

Apache-2.0

## 作者

Cognitive Emergence Lab / Human Judgment Systems Foundation 