📌 專案名稱

SOAP 臨床診斷推論模型（Distilled LLM）

📖 專案介紹

本專案使用大型語言模型（LLM），根據臨床 SOAP（Subjective, Objective, Assessment, Plan）紀錄，自動判斷單一主要診斷（Primary Diagnosis）。

模型已經過蒸餾（distillation）與指令微調（SFT），並限制輸出為固定診斷分類清單中的一項，以提升臨床應用的穩定性與可控性。

🎯 任務目標

輸入：

SOAP 病歷資料（S / O / A / P）

輸出：

僅一個主要診斷（英文小寫）
不包含解釋或其他文字
🧠 可預測診斷類別

模型僅允許輸出以下 11 類疾病：

stroke
transient ischemic attack
dementia
epilepsy
migraine
parkinsonism
neuropathy
radiculopathy
spine disease
carotid artery disease
syncope
⚙️ 使用方法
1️⃣ 安裝套件
pip install torch transformers pandas openpyxl
2️⃣ 設定模型與資料

在程式中修改：

MODEL_PATH = "hoho0106tw/femh-primary-dx-model"
EXCEL_PATH = "sample_200_v4.xlsx"
3️⃣ 執行推論
python soap_dx_distilled_model.py
📊 評估方式

程式會：

隨機抽樣資料（預設 100 筆）
比較模型輸出 vs 標準答案
計算 Accuracy
🔍 核心流程
建立 SOAP 格式輸入
套用 Chat Template Prompt
使用 HuggingFace 模型進行生成
清理輸出結果
與標準答案比對

👉 詳細程式可參考：


🚀 技術重點
LLM 蒸餾（Distilled Model）
指令式 Prompt Engineering（嚴格輸出限制）
多 GPU 推論（device_map="auto"）
醫療文本結構化（SOAP）
⚠️ 注意事項
本專案僅供研究用途，不可直接用於臨床診斷
模型輸出受限於訓練資料與分類清單
未涵蓋所有神經科疾病
