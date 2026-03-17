from bpe_tokenizer import BPETokenizer

# load dataset
with open("cpp_dataset_clean.txt", "r", encoding="utf-8") as f:
    text = f.read()

tokenizer = BPETokenizer(vocab_size=3000)

print("Training tokenizer...")

tokenizer.train(text)

tokenizer.save("tokenizer.json")

print("Tokenizer saved!")
