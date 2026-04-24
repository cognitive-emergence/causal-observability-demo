import pytest
from app import check_determinability, conflict_edges

def test_determined_case():
    """Ωₜ,ᵥ,ₕ: 防篡改哈希使目标可确定 (Section 10.2)"""
    configs = [
        {"id": "C1", "output": "correct", "tool_type": "code", "has_verification": 1, "verif_hash": "valid_hash", "target": 1},
        {"id": "C2", "output": "correct", "tool_type": "code", "has_verification": 0, "verif_hash": "none", "target": 0},
        {"id": "C3", "output": "correct", "tool_type": "calc", "has_verification": 0, "verif_hash": "none", "target": 0},
    ]
    result = check_determinability(configs, ["output", "tool_type", "has_verification", "verif_hash"], "target")
    assert result[0] == "Determined"
    assert len(result[1]) == 3

def test_not_determined_omega0():
    """Ω₀: 仅看最终输出，目标不可确定"""
    configs = [
        {"id": "C1", "output": "correct", "target": 1},
        {"id": "C2", "output": "correct", "target": 0},
    ]
    result = check_determinability(configs, ["output"], "target")
    assert result[0] == "NotDetermined"
    assert result[1].get("target") != result[2].get("target")

def test_not_determined_omega_t():
    """Ωₜ: 加入工具类型仍不足 (C1 vs C6)"""
    configs = [
        {"id": "C1", "output": "correct", "tool_type": "code", "has_verification": 1, "verif_hash": "valid_hash", "target": 1},
        {"id": "C6", "output": "correct", "tool_type": "code", "has_verification": 1, "verif_hash": "forged_hash", "target": 0},
    ]
    result = check_determinability(configs, ["output", "tool_type", "has_verification"], "target")
    assert result[0] == "NotDetermined"

def test_conflict_edges():
    """冲突图应覆盖所有目标不同的等价类对"""
    configs = [
        {"id": "C1", "output": "correct", "target": 1},
        {"id": "C2", "output": "correct", "target": 0},
    ]
    edges = conflict_edges(configs, ["output"], "target")
    assert len(edges) == 1
    assert edges[0][2] == {"output": "correct"}