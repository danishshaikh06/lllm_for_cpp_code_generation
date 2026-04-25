import numpy as np 

special = np.load("tokens.npy")

print('last 5 tokens without special tokens:', special[-5:])

max_token_id = int(special.max())
print("Max token ID without:", max_token_id)