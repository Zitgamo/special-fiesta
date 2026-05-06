# 🕹️ Manual Control Guide (Bật/Tắt Bot)

Trong trường hợp bạn không có sự hỗ trợ của AI, đây là hướng dẫn để bạn tự quản lý vận hành đội bay Iron Commander Elite.

## 🚀 1. Cách Bật Bot (Start)
Để khởi động toàn bộ hệ thống, bạn có hai lựa chọn:

*   **Lựa chọn 1 (Chạy tài khoản thật):** Chạy file `SOVEREIGN_REAL_LAUNCH.bat`. File này sẽ kích hoạt `sentinel.py` để canh gác tài khoản thật.
*   **Lựa chọn 2 (Khôi phục toàn bộ đội bay):** Chạy file `MISSION_RECOVERY.bat`. File này sẽ tự động mở các cửa sổ Terminal mới cho:
    *   `master.py` (Bộ não chỉ huy).
    *   `ALPHA`, `OMEGA`, `GAMMA` (Các đơn vị chiến đấu).
    *   `position_monitor.py` (Giám sát vị thế).

## 🛑 2. Cách Tắt Bot (Stop)
Có 2 cấp độ dừng bot:

### Cấp độ 1: Dừng tiến trình (Dừng tạm thời)
*   **Cách nhanh nhất:** Đóng tất cả các cửa sổ Terminal (CMD) đang chạy bot.
*   **Cách triệt để:** Mở **Task Manager** (Ctrl + Shift + Esc), tìm các tiến trình `python.exe` và chọn **End Task**.

### Cấp độ 2: Dừng khẩn cấp bằng Cơ sở dữ liệu (Emergency Pause)
Hệ thống có cơ chế "Fail-Closed". Bạn có thể kích hoạt dừng toàn cầu bằng cách can thiệp vào database `core_v3/iron_core.db`:
1. Mở database bằng một trình quản lý SQLite (như SQLite Browser).
2. Tìm bảng `hq_config`.
3. Sửa giá trị của `GLOBAL_PAUSE` thành `1`.
4. Khi đó, tất cả các đơn vị đang chạy sẽ tự động dừng thực hiện lệnh mới (Safety Abort).

## 📊 3. Theo dõi Dashboard
Để xem tình hình mà không cần code:
*   Mở file [`nexus/sovereign_nexus.html`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/nexus/sovereign_nexus.html) bằng trình duyệt (Chrome/Edge). Dashboard này tự động cập nhật dữ liệu từ database.

## 🧹 4. Bảo trì
Nếu thấy hệ thống nặng hoặc lag, hãy chạy file:
*   `python janitor.py --run`
Nó sẽ dọn dẹp log và kiểm tra lỗi database cho bạn.

---
**Lưu ý:** Luôn đảm bảo phần mềm **MetaTrader 5 (Exness)** đang mở và đã đăng nhập trước khi bật bot.
