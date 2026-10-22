# Excel tham khảo đã chỉnh — Nhóm 2

Bản ngày **22/10/2026**, dựa trên tệp `Nhom2.xlsx` mới nhất do nhóm cung cấp.

**[Tải Excel tham khảo đã chỉnh](Nhom2_Excel_tham_khao_da_chinh.xlsx)**

Mở liên kết rồi chọn **Download raw file** (biểu tượng tải xuống). Khi mở Excel, đọc sheet **HD_THAM_KHAO**, sau đó xem **TONG_HOP** và **DO_THI_MOI**.

## Những phần đã sửa và bổ sung

- Giữ hai sheet gốc, các hình công thức và bộ thông số mới của nhóm.
- Sửa hoành độ điểm cuối số V trên đồ thị nhân tố động lực học, gia tốc ngược và thời gian: điểm này ứng với **90,25 km/h**, không phải 95 km/h.
- Sửa tham chiếu điều kiện cản lăn ở `G161` cho nhất quán với vận tốc của điểm cuối số V.
- Ghi rõ bảng thời gian gốc là **thời gian riêng của từng tay số với lưới thưa**. Các kết quả này được giữ để đối chiếu cách tính hình thang và sai số bước chia.
- Thêm tích phân số V với lưới nhỏ và tách hai nhánh cản lăn ở **22,2 m/s**.
- Thêm bảng hành trình liên tục qua năm số, kể bốn lần ngắt lực kéo; thời gian và quãng đường được cộng dồn, vận tốc giảm trong chuyển số.
- Thêm bảng tổng hợp, đồ thị XY và hướng dẫn đọc công thức. Không cần macro hoặc MATLAB.

## Các sheet mới

| Sheet | Cách dùng |
|---|---|
| HD_THAM_KHAO | Hướng dẫn, các sửa đổi và giới hạn của mô hình |
| THAM_SO_MOI | Thông số liên kết về bản gốc và các giả thiết bổ sung |
| TICH_PHAN_SO_V | So sánh diện tích hình thang lưới thưa với tích phân đã chia nhỏ |
| HANH_TRINH | Công thức lực, gia tốc, thời gian và quãng đường ở từng bước của quá trình qua năm số |
| TONG_HOP | Kết quả theo pha kéo, chuyển số và toàn hành trình |
| DO_THI_MOI | Đồ thị tham khảo từ dữ liệu mới |

## Thông số và giả thiết dùng

Giữ đúng lựa chọn trong Excel mới: khối lượng 7.680 kg, f0 = 0,015, hiệu suất 0,85, số I = 6,5, số V truyền thẳng = 1, hộp số phụ = 1,25. Hệ số quán tính giữ theo công thức của nhóm: **δk = 1,05 + 0,05 ihk²**. Không tự thêm bình phương tỷ số truyền hộp số phụ vào công thức xấp xỉ này.

Giữ hệ số đổi mômen **10000/1,047** của file nguồn để đối chiếu trực tiếp. Hệ số này lớn hơn 60000/(2π) khoảng 0,0189%, nên tại đúng 95 km/h mô hình còn một gia tốc dương rất nhỏ; không tuyên bố cân bằng lực chính xác tại điểm đó.

Lịch chuyển số tham khảo chọn **2.600 vòng/phút** cho I→II, II→III, III→IV và IV→V, theo miền vòng tua trong bảng hiện tại. Mỗi lần ngắt lực kéo **1 giây**, dùng δcoast = 1,05. Đây là giả thiết bổ sung được ghi trong phần đầu vào, chưa phải lịch chuyển số tối ưu.

Tính từ số I tại 800 vòng/phút: **4,497041 km/h**; kết thúc ở **90,25 km/h**. Chưa tính khởi hành từ đứng yên bằng ly hợp trượt.

## Đọc kết quả đúng phạm vi

Toàn hành trình có thời gian khoảng **108,041 giây**, quãng đường khoảng **2.035,639 m** theo lưới tham khảo. Kiểm chứng tích phân thích nghi độc lập cho **108,041365 giây; 2.035,638388 m**; chênh lệch nhỏ là sai số số học của phương pháp chia lưới.

Riêng số V nếu tính từ 800 đến 2.470 vòng/phút, kết quả khoảng **118,688 giây**, so với **129,635 giây** trên lưới thưa của bảng gốc. Đây là bài tính riêng một số từ vận tốc thấp, **không phải** thời gian thực tế xe chạy ở số V sau khi đã tăng tốc qua bốn số trước. Vì vậy không cộng năm tổng thời gian riêng ở dòng 194 của sheet gốc để tính thời gian toàn xe.

Trong `HANH_TRINH`, dt = dv/j và dS = v dv/j chỉ áp dụng cho pha kéo có j > 0. Trong chuyển số, dùng tích phân theo thời gian của dv/dt = −Pc/(Mδcoast) và dS/dt = v. Các dòng đầu pha hoặc hai phía ngưỡng có thể có cùng t, S, v nhưng gia tốc khác; không cộng thêm thời gian cho việc đổi trạng thái.

Đồ thị dùng **Scatter (XY)**. Giữ thứ tự dòng theo thời gian, không sắp xếp toàn bộ dữ liệu theo vận tốc. Trong chuyển số, đường t(v) và S(v) phải đi lên đồng thời lùi về phía trái.

## Khi chỉnh đầu vào

Các sheet mới có công thức Excel và giá trị lưu sẵn. Các thông số liên kết cần sửa tại ô nguồn; các giả thiết bổ sung sửa ở phần đầu vào được đánh dấu. Đọc kiểm tra phạm vi áp dụng trong `TONG_HOP`: bố trí lưới dành cho phương án năm số hiện tại, các pha I–IV nằm dưới ngưỡng 22,2 m/s và pha số V đi qua ngưỡng. Nếu đổi tham số làm thay đổi cấu trúc phân miền này, cần chia lại miền tích phân.

Bản Excel này dùng phương án mới **f0 = 0,015, số V = 1**, khác bản Word đã phát hành trước đó theo **f0 = 0,018, số V = 0,8**. Nếu dùng bộ tính mới trong bài nộp, cần đồng bộ lại thuyết minh Word; không ghép hai bộ kết quả.
