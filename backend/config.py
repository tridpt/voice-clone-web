"""Cấu hình tập trung cho ứng dụng voice clone."""
from pathlib import Path

# ----- Đường dẫn -----
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "backend" / "model"      # nơi lưu weights viXTTS
STORAGE_DIR = BASE_DIR / "storage"               # audio mẫu + audio sinh ra
UPLOAD_DIR = STORAGE_DIR / "uploads"
OUTPUT_DIR = STORAGE_DIR / "outputs"

for _d in (MODEL_DIR, UPLOAD_DIR, OUTPUT_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ----- Model -----
# Repo Hugging Face chứa viXTTS (fine-tune tiếng Việt từ XTTS-v2)
HF_REPO_ID = "capleaf/viXTTS"
DEFAULT_LANGUAGE = "vi"

# ----- Thiết bị -----
# Tự dùng GPU nếu có (Colab Pro / máy có CUDA), nếu không thì CPU.
# Phát hiện torch ở dạng "mềm" để app vẫn khởi động được khi chưa cài torch.
def _detect_device() -> str:
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


DEVICE = _detect_device()

# ----- Giới hạn -----
MAX_TEXT_LENGTH = 1000          # số ký tự tối đa mỗi lần sinh
MIN_REFERENCE_SECONDS = 3       # độ dài tối thiểu của audio mẫu khuyến nghị
