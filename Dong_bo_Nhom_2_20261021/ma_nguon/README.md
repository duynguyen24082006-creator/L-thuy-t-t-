# Chạy lại bộ tính Nhóm 2

Không cần chạy mã để đọc Word và Excel đã cung cấp. Mã này phục vụ kiểm tra hoặc tính lại khi thay thông số; chưa tự cập nhật nội dung Word.

## Cài và chạy

Cài Python 3.10 trở lên. Mở Terminal/PowerShell tại thư mục `ma_nguon`, rồi chạy lần lượt:

```sh
python -m pip install -r requirements.txt
python calculate.py
python build_workbook.py
```

Trên máy dùng lệnh `python3`, thay `python` bằng `python3`. Không cần MATLAB hoặc macro Excel.

`calculate.py` sinh `model.json` và `trajectory.csv` trong thư mục mã. `build_workbook.py` đọc hai tệp này và tạo `Nhom2_Dong_bo_va_tang_toc.xlsx` ở thư mục phía trên. **Nếu đã có Excel cùng tên, chương trình ghi đè tệp đó**; sao lưu bản muốn giữ và đóng Excel trước khi chạy.

## Khi thay số

Chỉnh từ điển `P` đầu tệp `calculate.py`, sau đó chạy lại cả hai lệnh. Sửa ô đầu vào trong Excel không truyền dữ liệu ngược về Python. Các thông số dẫn xuất được tính tự động; giữ số chưa làm tròn khi tính.

Bộ tính dành cho phương án năm số tiến hiện tại: I–IV theo cấp số nhân, IV = 1, V chọn riêng; dùng lịch chuyển số cố định và ngắt lực kéo. Nếu thay số cấp, quy luật cản lăn, mô hình quán tính hoặc cách chuyển số thì phải sửa mô hình và kiểm tra lại, không chỉ đổi ô đầu vào. Không kéo dài miền đặc tính động cơ tùy ý ra ngoài 800 ≤ n ≤ nN.

Các giả thiết `delta`, `delta_coast`, `nshift`, thời gian chuyển số và mốc kết thúc được giải thích trong Word/README chính. Thay chúng làm thay đổi kết quả tăng tốc. Tệp Word và các đoạn mô tả số liệu cố định trong hướng dẫn không được tự viết lại khi chạy mã.

## Đối chiếu bộ số liệu phát hành

- Khối lượng: 7.680 kg.
- Điểm đầu/cuối: 4,251748251748 và 90,25 km/h.
- Thời gian: 104,015378946830 s.
- Quãng đường: 1.933,367599598443 m.
- Dữ liệu hành trình: 10.010 dòng, gồm năm pha kéo và bốn pha chuyển số.

Gia tốc, lực kéo và cản dùng SI. Tích phân hình thang tách miền cản lăn; chuyển số dùng RK4. Bộ tính còn tăng gấp đôi mật độ lưới để kiểm tra hội tụ. Excel xuất có giá trị công thức lưu sẵn và biểu đồ XY, đọc được trước khi phần mềm bảng tính tính lại.
