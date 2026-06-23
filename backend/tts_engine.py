"""Wrapper cho engine viXTTS.

Thiết kế dạng pluggable: nếu sau này muốn đổi sang VieNeu-TTS hay F5-TTS,
chỉ cần tạo class mới với cùng phương thức `synthesize()`.

Model được load lazy (chỉ load khi gọi lần đầu) để app khởi động nhanh.
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path

from config import (
    DEFAULT_LANGUAGE,
    DEVICE,
    HF_REPO_ID,
    MODEL_DIR,
    OUTPUT_DIR,
)


class ViXTTSEngine:
    """Bao bọc model viXTTS để clone giọng và sinh tiếng nói tiếng Việt."""

    def __init__(self) -> None:
        self._model = None          # lazy-load
        self._normalizer = None

    # ---------- chuẩn bị model ----------
    def _ensure_downloaded(self) -> Path:
        """Tải weights viXTTS từ Hugging Face nếu chưa có."""
        from huggingface_hub import snapshot_download

        required = ["config.json", "model.pth", "vocab.json"]
        have_all = all((MODEL_DIR / f).exists() for f in required)
        if not have_all:
            snapshot_download(
                repo_id=HF_REPO_ID,
                local_dir=str(MODEL_DIR),
                local_dir_use_symlinks=False,
            )
        return MODEL_DIR

    def _load(self) -> None:
        """Khởi tạo model trong bộ nhớ (chỉ chạy 1 lần)."""
        if self._model is not None:
            return

        # Import ở đây để app không nặng lúc khởi động khi chưa cần TTS
        try:
            from TTS.tts.configs.xtts_config import XttsConfig
            from TTS.tts.models.xtts import Xtts
        except ImportError as exc:
            raise RuntimeError(
                "Chưa cài thư viện TTS. Cài bằng: pip install coqui-tts torch torchaudio "
                "(xem README phần cài đặt đầy đủ)."
            ) from exc

        model_dir = self._ensure_downloaded()

        config = XttsConfig()
        config.load_json(str(model_dir / "config.json"))

        model = Xtts.init_from_config(config)
        model.load_checkpoint(
            config,
            checkpoint_dir=str(model_dir),
            use_deepspeed=False,
        )
        model.to(DEVICE)
        model.eval()
        self._model = model

    # ---------- chuẩn hóa text tiếng Việt ----------
    def _normalize_vi(self, text: str) -> str:
        """Chuẩn hóa số, ký hiệu... sang chữ để đọc tự nhiên hơn."""
        if self._normalizer is None:
            try:
                from vinorm import TTSnorm
                self._normalizer = TTSnorm
            except Exception:
                # Nếu vinorm chưa cài được, dùng text gốc
                self._normalizer = lambda t, **_: t
        try:
            return self._normalizer(text, unknown=False, lower=False, rule=True)
        except Exception:
            return text

    # ---------- sinh tiếng nói ----------
    def synthesize(
        self,
        text: str,
        reference_wav: str,
        language: str = DEFAULT_LANGUAGE,
    ) -> str:
        """Clone giọng từ `reference_wav` và đọc `text`.

        Trả về đường dẫn file wav kết quả.
        """
        self._load()
        text = self._normalize_vi(text.strip())

        # Lấy embedding đặc trưng giọng nói từ audio mẫu
        gpt_cond_latent, speaker_embedding = self._model.get_conditioning_latents(
            audio_path=reference_wav,
            gpt_cond_len=self._model.config.gpt_cond_len,
            max_ref_length=self._model.config.max_ref_len,
            sound_norm_refs=self._model.config.sound_norm_refs,
        )

        out = self._model.inference(
            text=text,
            language=language,
            gpt_cond_latent=gpt_cond_latent,
            speaker_embedding=speaker_embedding,
            temperature=0.3,
            enable_text_splitting=True,
        )

        out_path = OUTPUT_DIR / f"{uuid.uuid4().hex}.wav"
        self._save_wav(out["wav"], out_path)
        return str(out_path)

    @staticmethod
    def _save_wav(wav, path: Path) -> None:
        import torch
        import torchaudio

        tensor = torch.tensor(wav).unsqueeze(0)
        torchaudio.save(str(path), tensor, sample_rate=24000)


# Một instance dùng chung cho toàn app
engine = ViXTTSEngine()
