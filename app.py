import gradio as gr
from collections import defaultdict
import json

def check_determinability(configs, observed_keys, target_key):
    groups = defaultdict(list)
    for C in configs:
        omega_val = tuple(sorted((k, C.get(k)) for k in observed_keys if k in C))
        groups[omega_val].append(C)
    
    for w, group in groups.items():
        values = {C.get(target_key) for C in group}
        if len(values) > 1:
            vals = list(values)
            C1 = next(C for C in group if C.get(target_key) == vals[0])
            C2 = next(C for C in group if C.get(target_key) == vals[1])
            return ("NotDetermined", C1, C2, dict(w))
    
    delta = {w: group[0].get(target_key) for w, group in groups.items()}
    return ("Determined", delta)

def analyze(configs_json, observed_keys_str, target_key):
    try:
        configs = json.loads(configs_json)
        if not isinstance(configs, list):
            return "❌ 错误：配置必须是 JSON 列表", "", ""
        observed_keys = [k.strip() for k in observed_keys_str.split(",") if k.strip()]
        if not observed_keys:
            return "❌ 错误：观察函数至少需要一个属性", "", ""
        if not target_key.strip():
            return "❌ 错误：目标属性不能为空", "", ""
        
        result = check_determinability(configs, observed_keys, target_key.strip())
        
        if result[0] == "NotDetermined":
            _, C1, C2, w = result
            return (
                f"## ❌ NotDetermined\n\n"
                f"**观察签名**：`{json.dumps(w, ensure_ascii=False)}`\n\n"
                f"**反例对**（同一观察，不同目标）：\n\n"
                f"- C₁ 目标值 = `{C1.get(target_key.strip())}`：`{json.dumps(C1, ensure_ascii=False)}`\n"
                f"- C₂ 目标值 = `{C2.get(target_key.strip())}`：`{json.dumps(C2, ensure_ascii=False)}`\n\n"
                f"**结论**：该观察函数无法零误差确定目标。需要细化观察（增加属性）或限制配置族。",
                json.dumps([C1, C2], ensure_ascii=False, indent=2),
                ""
            )
        else:
            _, delta = result
            delta_str = {str(k): v for k, v in delta.items()}
            return (
                f"## ✅ Determined\n\n"
                f"所有观察等价类都是目标单色的（target-monochromatic）。\n\n"
                f"**决策表 δ**：\n```json\n{json.dumps(delta_str, ensure_ascii=False, indent=2)}\n```",
                "",
                json.dumps(delta_str, ensure_ascii=False, indent=2)
            )
    except Exception as e:
        return f"❌ 错误：{str(e)}", "", ""

EXAMPLE = json.dumps([
    {"id": "C1", "tool_type": "code", "has_verification": 1, "verif_hash": "valid_hash",   "output": "correct", "target": 1},
    {"id": "C2", "tool_type": "code", "has_verification": 0, "verif_hash": "none",       "output": "correct", "target": 0},
    {"id": "C3", "tool_type": "calc", "has_verification": 0, "verif_hash": "none",       "output": "correct", "target": 0},
    {"id": "C4", "tool_type": "search", "has_verification": 0, "verif_hash": "none",     "output": "correct", "target": 0},
    {"id": "C5", "tool_type": "code", "has_verification": 1, "verif_hash": "failed_hash", "output": "error",   "target": 0},
    {"id": "C6", "tool_type": "code", "has_verification": 1, "verif_hash": "forged_hash", "output": "correct", "target": 0},
    {"id": "C7", "tool_type": "search", "has_verification": 0, "verif_hash": "none",    "output": "error",   "target": 0},
    {"id": "C8", "tool_type": "calc", "has_verification": 0, "verif_hash": "none",      "output": "error",   "target": 0}
], ensure_ascii=False, indent=2)

with gr.Blocks(title="因果可观测性演示", css=".contain { max-width: 1200px; margin: auto; }") as demo:
    gr.Markdown("""
    # 因果可观测性演示
    ### Causal Observability Gap — Finite-Model Determinability Checker
    
    基于论文 *"A Theory of Target-Fact Determinability in Finite Causal Event Systems"* 的有限模型检验算法。
    
    > **核心定理**：D 可从 Ω 零误差确定 ⟺ D 在每个 Ω-等价类上为常数。
    > 
    > *D is determinable from Ω if and only if D is constant on every Ω-equivalence class.*
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("#### 输入")
            configs_input = gr.Textbox(
                label="配置族 F（JSON 列表）",
                value=EXAMPLE,
                lines=18,
                info="每个配置是一个对象。论文 10.2 节 LLM 代理审计的 8 配置已预填。"
            )
            observed_input = gr.Textbox(
                label="观察函数 Ω（可见属性，逗号分隔）",
                value="output",
                info="例如：output / output,tool_type / output,tool_type,has_verification / output,tool_type,has_verification,verif_hash"
            )
            target_input = gr.Textbox(
                label="目标函数 D（目标属性键）",
                value="target",
                info="审计者试图确定的事实"
            )
            btn = gr.Button("运行 CheckDeterminability", variant="primary")
            
            gr.Markdown("""
            #### 快速实验
            依次尝试以下观察函数，观察从 NotDetermined 到 Determined 的演进：
            1. `output` —— 仅看最终输出（Ω₀）
            2. `output,tool_type` —— 加入工具类型（Ωₜ）
            3. `output,tool_type,has_verification` —— 加入验证标志（Ωₜ,ᵥ）
            4. `output,tool_type,has_verification,verif_hash` —— 加入防篡改哈希（Ωₜ,ᵥ,ₕ）
            """)
        
        with gr.Column(scale=1):
            gr.Markdown("#### 输出")
            result_md = gr.Markdown()
            counterexample = gr.Textbox(label="反例对 Certificate", lines=6, info="NotDetermined 时输出")
            decision_table = gr.Textbox(label="决策表 Delta", lines=10, info="Determined 时输出")
    
    btn.click(analyze, inputs=[configs_input, observed_input, target_input], outputs=[result_md, counterexample, decision_table])
    
    gr.Markdown("""
    ---
    ### 算法说明
    
    本演示实现了论文 **Appendix D** 的 `CheckDeterminability` 算法：
    
    1. 按观察值 `Ω(C)` 将配置族 `F` 分组；
    2. 若某组内出现多个目标值，则返回 **NotDetermined** 及反例对 `(C₁, C₂)` 作为不可确定性的证书；
    3. 若所有组均为目标单色，则返回 **Determined** 及决策表 `δ`。
    
    该算法是论文 **Theorem 10.1** 的直接实现：对有限 `F`，返回 Determined 当且仅当 `D` 可从 `Ω` 零误差确定。
    
    ### 与 JEP 的关系
    
    JEP（Judgment / Delegation / Termination / Verification）四原语协议的核心层，正是基于该数学定理推导出的**最小稳定记录语法**——通过强制记录四类关键状态转换，打破 Ω-等价类中的目标歧义，使审计目标从数学上变为可确定。
    """)

if __name__ == "__main__":
    demo.launch()