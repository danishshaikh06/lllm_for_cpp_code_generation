import numpy as np 
from bpe_tokenizer import BPETokenizer  

tokenizer = BPETokenizer()
tokenizer.load("tokenizer.json")

print("Tokenizer loaded")


# read dataset
print("Reading dataset...")
with open("cpp_dataset_clean.txt", "r", encoding = 'utf-8') as f:
    text = f.read()

    print('dataset length:', len(text))
     
    # encode dataset
    print("Encoding dataset into token IDs...")
    tokens = tokenizer.encode(text[:1000]) # encode first 1000 tokens 
    print('number of tokens:', len(tokens))
    print('tokens:', tokens)