import numpy as np


# load tokens
tokens = np.load(r"C:\Users\Omen\Downloads\c++ Physics code dataset\tokens.npy")

print("Original token count:", len(tokens))

# tokenizer vocab size (example)
BASE_VOCAB_SIZE = 3000  # replace with your real tokenizer vocab

PAD_ID = BASE_VOCAB_SIZE
BOS_ID = BASE_VOCAB_SIZE + 1
EOS_ID = BASE_VOCAB_SIZE + 2

VOCAB_SIZE = BASE_VOCAB_SIZE + 3

print("PAD:", PAD_ID)
print("BOS:", BOS_ID)
print("EOS:", EOS_ID)
print("New vocab size:", VOCAB_SIZE)

# append BOS and EOS
tokens_with_special = np.concatenate(
    ([BOS_ID], tokens, [EOS_ID])
)

print("New token count:", len(tokens_with_special))
print("Max token ID:", tokens_with_special.max())

# save
np.save("tokens_with_special.npy", tokens_with_special)

print("Saved tokens_with_special.npy")
