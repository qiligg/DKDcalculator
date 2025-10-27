import streamlit as st
from typing import Optional, Dict
from risk_calculator import compute_all

st.set_page_config(page_title="DKD进展风险计算器", page_icon="🩺", layout="centered")

st.title("DKD进展风险计算器")
st.caption("使用给定的对数比值（lnOR）模型计算四个风险等级的发病风险（%）。")

with st.expander("使用说明 / 单位与取值"):
    st.markdown("""
- Age：是否年龄≥60岁（是=1，否=0）
- SBP（mmHg）、HDL-c（mmol/L）、UN（mmol/L）、UA（μmol/L）、AST（IU/L）、PTH（pg/ml）、Mg（mmol/L）、Alb（g/L）、HbA1c（%）
- 可只输入已有检测项目。每个风险等级会单独检查所需项目，缺失则提示，不会影响其他等级的计算。
- 风险（%）= 1 / (1 + e^(−lnOR)) × 100%，保留两位小数。
    """)

def parse_float(value: str) -> Optional[float]:
    value = (value or "").strip()
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None

with st.form("form"):
    col1, col2 = st.columns(2)
    with col1:
        age_flag = st.selectbox("年龄≥60岁？", options=["否 (0)", "是 (1)"], index=0)
        SBP = st.text_input("SBP（mmHg）")
        HDL_c = st.text_input("HDL-c（mmol/L）")
        UN = st.text_input("UN（mmol/L）")
        UA = st.text_input("UA（μmol/L）")
    with col2:
        AST = st.text_input("AST（IU/L）")
        PTH = st.text_input("PTH（pg/ml）")
        Mg = st.text_input("Mg（mmol/L）")
        Alb = st.text_input("Alb（g/L）")
        HbA1c = st.text_input("HbA1c（%）")

    submitted = st.form_submit_button("计算")

if submitted:
    inputs: Dict[str, Optional[float]] = {
        "Age": 1.0 if "1" in age_flag else 0.0,
        "SBP": parse_float(SBP),
        "HDL_c": parse_float(HDL_c),
        "UN": parse_float(UN),
        "UA": parse_float(UA),
        "AST": parse_float(AST),
        "PTH": parse_float(PTH),
        "Mg": parse_float(Mg),
        "Alb": parse_float(Alb),
        "HbA1c": parse_float(HbA1c),
    }

    results = compute_all(inputs)

    # 汇总表（Markdown 表格，无需额外依赖）
    st.subheader("Risk of DKD progression")

    def fmt_prob(v: Optional[float]) -> str:
        return f"{v:.2f} %" if v is not None else "—"

    low = results["Low Risk"]["prob"]
    mod = results["Moderate Risk"]["prob"]
    high = results["High Risk"]["prob"]
    vhigh = results["Very High Risk"]["prob"]

    table_md = (
        "| Low Risk | Moderate Risk | High Risk | Very High Risk |\n"
        "|---:|---:|---:|---:|\n"
        f"| {fmt_prob(low)} | {fmt_prob(mod)} | {fmt_prob(high)} | {fmt_prob(vhigh)} |"
    )
    st.markdown(table_md)

    # 缺失项提示
    for k, v in results.items():
        if v.get("error"):
            st.error(v["error"])

st.divider()
st.caption("仅用于科研/教学演示，不作为临床决定的唯一依据。")