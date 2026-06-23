"""FastAPI backend cho web clone giọng nói tiếng Việt (viXTTS).

Hai chức năng:
1. Studio thu âm: đọc các câu mẫu -> lưu từng đoạn -> xuất dataset.zip để fine-tune.
2. Thử giọng: dùng model (gốc hoặc đã fine-tune) để đọc câu test.

Mục đích: học tập / nghiên cứu. Chỉ dùng với giọng của chính bạn
hoặc giọng có sự đồng ý rõ ràng.
"""
from __future__ import annotations

import csv
import io
import shutil
import zipfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from config import (
    BASE_DIR,
    MAX_TEXT_LENGTH,
    STORAGE_DIR,
)
from sentences import SAMPLE_SENTENCES

app = FastAPI(title="Vietnamese Voice Clone Studio", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thư mục lưu các đoạn thu âm cho dataset
DATASET_DIR = STORAGE_DIR / "dataset"
WAVS_DIR = DATASET_DIR / "wavs"
WAVS_DIR.mkdir(parents=True, exist_ok=True)

# File ghi cặp (tên file <-> câu đã đọc)
METADATA_PATH = DATASET_DIR / "metadata.csv"


@app.get("/api/health")
def health() -> dict:
    """Trạng thái server + thiết bị + số mẫu đã thu."""
    from config import DEVICE

    recorded = len(list(WAVS_DIR.glob("*.wav")))
    return {
        "status": "ok",
        "device": DEVICE,
        "total_sentences": len(SAMPLE_SENTENCES),
        "recorded": recorded,
    }


@app.get("/api/sentences")
def get_sentences() -> dict:
    """Trả danh sách câu mẫu để đọc, kèm câu nào đã thu rồi."""
    recorded_ids = {p.stem for p in WAVS_DIR.glob("*.wav")}
    items = [
        {
            "id": i,
            "text": text,
            "recorded": f"{i:04d}" in recorded_ids,
        }
        for i, text in enumerate(SAMPLE_SENTENCES)
    ]
    return {"sentences": items}


# ---------------- Studio thu âm dataset ----------------
@app.post("/api/record")
async def record_sample(
    sentence_id: int = Form(...),
    audio: UploadFile = File(...),
) -> dict:
    """Lưu một đoạn thu âm tương ứng với câu mẫu thứ `sentence_id`.

    Audio đã được encode thành WAV phía trình duyệt nên backend
    chỉ cần lưu file, không cần thư viện xử lý audio nặng.
    """
    if sentence_id < 0 or sentence_id >= len(SAMPLE_SENTENCES):
        raise HTTPException(status_code=400, detail="sentence_id không hợp lệ.")

    wav_path = WAVS_DIR / f"{sentence_id:04d}.wav"
    with wav_path.open("wb") as f:
        shutil.copyfileobj(audio.file, f)

    _rebuild_metadata()
    recorded = len(list(WAVS_DIR.glob("*.wav")))
    return {"ok": True, "recorded": recorded, "total": len(SAMPLE_SENTENCES)}


@app.delete("/api/record/{sentence_id}")
def delete_sample(sentence_id: int) -> dict:
    """Xóa một đoạn đã thu để thu lại."""
    wav_path = WAVS_DIR / f"{sentence_id:04d}.wav"
    if wav_path.exists():
        wav_path.unlink()
        _rebuild_metadata()
    recorded = len(list(WAVS_DIR.glob("*.wav")))
    return {"ok": True, "recorded": recorded}


def _rebuild_metadata() -> None:
    """Sinh lại metadata.csv (LJSpeech-style) từ các file wav hiện có."""
    rows = []
    for p in sorted(WAVS_DIR.glob("*.wav")):
        idx = int(p.stem)
        if 0 <= idx < len(SAMPLE_SENTENCES):
            rows.append([f"wavs/{p.name}", SAMPLE_SENTENCES[idx], "speaker1"])
    with METADATA_PATH.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f, delimiter="|").writerows(rows)


@app.get("/api/dataset/download")
def download_dataset() -> StreamingResponse:
    """Đóng gói dataset (metadata.csv + wavs/) thành zip để tải về."""
    wavs = sorted(WAVS_DIR.glob("*.wav"))
    if not wavs:
        raise HTTPException(status_code=400, detail="Chưa thu âm mẫu nào.")

    _rebuild_metadata()

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(METADATA_PATH, "dataset/metadata.csv")
        for p in wavs:
            zf.write(p, f"dataset/wavs/{p.name}")
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=dataset.zip"},
    )


# ---------------- Thử giọng clone ----------------
@app.post("/api/tts")
async def try_voice(
    text: str = Form(...),
    consent: bool = Form(...),
    reference_id: int = Form(-1),
    audio: UploadFile | None = File(None),
) -> FileResponse:
    """Sinh tiếng nói từ `text` bằng giọng tham chiếu.

    Giọng tham chiếu lấy từ:
    - file audio upload (nếu có), hoặc
    - một mẫu đã thu trong dataset (reference_id), hoặc
    - mẫu đầu tiên trong dataset nếu không chỉ định.
    """
    if not consent:
        raise HTTPException(
            status_code=400,
            detail="Bạn cần xác nhận có quyền sử dụng giọng nói này.",
        )

    text = (text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Vui lòng nhập nội dung cần đọc.")
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Nội dung quá dài (tối đa {MAX_TEXT_LENGTH} ký tự).",
        )

    # Xác định file giọng tham chiếu
    ref_path = _resolve_reference(audio, reference_id)

    # Engine TTS nạp lazy; nếu chưa cài sẽ báo lỗi rõ ràng
    try:
        from tts_engine import engine

        out_path = engine.synthesize(text=text, reference_wav=str(ref_path))
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Lỗi khi sinh tiếng nói: {exc}")

    return FileResponse(out_path, media_type="audio/wav", filename="cloned_voice.wav")


def _resolve_reference(audio: UploadFile | None, reference_id: int) -> Path:
    """Tìm file wav giọng tham chiếu, ưu tiên file upload."""
    if audio is not None:
        ref_path = STORAGE_DIR / "uploads" / "ref_tmp.wav"
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        with ref_path.open("wb") as f:
            shutil.copyfileobj(audio.file, f)
        return ref_path

    if reference_id >= 0:
        p = WAVS_DIR / f"{reference_id:04d}.wav"
        if p.exists():
            return p

    # fallback: mẫu thu âm đầu tiên
    wavs = sorted(WAVS_DIR.glob("*.wav"))
    if not wavs:
        raise HTTPException(
            status_code=400,
            detail="Chưa có giọng mẫu. Hãy thu âm ở tab Studio hoặc tải file lên.",
        )
    return wavs[0]


# Phục vụ file audio đã thu (để nghe lại trong trình duyệt)
app.mount("/storage", StaticFiles(directory=str(STORAGE_DIR)), name="storage")

# Phục vụ frontend tĩnh (đặt cuối để không che các route /api)
frontend_dir = BASE_DIR / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
