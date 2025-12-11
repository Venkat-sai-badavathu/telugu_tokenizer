import sentencepiece as spm

# Load trained model
tokenizer = spm.SentencePieceProcessor()
tokenizer.load('model/telugu_bpe.model')

# Tokenize new text
sentence = "రాష్ట్రాలలోని సమస్యలను ప్రభుత్వం పరిష్కరించింది."
pieces = tokenizer.encode_as_pieces(sentence)

print("Original:", sentence)
print("Tokenized:", pieces)