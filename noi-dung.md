# Claude + Plugin: mở rộng công cụ tự vận hành

> **Đối tượng:** đồng nghiệp + sếp
> **Thời lượng:** ~70 phút + Q&A 5–10 phút
> **Giọng:** nhà phân tích (khái niệm → cơ chế → minh họa → áp dụng)
> **Ngôn ngữ:** tiếng Việt · **Thuật ngữ:** "plugin" là từ chủ đạo, hiểu theo nghĩa rộng = cơ chế mở rộng khả năng làm việc của Claude

---

## Luận điểm cốt lõi

> Claude Code vốn đã là công cụ tự vận hành — không phải chatbot.
> Plugin là cách mở rộng nó, lấp các khoảng trống mà bản nguyên bản chưa có.

**Điều muốn khán giả nhớ (1 câu):**
*Đừng chỉ dùng Claude như một chatbot — hãy mở rộng nó bằng plugin để nó tự vận hành trọn gói.*

**Mạch logic của cả buổi (3 bước):**
1. **Khái niệm & phân loại** — hạn chế của bản nguyên bản → "plugin" là gì → phân loại
2. **Cơ chế vận hành** — 4 cơ chế bên trong plugin (Skills, MCP, Hooks, Sub-agent)
3. **Minh họa thực tế** — 4 plugin demo, mỗi plugin lấp một giới hạn

---

## Sườn tổng

| # | Phần | TG | Vai trò |
|---|---|---|---|
| 1 | Mở bài — Luận điểm | 5' | Đặt luận điểm + công bố mạch 3 bước |
| 2 | **LỚN 1 — Khái niệm & phân loại** | 20' | 4 giới hạn của bản nguyên bản (đặt vấn đề) → khái niệm "plugin" → phân loại |
| 3 | **LỚN 2 — Cơ chế hoạt động** | 20' | Skills, MCP, Hooks, Sub-agent + giới hạn & rủi ro |
| 4 | Giới thiệu 4 plugin demo (nhỏ) | 4' | Đối chiếu 1:1 giới hạn → cơ chế → plugin |
| 5 | Demo — một flow xuyên suốt | 10' | Chứng minh bằng thực tế |
| 6 | Q&A | 5–10' | Đệm linh hoạt |

---

## NỘI DUNG TỪNG PHẦN

### Phần 1 — Mở bài: Luận điểm (5 phút)

**Mục tiêu:** Đặt luận điểm trong 60 giây, cho khán giả biết họ sẽ nắm được gì.

- Mở thẳng bằng luận điểm (không vòng vo):
  > "Hôm nay tôi muốn trình bày một quan điểm có chủ đích, thay vì chỉ liệt kê danh sách công cụ."
- Nêu luận điểm 2 câu + công bố **mạch 3 bước**.
- Hứa hẹn rõ:
  > "Đến cuối buổi, mọi người sẽ hiểu bản nguyên bản của Claude Code còn thiếu gì, và plugin mở rộng nó thế nào."
- **Đừng làm:** giới thiệu bản thân dài, kể lịch sử AI, đọc mục lục.

---

### Phần 2 — LỚN 1: Khái niệm & phân loại (20 phút)

**Mục tiêu:** Cho khán giả thấy rõ: Claude Code *bản nguyên bản* mạnh nhưng còn 4 giới hạn → "plugin" là gì → phân loại hệ sinh thái. **Chưa hé lộ 4 plugin demo.**

#### 2.1. Claude nguyên bản: đã mạnh, nhưng còn 4 giới hạn (8')

Đầu tiên phải làm rõ một hiểu lầm phổ biến: nhiều người hình dung Claude là chatbot — hỏi một câu, nhận câu trả lời, rồi copy-paste. **Với Claude Code, điều này không đúng.** Bản nguyên bản (chưa cài plugin gì) đã tự: đọc/sửa file, chạy lệnh shell, tìm code, thao tác git. Nó đã là công cụ *tự vận hành*.

Nhưng tự nó vẫn còn **4 giới hạn**:

| # | Giới hạn | Nghĩa là |
|---|---|---|
| 1 | **Biết làm, nhưng chưa có phương pháp chuẩn** | Viết được (ví dụ frontend) nhưng không theo một quy trình chuyên biệt nhất quán — chất lượng phụ thuộc cách đặt vấn đề từng lần |
| 2 | **Chỉ suy luận, không quan sát / hành động thực tế** | Đọc code, viết code, dự đoán lỗi — nhưng không *thực sự nhìn* và *thao tác* hệ thống bên ngoài (trình duyệt đang chạy, database, API) |
| 3 | **Chỉ làm khi được gọi** | Mỗi bước review / test / commit phải do con người chủ động yêu cầu — không có cơ chế "khi sự kiện X xảy ra thì tự chạy Y" |
| 4 | **Khó tổng hợp "đã làm gì"** | Việc lớn qua nhiều đầu việc — sau đó khó biết đã làm gì, đổi file nào, còn gì chưa xong |

→ **Kết luận:** Claude nguyên bản mạnh ở *suy nghĩ và viết code*; còn trống ở 4 chỗ: **phương pháp chuẩn, quan sát thực tế, tự kích hoạt, tổng hợp kết quả.** Trong đó có giới hạn *"chưa làm được"* (khoảng trống thật) và giới hạn *"làm được nhưng chưa nhất quán"*.

#### 2.2. "Plugin" là gì: cơ chế mở rộng (nghĩa rộng, 7')

Để lấp các khoảng trống đó, Claude được *mở rộng* — ta gọi chung là **plugin**.

- **"Plugin"** hiểu theo nghĩa rộng: **cơ chế mở rộng khả năng làm việc của Claude** — bên trong có thể là *một* thành phần đơn lẻ, hoặc *nhiều* thành phần kết hợp.
- Mỗi plugin nhắm một kiểu khoảng trống: **phương pháp** (cách làm), **hành động** (công cụ ngoài), **tự kích hoạt** (theo sự kiện), hoặc **tổng hợp** (gom kết quả).

→ **Kết luận:** plugin không biến Claude từ "không làm được" thành "làm được" — nó **mở rộng** Claude, lấp đúng các khoảng trống đã nêu: vừa lấp chỗ *"chưa làm được"*, vừa chuẩn hóa chỗ *"làm được nhưng chưa nhất quán"*.

#### 2.3. Hệ sinh thái plugin gồm những loại nào (5')

Phân loại theo **nguồn gốc & mục đích**:

| Loại plugin | Là gì | Ví dụ | Dùng khi nào |
|---|---|---|---|
| **Chính thức** | Anthropic phát triển, tích hợp sẵn trong Claude Code | Extension Claude Code trên VS Code | Công việc hằng ngày |
| **Mã nguồn mở** | Cộng đồng viết, kết nối công cụ bên ngoài | Playwright, Cline, Roo Code, Continue | Cần công cụ đặc thù |
| **Tự build (nội bộ)** | Đội ngũ tự đóng gói quy trình riêng | Skill `/review-pr`, hook chạy test | Chuẩn hóa quy trình team |

- **Điểm nhấn với sếp:** *"Hệ sinh thái có sẵn, không tự xây từ đầu — chi phí áp dụng thấp hơn nhiều người nghĩ."*

**Câu chuyển:**
> "Đã rõ plugin là gì và lấp khoảng trống gì. Giờ đi sâu một tầng: bên trong, plugin mở rộng Claude bằng những cơ chế nào?"

---

### Phần 3 — LỚN 2: Cơ chế hoạt động (20 phút)

**Mục tiêu:** Phần thể hiện chiều sâu chuyên môn — giải thích 4 cơ chế bên trong mà plugin dùng để mở rộng Claude.

> **Lưu ý người trình bày (nói ra, để tránh mâu thuẫn):** 4 cơ chế này **đều là tính năng có sẵn của Claude Code** — chỉ cần cấu hình, không bắt buộc plugin. Plugin chỉ là cách **đóng gói + chia sẻ** chúng lại. (Ngoại lệ duy nhất cần plugin: code intelligence / LSP — nhưng không cần đào sâu trước khán giả trừ khi bị hỏi.)

#### 3.1. Skills — "làm thế nào?" (5')

- **Là gì:** trả lời câu hỏi *"làm việc này theo cách nào"* — đóng gói một phương pháp/quy trình để Claude thực hiện nhất quán.
- **Ví dụ:** một skill thiết kế giao diện quy định trình tự: mục đích → cấu trúc thông tin → bố cục → màu → chữ → component → kiểm tra responsive.
- **Ý nghĩa:** biến *"biết làm"* thành *"làm theo phương pháp chuẩn"*.

#### 3.2. MCP server — "có thể làm gì?" (6')

- **Là gì:** trả lời *"Claude có thể thao tác gì với công cụ ngoài"* — chuẩn mở (Model Context Protocol) kết nối database, trình duyệt, API, filesystem.
- **Ví dụ:** một MCP server điều khiển trình duyệt thật — mở trang, click, nhập liệu, chụp ảnh.
- **Ý nghĩa:** từ *"suy luận, dự đoán"* sang *"quan sát, hành động thực tế"*.

#### 3.3. Hooks — "khi nào tự động làm?" (4')

- **Là gì:** trả lời *"khi nào tự chạy"* — lệnh tự động kích hoạt khi một sự kiện xảy ra (trước/sau một hành động).
- **Ví dụ:** khi chuẩn bị commit, hook tự chạy quy trình review + test.
- **Ý nghĩa:** biến từng bước thủ công thành *quy trình tự động*.

#### 3.4. Sub-agent — "ai làm phần nào?" (5')

- **Là gì:** trả lời *"ai làm phần nào"* và *"cuối cùng đã làm gì"* — chia việc lớn cho các agent con, chạy song song rồi tổng hợp.
- **Ví dụ:** 1 agent phân tích code, 1 agent kiểm tra frontend, 1 agent chạy test — gom thành báo cáo.
- **Ý nghĩa:** giải quyết việc lớn + tổng hợp kết quả cuối phiên.

#### 3.5. Giới hạn & rủi ro (chốt lại phần cơ chế)

Sau khi hiểu 4 cơ chế, nói rõ giới hạn và rủi ro (thể hiện sự tỉnh táo = chuyên môn):
- AI có thể sai → luôn cần con người review lại.
- Quản lý API key → không commit key lên repo.
- Chi phí token → theo dõi bằng Session Report.

**Câu chuyển:**
> "Bốn cơ chế này là nền tảng bên trong plugin. Giờ ghép chúng vào 4 plugin cụ thể — mỗi plugin lấp đúng một giới hạn ở Phần 2."

---

### Phần 4 — Giới thiệu 4 plugin demo (4 phút)

**Mục tiêu:** Đối chiếu 1:1 — giới hạn → cơ chế → plugin. Chỉ 1 bảng, không sa đà.

| Plugin demo | Cơ chế bên trong | Lấp giới hạn nào |
|---|---|---|
| Frontend Design | Skill | Biết làm nhưng chưa có phương pháp chuẩn |
| Playwright / DevTools | MCP server | Chỉ suy luận, không quan sát / hành động |
| Code Review & Commit | Hook + Skill | Chỉ làm khi được gọi |
| Session Report | Sub-agent + tổng hợp | Khó tổng hợp "đã làm gì" |

---

### Phần 5 — Demo: một flow xuyên suốt (10 phút)

**Kịch bản:** *"Xây dựng tính năng User Management Dashboard từ đầu đến cuối"* — một kịch bản duy nhất, đi qua cả 4 plugin.

| Bước | Plugin | Câu lệnh | Kết quả thấy ngay |
|---|---|---|---|
| 1. Dựng UI | Frontend Design | "Tạo UI User Dashboard: bảng người dùng, thanh tìm kiếm, biểu đồ, Tailwind." | Giao diện hoàn chỉnh, responsive |
| 2. Kiểm thử | Playwright/DevTools | "Mở trình duyệt, gõ tìm 'Admin', chụp ảnh kết quả." | Browser tự bật, tự gõ, screenshot xác minh |
| 3. Review & Commit | Code Review & Commit | "Kiểm tra các file vừa tạo và tạo commit." | Nhận xét + commit chuẩn |
| 4. Tổng kết | Session Report | "Xuất báo cáo phiên làm việc." | Dashboard token + sub-agent + việc xong |

> **Mẹo trình bày:** đây là *một* kịch bản liền mạch, không phải 4 demo rời. Mỗi bước lấp một giới hạn đã nêu ở Phần 2 — khán giả thấy Claude tự thực thi trọn gói.

---

### Phần 6 — Q&A (5–10 phút)

**Slide kết thúc (chủ đề chơi chữ, ẩn ý "xin đừng hỏi gì"):**
- Một đồng hồ đếm ngược **30 giây** + icon **🤫** (suỵt).
- Câu chữ: *"Cảm ơn đã lắng nghe — nếu được thì đừng hỏi gì ạ."*
- Ngụ ý nhẹ nhàng để phá băng; nếu có người vẫn hỏi thì chuyển sang phần trả lời dự phòng bên dưới.

**Chuẩn bị sẵn 4 câu trả lời (dự phòng, không chiếu lên slide):**

| Câu hỏi | Gợi ý trả lời |
|---|---|
| "So với GitHub Copilot thì sao?" | Copilot gợi ý từng dòng (bị động); Claude + plugin tự thực thi cả quy trình (chủ động). Hai thứ bổ trợ nhau. |
| "Tốn bao nhiêu?" | Dùng Session Report để đo; mô hình rẻ cho autocomplete, mô hình mạnh cho refactor. |
| "Có an toàn không?" | Quản lý API key qua biến môi trường; không commit key; kiểm soát quyền (plan/normal mode). |
| "AI có đáng tin không?" | Không tin tuyệt đối — luôn review lại. Plugin giúp AI thực thi, con người duyệt. |

---

## GHI CHÚ RIÊNG CHO NGƯỜI TRÌNH BÀY (không chiếu lên slide)

**Bản đồ "plugin" → cơ chế thật** (để trả lời nếu bị hỏi vặn):
- "Plugin" (từ chủ đạo cho khán giả, nghĩa rộng) = **cơ chế mở rộng khả năng làm việc của Claude**; bên trong là **Skills**, **MCP server**, **Hooks**, **Sub-agent** — một thành phần hoặc nhiều thành phần kết hợp.
- **Lưu ý kỹ thuật (đừng nói sai):** Skills / MCP / Hooks / Sub-agent đều là **tính năng có sẵn** của Claude Code — chỉ cần cấu hình trong `.claude/`, không bắt buộc plugin. Plugin là lớp **đóng gói + phân phối** (cài 1 gói, chia sẻ cả team). Thứ duy nhất *bắt buộc* cài plugin: **code intelligence (LSP)**.
- **Ánh xạ 4 giới hạn → 4 cơ chế → 4 plugin:**
  | Giới hạn (Phần 2) | Loại | Cơ chế | Plugin demo |
  |---|---|---|---|
  | Chưa có phương pháp chuẩn | Pain point (làm được, chưa nhất quán) | Skill | Frontend Design |
  | Không quan sát/hành động | Hard limit (chưa làm được) | MCP | Playwright / DevTools |
  | Chỉ làm khi được gọi | Tự động hóa | Hook (+ Skill) | Code Review & Commit |
  | Khó tổng hợp | Tổng hợp phiên | Sub-agent | Session Report |

**Kế hoạch dự phòng (backup):**
- Quay sẵn video demo toàn bộ flow (tốc độ 1.5x) làm phương án B.
- Gặp sự cố mạng / API chậm → bật video và thuyết minh trực tiếp, không vỡ trận.

---
*Đây là "nguyên liệu" để bạn tự dựng slide. Phần lớn 1 & 2 = nhiều slide; phần 4 = 1 slide; demo = vài slide.*
