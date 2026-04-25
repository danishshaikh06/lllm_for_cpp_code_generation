from main.project_paths import TOKENIZER_DIR
from main.tokenizer.bpe_tokenizer import BPETokenizer


with open(TOKENIZER_DIR / "cpp_dataset_clean.txt", "r", encoding="utf-8") as f:
    text = f.read()

tokenizer = BPETokenizer(vocab_size=3000)

print("Training tokenizer...")
tokenizer.train(text)
tokenizer.save(TOKENIZER_DIR / "tokenizer.json")
print("Tokenizer saved!")
