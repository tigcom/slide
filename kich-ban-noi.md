# Kịch bản nói — Claude + Plugin (70 phút)

> Đây là lời nói gợi ý cho từng phần, đồng bộ với `slides.json` (cùng id section). Bạn có thể đọc theo hoặc diễn đạt lại bằng cách của mình. Dấu `【…】` đánh dấu slide đang hiển thị.

---

【Trang bìa】

Dạ Chào mọi người. Hôm nay em xin trình bày về việc kết hơp sử dụng Plugin cho Claude — từ 1 công cụ tự vận hành đến việc khai phá các tiềm năng của claude.
---

## Phần 1 — Mở bài (5 phút)

【Mở bài — Luận điểm】

Phần 1 — Mở bài (5 phút).
Trong phần đầu tiên thì em sẽ chia sẻ về công dụng của plugin cũng như là lý do nó cần thiết với claude
【Luận điểm cốt lõi】

Đầu tiên để giới thiệu về claude thì nó là 1 công cụ hỗ trợ lập trình quá mạnh mẽ và nổi tiếng , nó hoàn toàn có thể thay thế được các thao tác lập trình thủ công. Và plugin là cách mở rộng các giới hạn của nó , giúp  lấp đầy những cái khoảng trống mà bản nguyên bản chưa có.**
【Điều cần nhớ】

Vẫn còn nhiều người chỉ sử dụng claude đơn thuẩn để thay thế các thao tác lập trình thủ công, và gặp nhiều khó khăn bởi các giới hạn, những điểm chưa tối ưu, mà vẫn chưa khai phá được hết những lợi ích mà claude có thể mang lại 
【Mạch của buổi nói】

Buổi đào tạo hôm nay em sẽ nói về các phần cụ thể như khái niệm và phân loại , về cơ chế vận hành của plugin, kết thúc sẽ là 1 demo nhỏ
---

## Phần 2 — Khái niệm & phân loại (20 phút)

【Khái niệm & phân loại】

Bắt đầu Phần 2 với Khái niệm & các loại plugin 

 trong này sẽ Đi qua các chủ đề như 4 giới hạn của bản nguyên bản → "plugin" là gì → 3 loại plugin chính
### 2.1 — Claude nguyên bản: 4 giới hạn (8 phút)

【Claude Code: Giới hạn】

Trước hết phải gỡ một hiểu lầm phổ biến đó là nhiều người vẫn hình dung Claude có thể làm được tất cả mọi thứ, thì 
một hệ thống chỉ có khả năng “tính toán trên thông tin nó được cung cấp”.Nó có thể mô tả hành động, nhưng không thực hiện hành động đó. và Không có khả năng tác động ra thế giới bên ngoài
Về lý thuyết, LLM chỉ có thể suy luận dựa trên:

input + context + kiến thức đã học + khả năng suy luận của model.
Nếu một thông tin không nằm trong những thứ đó, model không có cách trực tiếp để biết.
nếu cung cấp cho nó khả năng “biết cách lấy dữ liệu” thì nó có thể 
“có khả năng lấy dữ liệu”.
【Hai luồng xử lý một task khó】

cùng xem llm xử lý 1 task khó dưới một góc rất đơn giản:

Khi nhận một task khó, model sẽ phân tích yêu cầu và suy luận dựa trên context mà nó đang có. Về mặt khái niệm, chúng ta có thể hình dung là:

Input → Reason → Output.

Vấn đề xuất hiện khi trong quá trình suy luận, model phát hiện rằng để đi tiếp nó cần một thông tin mới, hoặc cần thực hiện một hành động nằm ngoài context và capability interface hiện tại.

Lúc này, nó không có cách trực tiếp để lấy thêm thông tin hoặc thực hiện hành động đó. Vì vậy, hệ thống có thể phải dừng lại, yêu cầu người dùng cung cấp thêm thông tin, hoặc đưa ra một câu trả lời dựa trên những gì hiện có.

Điểm quan trọng ở đây không phải là model tự nhiên trở nên thông minh hơn.

Thay vào đó, model có thêm một interface để tương tác với hệ thống bên ngoài.

Nó có thể suy luận, xác định cần capability nào, chọn tool và gọi tool. Hệ thống bên ngoài thực thi hành động đó và trả kết quả về.

Kết quả này trở thành một observation mới, tức là context của model được cập nhật bằng thông tin mà trước đó nó chưa có.

Sau đó model lại suy luận tiếp.

Nếu chưa đủ thì tiếp tục gọi tool. Nếu đã đủ thì hoàn thành task.

Vì vậy luồng xử lý trở thành một vòng lặp:

Suy luận → chọn tool → thực thi → nhận kết quả → quan sát trạng thái mới → suy luận tiếp.
【4 giới hạn của Claude nguyên bản】

Thứ nhất, **biết làm nhưng chưa có phương pháp chuẩn**: Claude viết được frontend, nhưng không theo một quy trình chuyên biệt nhất quán — nên chất lượng phụ thuộc cách mình đặt vấn đề, sự rõ ràng khi cung cấp yêu cầu, độ hoàn thiện không cao.

Thứ hai, **chỉ suy luận, không quan sát hay hành động thực tế**: nó đọc code, viết code, dự đoán lỗi — nhưng không thực sự nhìn và thao tác hệ thống bên ngoài, như trình duyệt đang chạy, database, API., nó có thể viết test  nhưng không biết data chuẩn để test là gì nếu ko chủ động cung cấp, test xong cũng ko nắm data nền để verify cho đúng ngữ cảnh

Thứ ba, **chỉ làm khi được gọi**: mỗi bước review, test, commit đều phải do mình chủ động yêu cầu — không có cơ chế "khi sự kiện xảy ra thì tự chạy".

Thứ tư, **khó tổng hợp "đã làm gì"**: việc lớn qua nhiều đầu việc, sau đó khó biết nó đã làm gì, đổi file nào, còn gì chưa xong.
【Kết luận】

Tóm lại: Claude nguyên bản mạnh ở suy nghĩ và viết code; còn giới hạn ở nhiều chỗ — chưa có phương pháp chuẩn, khả năng quan sát thực tế, tự nắm bắt linh hoạt, và tổng hợp kết quả. Tất nhiên là sẽ có : có giới hạn là "chưa làm được" và  có giới hạn là "làm được nhưng chưa nhất quán".
### 2.2 — "Plugin" là gì (7 phút)

【Plugin là gì】

Vậy giải pháp ở đây chính là plugin? Bằng cách mở rộng Claude 

"Plugin" ở đây hiểu theo nghĩa rộng: là cơ chế mở rộng khả năng làm việc của Claude. Bên trong một plugin có thể là một thành phần đơn lẻ, hoặc nhiều thành phần kết hợp.

Mỗi plugin nhắm một kiểu cải tiến khác nhau về phương pháp, hành động, tự kích hoạt, hoặc tổng hợp.
【Kết luận】

Tóm lại: plugin không biến Claude từ "không làm được" thành "làm được" nhưng nó mở rộng khả năng xử lý vấn đề của Claude, theo hai hướng đó là có thể bù đắp cho những gì "chưa làm  được", và chuẩn hóa chỗ "làm được nhưng chưa nhất quán".
### 2.3 — Phân loại (5 phút)

【Hệ sinh thái plugin — 3 loại】

Vậy hệ sinh thái plugin gồm những loại nào? Có 3 loại, chia theo nguồn gốc và mục đích.

Loại thứ nhất là **chính thức** — do Anthropic phát triển, tích hợp sẵn trong Claude Code. Ví dụ Extension Claude Code trên VS Code.

Loại thứ hai là **mã nguồn mở** — do cộng đồng viết, kết nối công cụ bên ngoài. Ví dụ Playwright, Cline, Roo Code, Continue.

Loại thứ ba là **tự build nội bộ** — đội ngũ tự đóng gói quy trình riêng. Ví dụ skill `/review-pr` hay hook chạy test.

【Điểm nhấn với ban quản lý】

plugin vốn là các tiện ích được dựng sẵn và đúc kết từ kinh nghiệm của các nhà phát triển khác giúp chi phí áp dụng thấp hơn nhiều người nghĩ.
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

Cơ chế thứ tư là **Sub-agent** — trả lời "ai làm phần nào". Nó chia việc lớn cho các agent con, chạy song song, mỗi agent làm một phần rồi gom kết quả về.

Ví dụ: code-review chạy 5 reviewer song song — soi bug, check quy chuẩn, đọc lịch sử git — rồi chấm điểm từng nhận xét.

Ý nghĩa: giải quyết việc lớn cần chia nhỏ; tổng hợp cả phiên là việc của Session Report.

【Giới hạn & rủi ro】

Một task có thể khó vì nhiều nguyên nhân khác nhau.
Ví dụ về mặt lý thuyết, độ khó có thể đến từ:
Thiếu thông tin
Thông tin quá lớn
Thông tin cần được lấy từ nguồn bên ngoài
Cần tính toán hoặc xử lý bằng hệ thống chuyên biệt
Cần thực hiện hành động bên ngoài model
Cần nhiều bước phụ thuộc lẫn nhau
Cần kiểm tra kết quả sau khi hành động
Cần trạng thái thay đổi theo thời gian
Do đó, không nên nói:
“LLM thất bại vì nó không đủ thông minh.”
Chính xác hơn:
“Task có thể yêu cầu những capability nằm ngoài interface mà LLM hiện đang được cung cấp.”
Trước khi sang các plugin cụ thể, cần nói rõ giới hạn và rủi ro. Thứ nhất, AI có thể sai, nên luôn cần con người review lại. Thứ hai, cần thật sự cân nhác về mặt chi phí, AI không toàn năng, nó là sự đánh đổi giữa kinh phí và năng xuất , nên tồn tại giới hạn là điều rõ ràng
---

## Phần 4 — Giới thiệu 4 plugin demo (4 phút)

【Giới thiệu 4 plugin demo】

Phần 4 — Giới thiệu 4 plugin demo (4 phút).

4 plugin, mỗi plugin lấp đúng một giới hạn đã nêu ở Phần 2.

【4 plugin demo】

"Để giải quyết triệt để 4 giới hạn ở Phần 2, chúng ta áp dụng ngay 4 plugin thực tế trong hệ sinh thái Claude Code. Mỗi plugin là một mảnh ghép lấp đúng một khoảng trống:

Frontend Design — Lấp giới hạn "Biết làm nhưng thiếu phương pháp"
Là một Skill, plugin này ép AI đi theo quy trình thiết kế bài bản trước khi viết code: chọn rõ phong cách (brutalist, luxury, retro...), phối cặp font chữ độc đáo và dựng bố cục phá cách. Nó giúp loại bỏ hoàn toàn kiểu giao diện AI nhạt nhòa, cho ra sản phẩm chuẩn sản xuất và có gu riêng.

Chrome DevTools — Lấp giới hạn "Chỉ suy luận, không quan sát hay hành động"
Đóng vai trò một MCP Server với 29 công cụ, plugin này cho phép Claude trực tiếp điều khiển trình duyệt Chrome thực tế. AI không còn 'đoán mò' nữa mà có thể tự click nút, kiểm tra lỗi Console, đo hiệu năng Network và soi vỡ giao diện trên mọi màn hình.

Code Review — Lấp giới hạn "Chỉ làm việc khi được gọi"
Kết hợp Hook, Command và Sub-agent, plugin này tự kích hoạt khi chuẩn bị commit. Nó vận hành song song 5 sub-agent chuyên biệt (soi bug, check quy chuẩn, đọc lịch sử Git...) và chấm điểm độ tin cậy. Chỉ những lỗi có độ chính xác trên 80% mới được báo lên, giúp kiểm soát chất lượng tự động mà không gây nhiễu.

Session Report — Lấp giới hạn "Khó tổng hợp quá trình"
Kết hợp Command và Skill, plugin này tự động quét dữ liệu phiên làm việc để xuất ra một báo cáo HTML trực quan. Bạn sẽ nắm trọn bức tranh về lượng token tiêu tốn, hiệu suất cache và những prompt đắt đỏ nhất để dễ dàng tối ưu chi phí.
---

## Phần 5 — Demo (10 phút)

【Demo — một flow xuyên suốt】

Phần 5 — Demo (10 phút).

phần cuối cùng em sẽ demo việc sử dụng plugin
【Kịch bản demo】

Kịch bản demo: xây dựng tính năng User Management Dashboard từ đầu đến cuối, và sử dụng cả 4 plugin.
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
- **Ánh xạ nhanh:** Phương pháp chuẩn → Skill → Frontend Design · Quan sát/hành động → MCP → Playwright · Tự kích hoạt → Hook + Command + Sub-agent → Code Review & Commit · Tổng hợp → Command + Skill → Session Report.
































