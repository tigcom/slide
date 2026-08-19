# Kịch bản nói — Claude + Plugin (70 phút)

> Đây là lời nói gợi ý cho từng phần, đồng bộ với `slides.json` (cùng id section). Bạn có thể đọc theo hoặc diễn đạt lại bằng cách của mình. Dấu `【…】` đánh dấu slide đang hiển thị.

---

【Trang bìa】

Chào mọi người. Hôm nay tôi trình bày về **Claude + Plugin** — từ công cụ tự vận hành đến nền tảng mở rộng.

Thời lượng ~70 phút + Q&A 5–10 phút. Đối tượng: đồng nghiệp + sếp.

---

## Phần 1 — Mở bài (5 phút)

【Mở bài — Luận điểm】

Phần 1 — Mở bài (5 phút).

Đặt luận điểm cốt lõi: **Claude Code không phải chatbot**, plugin là cách mở rộng nó. 3 slide tiếp: Luận điểm cốt lõi → Điều cần nhớ → Mạch của buổi nói.

【Luận điểm cốt lõi】

Hôm nay tôi muốn trình bày một quan điểm có chủ đích, thay vì chỉ liệt kê danh sách công cụ.

Quan điểm của tôi gồm hai ý. Thứ nhất: **Claude Code vốn đã là công cụ tự vận hành — không phải chatbot.** Thứ hai: **plugin là cách mở rộng nó, lấp các khoảng trống mà bản nguyên bản chưa có.**
【Điều cần nhớ】

Một câu để mọi người nhớ về buổi này: **đừng chỉ dùng Claude như một chatbot — hãy mở rộng nó bằng plugin để nó tự vận hành trọn gói.**
【Mạch của buổi nói】

Buổi nói đi theo 3 bước. Trước hết là **khái niệm và phân loại** — bản nguyên bản còn thiếu gì, plugin là gì. Tiếp theo là **cơ chế vận hành** — bên trong plugin gồm những cơ chế nào. Cuối cùng là **minh họa thực tế** bằng 4 plugin và một demo.

---

## Phần 2 — Khái niệm & phân loại (20 phút)

【Khái niệm & phân loại】

Phần 2 — Khái niệm & phân loại (20 phút).

Đi qua: 4 giới hạn của bản nguyên bản → "plugin" là gì → 3 loại plugin.

### 2.1 — Claude nguyên bản: 4 giới hạn (8 phút)

【Claude Code: Giới hạn】

Trước hết phải gỡ một hiểu lầm phổ biến: nhiều người hình dung Claude là chatbot — hỏi một câu, nhận câu trả lời, rồi copy-paste. Với Claude Code thì không đúng.

Bản nguyên bản — chưa cài plugin gì — đã tự đọc/sửa file, chạy lệnh, tìm code, thao tác git. Nó đã là công cụ tự vận hành.

Nhưng tự nó vẫn còn 4 giới hạn. Ta xem từng cái.

【4 giới hạn của Claude nguyên bản】

Thứ nhất, **biết làm nhưng chưa có phương pháp chuẩn**: Claude viết được frontend, nhưng không theo một quy trình chuyên biệt nhất quán — nên chất lượng phụ thuộc cách mình đặt vấn đề từng lần.

Thứ hai, **chỉ suy luận, không quan sát hay hành động thực tế**: nó đọc code, viết code, dự đoán lỗi — nhưng không thực sự nhìn và thao tác hệ thống bên ngoài, như trình duyệt đang chạy, database, API.

Thứ ba, **chỉ làm khi được gọi**: mỗi bước review, test, commit đều phải do mình chủ động yêu cầu — không có cơ chế "khi sự kiện xảy ra thì tự chạy".

Thứ tư, **khó tổng hợp "đã làm gì"**: việc lớn qua nhiều đầu việc, sau đó khó biết nó đã làm gì, đổi file nào, còn gì chưa xong.

【Kết luận】

Tóm lại: Claude nguyên bản mạnh ở suy nghĩ và viết code; còn trống ở 4 chỗ — phương pháp chuẩn, quan sát thực tế, tự kích hoạt, và tổng hợp kết quả. Lưu ý: có giới hạn là "chưa làm được", có giới hạn là "làm được nhưng chưa nhất quán".

### 2.2 — "Plugin" là gì (7 phút)

【Plugin là gì】

Vậy lấp các khoảng trống đó bằng cách nào? Bằng cách mở rộng Claude — ta gọi chung là **plugin**.

"Plugin" ở đây hiểu theo nghĩa rộng: là cơ chế mở rộng khả năng làm việc của Claude. Bên trong một plugin có thể là một thành phần đơn lẻ, hoặc nhiều thành phần kết hợp.

Mỗi plugin nhắm một kiểu khoảng trống: phương pháp, hành động, tự kích hoạt, hoặc tổng hợp.

【Kết luận】

Tóm lại: plugin không biến Claude từ "không làm được" thành "làm được" — nó mở rộng Claude, theo hai kiểu: lấp khoảng trống "chưa làm được", và chuẩn hóa chỗ "làm được nhưng chưa nhất quán".

### 2.3 — Phân loại (5 phút)

【Hệ sinh thái plugin — 3 loại】

Vậy hệ sinh thái plugin gồm những loại nào? Có 3 loại, chia theo nguồn gốc và mục đích.

Loại thứ nhất là **chính thức** — do Anthropic phát triển, tích hợp sẵn trong Claude Code. Ví dụ Extension Claude Code trên VS Code.

Loại thứ hai là **mã nguồn mở** — do cộng đồng viết, kết nối công cụ bên ngoài. Ví dụ Playwright, Cline, Roo Code, Continue.

Loại thứ ba là **tự build nội bộ** — đội ngũ tự đóng gói quy trình riêng. Ví dụ skill `/review-pr` hay hook chạy test.

【Điểm nhấn với ban quản lý】

Điểm cần lưu ý với ban quản lý: hệ sinh thái này **có sẵn**, chúng ta không tự xây từ đầu — chi phí áp dụng thấp hơn nhiều người nghĩ.

---

## Phần 3 — Cơ chế hoạt động (20 phút)

【Cơ chế hoạt động】

Phần 3 — Cơ chế hoạt động (20 phút).

Đã rõ plugin là gì và lấp khoảng trống gì. Giờ đi sâu một tầng: bên trong, plugin mở rộng Claude bằng những cơ chế nào? Có 4 cơ chế.

Lưu ý để tránh hiểu nhầm: **cả 4 cơ chế này đều là tính năng có sẵn của Claude Code** — chỉ cần cấu hình, không bắt buộc plugin. Plugin chỉ là cách đóng gói và chia sẻ.

### 3.1 — Skills (5 phút)

【Skills — làm thế nào?】

Cơ chế thứ nhất là **Skills** — trả lời câu hỏi "làm việc này theo cách nào". Nó đóng gói một phương pháp, một quy trình, để Claude thực hiện nhất quán.

Ví dụ: một skill thiết kế giao diện quy định trình tự rõ — xác định mục đích, cấu trúc thông tin, bố cục, màu, chữ, component, rồi kiểm tra responsive.

Ý nghĩa: biến "biết làm" thành "làm theo phương pháp chuẩn".

### 3.2 — MCP server (6 phút)

【MCP server — có thể làm gì?】

Cơ chế thứ hai là **MCP server** — trả lời "Claude có thể thao tác gì với công cụ ngoài". Đây là chuẩn mở, Model Context Protocol, để kết nối database, trình duyệt, API, filesystem.

Ví dụ: một MCP server điều khiển trình duyệt thật — mở trang, click, nhập liệu, chụp ảnh.

Ý nghĩa: đưa Claude từ "suy luận, dự đoán" sang "quan sát, hành động thực tế".

### 3.3 — Hooks (4 phút)

【Hooks — khi nào tự động làm?】

Cơ chế thứ ba là **Hooks** — trả lời "khi nào tự chạy". Đây là lệnh tự động kích hoạt khi một sự kiện xảy ra, trước hoặc sau một hành động.

Ví dụ: khi chuẩn bị commit, hook tự chạy quy trình review + test.

Ý nghĩa: biến từng bước thủ công thành quy trình tự động.

### 3.4 — Sub-agent (5 phút)

【Sub-agent — ai làm phần nào?】

Cơ chế thứ tư là **Sub-agent** — trả lời "ai làm phần nào" và "cuối cùng đã làm gì". Nó chia việc lớn cho các agent con, chạy song song, rồi tổng hợp về.

Ví dụ: một agent phân tích code, một agent kiểm tra frontend, một agent chạy test — rồi gom thành báo cáo.

Ý nghĩa: giải quyết việc lớn và tổng hợp kết quả cuối phiên.

【Giới hạn & rủi ro】

Trước khi sang các plugin cụ thể, cần nói rõ giới hạn và rủi ro. Thứ nhất, AI có thể sai, nên luôn cần con người review lại. Thứ hai, phải quản lý API key, không commit key lên repo. Thứ ba, chi phí token cần theo dõi — chính là vai trò của Session Report.

---

## Phần 4 — Giới thiệu 4 plugin demo (4 phút)

【Giới thiệu 4 plugin demo】

Phần 4 — Giới thiệu 4 plugin demo (4 phút).

4 plugin, mỗi plugin lấp đúng một giới hạn đã nêu ở Phần 2.

【4 plugin demo】

Bốn cơ chế đó giờ ghép vào 4 plugin cụ thể — mỗi plugin lấp đúng một giới hạn đã nêu ở Phần 2.

- **Frontend Design** là một Skill — lấp giới hạn "biết làm nhưng chưa có phương pháp chuẩn".
- **Playwright / DevTools** là một MCP server — lấp giới hạn "chỉ suy luận, không quan sát hay hành động".
- **Code Review & Commit** kết hợp Hook + Skill — lấp giới hạn "chỉ làm khi được gọi".
- **Session Report** dùng Sub-agent + tổng hợp — lấp giới hạn "khó tổng hợp đã làm gì".

---

## Phần 5 — Demo (10 phút)

【Demo — một flow xuyên suốt】

Phần 5 — Demo (10 phút).

Một flow xuyên suốt: xây User Management Dashboard từ đầu đến cuối, đi qua cả 4 plugin.

【Kịch bản demo】

Kịch bản demo: xây dựng tính năng User Management Dashboard từ đầu đến cuối, đi qua cả 4 plugin.

【Flow demo — 4 bước】

**Bước 1 — Dựng UI** (Frontend Design): tôi yêu cầu Claude tạo giao diện trang User Dashboard gồm bảng danh sách người dùng, thanh tìm kiếm và biểu đồ thống kê. Kết quả: giao diện hoàn chỉnh, responsive.

*[Thực hiện demo bước 1]*

**Bước 2 — Kiểm thử** (Playwright / DevTools): yêu cầu Claude mở trình duyệt, gõ tìm "Admin", chụp ảnh kết quả. Kết quả: trình duyệt tự bật, tự gõ, screenshot xác minh giao diện hoạt động đúng.

*[Thực hiện demo bước 2]*

**Bước 3 — Review & Commit** (Code Review & Commit): yêu cầu Claude kiểm tra các file vừa tạo và tạo commit. Kết quả: nhận xét về mã nguồn và commit message chuẩn.

*[Thực hiện demo bước 3]*

**Bước 4 — Tổng kết** (Session Report): xuất báo cáo phiên làm việc. Kết quả: dashboard thống kê token, danh sách sub-agent và các việc đã xong.

*[Thực hiện demo bước 4]*

Lưu ý: đây là một kịch bản liền mạch, không phải 4 demo rời — mỗi bước lấp một giới hạn đã nêu ở Phần 2, để thấy Claude tự thực thi trọn gói.

---

## Phần 6 — Q&A (5–10 phút)

【Q&A】

Phần 6 — Q&A (5–10 phút).

Slide cuối: đồng hồ đếm ngược 35 giây rồi lật sang QR điểm danh. Chuẩn bị bảng dự phòng câu hỏi ở slide tiếp.

【Q&A — hỏi đáp + QR điểm danh】

Buổi trình bày đến đây là hết phần nội dung. Trên slide đang chạy đồng hồ đếm ngược **35 giây** — hết giờ sẽ tự lật sang **mã QR điểm danh** (forms.office.com).

Lời dẫn: cảm ơn mọi người đã theo dõi; mời mọi người quét mã QR để điểm danh. Phần hỏi đáp gói gọn trong 35 giây — nếu được thì mọi người cứ theo dõi ạ. *[cười, chỉ vào đồng hồ đếm ngược đang chạy trên slide]*

*[Nếu thực sự có câu hỏi, tham khảo bảng dự phòng bên dưới]*

| Câu hỏi | Gợi ý trả lời |
|---|---|
| "So với GitHub Copilot thì sao?" | Copilot gợi ý từng dòng (bị động); Claude + plugin tự thực thi cả quy trình (chủ động). Hai thứ bổ trợ nhau. |
| "Tốn bao nhiêu?" | Dùng Session Report để đo; mô hình rẻ cho autocomplete, mô hình mạnh cho refactor. |
| "Có an toàn không?" | Quản lý API key qua biến môi trường; không commit key; kiểm soát quyền (plan/normal mode). |
| "AI có đáng tin không?" | Không tin tuyệt đối — luôn review lại. Plugin giúp AI thực thi, con người duyệt. |

---

## Phụ lục — chuẩn bị (không phải lời nói)

- **Backup:** quay sẵn video demo toàn bộ flow (tốc độ 1.5x). Nếu gặp sự cố mạng / API chậm, bật video và thuyết minh trực tiếp.
- **Bản đồ thuật ngữ** (trả lời nếu bị hỏi vặn): "plugin" (nghĩa rộng) = cơ chế mở rộng khả năng làm việc của Claude, bên trong là **Skills**, **MCP server**, **Hooks**, **Sub-agent** (một hoặc nhiều thành phần kết hợp). **Lưu ý:** 4 cơ chế này đều có sẵn trong Claude Code (chỉ cần cấu hình); plugin là lớp đóng gói + chia sẻ. Ngoại lệ bắt buộc plugin: code intelligence (LSP).
- **Ánh xạ nhanh:** Phương pháp chuẩn → Skill → Frontend Design · Quan sát/hành động → MCP → Playwright · Tự kích hoạt → Hook(+Skill) → Code Review & Commit · Tổng hợp → Sub-agent → Session Report.










