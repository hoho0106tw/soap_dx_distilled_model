# 📌 SOAP 臨床診斷推論模型（Distilled LLM）

## 📖 專案介紹
本專案使用大型語言模型（LLM），根據臨床 SOAP（Subjective, Objective, Assessment, Plan）紀錄，  
自動判斷單一主要診斷（Primary Diagnosis）。  

模型已經過蒸餾（distillation）與指令微調（SFT），  
並限制輸出為固定診斷分類清單中的一項，以提升穩定性與可控性。  

---

## 🎯 任務目標

**輸入：**  
SOAP 病歷資料（S / O / A / P）  

**輸出：**  
僅一個主要診斷（英文小寫）  
不包含解釋或其他文字  

---

## 🧠 可預測診斷類別

- stroke  
- transient ischemic attack  
- dementia  
- epilepsy  
- migraine  
- parkinsonism  
- neuropathy  
- radiculopathy  
- spine disease  
- carotid artery disease  
- syncope  

---

## ⚙️ 使用方法

```bash
pip install torch transformers pandas openpyxl


### 2️⃣ 設定模型與資料
MODEL_PATH = "hoho0106tw/femh-primary-dx-model"
EXCEL_PATH = "sample_200_v4.xlsx"


### 3️⃣ 執行
python soap_dx_distilled_model.py
