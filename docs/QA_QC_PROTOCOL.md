# 🛡️ SOVEREIGN QA/QC PROTOCOL: UI-BACKEND INTEGRATION

Bản giao kèo này thiết lập tiêu chuẩn kiểm định nghiêm ngặt để loại bỏ tình trạng "Vỏ rỗng" (Mockup không có logic).

## 1. TIÊU CHUẨN "NỐI DÂY" (E2E INTEGRATION)
- **Nguyên tắc 1: Không có API, không có UI**. Mọi thành phần hiển thị trên Dashboard phải được nuôi bằng dữ liệu thật từ Backend.
- **Nguyên tắc 2: Real-time Check**. Dữ liệu trên UI phải thay đổi khi dữ liệu trong Database thay đổi. Nếu dữ liệu đứng im (Hard-coded), Task đó bị coi là THẤT BẠI.

## 2. QUY TRÌNH KIỂM THỬ (TEST PROCEDURE)
Mỗi khi Coder báo hoàn thành một Component UI, Auditor phải thực hiện các bước:
1.  **Backend Audit**: Kiểm tra `nexus_bridge.py` để xác định Endpoint (`/api/...`) cung cấp dữ liệu.
2.  **Frontend Audit**: Kiểm tra lệnh `fetch()` hoặc `updateHUD()` trong HTML để xác định đường đi của dữ liệu.
3.  **Stress Test**: Thay đổi giả lập giá trị trong Database và quan sát UI có cập nhật đúng không.

## 3. TRƯỜNG HỢP ĐẶC BIỆT: BÁO CÁO NGÀY (BATTLE REPORT)
- Hiện trạng: Đang là một "Vỏ rỗng" trả về text đơn thuần.
- **Yêu cầu Fix**: 
    - Coder phải hoàn thiện Route `/report` để trả về file HTML có chứa bảng dữ liệu thực từ bảng `trades`.
    - Phải có bộ lọc (Filter) theo Unit_ID (ALPHA/OMEGA/GAMMA).

---
**Auditor Mandate:** *"Bản vẽ đẹp đến đâu mà không có điện chạy qua thì cũng chỉ là tờ giấy vụn."*
