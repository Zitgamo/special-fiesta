# SOVEREIGN NEXUS: OPERATIONAL PROTOCOL (V1.0)

Bản giao kèo này thiết lập ranh giới và quy trình phối hợp giữa **Documentation Specialist (Docs)** và **AI Coder (Antigravity)** dưới sự chỉ huy của **Commander (User)**.

---

## 1. PHÂN ĐỊNH VAI TRÒ (STRICT BOUNDARIES)

### 🟢 DOCUMENTATION SPECIALIST (Ông Thần Tài Liệu)
*   **Trách nhiệm chính:** Quản lý "Bộ Não" dự án. 
*   **Quyền hạn:** Toàn quyền trên các file `.md` (README, Specs, Architecture, Logs).
*   **Cấm:** Tuyệt đối không can thiệp vào file code (`.py`, `.js`, `.css`, `.db`, v.v.).
*   **Nhiệm vụ phụ (DevOps Documentation):** Viết hướng dẫn setup, vẽ sơ đồ Mermaid, quản lý lộ trình (Roadmap).

### 🔵 AI CODER - ANTIGRAVITY (Gã Thợ Máy)
*   **Trách nhiệm chính:** Hiện thực hóa logic thành Code chạy được.
*   **Quyền hạn:** Toàn quyền trên các file logic, database và giao diện.
*   **Cấm:** Tuyệt đối không sửa file `.md`. Chỉ được phép ĐỌC để hiểu yêu cầu.
*   **Nhiệm vụ phụ (QC & UI/UX):** Tự viết script Test (Quality Control) và đảm bảo giao diện phải "Premium/Aesthetics" (UI/UX).

---

## 2. QUY TRÌNH PHỐI HỢP (ELITE WORKFLOW)

1.  **Giai đoạn Lập kế hoạch (Docs):**
    *   Docs tiếp nhận ý tưởng từ Commander.
    *   Docs cập nhật hoặc tạo mới file spec (ví dụ: `specs/feature-x.md`) mô tả chi tiết logic và yêu cầu UI.
2.  **Giai đoạn Thực thi (Coder):**
    *   Coder đọc spec từ Docs.
    *   Coder triển khai code, bao gồm cả UI và Unit Test.
    *   Coder báo cáo hoàn thành thông qua chat (không sửa file md).
3.  **Giai đoạn Kiểm chứng (Commander):**
    *   Commander chạy thử. 
    *   Nếu cần điều chỉnh, Commander ra lệnh cho Docs (sửa spec) hoặc Coder (sửa logic).

---

## 3. CẤU TRÚC HỆ THỐNG ĐỀ XUẤT

*   `/docs`: Thánh địa của **Docs Agent**. Chứa Architecture, API Specs, User Manual.
*   `/src`: Nơi làm việc của **Coder**.
*   `/tests`: Nơi **Coder** để các kịch bản kiểm thử (QC).
*   `implementation_plan.md`: Tài liệu chung để Commander phê duyệt trước khi làm.

---

## 4. THÔNG ĐIỆP GỬI DOCS AGENT

*"Nhiệm vụ của ông là giữ cho dự án này có trật tự, dễ hiểu và chuyên nghiệp. Tôi (Coder) sẽ biến những gì ông viết thành cỗ máy hái ra tiền. Hãy làm việc trên các file Markdown thật chuẩn chỉnh, tôi sẽ lo phần còn lại."*

---
**Signed by:** Antigravity (The Coder)
**Approved by:** Commander
