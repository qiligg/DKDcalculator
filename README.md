# DKD 进展风险计算器

本项目实现了基于给定系数的 lnOR 风险计算，并将结果转换为概率（%），输出四个风险等级的结果。包含一个简易的 Streamlit Web 页面，方便交互输入与展示。

## 计算逻辑

- Low Risk：  
  lnOR = −9.383 − 1.209Age − 0.023SBP + 0.156AST − 0.005UA − 0.248UN + 6.703Mg − 0.033PTH  
  需要：Age, SBP, AST, UA, UN, Mg, PTH

- Moderate Risk：  
  lnOR = 5.868 + 0.020SBP − 7.190Mg − 1.866HDL-c + 0.029PTH  
  需要：SBP, Mg, HDL-c, PTH

- High Risk：  
  lnOR = 7.888 + 1.682Age − 0.214Alb − 7.015Mg − 0.506HbA1c  
  需要：Age, Alb, Mg, HbA1c

- Very High Risk：  
  lnOR = −4.750 − 0.127Alb + 0.689UN  
  需要：Alb, UN

- 概率（%）= 1 / (1 + e^(−lnOR)) × 100%，保留两位小数  
- Age 赋值：≥60岁为 1，<60岁为 0

每个风险等级独立检查所需变量。若缺失，则该项提示缺失，不影响其他项计算。

## 本地运行

```bash
# 1) 建议使用虚拟环境
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

# 2) 安装依赖
pip install -r requirements.txt

# 3) 运行 Web 应用
streamlit run app.py
```

启动后浏览器中访问 http://localhost:8501 按界面提示输入数据进行计算。
