import math
from typing import Dict, Optional, Tuple, List

def _sigmoid_pct(ln_or: float) -> float:
    """Convert ln(odds) to probability (%) with two decimals."""
    p = 1.0 / (1.0 + math.exp(-ln_or))
    return round(p * 100.0, 2)

def _check_missing(inputs: Dict[str, Optional[float]], required: List[str]) -> List[str]:
    missing = []
    for k in required:
        v = inputs.get(k, None)
        if v is None:
            missing.append(k)
    return missing

def compute_low(inputs: Dict[str, Optional[float]]) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    # Low Risk required fields
    required = ["Age", "SBP", "AST", "UA", "UN", "Mg", "PTH"]
    missing = _check_missing(inputs, required)
    if missing:
        return None, None, f"Low Risk 缺少参数: {', '.join(missing)}"

    Age = inputs["Age"]  # 0 或 1
    SBP = inputs["SBP"]
    AST = inputs["AST"]
    UA  = inputs["UA"]
    UN  = inputs["UN"]
    Mg  = inputs["Mg"]
    PTH = inputs["PTH"]

    ln_or = (-9.383
             - 1.209 * Age
             - 0.023 * SBP
             + 0.156 * AST
             - 0.005 * UA
             - 0.248 * UN
             + 6.703 * Mg
             - 0.033 * PTH)
    return ln_or, _sigmoid_pct(ln_or), None

def compute_moderate(inputs: Dict[str, Optional[float]]) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    # Moderate Risk required fields
    required = ["SBP", "Mg", "HDL_c", "PTH"]
    missing = _check_missing(inputs, required)
    if missing:
        return None, None, f"Moderate Risk 缺少参数: {', '.join(missing)}"

    SBP   = inputs["SBP"]
    Mg    = inputs["Mg"]
    HDL_c = inputs["HDL_c"]
    PTH   = inputs["PTH"]

    ln_or = (5.868
             + 0.020 * SBP
             - 7.190 * Mg
             - 1.866 * HDL_c
             + 0.029 * PTH)
    return ln_or, _sigmoid_pct(ln_or), None

def compute_high(inputs: Dict[str, Optional[float]]) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    # High Risk required fields
    required = ["Age", "Alb", "Mg", "HbA1c"]
    missing = _check_missing(inputs, required)
    if missing:
        return None, None, f"High Risk 缺少参数: {', '.join(missing)}"

    Age   = inputs["Age"]   # 0 或 1
    Alb   = inputs["Alb"]
    Mg    = inputs["Mg"]
    HbA1c = inputs["HbA1c"]

    ln_or = (7.888
             + 1.682 * Age
             - 0.214 * Alb
             - 7.015 * Mg
             - 0.506 * HbA1c)
    return ln_or, _sigmoid_pct(ln_or), None

def compute_very_high(inputs: Dict[str, Optional[float]]) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    # Very High Risk required fields
    required = ["Alb", "UN"]
    missing = _check_missing(inputs, required)
    if missing:
        return None, None, f"Very High Risk 缺少参数: {', '.join(missing)}"

    Alb = inputs["Alb"]
    UN  = inputs["UN"]

    ln_or = (-4.750
             - 0.127 * Alb
             + 0.689 * UN)
    return ln_or, _sigmoid_pct(ln_or), None

def compute_all(inputs: Dict[str, Optional[float]]) -> Dict[str, Dict[str, Optional[float] or str]]:
    """
    inputs keys:
      - Age (0/1), SBP, HDL_c, UN, UA, AST, PTH, Mg, Alb, HbA1c
    returns dict per risk:
      {
        "Low Risk": {"lnOR": float|None, "prob": float|None, "error": str|None},
        ...
      }
    """
    results = {}

    ln_or, prob, err = compute_low(inputs)
    results["Low Risk"] = {"lnOR": ln_or, "prob": prob, "error": err}

    ln_or, prob, err = compute_moderate(inputs)
    results["Moderate Risk"] = {"lnOR": ln_or, "prob": prob, "error": err}

    ln_or, prob, err = compute_high(inputs)
    results["High Risk"] = {"lnOR": ln_or, "prob": prob, "error": err}

    ln_or, prob, err = compute_very_high(inputs)
    results["Very High Risk"] = {"lnOR": ln_or, "prob": prob, "error": err}

    return results