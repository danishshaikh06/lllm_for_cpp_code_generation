# Personal C++ Code Generator - README Version 2

## Project Overview

This project is a personal **C++ code generation system** built from scratch using a custom tokenizer, a custom **decoder-only Transformer**, a base training pipeline for next-token prediction, and a later **fine-tuning pipeline** for instruction-style C++ responses.

The goal of the project is to move step by step from:

1. collecting C++ source data,
2. cleaning and tokenizing it,
3. training a small language model,
4. fine-tuning it on instruction-style coding datasets,
5. testing inference locally,
6. and later packaging it into a simple application.

The target behavior is:

- user gives a prompt such as:
  `write code for hello world`
- model returns:
  C++ code, and ideally an explanation as well

This README explains what the project does, how the pipeline works, which datasets are used, what model architecture is used, what tokenizer is used, which IDs are reserved for special tokens, and how the training pipeline was improved over time.

It also explains the planned future direction from the project roadmap, including:

- a simple website where the user types a prompt
- model-generated C++ code and explanation as the response
- local backend/frontend serving
- later Dockerization
- later hosting with Vercel for the frontend and a separate inference service if needed

## What This Project Does

This project currently does the following:

1. Collects and stores C++ source data extracted from GitHub repositories.
2. Cleans the raw source data into a training-ready C++ corpus.
3. Trains a custom **Byte Pair Encoding (BPE)** tokenizer on the cleaned corpus.
4. Converts the cleaned C++ corpus into token IDs.
5. Adds special tokens for training.
6. Trains a custom **decoder-only Transformer** on the C++ token stream.
7. Saves checkpoints and configuration files for reproducibility.
8. Runs local inference from trained checkpoints.
9. Builds instruction-style C++ fine-tuning datasets from Hugging Face data.
10. Fine-tunes the base checkpoint on instruction-style prompt/response data.
11. Includes a simple local API/frontend path for future usage and later Dockerization.
12. Plans a simple website where a user enters a prompt and receives generated C++ code.
13. Plans deployment in phases instead of trying to package everything at once.

## High-Level Pipeline

The project pipeline is:

1. **Data collection**
2. **Data cleaning**
3. **Tokenizer training**
4. **Token ID generation**
5. **Special token creation**
6. **Base model training**
7. **Instruction dataset preparation**
8. **Instruction fine-tuning**
9. **Inference testing**
10. **Later: Dockerization and simple app serving**
11. **Later: website deployment and hosting**

## Step 1 - Data Collection

At the beginning of the project, the dataset was built by extracting **C++ code data from GitHub repositories**.

Project folders related to this:

- [repos](C:/Users/Omen/Downloads/llm_for_cpp/repos)
- [data_cleaning](C:/Users/Omen/Downloads/llm_for_cpp/data_cleaning)

The intention of this stage is to create a large raw C++ corpus from real-world repositories so the model can first learn:

- C++ syntax
- header/includes patterns
- classes/structs/functions
- naming conventions
- common library usage

This raw corpus is not instruction data. It is base language-model training data.

## Step 2 - Data Cleaning

After collecting raw GitHub code, the data is cleaned and consolidated into:

- [cpp_dataset.txt](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/cpp_dataset.txt)
- [cpp_dataset_clean.txt](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/cpp_dataset_clean.txt)

The cleaned dataset is the one used for tokenizer training and base model training.

Known corpus size from the project notes:

- Raw/cleaned C++ training text length used in the project notes: about `45,321,473` characters

This cleaned dataset is the base corpus that teaches the model how C++ code looks.

## Step 3 - Tokenizer

The project uses a **custom Byte Pair Encoding (BPE) tokenizer** implemented in:

- [bpe_tokenizer.py](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/bpe_tokenizer.py)

### Tokenizer Type

- **Byte-level BPE**

This tokenizer:

1. Starts from raw UTF-8 bytes (`0-255`)
2. Learns merge rules from the training text
3. Builds a compact subword vocabulary
4. Encodes text into integer token IDs
5. Decodes token IDs back into text

### Why BPE Was Used

BPE is a good choice for this kind of project because:

- it is simpler than building a fully hand-crafted tokenizer
- it can handle rare tokens better than fixed word vocabularies
- it works reasonably well for source code, identifiers, punctuation, and mixed symbol patterns
- it keeps vocabulary size manageable

### Tokenizer Vocabulary

The tokenizer was trained with:

- `vocab_size = 3000`

Stored tokenizer file:

- [tokenizer.json](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/tokenizer.json)

From project notes:

- tokenizer merges learned: `2744`
- max token ID before special tokens: `2999`

### Tokenizer Scripts

- [train_tokenizer.py](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/train_tokenizer.py)
- [token_ids.py](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/token_ids.py)
- [adding_special_tokens.py](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/adding_special_tokens.py)
- [test_tokenizer.py](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/test_tokenizer.py)
- [test_tokens.py](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/test_tokens.py)

## Step 4 - Token IDs and Special Tokens

After tokenizer training, the cleaned C++ corpus is encoded into token IDs and saved as:

- [tokens.npy](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/tokens.npy)

Then special tokens are added and saved as:

- [tokens_with_specialv2.npy](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/tokens_with_specialv2.npy)

### Final Token Counts

From the project notes:

- original token count: `13,367,742`
- new token count after BOS/EOS: `13,367,744`

### Special Token IDs

These IDs are used consistently across training and inference:

- `PAD_ID = 3000`
- `BOS_ID = 3001`
- `EOS_ID = 3002`

### Final Vocabulary Size

- `VOCAB_SIZE = 3003`

### Why These Special Tokens Matter

- `PAD_ID` is used for padding-aware masking and loss ignoring
- `BOS_ID` marks the beginning of a token sequence
- `EOS_ID` marks the end of a token sequence

These IDs must remain consistent across:

- training
- fine-tuning
- inference

## Step 5 - Base Model Architecture

The base model is a **decoder-only Transformer** implemented in:

- [decoder_only.py](C:/Users/Omen/Downloads/llm_for_cpp/main/transformer/decoder_only.py)

### What Architecture Is Used

This project uses:

- token embeddings
- sinusoidal positional encoding
- masked multi-head self-attention
- feed-forward layers
- residual connections
- layer normalization
- output projection to vocabulary logits

### Why Decoder-Only Transformer Was Chosen

The project uses only a **decoder-only Transformer** because the task is **autoregressive next-token prediction**.

This is a good fit because:

- the model predicts the next token from previous tokens only
- code generation is naturally left-to-right
- inference becomes straightforward for prompt completion
- the design is closer to GPT-style generation
- it is simpler to build and reason about than a full encoder-decoder architecture for this project

### Why Not Encoder-Decoder Here

An encoder-decoder model is more common for sequence-to-sequence tasks like translation. This project first needed:

- a simple generative code model
- direct continuation behavior
- a smaller and easier-to-implement training pipeline

So decoder-only was the right starting architecture.

## Step 6 - Base Training

Base training is implemented in:

- [train.py](C:/Users/Omen/Downloads/llm_for_cpp/main/training/train.py)

### Base Training Goal

The purpose of base training is to teach the model the general structure of C++ code from the GitHub-derived corpus.

This stage is not instruction following. It is plain language-model pretraining on C++ text/code.

### Current Main Training Configuration

On CUDA/GPU, the current default configuration is:

- `seq_len = 256`
- `stride = 64`
- `batch_size = 16`
- `epochs = 10`
- `lr = 2e-4`
- `accum_steps = 4`
- `d_model = 384`
- `layers = 8`
- `heads = 8`
- `dropout = 0.1`
- `d_ff = 1536`

### What the Base Training Script Does

1. Loads `tokens_with_specialv2.npy`
2. Builds sliding token windows
3. Splits data into train and validation sets
4. Creates a decoder-only Transformer
5. Runs mixed precision training on GPU if available
6. Uses AdamW optimizer
7. Uses gradient accumulation
8. Uses gradient clipping
9. Saves training config into `artifacts/`
10. Saves best and per-epoch checkpoints
11. Prints sample generations every few epochs

### Training Artifacts

Training saves important files into:

- [artifacts](C:/Users/Omen/Downloads/llm_for_cpp/artifacts)

Important saved files include:

- [training_config.json](C:/Users/Omen/Downloads/llm_for_cpp/artifacts/training_config.json)
- [best_model.pt](C:/Users/Omen/Downloads/llm_for_cpp/artifacts/best_model.pt)
- epoch checkpoints like `model_epoch_*.pt`

### Why `training_config.json` Is Important

The checkpoint alone only stores weights.

The config file is necessary to rebuild:

- model dimension
- number of layers
- number of heads
- feed-forward size
- sequence length
- special token IDs
- vocabulary size

Without this config, inference can rebuild the wrong model shape.

## Step 7 - How the Training Pipeline Was Improved

The training pipeline was gradually improved during development.

### Main Improvements

1. **Removed Weights & Biases dependency**
   - The project originally used `wandb`
   - It was removed so training works locally without external credentials

2. **Added artifact/config saving**
   - Training now saves the model config with the checkpoint

3. **Added smoke-test mode**
   - quick verification mode with limited data/steps
   - useful for checking that training works before long runs

4. **Added stride**
   - initial sliding windows had stride `1`, which caused very large and redundant epochs
   - training now uses `stride = 64`
   - this reduces overlap and makes epochs much more practical

5. **Fixed accumulation handling**
   - the script was updated so the final accumulated gradients are not dropped at epoch end

6. **Fixed learning-rate scheduling**
   - LR schedule is now tied to optimizer updates instead of microbatches

7. **Improved token subset handling in smoke mode**
   - smoke-test trimming now preserves BOS/EOS correctly

8. **Removed noisy inner-loop logging**
   - excessive per-step debug prints were removed because they slowed training

### Why These Improvements Matter

These changes made the training pipeline:

- more stable
- faster to debug
- easier to reason about
- more correct mathematically
- easier to continue later with fine-tuning

## Step 8 - Inference

Inference is implemented in:

- [inference.py](C:/Users/Omen/Downloads/llm_for_cpp/main/inference.py)

### What Inference Does

1. Loads the tokenizer
2. Loads the training config
3. Rebuilds the decoder-only Transformer
4. Loads checkpoint weights
5. Encodes the prompt
6. Generates tokens autoregressively
7. Stops on EOS or on certain prompt-format boundaries

### Prompt Format

Inference uses a prompt structure aligned with fine-tuning:

```text
User: ...
Assistant:
```

This was done so training format and inference format match better.

## Step 9 - Fine-Tuning Data

After base training, the project moved to **instruction-style fine-tuning**.

### Why Fine-Tuning Was Needed

Base training on GitHub C++ code teaches syntax and code structure, but it does not teach:

- how to follow direct user prompts
- how to explain code
- how to return code in a response format

So fine-tuning data was needed to teach:

- `User -> Assistant` behavior
- prompt following
- explanation + code output style

### Hugging Face Datasets Used

The project used Hugging Face instruction-style datasets, including:

1. **CodeAlpaca-20k**
   - stored locally as:
     [code_alpaca_20k.json](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/code_alpaca_20k.json)

2. **CodeFeedback-Filtered-Instruction**
   - stored locally as:
     [CodeFeedback-Filtered-Instruction.json](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/CodeFeedback-Filtered-Instruction.json)

### Fine-Tuning Dataset Preparation

The fine-tuning datasets were filtered and cleaned using:

- [c_scrapper.py](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/c_scrapper.py)

This script was used to:

- read different dataset schemas
- extract C++-relevant rows
- reject many Java/Python rows using heuristics
- build a cleaner instruction dataset

Generated cleaned files include:

- [cleaned_c++_data.json](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/cleaned_c++_data.json)
- [cleaned_c++_v2data.json](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/cleaned_c++_v2data.json)

### Formatting for Fine-Tuning

The cleaned JSON examples were converted into text format using:

- [cpp_finetune_formatter.py](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/cpp_finetune_formatter.py)

This formatter writes examples like:

```text
User: ...
Assistant:
...
```

Generated formatted files include:

- [cpp_instruction_dataset.txt](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/cpp_instruction_dataset.txt)
- [cpp_instruction_dataset_v2.txt](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/cpp_instruction_dataset_v2.txt)

Those files were merged using:

- [merge_finetune_datasets.py](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/merge_finetune_datasets.py)

Final merged fine-tuning file:

- [fine_tuning_dataset.txt](C:/Users/Omen/Downloads/llm_for_cpp/main/tokenizer/fine_tuning_dataset.txt)

## Step 10 - Fine-Tuning

Fine-tuning is implemented in:

- [finetune.py](C:/Users/Omen/Downloads/llm_for_cpp/main/training/finetune.py)

### What Fine-Tuning Does

1. Loads the base model config from `training_config.json`
2. Loads the base checkpoint `best_model.pt`
3. Reads `fine_tuning_dataset.txt`
4. Tokenizes it internally using the existing tokenizer
5. Adds BOS/EOS in memory
6. Builds train/validation windows
7. Fine-tunes the model at a lower learning rate
8. Saves separate fine-tune checkpoints

### Fine-Tuning Checkpoints

Fine-tuning saves into:

- [artifacts/finetune](C:/Users/Omen/Downloads/llm_for_cpp/artifacts/finetune)

Important files:

- [finetune_config.json](C:/Users/Omen/Downloads/llm_for_cpp/artifacts/finetune/finetune_config.json)
- [finetune_best_model.pt](C:/Users/Omen/Downloads/llm_for_cpp/artifacts/finetune/finetune_best_model.pt)

### Why Fine-Tuning Uses the Same Tokenizer

The project keeps the same tokenizer during fine-tuning because:

- the base checkpoint expects that vocabulary
- changing tokenizer would break checkpoint compatibility
- continuing with the same tokenizer is simpler and correct for checkpoint reuse

## Step 11 - API, Frontend, and Docker Preparation

The project also contains an app layer for later deployment.

### Backend

- [app.py](C:/Users/Omen/Downloads/llm_for_cpp/main/backend/app.py)

This provides:

- a simple FastAPI application
- `/api/health`
- `/api/generate`
- `/api/model-info`

The backend now prefers the best fine-tuned checkpoint if it exists:

- [finetune_best_model.pt](C:/Users/Omen/Downloads/llm_for_cpp/artifacts/finetune/finetune_best_model.pt)

and falls back to the base checkpoint if a fine-tuned checkpoint is not available.

### Frontend

- [main/frontend/index.html](C:/Users/Omen/Downloads/llm_for_cpp/main/frontend/index.html)
- [main/frontend/styles.css](C:/Users/Omen/Downloads/llm_for_cpp/main/frontend/styles.css)
- [main/frontend/app.js](C:/Users/Omen/Downloads/llm_for_cpp/main/frontend/app.js)

This is a simple UI for:

- entering prompts
- submitting generation requests
- reading generated output

### Docker

The repo also includes:

- [Dockerfile](C:/Users/Omen/Downloads/llm_for_cpp/Dockerfile)
- [.dockerignore](C:/Users/Omen/Downloads/llm_for_cpp/.dockerignore)

The purpose is to support later containerization of:

- backend
- frontend
- model loading

## Step 11.5 - How To Run The Backend And Frontend

From the project root:

```powershell
uvicorn main.backend.app:app --reload
```

Then open:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)

What this starts:

1. FastAPI backend for model inference
2. static frontend served from `main/frontend`
3. local prompt-to-response generation in the browser

The main API routes are:

- `GET /api/health`
- `GET /api/model-info`
- `POST /api/generate`

### Expected Local Flow

1. Start the backend with `uvicorn`
2. Open the browser page at `127.0.0.1:8000`
3. Type a C++ prompt such as:
   - `write code for hello world`
   - `write a C++ function to check if a number is prime`
4. The frontend sends the prompt to `/api/generate`
5. The backend loads the tokenizer, model config, and best checkpoint
6. The model generates a response and returns it to the UI

## Step 12 - Planned Product Goal From the Roadmap

The long-term product goal is not only to train a model, but to build a **simple usable website** on top of it.

The intended user flow is:

1. A user opens a basic web page.
2. The user types a prompt such as:
   - `write code for hello world`
   - `write a C++ function to check if a number is prime`
   - `give me a black hole simulation code snippet`
3. The frontend sends the prompt to the backend.
4. The backend loads the fine-tuned model and tokenizer.
5. The backend runs inference.
6. The website returns generated C++ code, and ideally an explanation too.

This goal comes directly from the project roadmap in [codex.md](C:/Users/Omen/Downloads/llm_for_cpp/codex.md:1).

## Step 13 - Planned Phase-Based Product Roadmap

The project roadmap was designed in phases so the system can be built carefully rather than all at once.

## Current Model Results

The project has reached a working prototype stage.

### Base Training Result

After the base 10-epoch run, the model showed:

- Train Loss: `1.2452`
- Val Loss: `3.0875`
- Perplexity: `21.92`

This showed that the decoder-only Transformer learned C++ syntax patterns, but it was still weak at following direct user instructions.

### Fine-Tuning Result

After instruction-style fine-tuning on the filtered Hugging Face C++ dataset mixture, the latest recorded fine-tuning result showed:

- Train Loss: `1.8772`
- Val Loss: `1.9557`
- Perplexity: `7.07`

This indicates that fine-tuning improved prompt-following behavior compared with the base model, even though the model is still only prototype quality.

### Example Prototype Result

Example browser test:

Prompt:

```cpp
#include <iostream>
using namespace std;

int main(){
cout<
```

Model output:

```cpp
int main(){
    string s = "Hello World!";
    cout<<"Hello World!";
    cout<<"Hello World!";
    return 0;
}
```

This result shows:

- the app is able to serve the model in the frontend
- the model understands basic C++ code structure
- the model can produce a plausible completion
- but it is still weak at exact code completion and may repeat or improvise

### Accuracy And Evaluation Note

This project does **not** currently have a single reliable “accuracy” percentage in the way a classifier would.

For a generation model like this, the current useful quality signals are:

- validation loss
- perplexity
- sample prompt outputs
- later, task-based evaluation such as compile success and instruction-following checks

So the best reported quantitative metric right now is:

- latest fine-tuning perplexity: `7.07`

and the most honest practical evaluation is:

- the frontend works
- the model generates C++-like responses
- instruction following improved after fine-tuning
- but the outputs are still not production-grade


Anyone reading this project should understand it as:

- a learning project,
- a custom LLM training pipeline,
- a roadmap-driven build of a basic website-backed C++ assistant,
- and a practical step-by-step build toward a useful C++ coding assistant.
