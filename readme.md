# 🌐 Hybrid Telugu Morphological Tokenizer

## 1. Introduction

This project provides a **hybrid approach** to tokenizing **Telugu text** — a morphologically rich and agglutinative language. Standard tokenizers often fail to handle **Sandhi** (euphonic assimilation), where multiple morphemes merge into a single word.

For example:

> రాష్ట్రాలలోని (_"in the states"_) = రాష్ట్రాలు (_"states"_) + లోని (_"in"_)

To solve this, our tokenizer combines:

- A **rule-based Sandhi splitting engine**, and
- A **data-driven BPE (Byte-Pair Encoding)** model.

This hybrid method enables **grammatically aware tokenization**, improving performance in downstream **NLP tasks** like translation, summarization, and sentiment analysis.

---

## 2. Key Features

- **Morphological Segmentation**: Splits complex Sandhi forms into meaningful bpe-friendly morphemes using grammatical rules
- **Frequency-Based Validation**: Uses vocabulary frequencies to choose the most probable split
- **Subword Tokenization**: Employs BPE (Byte-Pair Encoding) via SentencePiece for robust handling of rare words
- **Modular Architecture**: Clean separation between rule-based splitting and statistical learning
- **Production-Ready**: Easy-to-use pipeline with command-line interface

---

## 3. Project Structure

```text
telugu_tokenizer/
├── src/
│   └── sandhi_splitter.py   # Core logic for grammatical rules (Library)
├── data/
│   ├── telugu_vocab.txt     # Word frequency list (Required for validation)
│   └── telugu_corpus.txt    # Raw text corpus (Required for training)
├── model/                   # Output directory for trained models
├── train_pipeline.py        # Main execution script
├── requirements.txt         # Python dependencies
└── README.md
```

### 🧠 The Hybrid Pipeline

The `train_pipeline.py` script automates the entire process:

1. **Rule-Based Splitting:** Uses `src/sandhi_splitter.py` to identify all possible **BPE-friendly splits** based on extensive Telugu and Sanskrit Sandhi rules.
2. **Frequency Validation:** Validates these splits against `telugu_vocab.txt` to select the most probable grammatical split.
3. **BPE Training:** Trains a **SentencePiece** model on this pre-processed data to create a robust tokenizer.
4. **Model Serialization:** Saves the trained BPE model and vocabulary for production use.

---

## 4. Data Requirements

Two external data files are required in the `data/` directory. These are not included in the repo due to size.

### 📘 Vocabulary File — `data/telugu_vocab.txt`

This file acts as a validator for the Sandhi splitter. It must contain a broad coverage of valid Telugu words, including:

- **Root Words** (e.g., `రామ`, `చెట్టు`)
- **Simple Inflected Forms** (e.g., `రాముడు`, `చెట్లు`)
- **Function Words** (e.g., `మరియు`, `కాని`)
- **Modern Vocabulary** (loanwords, technical terms)

**Format:**

```
ఇల్లు 98
నీరు 97
```

### 📗 Corpus File — `data/telugu_corpus.txt`

Raw Telugu sentences used to train the final BPE model.

- **Format:** One sentence per line.
- **Sources:** IndicCorp, Telugu Wikipedia Dumps, news articles, literature
- **Size:** Larger and more diverse corpora yield better tokenization models

---

## 5. Setup & Installation

### 1. Clone the Repository

```bash
git clone git@code.swecha.org:venkat29/telugu_tokenizer.git
cd telugu_tokenizer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Usage Workflow

You can run the entire pre-tokenization and training pipeline with a single command:

```bash
python train_pipeline.py --vocab data/telugu_vocab.txt --corpus data/telugu_corpus.txt
```

## 7. Using the Trained Model

Once the pipeline finishes, your model will be saved in the `model/` folder. You can load it in Python like this:

```python
import sentencepiece as spm

# Load trained model
tokenizer = spm.SentencePieceProcessor()
tokenizer.load('model/telugu_bpe.model')

# Tokenize new text
sentence = "రాష్ట్రాలలోని సమస్యలను ప్రభుత్వం పరిష్కరించింది."
pieces = tokenizer.encode_as_pieces(sentence)

print("Original:", sentence)
print("Tokenized:", pieces)
```

**Expected Output:**

```
Original: రాష్ట్రాలలోని సమస్యలను ప్రభుత్వం పరిష్కరించింది.
Tokenized: ['▁రాష్ట్రా', 'లలోని', '▁సమస్య', 'లను', '▁ప్రభుత్వం', '▁పరిష్', 'కరించింది', '.']

```

---

## 8. Technical Highlights

### Grammar-Aware Tokenization

- Implements comprehensive Telugu Sandhi rules (Savarna Deergha, Yan, Guna, Vriddhi, etc.)
- Handles both external and internal Sandhi phenomena
- Preserves morphological boundaries crucial for NLP tasks

### Two-Stage Validation

1. **Rule Application:** Generate all possible **BPE-friendly splits** based on grammatical patterns.
2. **Frequency Check:** Select the split where all components exist in vocabulary with highest combined frequency

### BPE Integration

- Combines the precision of rule-based splitting with the flexibility of statistical tokenization
- Handles out-of-vocabulary words gracefully through subword decomposition
- Produces consistent tokenization suitable for transformer models and neural networks

---
