#!/usr/bin/env python3
"""
Telugu Tokenizer Training Pipeline
----------------------------------
A robust CLI script to:
1. Load vocabulary and corpus.
2. Pre-tokenize the corpus using hybrid Sandhi rules.
3. Train a SentencePiece (BPE) tokenizer model.

Usage:
    python train_pipeline.py --vocab data/telugu_vocab.txt --corpus data/telugu_corpus.txt

Author: Swecha Contributor
Date: 2025-10-25
"""

import os
import sys
import argparse
import sentencepiece as spm

# Add 'src' to path to import the module
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
try:
    from sandhi_splitter import find_all_splits
except ImportError:
    print("Error: Could not import 'src.sandhi_splitter'. Ensure the folder structure is correct.")
    sys.exit(1)

def load_vocabulary_with_frequency(filepath):
    """
    Loads vocabulary and frequency counts from a text file.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Vocabulary file not found: {filepath}")

    vocab = {}
    print(f"[INFO] Loading vocabulary from '{filepath}'...")
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                word = ' '.join(parts[:-1])
                freq_str = parts[-1]
                vocab[word] = int(freq_str) if freq_str.isdigit() else 1
            else:
                vocab[line] = 1
    print(f"[INFO] Loaded {len(vocab)} words.")
    return vocab

def get_best_frequency_split(word, vocab):
    """
    Validates Sandhi splits against the vocabulary frequency.
    Returns the split with the highest frequency score.
    """
    possible_splits = find_all_splits(word)
    if not possible_splits:
        return [word]

    valid_splits = []
    for _, splits in possible_splits.items():
        for split_str in splits:
            parts = [p.strip().strip("'") for p in split_str.split('+')]
            if len(parts) == 2:
                part1, part2 = parts
                p1_in = part1 in vocab
                p2_in = part2 in vocab
                
                score = 0
                if p1_in and p2_in:
                    score = 1000 + min(vocab.get(part1, 1), vocab.get(part2, 1))
                elif p1_in or p2_in:
                    score = 100 + (vocab.get(part1, 1) if p1_in else vocab.get(part2, 1))
                
                if score > 0:
                    valid_splits.append({'parts': [part1, part2], 'score': score})

    if not valid_splits:
        return [word]

    best_split = max(valid_splits, key=lambda x: x['score'])
    return best_split['parts']

def pre_tokenize_corpus(input_path, output_path, vocab):
    """
    Reads corpus, applies best splits, and saves pre-tokenized text.
    """
    print(f"[INFO] Pre-tokenizing '{input_path}'...")
    
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for i, line in enumerate(infile):
            words = line.strip().split()
            pre_tokenized_words = []
            for word in words:
                sub_words = word.replace('\u200c', ' ').split()
                for sub_word in sub_words:
                    split_parts = get_best_frequency_split(sub_word, vocab)
                    pre_tokenized_words.extend(split_parts)
            
            outfile.write(' '.join(pre_tokenized_words) + '\n')
            
            if (i + 1) % 1000 == 0:
                print(f"  ...processed {i+1} lines", end='\r')
                
    print(f"\n[INFO] Pre-tokenization saved to '{output_path}'.")

def train_bpe_model(input_file, model_prefix, vocab_size=16000):
    """
    Trains the SentencePiece BPE model.
    """
    print(f"[INFO] Training BPE model (Vocab Size: {vocab_size})...")
    spm.SentencePieceTrainer.train(
        f'--input={input_file} '
        f'--model_prefix={model_prefix} '
        f'--vocab_size={vocab_size} '
        f'--model_type=bpe '
        f'--character_coverage=1.0'
    )
    print(f"[SUCCESS] Model saved as '{model_prefix}.model'")

def main():
    parser = argparse.ArgumentParser(description="Telugu Tokenizer Training Pipeline")
    parser.add_argument("--vocab", required=True, help="Path to vocabulary file (telugu_vocab.txt)")
    parser.add_argument("--corpus", required=True, help="Path to corpus file (telugu_corpus.txt)")
    parser.add_argument("--output_dir", default="model", help="Directory to save model")
    parser.add_argument("--vocab_size", type=int, default=16000, help="BPE Vocabulary size")

    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    pretokenized_corpus = os.path.join(os.path.dirname(args.corpus), "corpus.pretokenized.txt")
    model_prefix = os.path.join(args.output_dir, "telugu_bpe")

    # Step 1: Load Vocab
    vocabulary = load_vocabulary_with_frequency(args.vocab)

    # Step 2: Pre-tokenize
    pre_tokenize_corpus(args.corpus, pretokenized_corpus, vocabulary)

    # Step 3: Train Model
    train_bpe_model(pretokenized_corpus, model_prefix, args.vocab_size)

if __name__ == "__main__":
    main()