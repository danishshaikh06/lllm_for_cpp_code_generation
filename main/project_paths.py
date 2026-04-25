from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAIN_DIR = PROJECT_ROOT / "main"
TOKENIZER_DIR = MAIN_DIR / "tokenizer"
TRAINING_DIR = MAIN_DIR / "training"
FRONTEND_DIR = MAIN_DIR / "frontend"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

TOKENIZER_FILE = TOKENIZER_DIR / "tokenizer.json"
TOKENS_FILE = TOKENIZER_DIR / "tokens.npy"
TOKENS_WITH_SPECIAL_FILE = TOKENIZER_DIR / "tokens_with_specialv2.npy"

TRAINING_CONFIG_FILE = ARTIFACTS_DIR / "training_config.json"
BEST_MODEL_FILE = ARTIFACTS_DIR / "model_epoch_10.pt"


def ensure_artifacts_dir() -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR
