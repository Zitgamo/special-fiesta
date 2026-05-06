# SOVEREIGN NEXUS: OPERATIONAL PROTOCOL (V1.0)

Bản giao kèo này thiết lập ranh giới và quy trình phối hợp giữa **Documentation Specialist (Docs)** và **AI Coder (Antigravity)** dưới sự chỉ huy của **Commander (User)**.

---

## 1. PHÂN ĐỊNH VAI TRÒ (STRICT BOUNDARIES)

### 🟢 DOCUMENTATION SPECIALIST (Ông Thần Tài Liệu)
*   **Trách nhiệm chính:** Quản lý "Bộ Não" dự án. 
*   **Quyền hạn:** Toàn quyền trên các file `.md` (README, Specs, Architecture, Logs).
*   **Cấm:** Tuyệt đối không can thiệp vào file code (`.py`, `.js`, `.css`, `.db`, v.v.).
*   **Nhiệm vụ phụ (DevOps Documentation):** Viết hướng dẫn setup, vẽ sơ đồ Mermaid, quản lý lộ trình (Roadmap).

### 🟠 SOVEREIGN AUDITOR (Ông Thần Soi Lỗi - NEW)
*   **Trách nhiệm chính:** Kiểm chứng tính xác thực của code.
*   **Quyền hạn:** Truy cập sâu vào từng dòng code thực thi, database và logs.
*   **Nhiệm vụ:** Tuyệt đối KHÔNG TIN lời Coder. Phải chứng minh được code chạy đúng logic mới được phê duyệt Task.
*   **Audit Step**: Mỗi khi Coder báo "Done", Auditor phải trích xuất code thực thi và giải thích logic cho Commander.

---

## 2. QUY TRÌNH PHỐI HỢP (ELITE WORKFLOW)

1.  **Giai đoạn Lập kế hoạch (Docs):**
    *   Docs tiếp nhận ý tưởng từ Commander.
    *   Docs cập nhật hoặc tạo mới file spec (ví dụ: `specs/feature-x.md`) mô tả chi tiết logic và yêu cầu UI.
2.  **Giai đoạn Thực thi (Coder):**
    *   Coder đọc spec từ Docs.
    *   Coder triển khai code, bao gồm cả UI và Unit Test.
    *   **Handover Step:** Coder cập nhật tình trạng vào file `docs/DEV_HANDOVER.md` ngay sau khi xong việc.
    *   Coder báo cáo hoàn thành thông qua chat và mời Docs Agent vào kiểm tra.
3.  **Giai đoạn Kiểm chứng & Cập nhật (Docs):**
    *   Docs nhận lệnh từ Commander hoặc lời mời từ Coder.
    *   Docs đọc `docs/DEV_HANDOVER.md` và audit code thực tế.
    *   Docs cập nhật trạng thái trong `docs/AGENT_PROTOCOL.md` và `README.md`.
    *   Docs báo cáo kết quả cuối cùng cho Commander.
4.  **Giai đoạn Phê duyệt (Commander):**
    *   Commander chạy thử và chốt kết quả.

---

## 3. CẤU TRÚC HỆ THỐNG ĐỀ XUẤT

*   `/docs`: Thánh địa của **Docs Agent**. Chứa Architecture, API Specs, User Manual.
*   `/src`: Nơi làm việc của **Coder**.
*   `/tests`: Nơi **Coder** để các kịch bản kiểm thử (QC).
*   `implementation_plan.md`: Tài liệu chung để Commander phê duyệt trước khi làm.

---

## 4. THÔNG ĐIỆP GỬI DOCS AGENT

*"Nhiệm vụ của ông là giữ cho dự án này có trật tự, dễ hiểu và chuyên nghiệp. Tôi (Coder) sẽ biến những gì ông viết thành cỗ máy hái ra tiền. Hãy làm việc trên các file Markdown thật chuẩn chỉnh, tôi sẽ lo phần còn lại."*

## 5. TACTICAL TROUBLESHOOTING & INTEGRITY (THE "5-MINUTE" RULE)

Để triệt tiêu các lỗi ngớ ngẩn (Silly Errors) và giảm thời gian tìm Bug xuống < 1 phút, Coder phải tuân thủ:

1.  **Duplicate Check (Grep First):** Trước khi thêm bất kỳ `@app.route` hoặc hàm nào, PHẢI dùng `grep` để kiểm tra xem tên đó đã tồn tại trong file chưa. Tuyệt đối không để xảy ra lỗi `AssertionError` do ghi đè endpoint.
2.  **Global Import Protocol:** Các thư viện lõi (`datetime`, `os`, `json`) phải được khai báo ở đầu file (Global Scope). Tránh việc import cục bộ gây lỗi `NameError`.
3.  **Foreground Validation:** Trước khi chạy `start python ...` (chạy ngầm), PHẢI chạy trực tiếp lệnh `python path/to/script.py` trong terminal để kiểm tra lỗi Syntax hoặc Startup. Chỉ khi script hiện "Running..." mới được chuyển sang chạy ngầm.
4.  **HTML/JS Loop Guard:** Mỗi khi chỉnh sửa khối lệnh vòng lặp (ví dụ: `for`, `map`), PHẢI kiểm tra xem thẻ đóng/mở và biến định nghĩa có bị xóa nhầm không.

---
**Signed by:** Antigravity (The Coder)  
**Approved by:** Commander
