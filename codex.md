# Codex Plan for Personal C++ Code Generator

This file is the working guide for the project. Each major phase should be approved before implementation starts, and each phase should end with a short explanation of what changed, why it changed, and how to run it.

## Phase Gates

- Phase 0 approval: training cleanup, local inference, and code review of tokenizer/transformer.
- Phase 1 approval: product behavior for prompt-to-C++ generation.
- Phase 2 approval: backend, frontend, and local app flow.

## Phase 0

### Goal

Make the training pipeline runnable without Weights & Biases, keep artifacts organized, and add local sample generation so progress is visible during training.

### Changes

- Remove all `wandb` dependencies from training.
- Save checkpoints and the matching architecture config into `artifacts/`.
- Add sample inference every 5 epochs.
- Keep training numerically stable with device-aware mixed precision.
- Normalize project paths so scripts work from the repo root.

### How to run

```powershell
python -m main.training.train
```

### What to learn while doing it

- Why model config needs to be saved next to checkpoints.
- Why inference should reuse the same tokenizer, sequence length, and special-token IDs as training.
- Why noisy prints in the hot loop slow training.

## Phase 0.5

### Goal

Provide a standalone inference entrypoint for prompt-in, generated-text-out local testing.

### Changes

- Add `main/inference.py`.
- Use a simple prompt template that nudges the model toward explanation plus code.
- Support max tokens, temperature, top-k, and EOS stopping.

### How to run

```powershell
python -m main.inference "Give me a hello world program in C++ with explanation"
```

### What to learn while doing it

- How autoregressive decoding works one token at a time.
- Why temperature and top-k change output style.
- Why prompt formatting matters even for a small model.

## Phase 0.75

### Goal

Dockerize the local serving stack after training and inference work locally.

### Changes

- Add a simple `Dockerfile`.
- Keep the container focused on API plus frontend serving.
- Mount model artifacts into the container when needed.

### How to run

```powershell
docker build -t cpp-codegen .
docker run --rm -p 8000:8000 -v ${PWD}\artifacts:/app/artifacts cpp-codegen
```

### What to learn while doing it

- `docker build` creates the image from the Dockerfile.
- `docker run` starts a container from that image.
- `-p 8000:8000` maps the local port to the container port.
- `-v ...:/app/artifacts` mounts trained checkpoints into the container without baking them into the image.

## Phase 1

### Goal

Support the first product workflow: ask for C++ code and receive explanation plus code or a focused snippet.

### Rules

- Keep v1 focused on C++ generation and explanation only.
- Prefer full code by default.
- If the prompt explicitly asks for a snippet, return a snippet instead of a full application.

## Phase 2

### Goal

Add a minimal backend and a simple frontend for local usage before any hosting work.

### Changes

- Backend endpoint: `POST /api/generate`.
- Frontend: one prompt box, decoding controls, one response panel, and basic status messages.
- Keep the local app simple enough to understand and extend.

### How to run

```powershell
uvicorn main.app:app --reload
```

Open `http://127.0.0.1:8000`.

### What to learn while doing it

- The frontend sends JSON to the backend.
- The backend loads the model once, runs generation, and returns text.
- Keeping the frontend static makes local development simpler.

## Validation Checklist

- Tokenizer encode/decode still works for representative C++ snippets.
- Training saves checkpoints and config files into `artifacts/`.
- Training sample inference runs every 5 epochs.
- Standalone inference works from the command line.
- The backend responds on `/api/generate`.
- The frontend renders loading, success, and error states.

## Notes for Later Hosting

- Start with local serving first.
- If the model is too heavy for Vercel execution, host the frontend separately from inference.
- Keep the API boundary narrow so deployment can change later without rewriting the UI.
