# 🚀 Implementation Plan: Core Real & Stability (V1.0)

**Goal:** Establish the foundation for `core_real` while hardening `core_v3` with background monitoring and visual balance metrics.

## 1. PHÂN TÍCH YÊU CẦU (COMMANDER DIRECTIVE)

### 🛰️ Task 1: Git Status & Telegram Monitoring
- **Vấn đề:** Commander không nhận được thông báo Telegram về tình trạng Git mỗi giờ như mong đợi.
- **Giải pháp:** Thiết lập một dịch vụ nền (Background Task) tự động kiểm tra thay đổi chưa commit và bắn báo cáo trạng thái "Sức khỏe Codebase" qua Telegram mỗi 60 phút.

### ⚖️ Task 2: Sovereign Balance Scale (Ruột vs Vỏ)
- **Vấn đề:** Commander cần một chỉ số trực quan để biết tiến độ dự án đang cân bằng giữa **Logic (Ruột)** và **Giao diện (Vỏ)**.
- **Giải pháp:** 
  - Thêm một "Cân công lý" hoặc "Đồng hồ cân bằng" trên Nexus UI.
  - **Back Score (Ruột):** Tính toán dựa trên độ phức tạp của logic giao dịch, khối lượng dữ liệu trong DB và hiệu suất sinh lời thực tế.
  - **Front Score (Vỏ):** Tính toán dựa trên mức độ hoàn thiện của UI, các hiệu ứng Premium và độ rõ nét của thông tin hiển thị.
  - **Mục tiêu:** Giúp Commander có cảm hứng tiếp tục khi thấy cả "vỏ đẹp" và "ruột tốt" đều tăng trưởng.

---

## 🛠️ CHI TIẾT TRIỂN KHAI (DÀNH CHO CODER)

### 🔵 Component: Background Services
#### [NEW] `core_v3/git_monitor.py`
- Script này sẽ chạy trong một luồng (thread) riêng từ `master.py`.
- Mỗi 3600 giây:
  1. Chạy `git status --short`.
  2. Nếu có thay đổi: Gửi Telegram qua `SignalCommander` với format: `📦 GIT UPDATE: [X] file thay đổi chưa commit. Codebase đang phát triển!`
  3. Nếu không có thay đổi: Gửi Telegram: `✅ GIT SYNC: Hệ thống đang ở trạng thái ổn định nhất.`

### 🔵 Component: Backend (API)
#### [MODIFY] `core_v3/nexus_bridge.py`
- **[NEW] Git Info Endpoint:** Thêm logic sử dụng lệnh `git log` và `git status` để lấy thông tin commit mới nhất và trạng thái hệ thống.
- Bổ sung logic tính toán **Sovereign Balance Ratio**:
  - `back_score = (Số lượng lệnh thành công * 0.5) + (Kích thước DB * 0.1)`
  - `front_score = (Số lượng thành phần UI * 10) + (Mức độ CSS hiệu ứng)`
  - Output kết quả vào API `/api/telemetry`.

### 🔵 Component: UI (Frontend)
#### [MODIFY] `nexus/sovereign_nexus.html`
- Thiết kế và chèn một Component CSS/SVG: **"THE SOVEREIGN SCALE"**.
- **[NEW] Git Status Monitor:** 
    - Thêm một panel nhỏ hiển thị: `Last Commit Message`, `Time` và `Status` (Clean/Dirty).
    - Nếu có file chưa commit, panel sẽ nhấp nháy đỏ cảnh báo: *"UNCOMMITTED CHANGES DETECTED"*.
- Vị trí: Góc trên bên trái hoặc ngay dưới PnL Container.
- Hiệu ứng: Cây kim đồng hồ hoặc đĩa cân dao động dựa trên tỉ lệ `back_score : front_score`.
- Hiển thị thông báo động: *"Vỏ đẹp - Ruột tốt: Đạt trạng thái Tuyệt Đối"* hoặc *"Cảnh báo: Code đang chạy nhanh hơn Vỏ - Hãy làm đẹp giao diện!"*.

---

## 🏁 KẾ HOẠCH KIỂM CHỨNG (VERIFICATION)
1. **Manual Test:** Chạy `git_monitor.py` riêng lẻ để xem tin nhắn Telegram có về không.
2. **Visual Audit:** Mở Nexus UI, kiểm tra xem "Cân" có hiển thị đúng tỉ lệ không khi thay đổi giả lập dữ liệu API.
3. **End-to-End:** Khởi động lại toàn bộ Fleet và quan sát sự đồng bộ.

---
**Status:** Awaiting Commander Approval.
**Author:** Sovereign Docs Agent
