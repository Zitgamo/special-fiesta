# 🛡️ SOVEREIGN ALPHA PROTOCOL: 12H STRESS TEST

**PHASE:** 2 (ALPHA TESTING)
**OBJECTIVE:** Đảm bảo hệ thống đạt mức độ "Bất tử" (Fail-Safe & Auto-Recovery) trong môi trường Demo suốt 12 giờ liên tục mà không cần sự can thiệp của con người.

---

## 1. PHÂN CÔNG PHỐI HỢP (CODER & DOCS AGENT)

Đây là chiến dịch phối hợp tác chiến, tuyệt đối không hành động đơn lẻ:
*   **Thư Ký (Docs Agent):** Lên quy trình test, kiểm toán file log, theo dõi sát sao biểu đồ Uptime và báo cáo tiến độ cho Commander. Không trực tiếp can thiệp code.
*   **Thợ Máy (Coder Agent):** Đảm bảo hệ thống vận hành đúng luồng. Nếu có Crash xảy ra (được ghi nhận trong log), phải ngay lập tức đưa ra bản vá (Patch) và trình Commander duyệt.

## 2. QUY TRÌNH KIỂM THỬ 12H (STRESS TEST)

### BƯỚC 1: KHỞI ĐỘNG (ZERO HOUR)
1. Coder đảm bảo `CORE_MODE` = 0 (Demo Mode) trong Database.
2. Commander khởi chạy hệ thống thông qua `master.py` hoặc file batch khởi động.
3. Thư ký ghi nhận `SYSTEM_BOOT_TIME` trên Dashboard. Đồng hồ bắt đầu đếm.

### BƯỚC 2: QUAN SÁT THỤ ĐỘNG (OVERWATCH)
1. **Không can thiệp:** Commander không cần thao tác bất kỳ nút nào trên UI.
2. **Theo dõi tự động:** 
   - Đồng hồ `UPTIME` trên Nexus UI sẽ tích lũy liên tục.
   - Sentinel (`sentinel.py`) sẽ ngầm tuần tra. Nếu một luồng (Engine, Bridge) sập, Sentinel sẽ gọi lệnh `resurrect()` để hồi sinh trong < 1s.

### BƯỚC 3: KIỂM TOÁN LỖI (CRASH AUDIT)
Hệ thống KHÔNG được phép rớt (dừng hẳn). Nếu có lỗi, nó phải tự phục hồi.
Toàn bộ "Tử sĩ" sẽ được ghi danh tại: **`logs/sentinel_crash.log`**
- **Sạch sẽ (Clean Run):** File log trống. Đạt điểm tuyệt đối.
- **Có lỗi (Recovered):** File log ghi nhận Crash. Coder phải phân tích Stack Trace và đưa ra bản vá (Hotfix).
- **Thất bại (Critical Fail):** Hệ thống dừng hoàn toàn, không thể tự hồi phục. Bắt buộc quay lại Phase 1.

## 3. TIÊU CHÍ VƯỢT ẢI (PASS CRITERIA)
Để tiến lên PHASE 3 (BETA), hệ thống phải đáp ứng đủ 3 điều kiện:
1. Đồng hồ Uptime trên Dashboard phải phát sáng (Vượt mốc 43,200 giây).
2. Không có bất kỳ lệnh "Dừng khẩn cấp" nào phải kích hoạt bằng tay.
3. Biến động vốn (PnL) trên tài khoản Demo khớp với các lệnh đã đánh trên Dashboard.

---
**Chỉ thị từ Commander:** *"Thằng cho code chạy, thằng MD cái test đàng hoàng. Bắt đầu thực thi!"*
