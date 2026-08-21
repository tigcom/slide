# Ý tưởng: lệnh `/demo` — demo "ấm" để tránh im lặng & chạy quá giờ

> Trạng thái: **chỉ lưu ý tưởng, chưa triển khai** (2026-08-19).
> Ngữ cảnh: buổi thuyết trình ~70' về hệ plugin Claude. Phần Demo (10 phút, 4 bước) đang là chỗ rủi ro nhất.

## Vấn đề cần giải

1. Demo dễ **chạy quá giờ** (10 phút cho 4 bước).
2. Sợ nhất **khoảng im lặng** khi Claude đang chạy — người nói không muốn phải nói lấp chỗ chờ đó.

## Ý tưởng cốt lõi

- Làm trước **toàn bộ 1 dự án** theo đúng flow 4 bước (User Management Dashboard) cho **hoàn chỉnh**.
- Đóng gói thành một slash command **`/demo`**.
- Lúc lên sân khấu: chạy `/demo` với **cùng một prompt đã thống nhất từ trước** → Claude "diễn" lại nhịp suy nghĩ/làm việc trong ~10–15s, rồi **tiết lộ kết quả hoàn chỉnh ở mọi mặt**.

## Quyết định đã chốt (khi triển khai)

- **Kiểu hành xử của `/demo`:** `Re-run lệnh thật đã 'ấm'` — chạy lại các lệnh thật, nhưng output đã tồn tại sẵn nên trả kết quả **tức thì**. (Không phải thuần playback, không phải thuần live từ đầu.)

## Điểm kỹ thuật quan trọng (tránh hiểu sai)

- **KHÔNG dùng timer/sleep thật** để tạo 10–15s. Claude Code không có cách pause nào trông "đang làm việc" một cách đáng tin — `sleep` chỉ là màn hình đứng im.
- Thay vào đó, `/demo` là một **kịch bản tường thuật có chủ đích**: Claude in lần lượt các dòng *pha* (kèm 1–2 câu mô tả), mỗi pha gắn với một artifact đã build sẵn để "mở ra".
  - Độ dài 10–15s đến từ **số dòng + lượng chữ quy định sẵn**, không phải từ đồng hồ → kiểm soát được nhịp, không có gì để treo.
  - Ví dụ 4 pha: `▸ Đang dựng UI…` (Frontend Design) → `▸ Đang mở trình duyệt…` (Playwright) → `▸ Đang review + commit…` (Code Review) → `▸ Đang tổng kết…` (Session Report).

## Điểm "thủ" được khi bị hỏi vặn

- Chỉ **giả phần thời gian, không giả phần kết quả**: prompt là prompt thật, commit là commit thật (`git log`), report là report thật.
- Nếu ai bảo "cho xem diff đi" → `git log` là có ngay, không hụt hơi.
- Ranh giới: "demo ấm" (chuyên nghiệp) vs "diễn kịch" (dễ vỡ). Trình bày nên trung thực kiểu *"tôi đã chạy trước để không phải chờ API"* thay vì giả vờ chạy từ số 0.

## Các file sẽ tạo khi triển khai

| File | Vai trò |
|---|---|
| `.claude/commands/demo.md` | Slash command: đọc kịch bản, in từng pha, mở artifact tương ứng. |
| `demo/script.md` | Kịch bản 4 pha + đường dẫn artifact mỗi pha + prompt đã thống nhất. Sửa nhịp = sửa file này. |
| `demo/` (staging) | Project đã build hoàn chỉnh, screenshot, report. Lệnh chỉ trỏ tới đây. |

## Câu hỏi còn mở (cần trả lời trước khi làm)

- Project đã build nằm **trong repo này** (`demo/`) hay ở **repo ngoài**? → quyết định path ghi vào `demo/script.md`.
- Prompt "đã thống nhất" cuối cùng là câu lệnh gì (dán nguyên văn vào `demo/script.md`)?
