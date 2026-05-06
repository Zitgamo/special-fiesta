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

## 5. THE SOVEREIGN TROUBLESHOOTING SOP (THE "5-MINUTE" RULE)

Để triệt tiêu các lỗi ngớ ngẩn và đảm bảo thời gian xử lý sự cố < 5 phút, Coder phải tuân thủ:

1.  **Quy tắc "Tiên kiểm" (Grep-First):** Trước khi thêm hoặc sửa bất kỳ `@app.route`, tên hàm, hoặc tên bảng Database (ví dụ: `hq_config`), PHẢI dùng lệnh `Select-String` (grep) để kiểm tra sự tồn tại và tính đồng nhất trên toàn hệ thống.
2.  **Quy tắc "Cắm cọc" (Global Scope):** Tuyệt đối không import thư viện bên trong hàm. Mọi thư viện (`os`, `json`, `sqlite3`) phải nằm ở đầu file.
3.  **Quy tắc "Thử lửa" (Foreground Validation):** Trước khi cho một script chạy ngầm (`sentinel`, `bridge`), PHẢI chạy trực tiếp `python path/to/script.py` để kiểm tra lỗi Syntax và kết nối Database.
4.  **Quy tắc "Đối soát" (Cross-Reference):** Khi chỉnh sửa UI (JavaScript), PHẢI mở song song file Backend (Python) tương ứng để đảm bảo các Endpoint và tham số JSON trùng khớp 100%.

---

---
**Signed by:** Antigravity (The Coder)  
**Approved by:** Commander
