---
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

An interactive demonstration of target-relative determinability in a supplied finite model.

---

## Determinability Criterion

> **D is determinable from Ω ⟺ D is constant on every Ω-equivalence class.**

This is the standard quotient-factorization condition: a target function `D` can be recovered from an observation function `Ω` exactly when `D = δ ∘ Ω` for some decision rule `δ`.

For a specified configuration family `F`, two configurations with the same observation but different target values are a counterexample to zero-error determinability. No decision rule using only that observation can be correct for every configuration in `F`.

The result is relative to the supplied model. Applying it to an external problem requires justifying that the configurations, observations, and target preserve the relevant possibilities in that problem.

---

## Features

The checker in [app.py](app.py) groups configurations by observation and compares their target values:

- **Input**: Finite configuration family `F` (JSON), observation function `Ω` (list of visible attributes), target function `D` (target attribute key)
- **Output**:
  - `Determined` + decision table `δ`: the observation determines the target within the supplied model.
  - `NotDetermined` + counterexample pair `(C₁, C₂)`: the observation leaves a target conflict within the supplied model.

The preloaded agent-audit example contains eight illustrative configurations. It demonstrates observation refinement from Ω₀ to Ωₜ,ᵥ,ₕ. Refining observations or restricting the configuration family changes the model; any restriction used in a real application needs independent justification.

---

## Quick Experiment

Using the preloaded example and `target` as the target key, try the following observation fields in sequence:

1. `output` — output only (Ω₀) → **NotDetermined**
2. `output,tool_type` — add tool type (Ωₜ) → **NotDetermined**
3. `output,tool_type,has_verification` — add verification flag (Ωₜ,ᵥ) → **NotDetermined**
4. `output,tool_type,has_verification,verif_hash` — add the example's verification label (Ωₜ,ᵥ,ₕ) → **Determined**

The `verif_hash` values, such as `valid_hash` and `forged_hash`, are predefined labels in this example. The demo compares those labels; it does not calculate or authenticate hashes, verify signatures, or establish that a real verification occurred. The final result follows from the distinctions encoded in these eight configurations.

---

## Relationship with JEP

JEP represents Judgment, Delegation, Termination, and Verification events. Such records can contribute observations to a target-determinability analysis. Whether they are sufficient depends on the specified configuration family, observation function, target, and supporting evidence.

The determinability criterion does **not** derive J/D/T/V or establish that they form a unique or minimal event grammar. Expressive adequacy and minimality require separate definitions, arguments, and tests; [ART](https://github.com/cognitive-emergence/ART) treats these as research hypotheses.

Recording all four event types does not by itself make an external target determinable. Likewise, a valid signature or reference chain does not by itself establish the truth of an external claim. See the [JEP-Core draft](https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/) for the protocol's validation scope.

---

## Papers and Code

- Determinability framework: [*Target Determinability under Partial Causal Observation: A Faithful Reduction Framework*](https://doi.org/10.5281/zenodo.22673663).
- Event-grammar research: [*Judgment, Delegation, Termination, Verification: Toward a Minimal Accountability Grammar for Human-AI Agent Decision Chains*](https://doi.org/10.5281/zenodo.22716894).
- Supporting papers and evaluation corpus: [yuqiangJEP/jep-papers-and-corpus](https://huggingface.co/datasets/yuqiangJEP/jep-papers-and-corpus). This collection includes historical material and is not the normative JEP specification.
- Demo implementation and preloaded configurations: [app.py](app.py).

The demo originated with an earlier manuscript edition. Its historical section numbering should not be assumed to match the linked paper editions.

---

## License

Apache-2.0

---

## Author

Cognitive Emergence Lab
