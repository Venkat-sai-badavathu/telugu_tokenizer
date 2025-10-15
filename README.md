# 🌐 Hybrid Telugu Morphological Tokenizer

## 1. Introduction

This project provides a **hybrid approach** to tokenizing **Telugu text** — a morphologically rich and agglutinative language.  
Standard tokenizers often fail to handle **Sandhi** (euphonic assimilation), where multiple morphemes merge into a single word.

For example:

> రాష్ట్రాలలోని (“in the states”) = రాష్ట్రాలు (“states”) + లోని (“in”)

To solve this, our tokenizer combines:

- A **rule-based Sandhi splitting engine**, and
- A **data-driven BPE (Byte-Pair Encoding)** model.

This hybrid method enables **grammatically aware tokenization**, improving performance in downstream **NLP tasks** like translation, summarization, and sentiment analysis.

---

## 2. The Hybrid Approach

Our methodology uses **three phases** to combine linguistic knowledge with machine learning.

### 🧠 Phase 1: Rule-Based Sandhi Engine

The script `sandhi_splitter.py` acts as a _grammar brain_.  
It identifies all possible morphological splits for a given word based on extensive **Telugu and Sanskrit Sandhi rules**.

### 📊 Phase 2: Frequency-Based Pre-tokenization

The script `frequency_based_tokenizer.py`:

1. Retrieves all potential splits from the Sandhi engine.
2. Validates them using a **frequency-based vocabulary** (`te_full.txt`).
3. Scores and selects the **most probable grammatical split**.
4. Outputs a processed text file: `corpus.pretokenized.txt`.

### 🧩 Phase 3: BPE Model Training

The pre-tokenized corpus is then used to train a **SentencePiece (BPE)** model.  
This learns morphemes as base tokens, resulting in a **robust and linguistically aware tokenizer**.

---

## 3. Data Requirements

Two external data files are required (not included due to size):

### 📘 Vocabulary File — `te_full.txt`

- Contains Telugu words with frequencies.
- Format:
  ```
  పదం 1234
  మరోపదం 987
  ```
- Place in `data/` directory.

### 📗 Corpus File — `telugu_corpus.txt`

- Raw Telugu sentences, one per line.
- Example sources: **IndicCorp**, **Telugu Wikipedia Dumps**.
- Place in `data/` directory.

Expected directory structure:

```
data/
├── te_full.txt
└── telugu_corpus.txt
```

---

## 4. Usage Workflow

### 🔹 Step 1: Pre-tokenize the Corpus

```bash
python src/frequency_based_tokenizer.py
```

Generates `data/corpus.pretokenized.txt` with linguistically-aware splits.  
_(Processing time depends on corpus size.)_

### 🔹 Step 2: Train the BPE Model

```bash
spm_train     --input=data/corpus.pretokenized.txt     --model_prefix=models/telugu_bpe     --vocab_size=16000     --model_type=bpe     --character_coverage=1.0
```

> Adjust `vocab_size` (e.g., 32000) based on dataset scale.

### 🔹 Step 3: Use the Trained Tokenizer

```python
import sentencepiece as spm

# Load trained model
tokenizer = spm.SentencePieceProcessor()
tokenizer.load('models/telugu_bpe.model')

# Tokenize new text
sentence = "రాష్ట్రాలలోని సమస్యలను ప్రభుత్వం పరిష్కరించింది."
pieces = tokenizer.encode_as_pieces(sentence)

print("Original:", sentence)
print("Tokenized:", pieces)
```

**Expected Output:**

```
Original: రాష్ట్రాలలోని సమస్యలను ప్రభుత్వం పరిష్కరించింది.
Tokenized: ['రాష్ట్రాలు', 'లోని', 'సమస్యలు', 'ను', 'ప్రభుత్వం', 'పరిష్కరించింది', '.']
```
