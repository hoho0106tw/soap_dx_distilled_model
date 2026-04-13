#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# =============================
# 設定
# =============================
MODEL_PATH = "hoho0106tw/femh-primary-dx-model"
EXCEL_PATH = "sample_200_v4.xlsx"

SAMPLE_N = 100
SEED = 42
MAX_NEW_TOKENS = 10

# =============================
# SOAP
# =============================
def build_soap(row):
    return f"S:{row['S']}\nO:{row['O']}\nA:{row['A']}\nP:{row['P']}"

# =============================
# Prompt
# =============================
def build_messages(soap_text):

    system_prompt = """你是一位臨床醫師。

任務：
根據 SOAP 內容，只判斷此次就診最主要的一個疾病診斷。

嚴格規則：
- 只能輸出一個疾病診斷
- 只能輸出一行
- 不可輸出第二個診斷
- 不可解釋
- 不可摘要
- 不可輸出多餘文字
- 一律輸出英文小寫
- 不需要你的分析

強制分類規則：
- 只能從以下清單中選擇一個診斷
- 不可創造新名稱
- 不可修改名稱

可選清單：
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
只輸出答案。"""

    user_prompt = f"""SOAP:
{soap_text}

Return only one primary diagnosis."""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

# =============================
# 推論
# =============================
@torch.no_grad()
def predict(tokenizer, model, soap_text):

    messages = build_messages(soap_text)

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
    )

    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}
    input_len = inputs["input_ids"].shape[1]

    outputs = model.generate(
        **inputs,
        max_new_tokens=MAX_NEW_TOKENS,
        do_sample=False,
        temperature=0.0,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    gen_ids = outputs[0][input_len:]
    raw = tokenizer.decode(gen_ids, skip_special_tokens=True).strip()

    # 清理輸出
    lower_raw = raw.lower()

    if "final" in lower_raw:
        raw = raw[lower_raw.rfind("final") + 5:].strip()
    elif "analysis" in lower_raw:
        raw = raw[lower_raw.rfind("analysis") + 8:].strip()

    raw = raw.split("\n")[-1].strip()

    return raw

# =============================
# 讀資料
# =============================
df = pd.read_excel(EXCEL_PATH)

sample_df = df.sample(n=SAMPLE_N, random_state=SEED).reset_index(drop=True)

print("本次驗證筆數:", len(sample_df))
print("全部標準答案:")
print(sample_df["PRIMARY_DIAGNOSIS"].value_counts())

# =============================
# 載模型（🔥 HF 多 GPU）
# =============================
print("載入模型中...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
    device_map="auto"   # 🔥 自動分到 H100 x3
)

model.eval()

print("模型載入完成")

# =============================
# 驗證
# =============================
correct = 0

for i, row in sample_df.iterrows():

    soap = build_soap(row)
    gold = str(row["PRIMARY_DIAGNOSIS"]).strip()
    pred = predict(tokenizer, model, soap).strip()

    if pred == gold:
        correct += 1

    print("\n" + "=" * 100)
    print(f"Sample {i+1}")
    print("=" * 100)

    print("\n[SOAP]")
    print(soap)

    print("\n[標準答案]")
    print(gold)

    print("\n[模型輸出]")
    print(pred)

# =============================
# 統計
# =============================
print("\n" + "=" * 100)
print(f"答對題數: {correct} / {len(sample_df)}")
print(f"Accuracy: {correct / len(sample_df):.4f}")


# In[ ]:




