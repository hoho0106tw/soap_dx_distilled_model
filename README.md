# 📌 SOAP 臨床診斷推論模型（Distilled LLM）

## 📖 專案介紹
本專案使用大型語言模型（LLM），根據臨床 SOAP（Subjective, Objective, Assessment, Plan）紀錄，  
自動判斷單一主要診斷（Primary Diagnosis）。  

本模型基於 GPT 20B 架構，使用約 7000 筆臨床資料進行訓練，  
並經過約五天的資料挑選、清洗與整理，提升資料品質與一致性。  

同時結合機器學習與統計學方法，對資料進行優化，  
使模型在分類任務上達到更穩定的表現。  

最終模型準確率可達 **90% 以上**，並在推論效率上顯著優於原始模型。  


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

### 1️⃣ 安裝套件
```bash
pip install torch transformers pandas openpyxl

###2️⃣ 設定模型與資料
MODEL_PATH = "hoho0106tw/femh-primary-dx-model"
EXCEL_PATH = "sample_200_v4.xlsx"

###3️⃣ 執行
python soap_dx_distilled_model.py
---

##🚀 模型優勢

使用 GPT 20B 蒸餾模型（Distilled Model）
訓練資料約 7000 筆，經人工清洗與篩選
結合機器學習與統計方法進行資料優化
準確率達 90% 以上
推論速度顯著提升
###⚡ 推論效率比較
本模型：僅需生成 10 tokens 即可輸出答案
原始模型：約需 10 倍 tokens 才能完成推論

##👉 大幅降低推論時間與計算成本

---
###📊 評估方式
隨機抽樣資料（預設 100 筆）
比較模型輸出與標準答案
計算 Accuracy

---
###⚠️ 注意事項
僅供研究用途，不可用於臨床診斷
輸出受限於訓練資料與分類清單
