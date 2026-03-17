from bpe_tokenizer import BPETokenizer

tokenizer = BPETokenizer()
tokenizer.load("tokenizer.json")

text = "int main(){ return 0; }"

tokens = tokenizer.encode(text)

print("Tokens:", tokens)

decoded = tokenizer.decode(tokens)

print("Decoded:", decoded)
