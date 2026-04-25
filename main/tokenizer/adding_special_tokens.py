import numpy as np

from main.project_paths import TOKENIZER_DIR


tokens = np.load(TOKENIZER_DIR / "tokens.npy")

print("Original token count:", len(tokens))

max_token_id = int(tokens.max())

pad_id = max_token_id + 1
bos_id = max_token_id + 2
eos_id = max_token_id + 3

vocab_size = max_token_id + 4

print("PAD:", pad_id)
print("BOS:", bos_id)
print("EOS:", eos_id)
print("New vocab size:", vocab_size)

tokens_with_special = np.concatenate(([bos_id], tokens, [eos_id]))

print("New token count:", len(tokens_with_special))
print("Max token ID:", tokens_with_special.max())

np.save(TOKENIZER_DIR / "tokens_with_specialv2.npy", tokens_with_special)

print("Saved tokens_with_specialv2.npy")
