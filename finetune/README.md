# 🔧 Fine-tune viXTTS trên giọng riêng (Google Colab Pro)

Notebook `viXTTS_finetune_colab.ipynb` fine-tune **tiếp** từ checkpoint [viXTTS](https://huggingface.co/capleaf/viXTTS) (đã mở rộng tokenizer tiếng Việt) trên **giọng của riêng bạn** để đạt chất lượng cao hơn so với clone zero-shot.

> ⚠️ Chỉ fine-tune với giọng của chính bạn hoặc giọng có **đồng ý hợp pháp**. Mục đích: học tập / nghiên cứu.

## Chạy ở đâu

Toàn bộ cài đặt nằm **trong notebook** — không cài gì ở máy local. Mở trên Google Colab Pro, chọn Runtime GPU (T4/L4/A100), rồi chạy lần lượt từng cell.

## Chuẩn bị dữ liệu

Bạn cần audio giọng nói + bản ghi lời (transcript). Khuyến nghị:

- **Tổng thời lượng:** 10–60 phút (càng nhiều giọng càng giống, nhưng 15–30 phút đã cho kết quả tốt)
- **Mỗi đoạn:** 2–15 giây, một câu rõ ràng
- **Chất lượng:** thu sạch, ít ồn, một người nói, sample rate ≥ 22kHz
- **Định dạng file metadata** (LJSpeech-style), tên `metadata.csv`, phân tách bằng `|`:

```
wavs/0001.wav|Xin chào, đây là giọng nói mẫu của tôi.|speaker1
wavs/0002.wav|Hôm nay trời đẹp, tôi đi học rất vui.|speaker1
```

Cấu trúc thư mục dataset nén thành `dataset.zip`:

```
dataset/
├── metadata.csv
└── wavs/
    ├── 0001.wav
    ├── 0002.wav
    └── ...
```

Notebook có sẵn cell giúp **tự cắt + tạo transcript bằng Whisper** nếu bạn chỉ có vài file audio dài và chưa có transcript.

## Sau khi train xong

Notebook xuất ra checkpoint fine-tune (`model.pth`, `config.json`, `vocab.json`). Bạn:
1. Tải về máy
2. Copy vào `voice-clone-web/backend/model/` để web app dùng giọng đã fine-tune
   (hoặc trỏ `HF_REPO_ID`/đường dẫn model trong `config.py` tới checkpoint mới)

## Lưu ý thời gian / chi phí

- T4: ~vài giờ cho vài nghìn step (đủ cho dataset nhỏ)
- A100: nhanh hơn nhiều
- Lưu checkpoint định kỳ ra Google Drive để không mất khi Colab ngắt phiên
