# 🎙️ Web Clone Giọng Nói Tiếng Việt (viXTTS)

Web app cho phép **thu âm / tải lên giọng mẫu** rồi **clone giọng để đọc văn bản tiếng Việt**, chất lượng cao. Dùng cho **mục đích học tập / nghiên cứu**.

Engine mặc định: [`capleaf/viXTTS`](https://huggingface.co/capleaf/viXTTS) — fine-tune từ XTTS-v2 trên dataset viVoice, clone giọng chỉ từ ~6 giây audio.

> ⚠️ **Lưu ý đạo đức & pháp lý:** Chỉ dùng với giọng của chính bạn hoặc giọng có sự **đồng ý rõ ràng**. Clone giọng người khác để mạo danh, lừa đảo, hoặc tạo nội dung giả là vi phạm pháp luật. App có bước xác nhận đồng ý bắt buộc.

## Cấu trúc

```
voice-clone-web/
├── backend/
│   ├── main.py          # FastAPI: /api/sentences, /api/record, /api/dataset/download, /api/tts
│   ├── tts_engine.py    # Wrapper viXTTS (pluggable)
│   ├── sentences.py     # Bộ câu mẫu tiếng Việt để thu âm dataset
│   └── config.py        # Cấu hình đường dẫn, device, model
├── frontend/
│   ├── index.html       # 2 tab: Thu âm dữ liệu / Thử giọng clone
│   ├── style.css
│   ├── app.js           # Quản lý tab, gọi API
│   └── wav-recorder.js  # Thu âm và encode WAV phía trình duyệt
├── finetune/            # Notebook fine-tune viXTTS trên Colab
└── storage/             # Dataset đã thu + audio sinh ra
```

## Yêu cầu

- Python 3.10 hoặc 3.11 (khuyến nghị; Coqui TTS hợp nhất với các bản này)
- GPU NVIDIA có CUDA để chạy nhanh (CPU vẫn chạy được nhưng chậm)

## Chạy ở máy local

```bash
cd voice-clone-web
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

# Cài PyTorch trước (chọn 1 trong 2):
pip install torch torchaudio                                                   # CPU
# pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121  # GPU CUDA 12.x

pip install -r requirements.txt
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8808
```

Mở trình duyệt: <http://localhost:8808>

> Lần chạy đầu tiên sẽ tự **tải weights viXTTS** từ Hugging Face (~vài trăm MB) nên hơi lâu. Các lần sau load nhanh.

> Thu âm bằng micro yêu cầu trang chạy trên `localhost` hoặc HTTPS (giới hạn bảo mật của trình duyệt).

## Chạy trên Google Colab Pro

Colab Pro (GPU T4/L4/A100) chạy rất tốt. Tạo một cell:

```python
!git clone <repo-cua-ban> voice-clone-web   # hoặc upload thư mục
%cd voice-clone-web
!pip install -q -r requirements.txt
!pip install -q pyngrok

import threading, subprocess
from pyngrok import ngrok

# Chạy server nền
def run():
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8808"], cwd="backend")
threading.Thread(target=run, daemon=True).start()

# Mở tunnel công khai để truy cập UI từ trình duyệt
print(ngrok.connect(8808).public_url)
```

Bấm vào URL ngrok in ra là vào được giao diện web.

## Đổi sang model khác (nâng cao)

Engine thiết kế dạng **pluggable**. Để thử model khác (VieNeu-TTS, F5-TTS-Vietnamese...), tạo một class mới trong `tts_engine.py` có cùng phương thức:

```python
def synthesize(self, text: str, reference_wav: str, language: str = "vi") -> str:
    ...  # trả về đường dẫn file .wav
```

rồi gán `engine = YourEngine()` ở cuối file.

## Hướng phát triển tiếp
- Lọc nhiễu audio mẫu tự động trước khi clone
- Tách câu dài thành nhiều đoạn để đọc ổn định hơn
- Thêm xác thực người dùng nếu deploy công khai (hiện API chưa có auth)
```
