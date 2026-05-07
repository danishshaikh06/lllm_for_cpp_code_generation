from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from main.project_paths import FINETUNE_BEST_MODEL_FILE, TRAINING_CONFIG_FILE
from main.training.inference import generate_completion, load_runtime
from main.project_paths import FRONTEND_DIR


app = FastAPI(title="C++ Code Generator")


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User request for C++ code generation.")
    max_new_tokens: int = Field(default=180, ge=32, le=512)
    temperature: float = Field(default=0.8, ge=0.0, le=2.0)
    top_k: int = Field(default=40, ge=1, le=200)


@lru_cache(maxsize=1)
def get_runtime():
    return load_runtime()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/model-info")
def model_info():
    active_checkpoint = FINETUNE_BEST_MODEL_FILE if FINETUNE_BEST_MODEL_FILE.exists() else None
    quality_snapshot = None

    if active_checkpoint is not None:
        quality_snapshot = {
            "metric_type": "validation_perplexity",
            "value": 7.07,
            "notes": (
                "This is the latest recorded fine-tuning validation perplexity. "
                "For this project, it is a better quality signal than a single accuracy number."
            ),
        }

    return {
        "using_finetuned_model": active_checkpoint is not None,
        "checkpoint_path": str(active_checkpoint) if active_checkpoint else None,
        "config_path": str(TRAINING_CONFIG_FILE),
        "quality_snapshot": quality_snapshot,
    }


@app.post("/api/generate")
def generate_code(request: GenerateRequest):
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    try:
        runtime = get_runtime()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Model artifacts are missing. Train the model first so "
                f"{exc.filename or 'the checkpoint files'} can be loaded."
            ),
        ) from exc

    config = runtime["config"]

    try:
        response = generate_completion(
            model=runtime["model"],
            tokenizer=runtime["tokenizer"],
            prompt=prompt,
            seq_len=config["seq_len"],
            pad_id=config["pad_id"],
            eos_id=config["eos_id"],
            bos_id=config.get("bos_id"),
            device=runtime["device"],
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            top_k=request.top_k,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"prompt": prompt, "response": response}


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
