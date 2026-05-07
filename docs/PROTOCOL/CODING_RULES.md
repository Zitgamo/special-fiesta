# AGENT_PROTOCOL_AND_TRACKER.md

# AGENT CORE PROTOCOL: SURGICAL EDITING MODE

**1. QUY TẮC SINH TỬ (STRICT LIMIT):**
- KHÔNG BAO GIỜ output quá 100-200 dòng code. 
- NẾU FILE DÀI: Tuyệt đối không rewrite toàn bộ file.

**2. GIAO THỨC SỬA CODE (SURGICAL EDIT):**
- Sử dụng tool `read_file` để tìm chính xác số dòng cần sửa.
- CHỈ output đoạn code thay thế và báo rõ: "Thay thế từ dòng X đến dòng Y".
- Dùng công cụ `search_and_replace` để sửa, tuyệt đối không chép lại cả file.


## 1. CORE PROTOCOLS (Quy tắc sinh tử)
- **Quy tắc 1**: KHÔNG BAO GIỜ output quá 150 - 200 dòng code trong một lần phản hồi.
- **Quy tắc 2**: Khi sửa file lớn, CHỈ viết phần logic thay đổi. Dùng comment `// ... [giữ nguyên code cũ] ...` cho phần còn lại.
- **Quy tắc 3**: Luôn đọc file này và chia nhỏ Sub-tasks trước khi bắt đầu code.

## 2. CURRENT STATUS (Tiến độ hiện tại)
- **Hệ thống thời gian**: ICT (+7h) ổn định trên toàn bộ DB và Bridge.
- **Hardening (Bảo mật & Chống Spam)**: Đã triển khai Cooldown 30 phút theo symbol và Persistent Signal Tracking.
- **Task 9 (Fix NULL Engine)**: Đã hoàn thành triệt để. Context trade được bảo toàn qua restart. Database đã sạch record lỗi.
- **Task 11 (AUDUSD Spam)**: Đã fix lỗi race condition. AUDUSD và các symbol khác đã có cơ chế chặn spam an toàn.
- **Giao diện Nexus (v8.0)**: Đã nâng cấp Glassmorphism, Neural Scan radar và Ao Làng Audit panel (soi lệnh VN30).
- **Đội hình (Squadron)**: Đã cân bằng lại logic gán lệnh. GAMMA đã được triển khai (NAS100/XAGUSD).

## 3. TACTICAL TASKS (Danh sách nhiệm vụ)
- [x] **Task 1**: Audit và vá lỗi `optimizer.py`. Đảm bảo hệ số SL/TP luôn dương.
- [x] **Task 2**: Khôi phục thẻ Binance (Eastern Front) trong `sovereign_nexus.html`.
- [x] **Task 3**: Sửa logic hiển thị `intel-list` (Learning Engine) trong `sovereign_nexus.html`.
- [x] **Task 4**: Rà soát tổng thể bố cục Nexus để đảm bảo không bị tràn.
- [x] **Task 5**: Kiểm tra cuối cùng (Final Audit) về tính đồng bộ thời gian.
- [x] **Task 6**: Sửa lỗi hiển thị DD (Drawdown) cho Binance và Ao Làng (Vn30).
- [x] **Task 7**: Nâng cấp Neural Scan (Thêm hiệu ứng Hover/Radar).
- [x] **Task 8**: Khôi phục hiển thị ER Configuration.
- [x] **Task 9**: Fix triệt để lỗi NULL trong Learning Engine (Persistence Guard).
- [x] **Task 10**: Sửa lỗi mất kết nối/đường dẫn của nút Battle Report.
- [x] **Task 11**: Kiểm tra và ổn định AUDUSD (Chống spam lệnh bằng Symbol Cooldown).

