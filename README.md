title: Causal Observability Demo
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.20.0
app_file: app.py
pinned: false
---

# Causal Observability Demo

**Causal Observability Gap — Finite-Model Determinability Checker**

An interactive demonstration of the finite-model checking algorithm from the paper *"A Theory of Target-Fact Determinability in Finite Causal Event Systems"*.

---

## Core Theorem

> **D is determinable from Ω ⟺ D is constant on every Ω-equivalence class.**

This theorem defines the mathematical boundary of accountability: if the observation function Ω is not rich enough, causing configurations with different targets to fall into the same observation equivalence class, then no audit procedure can determine the target fact with zero error.

---

## Features

This Space implements the `CheckDeterminability` algorithm from **Appendix D** of the paper:

- **Input**: Finite configuration family `F` (JSON), observation function `Ω` (list of visible attributes), target function `D` (target attribute key)
- **Output**:
  - `Determined` + decision table `δ` (audit feasible)
  - `NotDetermined` + counterexample pair `(C₁, C₂)` (audit infeasible; refine observation or restrict configuration family)

Pre-loaded with the LLM agent audit case from **Section 10.2** of the paper (8 configurations), allowing direct reproduction of the observation refinement progression from Ω₀ to Ωₜ,ᵥ,ₕ.

---

## Quick Experiment

Try the following in the "Observation Function" input field in sequence:

1. `output` — output only (Ω₀) → **NotDetermined**
2. `output,tool_type` — add tool type (Ωₜ) → **NotDetermined**
3. `output,tool_type,has_verification` — add verification flag (Ωₜ,ᵥ) → **NotDetermined**
4. `output,tool_type,has_verification,verif_hash` — add tamper-resistant hash (Ωₜ,ᵥ,ₕ) → **Determined**

---

## Relationship with JEP

The core layer of the JEP (Judgment · Delegation · Termination · Verification) four-primitive accountability protocol is derived from this mathematical theorem as the **minimal stable record grammar**. The role of the four primitives is to artificially break target ambiguity within Ω-equivalence classes by mandating the recording of critical state transitions, making the audit target mathematically determinable.

---

## Papers and Code

- Mathematical foundation paper (Paper 2): *A Theory of Target-Fact Determinability in Finite Causal Event Systems*
- Protocol architecture paper (Paper 1): *Judgment, Delegation, Termination, Verification: A Minimal Grammar for AI Accountability*
- Paper PDFs and evaluation corpus available in Dataset: [cognitiveemergencelab/jep-papers-and-corpus](https://huggingface.co/datasets/yuqiangJEP/jep-papers-and-corpus)

---

## License

Apache-2.0

---

## Author

Cognitive Emergence Lab
