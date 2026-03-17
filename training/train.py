import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
from decoder_only import build_transformer
from tqdm import tqdm
# =========================
# CONFIG
# =========================

SEQ_LEN = 128
BATCH_SIZE = 32
EPOCHS = 10
LR = 3e-4

BASE_VOCAB_SIZE = 3000
VOCAB_SIZE = BASE_VOCAB_SIZE + 3

PAD_ID = BASE_VOCAB_SIZE

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# DATASET
# =========================

class TokenDataset(Dataset):

    def __init__(self, tokens, seq_len):
        self.tokens = tokens
        self.seq_len = seq_len

    def __len__(self):
        return len(self.tokens) - self.seq_len

    def __getitem__(self, idx):

        x = self.tokens[idx : idx + self.seq_len]
        y = self.tokens[idx + 1 : idx + self.seq_len + 1]

        return torch.tensor(x, dtype=torch.long), torch.tensor(y, dtype=torch.long)



# =========================
# LOAD TOKENS
# =========================

tokens = np.load("tokens_with_special.npy")

print("Total tokens:", len(tokens))

dataset = TokenDataset(tokens, SEQ_LEN)

dataloader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    drop_last=True
)

# =========================
# BUILD MODEL
# =========================

model = build_transformer(
    tgt_vocab_size=VOCAB_SIZE,
    tgt_seq_len=SEQ_LEN,
    d_model=256,
    N=6,
    h=8,
    dropout=0.1,
    d_ff=1024
)

model = model.to(DEVICE)

print("Model parameters:", sum(p.numel() for p in model.parameters()))

# =========================
# LOSS
# =========================

criterion = nn.CrossEntropyLoss(ignore_index=PAD_ID)

# =========================
# OPTIMIZER
# =========================

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LR,
    weight_decay=0.01
)

# =========================
# TRAIN LOOP
# =========================

for epoch in range(EPOCHS):

    model.train()

    total_loss = 0

    for step, (x, y) in enumerate(dataloader):

        x = x.to(DEVICE)
        y = y.to(DEVICE)

        tgt_mask = model.create_tgt_mask(x, PAD_ID)

        logits = model(x, tgt_mask)

        loss = criterion(
            logits.view(-1, VOCAB_SIZE),
            y.view(-1)
        )

        optimizer.zero_grad()

        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        optimizer.step()

        total_loss += loss.item()

        if step % 100 == 0:

            print(
                f"Epoch {epoch} Step {step} Loss {loss.item():.4f}"
            )

    avg_loss = total_loss / len(dataloader)

    print("Epoch Loss:", avg_loss)

    torch.save(
        model.state_dict(),
        f"model_epoch_{epoch}.pt"
    )
