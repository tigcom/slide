"""Sinh audio thuyết trình từ kich-ban-noi.md bằng giọng clone (VieNeu-TTS).

Dùng:
    python build_audio.py --dry-run      # xem trước text đã lọc cho từng slide
    python build_audio.py --generate     # sinh audio/slide_NN.wav cho các slide có lời nói
"""
import os
import re
import sys
import time

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC = "kich-ban-noi.md"
REF = "clone_ref_5s.wav"
OUTDIR = "audio"
VOICE_NAME = "GiongThuyetTrinh"

MARKER_RE = re.compile(r"^【([^】]+)】[ \t]*$")
SECTION_LABEL_RE = re.compile(r"^Phần \d+\s*[—–-].*phút", re.IGNORECASE)
HAS_LETTER = re.compile(r"[a-zA-ZÀ-ỹĐđ]")


def clean_body(lines):
    """Chuyển phần note thô của một slide thành văn bản lời nói sạch."""
    out = []
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if re.match(r"^#{1,6}\s", s):        # tiêu đề cấu trúc
            continue
        if re.match(r"^-{3,}$", s):          # dấu ngăn cách
            continue
        if s.startswith(">"):                 # blockquote
            continue
        if s.startswith("|"):                 # dòng bảng
            continue
        if SECTION_LABEL_RE.match(s):         # "Phần 1 — Mở bài (5 phút)."
            continue
        s = re.sub(r"\*\[[^\]]*\]\*", " ", s)  # chỉ dẫn sân khấu *[...]*
        s = s.replace("**", "")
        s = s.replace("`", "")
        s = s.replace("*", "")
        s = s.replace("→", ", ")
        s = re.sub(r"^\s*[-•]\s+", "", s)     # đầu dòng gạch/chấm
        s = re.sub(r"^\s*\d+[.)]\s+", "", s)  # đầu dòng đánh số
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            out.append(s)
    return " ".join(out)


def has_speech(text):
    return bool(HAS_LETTER.search(text)) and len(text) >= 8


def parse_slides():
    with open(SRC, encoding="utf-8") as f:
        lines = f.read().splitlines()
    slides = []
    cur = None
    for ln in lines:
        if re.match(r"^##\s*Phụ lục", ln):     # dừng ở phần phụ lục (không phải lời nói)
            break
        m = MARKER_RE.match(ln)
        if m:
            if cur:
                slides.append(cur)
            cur = {"name": m.group(1), "lines": []}
        elif cur is not None:
            cur["lines"].append(ln)
    if cur:
        slides.append(cur)
    return slides


def main():
    mode = "--generate" if "--generate" in sys.argv else "--dry-run"
    slides = parse_slides()

    prepared = []
    for i, sl in enumerate(slides, start=1):
        text = clean_body(sl["lines"])
        if has_speech(text):
            prepared.append({"n": i, "name": sl["name"], "text": text})

    print(f"Tổng {len(slides)} marker, {len(prepared)} slide có lời nói.\n")

    if mode == "--dry-run":
        for p in prepared:
            print(f"── [{p['n']:02d}] {p['name']} ──")
            print(p["text"])
            print()
        print("Dùng `--generate` để sinh audio.")
        return 0

    # ── Generate ──
    from vieneu import Vieneu

    os.makedirs(OUTDIR, exist_ok=True)
    print("Khởi tạo model Vieneu...")
    tts = Vieneu()
    print(f"Đăng ký giọng '{VOICE_NAME}' từ {REF}...")
    tts.add_voice(VOICE_NAME, REF, denoise=True)

    for p in prepared:
        out_path = os.path.join(OUTDIR, f"slide_{p['n']:02d}.wav")
        if os.path.exists(out_path):
            print(f"[{p['n']:02d}] đã có, bỏ qua: {out_path}")
            continue
        t0 = time.time()
        print(f"[{p['n']:02d}/{len(slides)}] {p['name']} ({len(p['text'])} ký tự)...", flush=True)
        audio = tts.infer(p["text"], voice=VOICE_NAME, denoise=True, apply_watermark=False)
        tts.save(audio, out_path)
        print(f"    -> {out_path} ({len(audio)/48000:.1f}s, {time.time()-t0:.1f}s)", flush=True)

    print("\nHoàn tất.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
