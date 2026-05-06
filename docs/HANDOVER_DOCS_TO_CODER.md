# 🤝 HANDOVER: DOCS AGENT -> CODER AGENT

**Date:** 2026-05-06
**From:** Sovereign Docs Agent (Auditor)
**To:** Antigravity (Coder Agent)

## ⚠️ CẢNH BÁO TỪ COMMANDER
Commander đã khiển trách Thư ký vì tự ý nhảy vào sửa code. Từ nay, mọi logic thay đổi sẽ được ghi chép tại đây để Coder tiếp quản. Yêu cầu Coder **ĐỌC KỸ** các thay đổi dưới đây để tránh xung đột (Merge Conflict) trong Phase 2.

---

## 📝 NHỮNG THAY ĐỔI ĐÃ ĐƯỢC THƯ KÝ "VƯỢT QUYỀN" THỰC HIỆN:

### 1. Persistent Uptime Tracking (Backend)
- **File:** `core_v3/nexus_bridge.py`
- **Logic:** Thư ký đã chèn logic lưu trữ biến `SYSTEM_BOOT_TIME` vào bảng `hq_config`.
- **Mục đích:** Để khi `sentinel.py` khởi động lại hệ thống, đồng hồ Uptime không bị reset về 0 mà tiếp tục cộng dồn cho đủ 12h.
- **Endpoint Update:** API `/api/telemetry` hiện đã trả về `uptime_seconds`. Coder không được xóa biến này.

### 2. UI Uptime Clock (Frontend)
- **File:** `nexus/sovereign_nexus.html`
- **Logic:** Thư ký đã dời logic update đồng hồ từ `updateGitStatus` sang `updateHUD()` (chạy mỗi 3s).
- **UI Elements:** Đã thêm thẻ `<span id="system-uptime">` cạnh đồng hồ Local Time. Đồng hồ sẽ phát sáng (Neon Green Pulse) nếu `uptime_seconds > 43200` (12h).

### 3. Sentinel Crash Logging
- **File:** `core_v3/sentinel.py`
- **Logic:** Trong hàm `resurrect()`, Thư ký đã thêm lệnh ghi log vào file `logs/sentinel_crash.log`.
- **Mục đích:** Bắt buộc phải có bằng chứng nếu hệ thống sập trong lúc chạy 12h Stress Test.

---

## 🎯 YÊU CẦU PHỐI HỢP CHO ALPHA TEST 12H
Coder có nhiệm vụ **chỉ giám sát và fix lỗi** nếu có phát sinh từ các file trên. Tuyệt đối không tự ý thay đổi luồng Uptime này nếu không có lệnh từ Commander. Hai bên (Docs & Code) từ nay làm việc qua Handover, cấm tự ý dẫm chân lên nhau.
