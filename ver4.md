Khung Đào Tạo Kỹ Thuật (70 Phút): Tối Ưu Năng Suất Lập Trình Cho Junior Dev Với Hệ Sinh Thái Plugin Claude
Buổi chia sẻ được thiết kế dành cho các lập trình viên muốn chuyển đổi từ tư duy "dùng AI để gõ code hộ" (Chatbot/Copilot) sang tư duy "điều phối AI Agent hoàn thành tác vụ" thông qua hệ sinh thái Plugin. Chương trình tập trung vào tính ứng dụng cao, dễ trình bày, không cầu kỳ về mặt kiến trúc doanh nghiệp nhưng mang lại hiệu ứng thị giác mạnh mẽ thông qua bài Demo thực tế.   

Cấu Trúc Thời Lượng Chi Tiết (Tổng 70 Phút)
Mốc Thời Gian	Thời Lượng	Nội Dung Trọng Tâm	Mục Tiêu Đạt Được
Phần 1	10 Phút	Mở Đầu & Đặt Vấn Đề: Tại sao Junior Dev nên dùng Claude + Plugin?	
Phân biệt sự khác nhau giữa gõ prompt thông thường và dùng Plugin để biến Claude thành Full-stack Dev tự động.

Phần 2	15 Phút	Giới Thiệu Bộ 4 Plugin Trọng Tâm	
Nắm rõ vai trò của 4 plugin: Dựng UI, Test trình duyệt, Review & Commit Git, và Báo cáo phiên làm việc.

Phần 3	15 Phút	LIVE DEMO: "Xây dựng & Test tính năng User Dashboard từ A-Z"	Trình diễn kịch bản 4 bước thực tế (8–10 phút demo + 5 phút giải thích phản ứng của AI).
Phần 4	20 Phút	Bóc Tách Kỹ Thuật & Mẹo Làm Chủ Plugin	
Hướng dẫn tạo tệp CLAUDE.md, quản lý phân quyền (Plan mode / Normal mode) và cách tránh tiêu tốn nhiều token.

Phần 5	10 Phút	Q&A & Bỏ Túi Bí Kíp (Takeaways)	Giải đáp thắc mắc cho học viên và chia sẻ checklist câu lệnh bỏ túi cho Junior.
  
Chi Tiết Bộ 4 Plugin Trọng Tâm Cho Junior Dev
Thay vì giới thiệu quá nhiều công cụ phức tạp, buổi chia sẻ chỉ tập trung vào 4 plugin cốt lõi phối hợp với nhau để giải quyết một bài toán lập trình hoàn chỉnh:   

Frontend Design Plugin:

Nhiệm vụ: Tự động sinh giao diện chuẩn UI/UX, responsive với Tailwind CSS.   

Giá trị: Giúp lập trình viên không mất thời gian căn chỉnh CSS thủ công hay viết các HTML đơn điệu.

Playwright / Chrome DevTools Plugin:

Nhiệm vụ: Khởi chạy trình duyệt thật, mô phỏng thao tác gõ/click và chụp ảnh màn hình (screenshot).

Giá trị: Tự động hóa việc kiểm thử giao diện mà không cần người dùng tự mở trình duyệt test tay.

Code Review & Commit Commands:

Nhiệm vụ: Quét lại các file vừa tạo/sửa, liệt kê điểm cần tối ưu và tạo commit message chuẩn.   

Giá trị: Chuẩn hóa quy trình Git và nâng cao chất lượng mã nguồn trước khi tạo Pull Request.   

Session-Report Plugin:

Nhiệm vụ: Xuất báo cáo tổng kết phiên làm việc dạng Dashboard HTML.   

Giá trị: Minh bạch lượng token đã tiêu tốn và theo dõi danh sách các sub-agent đã chạy.   

Kịch Bản Live Demo Trung Tâm (8 – 10 Phút)
Bối cảnh: Phát triển nhanh tính năng "User Management Dashboard" cho ứng dụng web.

Bước 1: Khởi động & Tạo giao diện chuyên nghiệp (2 phút)
Plugin: Frontend Design

Thao tác: Yêu cầu Claude: "Tạo cho tôi UI trang User Dashboard với bảng danh sách người dùng, thanh tìm kiếm và biểu đồ thống kê bằng Tailwind CSS."

Hiệu ứng thấy ngay: Claude sinh ra file mã nguồn giao diện hoàn chỉnh, màu sắc phối chuẩn UI/UX, có sẵn layout responsive.

Bước 2: Tự động hóa kiểm thử UI & Debug trực tiếp (3 phút)
Plugin: Playwright hoặc Chrome DevTools

Thao tác: Yêu cầu Claude: "Mở trình duyệt, truy cập vào giao diện vừa dựng, thử gõ tìm kiếm 'Admin' và chụp ảnh màn hình kết quả."

Hiệu ứng thấy ngay: Trình duyệt tự động mở lên, con trỏ tự gõ chữ vào ô tìm kiếm và Claude xuất ngay ảnh chụp màn hình (screenshot) báo cáo giao diện hiển thị chuẩn xác.

Bước 3: Tự động Review Code & Tạo Git Commit (2 phút)
Plugin: Code Review & Commit Commands

[cite: 1]

Thao tác: Gõ lệnh yêu cầu Claude kiểm tra lại toàn bộ file vừa tạo/sửa.   

Hiệu ứng thấy ngay: Claude đưa ra nhận xét ngắn gọn về mã nguồn, sau đó tự đóng gói lệnh git status và tạo commit message chuẩn Conventional Commits (feat(dashboard): add user management UI and analytics chart).   

Bước 4: Tổng kết hiệu suất phiên làm việc (1 phút)
Plugin: session-report

[cite: 1]

Thao tác: Gõ lệnh xuất báo cáo phiên làm việc.   

Hiệu ứng thấy ngay: Claude mở trang Dashboard HTML tổng kết chi tiết số token đã dùng và các sub-agent đã tham gia thực thi tác vụ.   

Bí Kíp Dành Cho Junior Dev Khi Trình Bày
Cách truyền tải đơn giản: Nhấn mạnh rằng dùng Plugin giống như việc cho Claude "thêm tay thêm mắt" (mắt là Playwright quan sát màn hình, tay là Frontend Design tự viết code) để làm việc thay mình.

Mẹo chuẩn bị trước tệp CLAUDE.md: Trước buổi demo, hãy chuẩn bị sẵn tệp CLAUDE.md trong thư mục project với các quy định ngắn (ví dụ: "Ưu tiên dùng Tailwind CSS, code viết bằng React/TypeScript, commit bằng tiếng Anh"). Khi demo, chỉ cần mở file này cho khán giả thấy cách Claude tự động tuân thủ luật của dự án.   

Kế hoạch dự phòng (Backup Plan): Quay trước một video thao tác demo 8 phút ở tốc độ 1.5x. Nếu buổi chia sẻ gặp sự cố mạng hoặc API phản hồi chậm, bạn có thể bật video và thuyết minh trực tiếp trên đoạn clip đó mà không bị vỡ trận.
