# 🏛️ SOVEREIGN PROJECT MANAGEMENT STANDARDS

Bản tiêu chuẩn này thiết lập cách thức quản lý dự án theo phong cách chuyên nghiệp (Agile/Scrum), đảm bảo sự bền vững và khả năng mở rộng.

## 1. QUẢN LÝ CÔNG VIỆC (BACKLOG SYSTEM)
- **Hàng đợi (Backlog)**: Mọi ý tưởng phát sinh trong quá trình Build sẽ được ghi vào Backlog, không làm ngay để tránh làm loãng Version hiện tại.
- **Sprint (Giai đoạn)**: Mỗi Version (v1.0, v1.1...) là một Sprint. Chỉ tập trung dứt điểm các Task đã chốt cho Sprint đó.

## 2. KIỂM SOÁT THAY ĐỔI (CHANGE CONTROL)
- Commander ra lệnh -> Thư ký phân tích tác động -> Coder triển khai.
- **Nguyên tắc "Đóng băng" (Feature Freeze)**: Khi đã bước vào giai đoạn BETA (Phase 3), tuyệt đối không thêm tính năng mới. Chỉ sửa lỗi.

## 3. QUẢN LÝ RỦI RO (RISK MITIGATION)
- **Auto-Backup**: Sentinel phải tự động sao lưu Database mỗi 4 tiếng.
- **Kill Switch**: Luôn duy trì cơ chế dừng khẩn cấp bằng tay và bằng DB.

## 4. TIÊU CHUẨN "SHIP" HÀNG (DEFINITION OF DONE)
Một Task chỉ được coi là "Done" khi:
1. Code đã được Coder tự Test (Unit Test passed).
2. Thư ký đã Audit code và xác nhận đúng Spec.
3. Tài liệu README/Manual đã được cập nhật tương ứng.
4. Git đã được Commit và Tag Version.

---
**Secretary Mandate:** *"Chúng ta không chỉ xây dựng một con Bot, chúng ta đang xây dựng một Đế chế phần mềm bền vững."*
