from main.project_paths import TOKENIZER_DIR
from main.tokenizer.bpe_tokenizer import BPETokenizer


tokenizer = BPETokenizer()
tokenizer.load(TOKENIZER_DIR / "tokenizer.json")

print("Tokenizer loaded")

print("Reading dataset...")
with open(TOKENIZER_DIR / "cpp_dataset_clean.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("dataset length:", len(text))

print("Encoding dataset into token IDs...")
tokens = tokenizer.encode(text[:1000])
print("number of tokens:", len(tokens))
print("tokens:", tokens)
