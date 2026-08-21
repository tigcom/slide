"""Test clone một đoạn ngắn từ giọng thật (clone_ref.wav) bằng VieNeu-TTS."""
import os
import sys
import time

# Windows console mặc định là cp1252, không in được tiếng Việt có dấu.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

TEST_TEXT = "Dạ chào mọi người. Hôm nay em xin trình bày về việc kết hợp sử dụng plugin cho Claude."
REF = "clone_ref_5s.wav"
OUT = "test_clone_output.wav"


def main() -> int:
    if not os.path.exists(REF):
        print(f"Thiếu file ref: {REF}", file=sys.stderr)
        return 2

    from vieneu import Vieneu

    t0 = time.time()
    print("Đang khởi tạo model Vieneu (lần đầu sẽ tải model từ HuggingFace)...")
    tts = Vieneu()
    print(f"Khởi tạo xong trong {time.time() - t0:.1f}s")

    t1 = time.time()
    print(f"Đang clone: {TEST_TEXT!r}")
    audio = tts.infer(TEST_TEXT, ref_audio=REF, denoise=True)
    print(f"Suy luận xong trong {time.time() - t1:.1f}s")

    tts.save(audio, OUT)
    size = os.path.getsize(OUT)
    print(f"Đã lưu: {OUT} ({size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
