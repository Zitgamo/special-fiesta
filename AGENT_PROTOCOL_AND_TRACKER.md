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
- **Hệ thống thời gian**: Đã đồng bộ ICT (+7h) bằng phương pháp Hard-coded cho toàn bộ DB và Bridge.
- **Dữ liệu DNA**: Đã khôi phục các hệ số nhân SL/TP dương (Alpha: 1.0, Omega/Gamma: 1.5) để duy trì tính Dynamic ATR.
- **Giao diện Nam Chiến Tuyến (Southern Command)**: Đã nâng cấp chữ to, có khung cuộn và khớp giờ ICT.
- **Giao diện Nexus**: Đang bị lỗi hiển thị (Mất Binance card, Learning Engine báo NULL) và cần tinh chỉnh bố cục chống tràn.
- **Logic Tối ưu**: Phát hiện `optimizer.py` sinh ra số âm cho SL/TP, gây lỗi DNA.

## 3. TACTICAL TASKS (Danh sách nhiệm vụ)
- [x] **Task 1**: Audit và vá lỗi `optimizer.py`. Đảm bảo hệ số SL/TP luôn dương (Dùng `abs()` hoặc `max(0.1, val)`).
- [x] **Task 2**: Khôi phục thẻ Binance (Eastern Front) trong `sovereign_nexus.html`.
- [x] **Task 3**: Sửa logic hiển thị `intel-list` (Learning Engine) trong `sovereign_nexus.html` để không bị NULL.
- [x] **Task 4**: Rà soát tổng thể bố cục Nexus để đảm bảo không bị tràn trên màn hình người dùng.
- [x] **Task 5**: Kiểm tra cuối cùng (Final Audit) về tính đồng bộ thời gian trên toàn bộ Strike Log.
- [x] **Task 6**: Sửa lỗi hiển thị DD (Drawdown) cho Binance và Southern (Vn30).
- [x] **Task 7**: Nâng cấp Neural Scan (Thêm hiệu ứng Hover/Click để xem chi tiết asset).
- [x] **Task 8**: Khôi phục hiển thị ER Configuration (Efficiency Ratio) trong phần Deployment.
- [/] **Task 9**: Fix triệt để lỗi NULL trong Learning Engine (Kiểm tra logic API và render).
- [x] **Task 10**: Sửa lỗi mất kết nối/đường dẫn của nút Battle Report.
- [/] **Task 11**: Kiểm tra và ổn định AUDUSD (Chống spam lệnh).
