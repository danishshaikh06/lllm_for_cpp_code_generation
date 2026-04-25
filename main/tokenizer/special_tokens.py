import numpy as np

from main.project_paths import TOKENIZER_DIR


special = np.load(TOKENIZER_DIR / "tokens.npy")

print("last 5 tokens without special tokens:", special[-5:])

max_token_id = int(special.max())
print("Max token ID without:", max_token_id)
