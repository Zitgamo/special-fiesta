# 🚢 SOVEREIGN SHIPMENT: VERSION LIFECYCLE (SDLC)

Để tránh việc sửa chữa vụn vặt và sa lầy vào tiểu tiết, dự án sẽ tuân thủ quy trình **"Build - Test - Ship"** theo từng phiên bản.

## 🔄 CHU KỲ PHÁT TRIỂN (THE LOOP)

1.  **PHASE 1: SPEC (Docs Agent)**
    *   Lập bản vẽ chi tiết cho các tính năng mới trong phiên bản tiếp theo.
    *   Commander phê duyệt bản vẽ.
2.  **PHASE 2: BUILD (Coder Agent)**
    *   Triển khai code dựa trên Spec.
    *   **Cấm**: Không sửa các tính năng của Version cũ đã "Ship". Chỉ làm cái mới.
3.  **PHASE 3: QC & AUDIT (Docs Agent)**
    *   Thư ký kiểm tra code, test lỗi.
    *   Cập nhật tài liệu, hướng dẫn sử dụng cho Version đó.
4.  **PHASE 4: SHIP (The Commander)**
    *   Đóng gói thành một Version hoàn chỉnh (ví dụ: v1.0).
    *   Gắn Tag Git (Release). 
    *   **Nguyên tắc**: Một khi đã Ship, không sửa lại "ruột" của Version đó trừ khi có lỗi chí tử.

---

## 🛠️ CHIẾN LƯỢC TIẾP THEO: VERSION 1.0 (STABILITY)
Mục tiêu của v1.0 là **Sự ổn định Tuyệt đối** trước khi sang v2.0 (Tính năng nâng cao).

### Các hạng mục v1.0:
- [ ] **Single Switch**: Tự động chuyển Demo/Real qua 1 file config.
- [ ] **Auto-Janitor**: Dọn rác tự động theo sự kiện (Event-driven).
- [ ] **Git UI Status**: Giám sát Coder trên Dashboard.
- [ ] **Smart Blacklist**: Fix lỗi bỏ qua danh sách đen trong Engine.

---
**Commander Directive:** *"Sửa Front => Back => Test => XYZ => SHIP. Xong là Loop lại, không làm quẩn quanh một chỗ."*
