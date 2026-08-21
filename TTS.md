# Voice clone TTS (VieNeu-TTS)

Clone giọng nói để đọc kịch bản `kich-ban-noi.md` thành 27 file audio cho từng slide.

## Yêu cầu

- Python 3.11 (dùng đúng Python global, không phải venv khác — xem mục "Ghi chú").
- `ffmpeg` (để cắt ref audio).
- Mạng lần đầu để tải model (~305MB, cache vào HuggingFace).

## Cài đặt

```bash
pip install vieneu
pip install "transformers==4.57.6"      # vieneu cần transformers 4.57.x
pip install "protobuf>=6.31.1,<8.0.0"   # tránh xung đột protobuf/tensorflow
```

## Chuẩn bị giọng (ref audio)

- Cần một đoạn **3–5 giây**, giọng rõ, ít tạp âm. **Không dùng file dài** — clone sẽ sai giọng / méo.
- Cắt đoạn sạch nhất thành mono 48kHz bằng ffmpeg:

```bash
ffmpeg -y -i <file_goc.wav> -ss 7.5 -t 5 -ac 1 -ar 48000 clone_ref_5s.wav
```

- Đặt đúng tên `clone_ref_5s.wav` ở gốc repo (mono, 48kHz).

## Chạy

```bash
# Windows: cần PYTHONIOENCODING=utf-8 (console cp1252 không in được tiếng Việt)
python build_audio.py --dry-run     # xem trước text đã lọc cho từng slide
python build_audio.py --generate    # sinh audio/slide_01.wav ... slide_27.wav
```

- `build_audio.py` tự: parse 27 marker `【…】` trong `kich-ban-noi.md`, lọc bỏ tiêu đề phần / chỉ dẫn sân khấu `*[...]*` / bảng / phụ lục, rồi clone từng slide.
- `test_clone.py` dùng để test nhanh một câu trước khi chạy cả bài.

## Ghi chú môi trường

- Dùng Python global `C:\Users\...\Programs\Python\Python311\python.exe`; lệnh `python` có thể trỏ vào một venv khác (không có vieneu/pip). Kiểm tra bằng `python -c "import vieneu"`.
- Model tự tải về cache HuggingFace, không cần tải thủ công.
- Giọng (`clone_ref*.wav`) và audio output (`audio/`) **không được commit** — đã nằm trong `.gitignore`.
