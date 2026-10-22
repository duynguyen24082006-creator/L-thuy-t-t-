# Nhóm 2 — đồng bộ Word theo Excel và bổ sung tính tăng tốc

Bản hoàn thiện ngày **22/10/2026**, dựa trên hai tệp nhóm cung cấp: `BTL_Nhom_2_chuacodothi.docx` và `Nhom2.xlsx`. Tên thư mục giữ ngày bắt đầu xử lý 21/10. Đây là bộ kết quả mới dùng cho yêu cầu đồng bộ số liệu; các hồ sơ trước trong repository sử dụng giả thiết khác.

## Tải tệp

- [Word đã cập nhật công thức, bảng số liệu và giải thích tăng tốc](BTL_Nhom_2_Dong_bo_Excel_va_giai_thich_tang_toc.docx)
- [Excel bổ sung: lực kéo, nhân tố động lực học, gia tốc và tích phân tăng tốc](Nhom2_Dong_bo_va_tang_toc.xlsx)
- [Tải cả bộ ZIP](Nhom2_Word_Excel_va_ma_tinh.zip)
- [Mã tính và cách chạy lại](ma_nguon/README.md)

Mở tệp trên GitHub rồi chọn **Download raw file** (biểu tượng tải xuống). Gói ZIP gồm Word, Excel, hướng dẫn và mã tính; không kèm bản sao các tài liệu tham khảo.

## Nội dung đã chỉnh

Giữ bản Word nhóm tự chỉnh làm nền, gồm bìa, thông tin thành viên, đề bài và cách trình bày chính. Cập nhật các công thức và bảng theo bộ đầu vào Excel; bổ sung lại mục gia tốc và gia tốc ngược để đủ yêu cầu đề bài. Word **không chèn ảnh đồ thị**; tám khung đồ thị để trống. Bản xuất kiểm tra có 30 trang; số trang có thể đổi khi mở bằng phiên bản Word hoặc phông chữ khác. Sau khi thêm hình, cập nhật toàn bộ mục lục.

Excel nguồn không bị ghi đè. Tệp Excel mới có 9 trang tính, 854 công thức, bảng tăng tốc chi tiết 10.010 dòng và 4 biểu đồ XY chỉnh sửa được. Sheet `Huong_dan` giải thích từng phần và giới hạn tự cập nhật.

| Đại lượng | Giá trị dùng trong bản mới |
|---|---:|
| Khối lượng mỗi người | 65 kg, theo Excel |
| Khối lượng toàn tải | 7.680 kg |
| Trọng lượng toàn tải | 75.340,8 N |
| Hiệu suất truyền lực | 0,85 |
| Hệ số cản lăn cơ sở | 0,018 |
| Bán kính lăn tính toán | 0,3921125 m |
| Tỷ số truyền hộp số phụ | 1,25 |
| Tỷ số truyền lực chính | 4,045680187 |
| Các số tiến I–V | 5,5; 3,115839842; 1,765174168; 1; 0,8 |
| Công suất động cơ yêu cầu tại 95 km/h | 124,884975 kW |
| Tham số công suất chuẩn Nmax | 133,424118 kW |
| Mômen cực đại | 468,601661 N·m |
| Giới hạn bám tĩnh đang dùng | 39.553,92 N |

**Chuẩn hóa công thức mômen:** dùng `Me = [60000/(2π)] Ne/n`, với Ne tính bằng kW, n tính bằng vòng/phút. Excel nguồn dùng hệ số `10000/1,047`; hệ số nguồn lớn hơn hệ số chuẩn khoảng **0,0188683%**. Chênh lệch nhỏ này được nêu trong Word và Excel, không phải sao chép sai số. Các đầu vào khác được giữ theo lựa chọn của nhóm; dùng giá trị chưa làm tròn khi tính.

Đặc tính động cơ là mô hình tính toán trong miền 800 ≤ n ≤ nN, với nN = 2.600/0,9 = 2.888,888889 vòng/phút. Nmax lớn nhất trong miền này; nếu kéo dài đa thức ra ngoài miền, cực đại toán học không nằm tại n = nN. Chưa chọn hoặc xác nhận một mã động cơ thương mại.

## Đọc đúng các bảng lực kéo và nhân tố động lực học

Một dòng của bảng động cơ là **cùng vòng tua n**, nhưng năm tay số có **năm vận tốc xe khác nhau**:

`vk = 2π rb n / (60 i0 ip ihk)`

`Pk,k = Me i0 ip ihk ηt / rb`

`Dk = (Pk,k − KF vk²) / G`

Vì vậy, khi dựng Pk(v) hoặc D(v), mỗi tay số phải ghép với cột vận tốc của chính nó. Không dùng một vận tốc hoặc một lực cản không khí chung cho cả năm cột trên cùng dòng n. Muốn so các số ở cùng vận tốc xe, phải tính lại vòng tua tương ứng của từng số.

## Cách tính thời gian và quãng đường

Word trình bày chi tiết ở mục **3.4–3.5**, gồm công thức, ví dụ một khoảng nhỏ, cách xử lý chuyển số và bảng tổng hợp chín giai đoạn.

1. Tính gia tốc ở mỗi vận tốc và tay số: `j = [min(Pk, Pφ) − Gf(v) − KFv²] / (Mδ)`.
2. Trong một pha kéo có j > 0, dùng `dt = dv/j` và `dS = v dv/j`. Vì gia tốc thay đổi, phải tích phân; không dùng một gia tốc trung bình tùy ý cho toàn bộ hành trình.
3. Với hai điểm A, B gần nhau trong cùng tay số và cùng nhánh cản lăn, dùng hình thang:
   - `Δt ≈ (1/jA + 1/jB)(vB − vA)/2`.
   - `ΔS ≈ (vA/jA + vB/jB)(vB − vA)/2`.
4. Cộng dồn t và S theo thứ tự chuyển động. Vận tốc trong phép tính phải là **m/s**; chỉ đổi sang km/h khi hiển thị hoặc vẽ trục.
5. Trong lúc chuyển số, ngắt lực kéo và giải riêng `dv/dt = −Pc/(Mδcoast)`, `dS/dt = v`. Vận tốc giảm nhưng thời gian và quãng đường vẫn tăng. Vào số mới tại vận tốc sau ngắt; không đặt lại t, S về 0.

Bộ tính dùng 1.600 khoảng vận tốc cho mỗi đoạn trơn; chuyển số dùng Runge–Kutta bậc bốn với bước 0,01 s. Quy luật cản lăn của Excel có bước nhảy tại 22,2 m/s, nên tích phân được tách ở ngưỡng này. Hai trạng thái ở hai phía ngưỡng không làm phát sinh thêm thời gian hoặc quãng đường.

Các giả thiết bổ sung được ghi rõ vì Excel nguồn chưa cung cấp phần tăng tốc: `δk = 1,05 + 0,05(ihk ip)²`, `δcoast = 1,05`, chuyển số tại 2.340 vòng/phút, ngắt lực kéo 1 giây/lần. Hệ số quán tính này là xấp xỉ, không phải dữ liệu đo. Lịch chuyển số giữ theo Word, chưa tối ưu.

**Kết quả:** từ **4,251748 đến 90,25 km/h**, thời gian **104,015379 s**, quãng đường **1.933,367600 m**, gồm bốn lần chuyển số. Chưa tính giai đoạn khởi hành từ đứng yên bằng ly hợp trượt. Điểm cuối chọn 0,95vmax; tại đúng 95 km/h, j = 0 nên tích phân tới điểm cân bằng không cho thời gian hữu hạn trong mô hình này.

Để vẽ trong Excel, dùng **Scatter (XY) → Straight Lines**. Trong `Tang_toc_chi_tiet`, X là `v_kmh`, Y là `t` hoặc `S`. Giữ nguyên thứ tự dòng theo thời gian, **không sắp xếp lại theo vận tốc**: đoạn chuyển số phải lùi về phía trái trên trục vận tốc. Sheet `Do_thi` đã dựng sẵn các đường tham khảo.

## Khi thay dữ liệu

Các bảng động cơ, vận tốc, lực kéo, lực cản và gia tốc có công thức Excel. Riêng bảng tích phân chi tiết và các trạng thái chuyển số là kết quả đã tính bằng Python; **không tự chạy lại khi sửa ô đầu vào trong Excel**. Để cập nhật toàn bộ nhất quán, chỉnh bộ tham số trong `ma_nguon/calculate.py`, chạy bộ tính rồi tạo lại Excel theo hướng dẫn. Mã kèm không tự sửa Word; sau khi đổi bộ số liệu cần cập nhật thuyết minh tương ứng.

Đã đối chiếu các ô lực kéo, nhân tố động lực học và gia tốc bằng phép tính độc lập; kiểm tra cân bằng công suất tại 95 km/h. Kết quả tích phân thích nghi độc lập lệch khoảng 0,000006 s và 0,000142 m so với bảng hình thang/RK4, nhỏ hơn độ chính xác trình bày. Đây là kiểm chứng phép tính trong các giả thiết đang dùng, không phải kết quả thử nghiệm xe thực.
