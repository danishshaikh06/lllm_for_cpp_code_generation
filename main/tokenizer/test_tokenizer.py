from main.project_paths import TOKENIZER_DIR
from main.tokenizer.bpe_tokenizer import BPETokenizer


tokenizer = BPETokenizer()
tokenizer.load(TOKENIZER_DIR / "tokenizer.json")

text = "int main(){ return 0; }"

tokens = tokenizer.encode(text)
print("Tokens:", tokens)

decoded = tokenizer.decode(tokens)
print("Decoded:", decoded)
