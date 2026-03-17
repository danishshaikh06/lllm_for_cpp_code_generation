import numpy as np
from bpe_tokenizer import BPETokenizer

# load tokenizer
tokenizer = BPETokenizer()
tokenizer.load("tokenizer.json")

print("Tokenizer loaded")

# read dataset
with open("cpp_dataset_clean.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Dataset length:", len(text))

chunk_size = 1_000_000   # 1M characters per chunk
tokens_list = []

total_chunks = (len(text) + chunk_size - 1) // chunk_size

for i in range(total_chunks):

    start = i * chunk_size
    end = start + chunk_size

    chunk = text[start:end]

    tokens = tokenizer.encode(chunk)

    tokens_list.append(np.array(tokens, dtype=np.int32))

    print(f"Chunk {i+1}/{total_chunks} | tokens: {len(tokens)}")

# concatenate once (very important for speed)
tokens_array = np.concatenate(tokens_list)

np.save("tokens.npy", tokens_array)

print("Final token count:", len(tokens_array))
print("Saved tokens.npy")
