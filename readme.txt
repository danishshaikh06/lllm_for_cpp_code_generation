#data from special tokens.py
-Tokenizer data keys: dict_keys(['vocab_size', 'merges'])
-Tokenizer vocab size: 3000
-Tokenizer merges: 2744
-<class 'dict'>
-First 10 merges: ['32,32', '10,9', '256,256', '44,257', '44,32', '105,110', '101,114', '97,116', '111,110', '258,258']
-Last 10 merges: ['1890,397', '1188,334', '76,1120', '119,262', '68,32', '1051,262', '724,1469', '707,1793', '1146,469', '2705,122']

# data from cpp_dataset_clean
-Length of raw text: 45321473

# data from tokens.npy -> without special tokens 
-last 5 tokens without special tokens: [ 554 2993  290 2853  771]
-Max token ID without special tokens: 2999

# dont concatenate pad_id in tokens along with special tokens only add BOS_id and EOSid pad_is is only use to pad if seq_len is not reached as per given in the hyperparameter 

# Final tokens and vocab size for training 
-Original token count: 13367742
-PAD: 3000
-BOS: 3001
-EOS: 3002
-New vocab size: 3003
-New token count: 13367744
-Max token ID: 3002
-Saved tokens_with_specialv2.npy