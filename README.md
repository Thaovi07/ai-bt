# HỆ THỐNG AI AGENT PHÂN TÍCH HIỆU QUẢ KINH DOANH CHUỖI CỬA HÀNG
## Doanh nghiệp: Công ty Bán lẻ Phúc An (Phúc An Retail Chain - 18 Cửa hàng)
### Môn học: AI301 | Đề 07

---

## 📌 PHẦN 1: BÁO CÁO PHÂN TÍCH & THIẾT KẾ (TASK 1)

### 1.1. Phân tích quy trình hiện tại & 3 Vấn đề cốt lõi
* **Bối cảnh**: Công ty Phúc An vận hành chuỗi 18 cửa hàng bán lẻ, mỗi tháng phát sinh ~60.000 dòng dữ liệu bán hàng và đổi trả. Việc ghép nối dữ liệu bán hàng, giá vốn và mục tiêu hiện đang thực hiện thủ công bằng Excel.
* **Vấn đề 1: Đếm trùng giao dịch và cộng cả đơn hủy**
  * *Ảnh hưởng cụ thể*: Doanh thu bị thổi phồng ảo (Overstated Revenue), dẫn đến ngộ nhận về hiệu quả bán hàng thực tế. Các cửa hàng có tỷ lệ hủy đơn cao (do lỗi hệ thống POS, khách đổi ý, tồn kho ảo) vẫn được ghi nhận doanh số, làm sai lệch báo cáo dòng tiền và đánh giá sai KPI nhân viên.
* **Vấn đề 2: Xử lý hàng trả không đồng nhất và so sánh lệch kỳ thời gian**
  * *Ảnh hưởng cụ thể*: Nhiều cửa hàng trừ tiền trả lại nhưng không hoàn nhập giá vốn hàng bán, hoặc trừ hàng trả vào doanh thu của cửa hàng khác. Nghiêm trọng hơn, việc so sánh doanh thu giữa các khoảng thời gian không tương đồng (ví dụ so sánh tháng 31 ngày với tháng 28 ngày, hoặc so sánh kỳ có tuần khuyến mãi với kỳ không khuyến mãi) tạo ra "tăng trưởng ảo", khiến cấp quản lý bỏ qua những cửa hàng đang thực sự suy thoái.
* **Vấn đề 3: Đề xuất cải thiện phiến diện, chỉ dựa vào doanh thu mà bỏ qua cơ cấu sản phẩm và biên lợi nhuận gộp**
  * *Ảnh hưởng cụ thể*: Cửa hàng đạt doanh thu cao nhưng thực chất chỉ bán hàng khuyến mãi biên mỏng hoặc hàng xả lỗ, khiến lợi nhuận gộp thực tế teo tóp. Ngược lại, những cửa hàng bán hàng đặc thù biên lợi nhuận cao nhưng doanh thu số học thấp hơn lại bị đánh giá kém.

---

### 1.2. Quy trình đề xuất chuẩn hóa (8 Bước bám sát sơ đồ Phúc An)

| Bước | Tên bước | Đầu vào | Công việc thực hiện | Đầu ra | Trách nhiệm |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Tiếp nhận & kiểm tra dữ liệu | File CSV/XLSX hoặc Link Google Sheets (Giao dịch, Đổi trả, Giá vốn, Mục tiêu, Cửa hàng) | Kiểm tra định dạng, kiểm tra tính sẵn sàng của các tệp dữ liệu nguồn | Tập dữ liệu thô đã được nạp vào bộ nhớ | **Data Team** |
| **2** | Xử lý & làm sạch dữ liệu | Dữ liệu giao dịch, đổi trả, danh mục giá vốn | Loại trùng bản ghi, lọc đơn hủy, đối soát đơn đổi trả với hóa đơn gốc, cách ly giao dịch thiếu giá vốn | Dữ liệu sạch + Bảng cách ly "Dữ liệu chưa đủ căn cứ" | **AI Agent** |
| **3** | Tính toán chỉ số kinh doanh | Dữ liệu sạch, bảng giá vốn, chỉ tiêu mục tiêu | Tính Doanh thu gộp, Hàng trả lại, Doanh thu thuần, Giá vốn chuẩn, Lợi nhuận gộp, % Hoàn thành kế hoạch | Bảng chỉ số cơ sở theo từng cửa hàng | **AI Agent** |
| **4** | Tổng hợp & phân tích | Bảng chỉ số cơ sở kỳ báo cáo & kỳ so sánh | So sánh tăng trưởng MoM, phân tích cơ cấu ngành hàng, tính điểm chẩn đoán thiếu hụt | Bảng phân tích tăng trưởng + Top 3 cửa hàng ưu tiên | **AI Agent** |
| **5** | Kiểm tra kết quả có hợp lệ? (Gate) | Toàn bộ kết quả Bước 2-4 & Danh sách dữ liệu cách ly | Rà soát tỷ lệ dữ liệu sạch, phát hiện bất thường logic. Nếu sai lệch -> Trả về Bước 1 kèm cảnh báo | Xác nhận kết quả hợp lệ / Lệnh từ chối | **Con người (Data Reviewer)** |
| **6** | Con người kiểm tra & ra quyết định | Đề xuất phân tích từ AI + Số liệu chẩn đoán | Xem xét 3 cửa hàng AI đề xuất, đối chiếu bối cảnh thị trường thực tế, phê duyệt quyết định | Quyết định chính thức danh sách 3 cửa hàng cần hỗ trợ | **Giám đốc Kinh doanh** |
| **7** | Xuất báo cáo quản trị | Kết quả phân tích đã được phê duyệt | Tạo bảng chỉ số theo cửa hàng, cơ cấu ngành hàng, danh sách dữ liệu cách ly và đề xuất hành động | Tệp Báo cáo Excel + JSON Lineage Log | **AI Agent** |
| **8** | Bàn giao báo cáo | Báo cáo quản trị & Nhật ký truy vết | Trình báo cáo cho Ban Giám đốc, lưu trữ log kiểm toán phục vụ thanh tra/đối soát | Kết thúc quy trình, hoàn thành mục tiêu | **Phòng Kinh doanh & BGĐ** |

---

### 1.3. Lựa chọn bước cho AI Agent & Điểm can thiệp của Con người

#### A. 3 Bước AI Agent tự thực hiện:
1. **Bước 2: Xử lý & làm sạch dữ liệu**: Khối lượng ~60.000 dòng/tháng vượt quá khả năng xử lý tay của con người. Agent thực thi các quy tắc đối soát chính xác 100%: bắt trùng lặp, lọc đơn hủy, đối soát chéo mã đơn gốc của hàng trả lại, phân loại nguyên nhân cách ly.
2. **Bước 3: Tính toán chỉ số kinh doanh**: Đảm bảo tính toán nhất quán công thức Doanh thu thuần và Lợi nhuận gộp, tự động tính tỷ lệ hoàn thành kế hoạch không phụ thuộc vào cảm tính.
3. **Bước 4: Tổng hợp & Phân tích cơ cấu**: Thuật toán tính chỉ số thiếu hụt (Deficit Diagnostic Scoring) tổng hợp đồng thời 4 chiều: % Đạt doanh thu, % Đạt lợi nhuận, Tăng trưởng MoM và Tỷ lệ đổi trả để xếp hạng khách quan.

#### B. 2 Điểm Con người kiểm tra / ra quyết định (Human-in-the-Loop):
1. **Bước 5: Thẩm định chất lượng dữ liệu (Quality Gate)**:
   * *Điều kiện chuyển tiếp*: Tỷ lệ dữ liệu sạch đạt yêu cầu (>95%), không có lỗi hệ thống nghiêm trọng.
   * *Điều kiện chuyển xử lý ngược*: Khi tỷ lệ cách ly bất thường (ví dụ >10% giao dịch thiếu giá vốn hoặc hàng trả không tìm thấy đơn gốc), người kiểm duyệt bấm Bác bỏ, hệ thống gửi thông báo lỗi ngược lại Bước 1 cho Data Team để cập nhật Master Data.
2. **Bước 6: Giám đốc Kinh doanh phê duyệt quyết định**:
   * AI Agent chỉ đóng vai trò trợ lý đưa ra khuyến nghị dựa trên số liệu. Giám đốc Kinh doanh là người chịu trách nhiệm cuối cùng, kết hợp dữ liệu với các yếu tố định tính (đường sá tu sửa, nhân sự mới, biến động địa phương) để chốt phân bổ ngân sách và nhân sự hỗ trợ.

---

## 💻 PHẦN 2: GIẢI PHÁP PHẦN MỀM CHẠY ĐƯỢC (TASK 2)

### 2.1. Kiến trúc Giải pháp & 2 Kỹ Năng Nghiệp Vụ Phối Hợp
* **Skill 1 (`SkillDataQuality`)**: Kỹ năng Kiểm tra chất lượng dữ liệu, Loại trùng, Lọc đơn hủy, Đối chiếu đổi trả và Cách ly bản ghi lỗi. Mọi bản ghi loại trừ đều được gắn mã nguyên nhân cụ thể và lưu vết.
* **Skill 2 (`SkillBusinessAnalytics`)**: Kỹ năng Phân tích chỉ số kinh doanh chuỗi bán lẻ, Đánh giá tăng trưởng kỳ trước, Cơ cấu ngành hàng và Thuật toán xếp hạng Top 3 cửa hàng ưu tiên hỗ trợ.
* **Central Audit Trail (`AuditLogger`)**: Ghi nhận toàn bộ vết thực thi, thời gian, tên quy tắc và đường dẫn dữ liệu.

### 2.2. Kết quả Chẩn đoán Top 3 Cửa Hàng Phúc An Cần Hỗ Trợ Khẩn Cấp
1. **Phúc An Hà Đông (PA_HN05)**:
   * *Căn cứ số liệu*: Doanh thu sụt giảm mạnh nhất chuỗi, chỉ đạt ~61.5% kế hoạch; Tăng trưởng MoM âm (-38.2%).
   * *Đề xuất*: Rà soát lưu lượng khách vãng lai, triển khai chương trình kích cầu cuối tuần và bán chéo tại quầy thu ngân.
2. **Phúc An Nha Trang (PA_NT01)**:
   * *Căn cứ số liệu*: Tỷ lệ đổi trả hàng lên tới 8.6% (vượt xa benchmark chuỗi 2.2%), tập trung ở nhóm Điện gia dụng và Thời trang.
   * *Đề xuất*: Thanh tra quy trình bảo quản tại kho cửa hàng, siết chặt kiểm tra ngoại quan trước khi giao khách, đào tạo lại nhân viên tư vấn thông số kỹ thuật.
3. **Phúc An Gò Vấp (PA_HCM05)**:
   * *Căn cứ số liệu*: Doanh thu đạt khá nhưng Biên lợi nhuận gộp teo tóp chỉ còn 22.4% (trung bình chuỗi 35.8%) do doanh số bị lệch vào các mặt hàng khuyến mãi biên mỏng.
   * *Đề xuất*: Cơ cấu lại mặt bằng trưng bày, giảm tỷ trọng hàng giá rẻ, tập trung combo đẩy hàng biên lợi nhuận cao.

---

## 🚀 HƯỚNG DẪN KHỞI CHẠY HỆ THỐNG

### Cách 1: Chạy trực tiếp bằng tệp `run.bat`
Nhấp đúp chuột vào file **`run.bat`** trong thư mục dự án. Trình duyệt sẽ mở tại `http://localhost:8000`.

### Cách 2: Chạy bằng dòng lệnh Terminal
```bash
python server.py 8000
```
Sau đó truy cập: `http://localhost:8000` trên trình duyệt.

### Tính năng trên giao diện:
1. **Nút "Nạp Dữ Liệu Mẫu (18 Cửa hàng) & Chạy"**: Tự động nạp bộ dữ liệu thử nghiệm 25.000+ dòng của Công ty Phúc An và thực thi Bước 1 -> Bước 4 chỉ trong 1 giây.
2. **Hỗ trợ Tải Tệp / Link Google Sheets**: Người dùng có thể tải lên tệp CSV/Excel của riêng mình hoặc nhập Link Google Sheets công khai.
3. **Cổng kiểm duyệt Người - Máy (Human-in-the-loop)**: Bấm nút xác nhận Bước 5 và Bước 6 trực tiếp trên giao diện để chuyển tiếp quy trình.
4. **Tải Báo Cáo Excel & Tệp Audit Lineage Log**: Tự động kết xuất file Excel đầy đủ 4 sheet nghiệp vụ.

