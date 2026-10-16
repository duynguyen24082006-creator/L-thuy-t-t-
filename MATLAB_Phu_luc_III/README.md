# Mã MATLAB — Phụ lục III và hướng dẫn sử dụng

Nguồn: **Bài tập Lý thuyết ô tô**, PGS.TS Đào Mạnh Hùng – ThS Vũ Văn Tấn – KS Tạ Thị Thanh Huyền; bản PDF người dùng cung cấp mang tên “[studocu.com] - Ôn tập lý thuyết và bài tập ô tô GTVT - Môn học LTO.pdf”. Mã nằm ở **trang in 222–232, tương ứng trang PDF 223–233**. Đây là phụ lục của tài liệu mới tải lên, không phải mã trích từ sách Nguyễn Hữu Cẩn.

## 1. Chọn tệp

- `phu_luc_III_ban_trich.m`: bản trích để đối chiếu nguồn. Giữ công thức và số liệu của tài liệu; chỉ bỏ đầu/chân trang, nối các dòng bị ngắt do dàn trang, thêm chú thích nguồn và mốc trang. Cần **Symbolic Math Toolbox** vì dùng `syms`, `subs`.
- `phu_luc_III_khong_symbolic.m`: bản chỉnh kỹ thuật để sử dụng với MATLAB cơ bản, không cần Symbolic Math Toolbox. Nên bắt đầu bằng tệp này. Các thay đổi được liệt kê ở mục 7.
- `MATLAB_Phu_luc_III.zip`: gói gồm hai tệp `.m` và hướng dẫn này.

Các thông số mặc định vẫn là **ví dụ trong phụ lục**, không phải số liệu bài tập lớn Nhóm 2. Bản chỉnh kỹ thuật giữ phương pháp xấp xỉ của tài liệu, chưa thay bằng mô hình tính toán đầy đủ của nhóm.

## 2. Cách mở và chạy

1. Tải ZIP rồi giải nén vào một thư mục, ví dụ `D:\BTL_MATLAB`. Trên GitHub có thể mở từng tệp và chọn **Download raw file**. Nếu trình duyệt mở mã thành văn bản, lưu đúng đuôi `.m`, không phải `.m.txt`.
2. Mở MATLAB trên máy; đặt **Current Folder** vào thư mục vừa giải nén. Hoặc dùng MATLAB Online tại https://matlab.mathworks.com/ và tải hai tệp `.m` lên thư mục làm việc bằng nút Upload. Quyền sử dụng phụ thuộc tài khoản MATLAB của bạn.
3. Mở `phu_luc_III_khong_symbolic.m` trong Editor, chọn **Run**. Nếu được hỏi, chọn **Change Folder** để chuyển sang thư mục chứa tệp.
4. Nhập lần lượt bốn hộp thoại ở mục 3. Lần đầu nên giữ nguyên các số mẫu để hiểu cách hoạt động.
5. Chạy **toàn bộ tệp**. Các dấu `%%` chỉ đánh dấu trang nguồn; không chạy riêng từng section vì phần sau phụ thuộc biến đã tạo ở phần trước.

Cũng có thể gõ trong Command Window, khi đã ở đúng thư mục:

```matlab
phu_luc_III_khong_symbolic
```

Chương trình có `clear` và bản chỉnh có `close all`: khi chạy lại sẽ xóa biến trong workspace hiện tại và đóng các cửa sổ đồ thị đang mở. Hãy lưu phần làm việc cần giữ trước khi chạy.

## 3. Nhập dữ liệu

Dùng **dấu chấm thập phân**, ví dụ `0.85`; nhập các phần tử vector cách nhau bằng dấu cách. Với bản không Symbolic, không nhập dấu ngoặc vuông hoặc dấu phẩy quanh vector.

### Hộp 1 — động cơ

| Ô nhập | Ý nghĩa | Mẫu trong tài liệu |
|---|---|---:|
| Số vòng quay tối thiểu | `nemin`, vòng/phút | 500 |
| Số vòng quay n_e_M | `neM`, vòng/phút tại mômen cực đại khai báo | 1800 |
| Mômen M_e_max | `Memax`, N·m | 383 |
| Số vòng quay n_e_N | `neN`, vòng/phút tại công suất cực đại khai báo | 3200 |
| Công suất N_e_max | kW, không phải W hoặc mã lực | 114 |
| Số điểm n | Số mẫu trên đường đặc tính động cơ | 100 |

`neM` và `Memax` được dùng để tính các hệ số `Km`, `Kc`, `Md`; chương trình gốc **không dùng chúng để khớp đường đặc tính**. Đường đặc tính thực tế phụ thuộc `MeN`, `neN` và `a,b,c`. Vì vậy nhập một mômen cực đại không có nghĩa đồ thị chắc chắn đi qua điểm đó.

### Hộp 2 — hệ số Lây-đéc-man

Mẫu trong tài liệu: `a=1`, `b=1`, `c=1`. Với mô hình Diesel phun trực tiếp đã dùng trong BTL Nhóm 2: `a=0.5`, `b=1.5`, `c=1`. Không đổi hệ số chỉ để ép hình dạng đồ thị mong muốn.

### Hộp 3 — xe và truyền lực

| Ô nhập | Mẫu trong tài liệu | Đơn vị / cách hiểu |
|---|---|---|
| Tỷ số truyền hộp số | `5.38 3.028 1.70 1 0.722` | Đúng 5 phần tử theo thứ tự số 1 → số 5 |
| Tỷ số truyền cầu xe | `8.8` | Không thứ nguyên |
| Hiệu suất truyền lực | `0.85 0.85 0.85 0.85 0.85` | Đúng 5 phần tử, ứng với từng số; trong công thức đóng vai trò hiệu suất toàn bộ đường truyền lực |
| Bán kính tính toán | `0.55` | m |
| Chiều rộng B | `2.035` | m |
| Chiều cao H | `2.755` | m |
| Khối lượng toàn bộ | `6600` | kg |

**Lỗi nhãn trong bản gốc:** ô cuối ghi `G(N)` nhưng lệnh `G=9.81*...` nhân giá trị nhập với gia tốc trọng trường. Do đó phải nhập **khối lượng kg**, ví dụ 6600, không nhập trọng lượng 64746 N. Bản chỉnh đã sửa nhãn thành `m(kg)`.

Tài liệu dùng diện tích cản chính diện xấp xỉ `B*H`, không có hệ số hình dạng riêng trong biểu thức này. Số cao nhất mẫu là số truyền tăng `0.722`; số thứ tư là truyền thẳng `1`.

### Hộp 4 — điều kiện bên ngoài

| Ô nhập | Mẫu trong tài liệu | Đơn vị |
|---|---:|---|
| Hệ số cản không khí K | 0.45 | N·s²/m⁴ |
| Hệ số cản lăn fcl | 0.015 | Không thứ nguyên |

## 4. Mã thực hiện những phép tính nào?

Các dòng cốt lõi trong bản trích:

```matlab
MeN=30*1000*str2num(char(giatrinhap1(5)))/(neN*pi);
Me=MeN*(a+b*(n_e/neN)-c*((n_e/neN)^2)); % Nm
Ne=Me*n_e*pi/30; % W

V(i,j)=pi*Omega_e(j)*R_k/(30*I_tl(i));
P_k(i,j)=N_e(j)*Eta_tl(i)/V(i,j);
D(i,j)=(P_k(i,j)-K*B*H*(V(i,j))^2)/G;

Denta=1+0.05*(1+I_hs.*I_hs);
gt(i,j)=9.81*(D(i,j)-Sy)/Denta(i);
gtn(i,j)=1/gt(i,j);
```

- `MeN`: mômen tại tốc độ công suất cực đại, N·m.
- `M_e`, `N_e`: mômen N·m và công suất **W** trên lưới tốc độ quay. `Omega_e` trong mã thực tế lưu **vòng/phút**, dù tên gợi liên tưởng đến tốc độ góc rad/s.
- `V`: vận tốc m/s; khi vẽ nhân `3.6` để đổi sang km/h.
- `P_k`: lực kéo tại bánh xe, N.
- `D`: nhân tố động lực học, không thứ nguyên.
- `Denta`: hệ số kể đến quán tính các khối lượng quay.
- `gt`: gia tốc m/s²; `gtn`: nghịch đảo gia tốc s²/m.
- `polyfit(...,2)` và `polyval`: xấp xỉ bình phương tối thiểu đường `1/j` bằng đa thức bậc hai; không phải phép nội suy đảm bảo đi qua mọi điểm dữ liệu.
- Các vòng lặp `Dt`, `T` cộng dồn tích phân hình thang để tính thời gian; `D_t`, `S` tính quãng đường từ vận tốc và bước thời gian. Có cộng thời gian/quãng đường trong quá trình chuyển số theo công thức xấp xỉ của phụ lục.

## 5. Đọc và lưu kết quả

Chương trình tạo **6 cửa sổ hình**, theo thứ tự:

1. Đặc tính ngoài động cơ.
2. Nhân tố động lực học theo vận tốc.
3. Lực kéo ở năm số truyền.
4. Thời gian tăng tốc.
5. Quãng đường tăng tốc.
6. Gia tốc.

Trong hình động cơ, tác giả vẽ `200*M_e` và `N_e` (W) trên cùng trục. **200 chỉ là hệ số phóng đại để trình bày**, không phải đổi đơn vị mômen. Khi đọc đường mômen phải chia tung độ tương ứng cho 200.

Hình có tên “cân bằng lực kéo” của mã gốc thực tế chỉ vẽ năm đường lực kéo; biến tổng cản `Ptc` được tính nhưng **chưa được đưa vào lệnh plot**. Mã cũng chưa tạo hình cân bằng công suất hoặc hình gia tốc ngược riêng. Sáu hình này không đủ toàn bộ tám hình yêu cầu trong BTL Nhóm 2.

Trong Workspace, nhấp đúp vào `V`, `P_k`, `D`, `gt`, `Ttt`, `Stt` để xem bảng. Với các ma trận đầu, hàng là tay số và cột là mẫu tốc độ động cơ. Vận tốc của cùng một cột khác nhau giữa các hàng.

Lưu toàn bộ biến và hình sau khi chạy:

```matlab
save('ket_qua_phu_luc.mat');
figs = findall(groot,'Type','figure');
for k = 1:numel(figs)
    ten = sprintf('do_thi_%02d', get(figs(k),'Number'));
    savefig(figs(k), [ten '.fig']);
    print(figs(k), [ten '.png'], '-dpng', '-r300');
end
```

Lưu đường đặc tính động cơ ra CSV bằng MATLAB hiện đại:

```matlab
bang_dong_co = table(Omega_e(:), M_e(:), N_e(:)/1000, ...
    'VariableNames', {'n_vong_phut','M_Nm','N_kW'});
writetable(bang_dong_co,'dac_tinh_dong_co.csv');
```

## 6. Những điểm cần xử lý trước khi áp dụng cho BTL Nhóm 2

1. **Không thay số rồi mặc nhiên coi kết quả trùng thuyết minh.** Hai mô hình đang khác quy luật cản lăn, cách chuyển số, giới hạn vận tốc và cách tích phân.
2. Mã gốc cố định `linspace(nemin,3200,n)`. Bản chỉnh dùng `neN` thay 3200. Đây vẫn là chọn điểm kết thúc miền tính bằng `neN`, chưa phải một mô hình giới hạn tua độc lập.
3. Mã dùng `alpha=5*pi/180` và `fcl=fcl0+0.000007*Vgd.^2` khi tính `Ptc`, nhưng phần gia tốc lại dùng `Sy=fcl0`, tương ứng đường bằng và cản lăn hằng số. Đổi riêng `alpha` sẽ **không** làm phần tính tăng tốc trở thành tính trên dốc.
4. Mã không kiểm tra lực kéo theo giới hạn bám; chưa xét tải động lên cầu chủ động. Không suy ra mọi lực kéo động cơ đều truyền được xuống đường.
5. Mã tính đến tốc độ động cơ cuối dải của từng số, không tự chọn chuyển số ở 2340 vòng/phút như BTL hiện tại và không tự dừng ở 90.25 km/h.
6. Chỉ được tích phân `1/j` trên miền có `j>0`; tại tốc độ cân bằng `j=0`, tích phân thời gian tới đúng tốc độ ấy có thể phân kỳ. Bản chỉnh sẽ dừng báo lỗi nếu lưới gia tốc có điểm không dương. Không sửa lỗi bằng `abs(j)` hoặc bỏ qua cảnh báo.
7. Thời gian bắt đầu tại vận tốc ứng với `nemin` ở số một, **không phải từ xe đứng yên**. Mô hình không mô phỏng ly hợp trượt khi khởi hành.
8. `n` điều khiển số mẫu động cơ, nhưng phần tích phân từng số vẫn dùng 100 điểm cố định. Tăng `n` không tự làm toàn bộ thuật toán hội tụ.
9. Khi đổi tỷ số truyền, phải kiểm tra tốc độ quay sau chuyển số vẫn nằm trong miền đặc tính; mã nguồn có thể ngoại suy đa thức ra ngoài miền đó.
10. Các hệ số xấp xỉ mất vận tốc `9.3` và quãng đường chuyển số `4.73` được giữ theo bản in. Chúng không tạo thành một mô hình giảm tốc hằng số hoàn toàn nhất quán (nếu dùng 9.3 thì hệ số nửa gia tốc phải là 4.65). Bản chỉnh không thay phần này bằng mô hình động lực học mới.

Các giá trị đối chiếu với BTL hiện tại, **không phải bộ nhập hoàn chỉnh bảo đảm chạy đúng BTL**:

| Đại lượng | BTL Nhóm 2 hiện tại |
|---|---:|
| m | 7690 kg |
| Nmax | 117.011912 kW |
| nN | 2600 vòng/phút |
| nmin | 800 vòng/phút |
| Mmax | 456.622229 N·m |
| nM | 1950 vòng/phút |
| a, b, c | 0.5; 1.5; 1 |
| ih | 7; 4.3035170707; 2.6457513111; 1.6265765617; 1 |
| i0 | 3.5836209239 |
| eta | 0.89 ở cả năm số |
| rk | 0.38592125 m |
| K | 0.65 N·s²/m⁴ |
| Diện tích F | 4.5 m²; mã phụ lục dùng B*H, không tự có F riêng |
| f0 | 0.015; BTL áp dụng thêm quy luật tốc độ cao |

Không tự gán chiều rộng/chiều cao thực của xe chỉ từ diện tích F=4.5 m².

## 7. Các thay đổi của bản không Symbolic

- Thay biểu thức `syms/subs` bằng phép tính vector số tương đương (`.^`, `.*`).
- Dùng `neN` thay hằng số 3200 trong lưới tốc độ quay.
- Sửa nhãn đầu vào khối lượng kg và hiệu suất toàn bộ truyền lực.
- Dùng `str2double` cho số đơn, `sscanf` cho vector; xử lý nút Cancel; kiểm tra miền thông số và đúng năm số truyền.
- Thống nhất `ts1=1.2 s` ở cả phần thời gian và quãng đường. Bản gốc dùng 1.2 s ở phần thời gian nhưng 1 s ở phần quãng đường.
- Kiểm tra gia tốc hữu hạn, dương trước khi nghịch đảo; kiểm tra giá trị đa thức xấp xỉ dương trên lưới tích phân. Những kiểm tra này không chứng minh độ chính xác của phép xấp xỉ bậc hai.
- In mômen cực đại khai báo và mômen lớn nhất trên lưới để người dùng thấy nếu chúng không khớp nhau; thêm `clc`, `close all`.

Không đổi các số mẫu, không tự đưa số liệu Nhóm 2 vào, không bổ sung mô hình bám hoặc thay thuật toán xấp xỉ của tài liệu.

## 8. Kiểm tra và xử lý lỗi

Đã đối chiếu văn bản trích với PDF, kiểm tra cú pháp bằng trình phân tích MATLAB và đối chiếu các phép tính số của bộ mặc định bằng Python. Môi trường thực hiện không có MATLAB/Octave nên **chưa chạy trực tiếp giao diện hộp thoại và đồ thị trong MATLAB**.

| Hiện tượng | Cách xử lý |
|---|---|
| Báo không nhận ra `syms` | Mở bản `phu_luc_III_khong_symbolic.m`, hoặc kiểm tra Symbolic Math Toolbox nếu dùng bản trích |
| Không tìm thấy tệp/lệnh | Đặt Current Folder đúng thư mục, kiểm tra đuôi `.m` |
| Báo cần đúng 5 tỷ số/hiệu suất | Nhập 5 số cách nhau bằng dấu cách, không có ngoặc hoặc dấu phẩy |
| Báo dữ liệu không hữu hạn | Dùng dấu chấm thập phân và không nhập đơn vị vào ô số |
| Báo gia tốc không dương | Bộ thông số vượt miền tăng tốc; phải xác định lại giới hạn vận tốc và cách tích phân |
| Chạy riêng một section báo thiếu biến | Chạy lại toàn bộ tệp bằng Run |

Nguồn gốc và các hạn chế được giữ rõ để phân biệt mã tham khảo với chương trình đã hiệu chỉnh cho một đề bài cụ thể.
