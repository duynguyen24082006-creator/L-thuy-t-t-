#!/usr/bin/env python3
"""Build the reviewed supplemental workbook from model.json + trajectory.csv.
Does not import calculate.py and never modifies the uploaded workbook.
"""
from pathlib import Path
import csv, json, math, re
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell as xc

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent
OUT.mkdir(parents=True,exist_ok=True)
model=json.loads((ROOT/'model.json').read_text(encoding='utf-8'))
p=model['parameters']; er=model['engine_rows']; road=model['road_rows']
with (ROOT/'trajectory.csv').open(newline='',encoding='utf-8') as f:
    reader=csv.DictReader(f); fields=reader.fieldnames; trajectory=list(reader)
path=OUT/'Nhom2_Dong_bo_va_tang_toc.xlsx'
w=xlsxwriter.Workbook(path)
w.set_properties({'title':'Nhóm 2 — Đồng bộ Excel, Word và tính tăng tốc',
 'subject':'Đầu vào theo Nhom2.xlsx; chuẩn hóa công thức mômen; tính bổ sung tăng tốc',
 'author':'Nhóm 2','comments':'Nguồn đầu vào và các giả thiết bổ sung được ghi trong Thong_so và Huong_dan.'})
w.set_calc_mode('auto')
navy='#17365D'; blue='#DCEAF7'; teal='#E2F0D9'; red='#9C0006'; grey='#666666'
fmt={
 'title':w.add_format({'bold':True,'font_size':17,'font_color':'white','bg_color':navy,'valign':'vcenter'}),
 'subtitle':w.add_format({'font_size':10,'font_color':grey,'text_wrap':True,'valign':'top'}),
 'note':w.add_format({'font_color':red,'bg_color':'#FFF2CC','text_wrap':True,'valign':'top','font_size':10}),
 'head':w.add_format({'bold':True,'font_color':'white','bg_color':navy,'text_wrap':True,'align':'center','valign':'vcenter','border':1}),
 'group':w.add_format({'bold':True,'font_color':navy,'bg_color':blue,'border':1,'align':'center'}),
 'text':w.add_format({'text_wrap':True,'valign':'top','font_size':10}),
 'num':w.add_format({'num_format':'#,##0.000000','font_size':10}),
 'small':w.add_format({'num_format':'0.000000000','font_size':10}),
 'int':w.add_format({'num_format':'0','font_size':10}),
 'input':w.add_format({'num_format':'0.#########','font_color':'#0057B7','bg_color':'#EEF6FF','font_size':10}),
 'derived':w.add_format({'num_format':'#,##0.000000','bg_color':'#F2F8EE','font_size':10}),
 'static':w.add_format({'num_format':'#,##0.000000','bg_color':'#FFF7E6','font_size':10}),
 'good':w.add_format({'bold':True,'font_color':'#006100','bg_color':teal,'num_format':'#,##0.000000'}),
 'link':w.add_format({'font_color':'blue','underline':True}),
}
sheets={name:w.add_worksheet(name) for name in ['Huong_dan','Thong_so','Dong_co','Van_toc_Pk_D','Can_chuyen_dong','Gia_toc','Tang_toc_chi_tiet','Tong_hop','Do_thi']}
for name,s in sheets.items():
    s.hide_gridlines(2);s.set_zoom(90);s.set_landscape();s.fit_to_pages(1,0)
    s.set_margins(.3,.3,.45,.45);s.set_header('&LNhóm 2 — Lý thuyết ô tô&R'+name)
    s.set_footer('&LTham khảo hướng dẫn trước khi thay số&P / &N')
    s.set_default_row(18)

def title(s,text,last=9,note=None):
    s.merge_range(0,0,0,last,text,fmt['title']);s.set_row(0,30)
    if note:s.merge_range(1,0,2,last,note,fmt['note']);s.set_row(1,24);s.set_row(2,24)

def header(s,row,cols):
    for c,value in enumerate(cols):s.write(row,c,value,fmt['head'])
    s.set_row(row,32)

# Excel defined names are case-insensitive. Python parameters g/G and nv/Nv
# must therefore have distinct Excel spellings before any formula is written.
parameter_aliases={'g':'p_gravity','G':'p_weight','nv':'p_rpm_vmax','Nv':'p_power_vmax'}
def parameter_name(key):
    return parameter_aliases.get(key,'p_'+key)

def form(s,row,col,formula,value,style='num'):
    formula=re.sub(r'\bp_(g|G|nv|Nv)\b',lambda match:parameter_name(match.group(1)),formula)
    s.write_formula(row,col,formula,fmt[style],value)

# Named parameters: numerical inputs retain source choices; derived scalars are formula cells.
labels={
'm0':('Khối lượng bản thân','kg','THÔNG SỐ CHO TRƯỚC!E9'),
'payload':('Tải hàng định mức','kg','THÔNG SỐ CHO TRƯỚC!E10'),
'persons':('Số người','người','THÔNG SỐ CHO TRƯỚC!E8'),
'person_mass':('Khối lượng mỗi người','kg','THÔNG SỐ CHO TRƯỚC!E21'),
'g':('Gia tốc trọng trường','m/s²','Hệ số 9,81 trong Excel nguồn'),
'front_fraction':('Tỷ lệ tải tĩnh cầu trước','—','THÔNG SỐ CHO TRƯỚC!E11'),
'rear_fraction':('Tỷ lệ tải tĩnh cầu sau','—','THÔNG SỐ CHO TRƯỚC!E12'),
'vmax_kmh':('Vận tốc cực đại yêu cầu','km/h','THÔNG SỐ CHO TRƯỚC!E13'),
'psi_max':('Hệ số cản đường lớn nhất','—','THÔNG SỐ CHO TRƯỚC!E14'),
'f0':('Hệ số cản lăn cơ sở','—','THÔNG SỐ CHO TRƯỚC!E23'),
 'threshold':('Ngưỡng ghép mô hình cản lăn','m/s','Theo hai miền công thức Excel/Word'),
'K':('Hệ số cản không khí','N·s²/m⁴','THÔNG SỐ CHO TRƯỚC!E25'),
'F':('Diện tích cản chính diện','m²','THÔNG SỐ CHO TRƯỚC!E26'),
'eta':('Hiệu suất truyền lực','—','THÔNG SỐ CHO TRƯỚC!E27'),
'lambda_v':('Tỷ lệ nv/nN','—','THÔNG SỐ CHO TRƯỚC!E28'),
'nv':('Vòng tua tại vmax','vòng/phút','THÔNG SỐ CHO TRƯỚC!E29; làm rõ ý nghĩa nv'),
'nmin':('Vòng tua nhỏ nhất khảo sát','vòng/phút','Miền bảng động cơ Excel nguồn'),
'a':('Hệ số Lây-đéc-man a','—','THÔNG SỐ CHO TRƯỚC!E30'),
'b':('Hệ số Lây-đéc-man b','—','THÔNG SỐ CHO TRƯỚC!E31'),
'c':('Hệ số Lây-đéc-man c','—','THÔNG SỐ CHO TRƯỚC!E32'),
 'tire_width_in':('Bề rộng danh nghĩa lốp','inch','TÍNH TOÁN !E12'),
'rim_in':('Đường kính vành','inch','TÍNH TOÁN !E13'),
'lambda_t':('Hệ số bán kính lăn','—','THÔNG SỐ CHO TRƯỚC!E33'),
'ip':('Tỷ số hộp số phụ ở cấp khảo sát','—','TÍNH TOÁN !E46'),
'ih1':('Tỷ số truyền số I','—','TÍNH TOÁN !E55'),
 'top':('Tỷ số truyền số V','—','TÍNH TOÁN !E61'),
'phi':('Hệ số bám','—','TÍNH TOÁN !E52'),
'mb':('Hệ số thay đổi tải trọng động','—','TÍNH TOÁN !B111; lấy 1 ở bước tĩnh'),
'nshift':('Vòng tua chuyển số I→IV','vòng/phút','GIẢ THIẾT BỔ SUNG: 2340'),
'shift_seconds':('Thời gian ngắt lực kéo mỗi lần','s','GIẢ THIẾT BỔ SUNG: 1 giây'),
'delta_coast':('Hệ số quán tính khi ngắt truyền lực','—','GIẢ THIẾT BỔ SUNG: 1,05'),
 'target_factor':('Tỷ lệ vận tốc kết thúc/vmax','—','GIẢ THIẾT BỔ SUNG: 0,95'),
'drive_intervals_per_smooth_segment':('Số khoảng mỗi miền trơn khi kéo','khoảng','THIẾT LẬP TÍCH PHÂN: 1600'),
'coast_dt':('Bước thời gian khi chuyển số','s','THIẾT LẬP TÍCH PHÂN: 0,01'),
'M':('Khối lượng toàn tải','kg','Tính từ đầu vào Excel'),
'G':('Trọng lượng toàn bộ','N','G=M·g'),
'G1':('Tải tĩnh cầu trước','N','G1=G·tỷ lệ trước'),
'G2':('Tải tĩnh cầu sau','N','G2=G·tỷ lệ sau'),
'W':('Nhân tố cản không khí KF','N·s²/m²','W=K·F'),
'vmax':('Vận tốc cực đại chính xác','m/s','95/3,6; không nhập lại 26,39'),
'nN':('Vòng tua công suất cực đại','vòng/phút','nv/lambda_v; giữ số chưa làm tròn'),
'r0':('Bán kính hình học xấp xỉ','m','(B+d/2)·0,0254'),
'rb':('Bán kính lăn giả thiết','m','lambda_t·r0; không phải bán kính tĩnh catalogue'),
'fvmax':('Hệ số cản lăn tại vmax','—','Theo luật ghép'),
'Pfmax':('Cản lăn tại vmax','N','G·f(vmax)'),
'Pwmax':('Cản không khí tại vmax','N','W·vmax²'),
'Pcmax':('Tổng cản tại vmax','N','Pf+Pw'),
'Nv':('Công suất động cơ tại vmax','kW','Pc·vmax/(1000·eta)'),
'Nmax':('Tham số công suất cực đại động cơ','kW','Nv/(aλ+bλ²−cλ³)'),
'nM':('Vòng tua mômen cực đại','vòng/phút','b·nN/(2c)'),
'i0':('Tỷ số truyền lực chính','—','Điều kiện đạt vmax ở số V'),
'q':('Công bội số I–IV','—','(ih1/1)^(1/3)'),
'iR':('Tỷ số truyền số lùi','—','GIẢ THIẾT BỔ SUNG: 1,2·ih1'),
'Pphi':('Giới hạn bám tĩnh','N','phi·mb·G2'),
'Mmax':('Mômen cực đại chuẩn hóa','N·m','Hệ số chuẩn 60000/(2π)'),
'ih_min':('Cận số I theo sức cản (bỏ Pw)','—','psi_max·G·rb/(Mmax·i0·ip·eta)'),
'ih_max':('Cận số I theo bám','—','Pphi·rb/(Mmax·i0·ip·eta)'),
'vstart':('Vận tốc bắt đầu tích phân','m/s','Số I, nmin; chưa xét trượt ly hợp'),
 'target':('Vận tốc kết thúc tích phân','m/s','0,95·vmax=90,25 km/h'),
'peak_v1':('Vận tốc tại mômen cực đại, số I','m/s','Kiểm tra số I'),
'peak_pk1':('Lực kéo cực đại số I','N','Mmax·it1·eta/rb'),
'peak_required':('Cản đường lớn nhất + cản khí động','N','psi_max·G+W·peak_v1²'),
'peak_margin':('Dự trữ lực tại điểm kiểm tra','N','peak_pk1−peak_required'),
'peak_pkR':('Lực kéo cực đại số lùi','N','Mmax·iR·i0·ip·eta/rb'),
'peak_D1':('D tại mômen cực đại, số I','—','(Pk−Pw)/G'),
'grade_at_torque_peak_percent':('Dốc tại điểm kiểm tra, không chuyển tải','%','Giải D=f0 cosα+sinα; i=tanα'),
 'time':('Thời gian tăng tốc của bộ dữ liệu hiện tại','s','KẾT QUẢ TĨNH: chạy lại calculate.py khi đổi số'),
 'distance':('Quãng đường tăng tốc của bộ dữ liệu hiện tại','m','KẾT QUẢ TĨNH: chạy lại calculate.py khi đổi số'),
}
derived={
'M':'=p_m0+p_persons*p_person_mass+p_payload','G':'=p_M*p_g',
'G1':'=p_G*p_front_fraction','G2':'=p_G*p_rear_fraction','W':'=p_K*p_F',
'vmax':'=p_vmax_kmh/3.6','nN':'=p_nv/p_lambda_v',
'r0':'=(p_tire_width_in+p_rim_in/2)*0.0254','rb':'=p_lambda_t*p_r0',
'fvmax':'=IF(p_vmax<=p_threshold,p_f0,p_f0*(1+p_vmax^2/1500))',
'Pfmax':'=p_G*p_fvmax','Pwmax':'=p_W*p_vmax^2','Pcmax':'=p_Pfmax+p_Pwmax',
'Nv':'=p_Pcmax*p_vmax/(1000*p_eta)',
'Nmax':'=p_Nv/(p_a*p_lambda_v+p_b*p_lambda_v^2-p_c*p_lambda_v^3)',
'nM':'=p_b*p_nN/(2*p_c)',
'i0':'=2*PI()*p_rb*p_nv/(60*p_top*p_ip*p_vmax)','q':'=p_ih1^(1/3)',
'iR':'=1.2*p_ih1','Pphi':'=p_phi*p_mb*p_G2',
'Mmax':'=60000/(2*PI())*p_Nmax/p_nN*(p_a+p_b*(p_nM/p_nN)-p_c*(p_nM/p_nN)^2)',
'ih_min':'=p_psi_max*p_G*p_rb/(p_Mmax*p_i0*p_ip*p_eta)',
'ih_max':'=p_Pphi*p_rb/(p_Mmax*p_i0*p_ip*p_eta)',
'vstart':'=2*PI()*p_nmin*p_rb/(60*p_i0*p_ih1*p_ip)',
'target':'=p_target_factor*p_vmax',
'peak_v1':'=2*PI()*p_nM*p_rb/(60*p_i0*p_ih1*p_ip)',
'peak_pk1':'=p_Mmax*p_i0*p_ih1*p_ip*p_eta/p_rb',
'peak_required':'=p_psi_max*p_G+p_W*p_peak_v1^2',
'peak_margin':'=p_peak_pk1-p_peak_required',
'peak_pkR':'=p_Mmax*p_iR*p_i0*p_ip*p_eta/p_rb',
'peak_D1':'=(p_peak_pk1-p_W*p_peak_v1^2)/p_G',
'grade_at_torque_peak_percent':'=100*TAN(ASIN(p_peak_D1/SQRT(1+p_f0^2))-ATAN(p_f0))',
}
s=sheets['Thong_so'];title(s,'THÔNG SỐ VÀ CƠ SỞ TÍNH TOÁN',5,
 'Ô xanh nhạt: đầu vào/giả thiết. Ô xanh lá: công thức có giá trị lưu sẵn. Ô vàng nhạt: kết quả tích phân tĩnh, không tự cập nhật khi đổi đầu vào. Không dùng bản đã sửa ô Excel để thay cho chạy lại bộ tính.')
s.set_column('A:A',29);s.set_column('B:B',41);s.set_column('C:C',21);s.set_column('D:D',15);s.set_column('E:F',35)
header(s,4,['Mã biến','Đại lượng','Giá trị','Đơn vị','Nguồn / cách tính','Phạm vi'])
scalar_keys=[key for key,value in p.items() if not isinstance(value,list)]
param_rows={}
for i,key in enumerate(scalar_keys,5):
    param_rows[key]=i;label,unit,source=labels.get(key,(key,'—','Từ model.json'))
    s.write(i,0,key,fmt['text']);s.write(i,1,label,fmt['text']);s.write(i,3,unit,fmt['text']);s.write(i,4,source,fmt['text']);s.set_row(i,32)
    w.define_name(parameter_name(key),"='Thong_so'!"+xc(i,2,True,True))
    if key in derived:form(s,i,2,derived[key],p[key],'derived');s.write(i,5,'Công thức; liên kết đầu vào',fmt['text'])
    else:s.write_number(i,2,p[key],fmt['static' if key in ['time','distance'] else 'input']);s.write(i,5,'Tích phân tĩnh' if key in ['time','distance'] else 'Đầu vào / giả thiết đã công bố',fmt['text'])
s.freeze_panes(5,2);s.autofilter(4,0,4+len(scalar_keys),5)
ghead=7+len(scalar_keys)
s.merge_range(ghead,0,ghead,7,'HỘP SỐ VÀ QUÁN TÍNH QUY ĐỔI — δh = 1,05 + 0,05(ih·ip)²',fmt['group'])
header(s,ghead+1,['Tay số','ih','ih·ip','it = ih·ip·i0','δh','v(nmin), km/h','v(nshift), km/h','v(nv), km/h'])
s.set_column('G:H',21)
for k,ih in enumerate(p['ih']):
    r=ghead+2+k;s.write_number(r,0,k+1,fmt['int'])
    hformula=['=p_ih1','=p_ih1/p_q','=p_ih1/p_q^2','=1','=p_top'][k]
    form(s,r,1,hformula,ih);form(s,r,2,'='+xc(r,1)+'*p_ip',ih*p['ip'])
    form(s,r,3,'='+xc(r,2)+'*p_i0',p['it'][k]);form(s,r,4,'=1.05+0.05*'+xc(r,2)+'^2',p['delta'][k])
    for name,col in [('h_',1),('it_',3),('delta_',4)]:w.define_name(name+str(k+1),"='Thong_so'!"+xc(r,col,True,True))
    for col,key in [(5,'nmin'),(6,'nshift'),(7,'nv')]:form(s,r,col,'=3.6*2*PI()*p_'+key+'*p_rb/(60*'+xc(r,3)+')',3.6*2*math.pi*p[key]*p['rb']/(60*p['it'][k]))
s.merge_range(ghead+8,0,ghead+10,7,'δh dùng tỷ số trước truyền lực chính ih·ip để kể sơ bộ hộp số phụ. Đây là giả thiết bổ sung của bản đồng bộ, không phải bảng có sẵn trong Excel gốc hoặc kết quả từ mômen quán tính cấu kiện. δcoast=1,05 khi ngắt truyền lực. Không trộn với δ=1,05+0,05ih² của bản cũ.',fmt['note'])

# Engine.
s=sheets['Dong_co'];title(s,'ĐẶC TÍNH NGOÀI ĐỘNG CƠ — CÔNG THỨC CHUẨN',5,
 'Ne tính kW; Me = 60000·Ne/(2πn), N·m. Điểm nM, nv và nN dùng số chưa làm tròn. Công thức có cache để đọc ngay cả khi ứng dụng chưa tính lại.')
s.set_column('A:E',20);s.set_column('F:F',43);header(s,4,['n, vòng/phút','x = n/nN','Ne, kW','Me, N·m','Nk, kW','Điểm / ý nghĩa'])
for i,d in enumerate(er,5):
    n=d['n'];key=next((key for key in ['nM','nv','nN'] if abs(n-p[key])<1e-7),None)
    if key:form(s,i,0,'=p_'+key,n)
    else:s.write_number(i,0,n,fmt['num'])
    rn=i+1;form(s,i,1,f'=A{rn}/p_nN',n/p['nN'])
    form(s,i,2,f'=p_Nmax*(p_a*B{rn}+p_b*B{rn}^2-p_c*B{rn}^3)',d['Ne'])
    form(s,i,3,f'=60000*C{rn}/(2*PI()*A{rn})',d['Me'])
    form(s,i,4,f'=p_eta*C{rn}',d['Nk'])
    s.write(i,5,{'nM':'Mômen cực đại giải tích','nv':'Điểm đạt 95 km/h ở số V','nN':'Vòng tua định mức chính xác'}.get(key,'Điểm khảo sát'),fmt['text'])
s.freeze_panes(5,1);s.autofilter(4,0,4+len(er),5)

# Per-gear v/Pk/D. Each gear has its own speed axis; no shared v on one n row.
s=sheets['Van_toc_Pk_D'];title(s,'VẬN TỐC, LỰC KÉO VÀ NHÂN TỐ ĐỘNG LỰC HỌC',25,
 'Mỗi dòng có cùng n, nhưng mỗi tay số có v riêng. Khi vẽ XY: số I dùng cột vI riêng, số II dùng vII riêng… Không dùng một cột v chung cho cả năm đường Pk hoặc D.')
s.set_column(0,0,17);s.set_column(1,25,16)
s.merge_range(3,0,4,0,'n, vòng/phút',fmt['head'])
for k in range(5):
    base=1+5*k;s.merge_range(3,base,3,base+4,f'SỐ {k+1}',fmt['group'])
    for j,label in enumerate(['v, m/s','v, km/h','Pk, N','D','Dφ tại v của số này']):s.write(4,base+j,label,fmt['head'])
for i,d in enumerate(er,5):
    rn=i+1;form(s,i,0,f"='Dong_co'!A{rn}",d['n'])
    for k,gear in enumerate(d['gears']):
        b=1+5*k;vcell=xc(i,b);pkcell=xc(i,b+2)
        form(s,i,b,f'=2*PI()*$A{rn}*p_rb/(60*it_{k+1})',gear['v'])
        form(s,i,b+1,'=3.6*'+vcell,gear['v_kmh'])
        form(s,i,b+2,f"='Dong_co'!D{rn}*it_{k+1}*p_eta/p_rb",gear['Pk'])
        form(s,i,b+3,f'=({pkcell}-p_W*{vcell}^2)/p_G',gear['D'])
        form(s,i,b+4,f'=(p_Pphi-p_W*{vcell}^2)/p_G',gear['Dphi'])
s.freeze_panes(5,1);s.set_row(4,38)

# Road forces including both sides of the empirical rolling resistance discontinuity.
s=sheets['Can_chuyen_dong'];title(s,'LỰC CẢN, CÔNG SUẤT CẢN VÀ GIỚI HẠN BÁM',11,
 'Hai dòng 22,200− và 22,200+ là giới hạn hai phía của mô hình f(v). Không nội suy cản lăn qua bước nhảy. vmax và vận tốc kết thúc dùng giá trị chính xác, chỉ làm tròn khi hiển thị.')
s.set_column('A:L',17);header(s,4,['Vị trí / nhãn','v, m/s','v, km/h','f(v)','Pf, N','Pw, N','Pc, N','Pφ, N','Dφ','Nf, kW','Nw, kW','Nc, kW'])
for r,d in enumerate(road,5):
    rn=r+1;lab=d['label'] or ('vmax' if abs(d['v']-p['vmax'])<1e-8 else 'v kết thúc' if abs(d['v']-p['target'])<1e-8 else '')
    s.write(r,0,lab,fmt['text'])
    if lab=='vmax':form(s,r,1,'=p_vmax',d['v'])
    elif lab=='v kết thúc':form(s,r,1,'=p_target',d['v'])
    elif d['label']:form(s,r,1,'=p_threshold',d['v'])
    else:s.write_number(r,1,d['v'],fmt['num'])
    form(s,r,2,f'=3.6*B{rn}',d['v']*3.6)
    ff=f'=p_f0*(1+B{rn}^2/1500)' if d['label']=='22,200+' else f'=IF(B{rn}<=p_threshold,p_f0,p_f0*(1+B{rn}^2/1500))'
    form(s,r,3,ff,d['f']);form(s,r,4,f'=p_G*D{rn}',d['Pf']);form(s,r,5,f'=p_W*B{rn}^2',d['Pw']);form(s,r,6,f'=E{rn}+F{rn}',d['Pc'])
    form(s,r,7,'=p_Pphi',d['Pphi']);form(s,r,8,f'=(H{rn}-F{rn})/p_G',d['Dphi'])
    form(s,r,9,f'=E{rn}*B{rn}/1000',d['Nf']);form(s,r,10,f'=F{rn}*B{rn}/1000',d['Nw']);form(s,r,11,f'=J{rn}+K{rn}',d['Nc'])
s.freeze_panes(5,2);s.autofilter(4,0,4+len(road),11)

# Acceleration tables. Infinity is textual, not a division-by-zero error.
s=sheets['Gia_toc'];title(s,'GIA TỐC VÀ GIA TỐC NGƯỢC THEO TỪNG TAY SỐ',9,
 'δh = 1,05 + 0,05(ih·ip)² là giả thiết bổ sung. Chỉ tích phân 1/j trong miền j>0; ∞ là điểm j=0, dấu — là j<0. Những điểm ngoài khả năng tăng tốc vẫn được giữ để đọc đặc tính.')
s.set_column('A:J',18)
for k in range(5):
    head=4+k*12;s.merge_range(head,0,head,9,f'SỐ {k+1}',fmt['group'])
    header(s,head+1,['n, vòng/phút','v, m/s','v, km/h','f(v)','δh','Pk, N','Pc, N','j, m/s²','1/j, s²/m','Miền'])
    for i,d in enumerate(er):
        r=head+2+i;rn=r+1;sr=6+i;gear=d['gears'][k];base=1+5*k
        form(s,r,0,f"='Dong_co'!A{sr}",d['n'])
        form(s,r,1,"='Van_toc_Pk_D'!"+xc(5+i,base),gear['v']);form(s,r,2,f'=3.6*B{rn}',gear['v_kmh'])
        form(s,r,3,f'=IF(B{rn}<=p_threshold,p_f0,p_f0*(1+B{rn}^2/1500))',gear['f'])
        form(s,r,4,f'=delta_{k+1}',p['delta'][k]);form(s,r,5,"='Van_toc_Pk_D'!"+xc(5+i,base+2),gear['Pk'])
        form(s,r,6,f'=p_G*D{rn}+p_W*B{rn}^2',gear['Pc'])
        jf=f'(MIN(F{rn},p_Pphi)-G{rn})/(p_M*E{rn})'
        j=gear['j'];form(s,r,7,f'=IF(ABS({jf})<1E-10,0,{jf})',0 if abs(j)<1e-10 else j)
        inv=gear['invj'] if gear['invj'] is not None else ('∞' if abs(j)<1e-10 else '—')
        form(s,r,8,f'=IF(H{rn}>1E-10,1/H{rn},IF(ABS(H{rn})<=1E-10,"∞","—"))',inv)
        form(s,r,9,f'=IF(H{rn}>1E-10,"j > 0",IF(ABS(H{rn})<=1E-10,"Cân bằng","j < 0"))','j > 0' if j>1e-10 else ('Cân bằng' if abs(j)<=1e-10 else 'j < 0'),'text')
s.freeze_panes(6,1)

# Dense trajectory is a frozen result of numerical integration, with all columns retained.
s=sheets['Tang_toc_chi_tiet'];title(s,f'DỮ LIỆU TĂNG TỐC CHI TIẾT — {len(trajectory):,} DÒNG THEO THỨ TỰ THỜI GIAN'.replace(',','.'),21,
 'DỮ LIỆU TĨNH từ trajectory.csv: đổi đầu vào phải chạy lại calculate.py rồi build_workbook.py. Không sắp xếp theo v. Khi chuyển số (coast), v giảm, t/S tăng; n, D và 1/j để trống vì không dùng đặc tính kéo.')
units={'n':'vòng/phút','Ne':'kW','Me':'N·m','v':'m/s','v_kmh':'km/h','Pk':'N','Pw':'N','Pf':'N','Pc':'N','f':'—','D':'—','Dphi':'—','j':'m/s²','invj':'s²/m','stage':'giai đoạn','kind':'drive/coast','gear':'tay số trước chuyển','side':'low/high','dt':'s','ds':'m','t':'s','S':'m'}
header(s,4,[key+'\n'+units[key] for key in fields]);s.set_row(4,40)
s.set_column(0,13,17);s.set_column(14,14,19);s.set_column(15,17,14);s.set_column(18,21,19)
textfields={'stage','kind','side'}
for r,d in enumerate(trajectory,5):
    for c,key in enumerate(fields):
        value=d[key]
        if value=='':continue
        if key in textfields:s.write_string(r,c,value,fmt['text'])
        else:s.write_number(r,c,float(value),fmt['int' if key=='gear' else 'num'])
s.freeze_panes(5,5);s.autofilter(4,0,4+len(trajectory),len(fields)-1)
s.conditional_format(5,12,4+len(trajectory),12,{'type':'cell','criteria':'<','value':0,'format':w.add_format({'font_color':red})})

# Summary aggregates the static trajectory with live, cached SUMIF/SUM formulae.
s=sheets['Tong_hop'];title(s,'TỔNG HỢP 9 PHA VÀ KIỂM TRA KẾT QUẢ',8,
 'Công thức SUMIF cộng dữ liệu chi tiết đã lưu; chúng không chạy lại mô phỏng khi đầu vào thay đổi. Kết quả là từ 4,251748 đến 90,25 km/h, gồm 4 lần chuyển số; chưa mô phỏng xuất phát bằng ly hợp trượt.')
s.set_column('A:A',24);s.set_column('B:C',15);s.set_column('D:I',20)
header(s,4,['Giai đoạn','Loại','Tay số','v đầu, m/s','v cuối, m/s','Δt, s','ΔS, m','t tích lũy, s','S tích lũy, m'])
last=5+len(trajectory);stagecol=xc(5,fields.index('stage'),True,True)+':'+xc(last-1,fields.index('stage'),True,True)
dtcol=xc(5,fields.index('dt'),True,True)+':'+xc(last-1,fields.index('dt'),True,True)
dscol=xc(5,fields.index('ds'),True,True)+':'+xc(last-1,fields.index('ds'),True,True)
for r,d in enumerate(model['phases'],5):
    rn=r+1;s.write(r,0,d['stage'],fmt['text']);s.write(r,1,d['kind'],fmt['text']);s.write_number(r,2,d['gear'],fmt['int']);s.write_number(r,3,d['v0'],fmt['static']);s.write_number(r,4,d['v1'],fmt['static'])
    form(s,r,5,f'=SUMIF(\'Tang_toc_chi_tiet\'!{stagecol},A{rn},\'Tang_toc_chi_tiet\'!{dtcol})',d['dt'])
    form(s,r,6,f'=SUMIF(\'Tang_toc_chi_tiet\'!{stagecol},A{rn},\'Tang_toc_chi_tiet\'!{dscol})',d['ds'])
    form(s,r,7,f'=SUM($F$6:F{rn})',d['t']);form(s,r,8,f'=SUM($G$6:G{rn})',d['S'])
s.write(15,0,'TỔNG',fmt['good']);form(s,15,5,'=SUM(F6:F14)',p['time'],'good');form(s,15,6,'=SUM(G6:G14)',p['distance'],'good')
s.merge_range(18,0,18,8,'THÔNG SỐ BỐN LẦN CHUYỂN SỐ — DỮ LIỆU TÍCH PHÂN ĐÃ LƯU',fmt['group'])
header(s,19,['Từ số','Sang số','v trước, m/s','v sau, m/s','Mất tốc độ, m/s','Δt, s','ΔS, m','n sau nối, v/ph','Ghi chú'])
for r,d in enumerate(model['shifts'],20):
    for c,key in enumerate(['from','to','v0','v1','dv','dt','ds','n_after']):s.write_number(r,c,d[key],fmt['int' if c<2 else 'static'])
    s.write(r,8,'Ngắt lực kéo; δcoast=1,05',fmt['text'])
s.merge_range(26,0,26,8,'KIỂM TRA VÀ SAI KHÁC DO CHUẨN HÓA',fmt['group'])
checks=[('Thời gian cuối CSV, s',p['time']),('Quãng đường cuối CSV, m',p['distance']),('Sai số thời gian khi gấp đôi lưới, s',model['checks']['grid_double_delta_t']),('Sai số quãng đường khi gấp đôi lưới, m',model['checks']['grid_double_delta_S']),('Dư công suất ở 95 km/h, kW',model['checks']['power_residual_kW']),('Dư lực ở 95 km/h, N',model['checks']['force_residual_N']),('Mômen nguồn cao hơn công thức chuẩn, %',100*model['checks']['source_torque_relative_difference'])]
for r,(label,val) in enumerate(checks,27):s.merge_range(r,0,r,4,label,fmt['text']);s.write_number(r,5,val,fmt['small'])
s.merge_range(36,0,36,8,'VÍ DỤ MỘT KHOẢNG HÌNH THANG (SỐ I) — KHÔNG THAY TOÀN BỘ TÍCH PHÂN',fmt['group'])
header(s,37,['vA, m/s','vB, m/s','jA, m/s²','jB, m/s²','Δt, s','ΔS, m','Ý nghĩa','',''])
ex=model['worked_example']
for c,key in enumerate(['vA','vB','jA','jB']):s.write_number(38,c,ex[key],fmt['static'])
form(s,38,4,'=0.5*(1/C39+1/D39)*(B39-A39)',ex['dt']);form(s,38,5,'=0.5*(A39/C39+B39/D39)*(B39-A39)',ex['ds'])
s.merge_range(38,6,39,8,'Cộng từng khoảng nhỏ trên từng miền trơn; chuyển số tích phân theo thời gian riêng.',fmt['text'])
s.freeze_panes(5,3)

# Native XY charts. Dense acceleration charts preserve every point in time order.
s=sheets['Do_thi'];title(s,'ĐỒ THỊ XY THAM KHẢO — KHÔNG CHÈN VÀO WORD',21,
 'Pk và D có trục v riêng cho từng tay số. t(v), S(v) dùng nguyên thứ tự 10.010 dòng, giữ các đoạn vận tốc giảm khi chuyển số. Các đường từ bảng 8 điểm là đường tham khảo; mô phỏng tăng tốc dùng lưới dày đã lưu.')
s.set_column('A:V',10)
colors=['#0072B2','#D55E00','#009E73','#CC79A7','#E69F00']
def chart(title_,ylabel):
    ch=w.add_chart({'type':'scatter','subtype':'straight'})
    ch.set_title({'name':title_});ch.set_x_axis({'name':'Vận tốc v (km/h)','min':0,'major_gridlines':{'visible':False}});ch.set_y_axis({'name':ylabel,'major_gridlines':{'visible':True,'line':{'color':'#E1E1E1'}}})
    ch.set_legend({'position':'bottom'});ch.set_size({'width':800,'height':430});return ch
for series_kind,title_,ylabel,pos,coloffset in [('Pk','Lực kéo theo từng tay số','Pk (N)','A5',2),('D','Nhân tố động lực học','D (không đơn vị)','L5',3)]:
    ch=chart(title_,ylabel)
    for k in range(5):
        base=1+5*k;ch.add_series({'name':f'Số {k+1}','categories':['Van_toc_Pk_D',5,base+1,12,base+1],'values':['Van_toc_Pk_D',5,base+coloffset,12,base+coloffset],'line':{'color':colors[k],'width':1.6},'marker':{'type':'none'}})
    if series_kind=='Pk':
        for label,col in [('Tổng cản Pc',6),('Giới hạn bám Pφ',7)]:ch.add_series({'name':label,'categories':['Can_chuyen_dong',5,2,14,2],'values':['Can_chuyen_dong',5,col,14,col],'line':{'color':'#333333','dash_type':'dash'},'marker':{'type':'none'}})
    else:ch.add_series({'name':'Giới hạn Dφ','categories':['Can_chuyen_dong',5,2,14,2],'values':['Can_chuyen_dong',5,8,14,8],'line':{'color':'#333333','dash_type':'dash'},'marker':{'type':'none'}})
    s.insert_chart(pos,ch)
for field,title_,ylabel,pos in [('t','Thời gian tăng tốc theo vận tốc','t (s)','A28'),('S','Quãng đường tăng tốc theo vận tốc','S (m)','L28')]:
    ch=chart(title_,ylabel);ch.add_series({'name':'Từ 4,252 đến 90,25 km/h','categories':['Tang_toc_chi_tiet',5,fields.index('v_kmh'),last-1,fields.index('v_kmh')],'values':['Tang_toc_chi_tiet',5,fields.index(field),last-1,fields.index(field)],'line':{'color':'#0072B2','width':1.5},'marker':{'type':'none'}});s.insert_chart(pos,ch)

# User instructions and provenance.
s=sheets['Huong_dan'];title(s,'HƯỚNG DẪN SỬ DỤNG BẢNG TÍNH NHÓM 2',7)
s.set_column('A:A',5);s.set_column('B:H',15)
notes=[
('Mục đích','Bản bổ sung dùng đầu vào của Nhom2.xlsx để đồng bộ số liệu, chuẩn hóa phép đổi mômen và tính thêm gia tốc, chuyển số, thời gian/quãng đường. Excel gốc không bị sửa hoặc xuất lại; ảnh trong ô/richData của tệp gốc được giữ nguyên trong tệp gốc.'),
('Kết quả đang lưu',f"M = {p['M']:.0f} kg; Nmax = {p['Nmax']:.6f} kW. Tăng tốc từ {p['vstart']*3.6:.6f} đến {p['target']*3.6:.2f} km/h: t = {p['time']:.9f} s; S = {p['distance']:.9f} m. Chưa tính xuất phát bằng ly hợp trượt; không gọi là 0–95 km/h."),
('Chuẩn hóa so với Excel gốc','Me = 60000·Ne/(2πn) thay hệ số 10000/1,047; mômen gốc cao hơn khoảng 0,0188683%. Dùng nN = 2600/0,9 và vmax = 95/3,6 chính xác, chỉ làm tròn hiển thị. Các lựa chọn 65 kg/người, f0=0,018, η=0,85, rb=0,3921125, ip=1,25 và các tỷ số hộp số được giữ.'),
('Giả thiết bổ sung','δh = 1,05 + 0,05(ih·ip)²; δcoast=1,05; chuyển số ở 2340 vòng/phút; ngắt lực kéo 1 giây/lần; 4 lần chuyển; điểm kết thúc 0,95vmax. Đây là giả thiết được nêu thêm vì Excel gốc chưa có δ, gia tốc hay tích phân tăng tốc. Chưa tối ưu lịch chuyển số.'),
('Những gì Excel tự cập nhật','Thong_so, Dong_co, Van_toc_Pk_D, Can_chuyen_dong và Gia_toc có công thức kèm cache. Khi Excel tính lại, các công thức có thể đổi theo đầu vào. Phần SUMIF trong Tong_hop chỉ cộng lại dữ liệu tĩnh của Tang_toc_chi_tiet.'),
('QUAN TRỌNG: khi thay đầu vào','Tang_toc_chi_tiet, các pha chuyển số, kiểm chứng hội tụ, ví dụ đã lưu và biểu đồ t/S KHÔNG tự chạy lại khi sửa ô Thong_so. Muốn có bộ kết quả nhất quán phải sửa đầu vào trong bộ tính Python rồi chạy calculate.py để sinh model.json + trajectory.csv, sau đó chạy build_workbook.py. Chỉ chạy build_workbook.py sẽ đóng gói lại kết quả hiện có, không tính mô hình mới.'),
('Lệnh chạy lại','Trong thư mục chứa calculate.py, build_workbook.py và dữ liệu: chạy python calculate.py, sau khi hoàn thành chạy python build_workbook.py. Nếu đã được cấp gói mã nguồn, đọc README của gói để cài thư viện. Script build_workbook.py dùng json, csv và xlsxwriter; không yêu cầu MATLAB.'),
('Đọc bảng theo vòng tua','Ở Van_toc_Pk_D, cùng một dòng là cùng vòng tua động cơ n. Năm tay số có năm vận tốc khác nhau. Khi vẽ Pk hoặc D dùng đúng cột v của tay số tương ứng. Không gán chung cột v số I cho các số khác.'),
('Cách vẽ thời gian trong Excel','Vào Tang_toc_chi_tiet. Chọn Insert → Scatter (XY) → Straight Lines. Add Series: X là cột v_kmh, Y là cột t, từ dòng dữ liệu đầu đến dòng cuối. Tên series tùy chọn. Không dùng Line chart theo danh mục và không sắp xếp lại các dòng theo vận tốc.'),
('Cách vẽ quãng đường trong Excel','Tạo Scatter (XY) tương tự; X = v_kmh, Y = S. Giữ toàn bộ thứ tự thời gian của CSV. Trong chuyển số, v giảm trong khi t/S tăng; đường đi lùi theo trục vận tốc là đúng. Không nối lại bằng thứ tự v tăng dần.'),
('Nhận diện các pha','kind=drive: đang kéo; kind=coast: ngắt lực kéo chuyển số. Khi coast, j âm; n, D, invj trống. gear ở coast là số trước khi chuyển, không có nghĩa đang truyền mômen qua số đó. dt/ds bằng 0 ở đầu pha hoặc hai phía ngưỡng không phải mất dữ liệu.'),
('Ngưỡng cản lăn','Mô hình giữ f=f0 với v≤22,2 m/s và f=f0(1+v²/1500) phía trên. Hai dòng low/high tại 22,2 biểu diễn hai giới hạn, không phải một biến đổi lực vật lý tức thời. Tích phân tách miền; không nội suy vượt qua bước nhảy.'),
('Gia tốc ngược','Chỉ dùng 1/j khi j>0. Dấu ∞ ở j=0 biểu thị giới hạn, không phải số để tính tổng. Dấu — khi j<0 nghĩa không dùng cho tích phân tăng tốc. Miền số V trên 95 km/h có thể j âm dù còn nằm trong dải vòng tua.'),
('Cách mở và xem','Mở bằng Excel hoặc phần mềm hỗ trợ .xlsx. Các ô công thức đã có giá trị cache, biểu đồ là biểu đồ Excel chỉnh sửa được. Nếu xem trên trình đọc không tự tính, vẫn đọc được kết quả bộ dữ liệu hiện tại. Không cần bật macro.'),
('Các sheet','Thong_so: nguồn và giả thiết; Dong_co: Ne/Me/Nk; Van_toc_Pk_D: 5 trục vận tốc; Can_chuyen_dong: lực/công suất cản; Gia_toc: j,1/j; Tang_toc_chi_tiet: toàn bộ 10.010 dòng; Tong_hop: 9 pha / 4 lần chuyển / kiểm tra; Do_thi: 4 đồ thị XY.'),
]
r=3
for heading,text in notes:
    s.merge_range(r,0,r,7,heading,fmt['group']);s.merge_range(r+1,0,r+3,7,text,fmt['note' if heading.startswith('QUAN TRỌNG') else 'text']);s.set_row(r+1,24);s.set_row(r+2,24);s.set_row(r+3,24);r+=5
for i,name in enumerate(list(sheets)[1:]):s.write_url(r+i,1,"internal:'"+name+"'!A1",fmt['link'],name)
s.freeze_panes(3,0);s.activate()
w.close()

# Verification against cached values and provenance expectations; no recalculation required.
import openpyxl
values=openpyxl.load_workbook(path,data_only=True)
forms=openpyxl.load_workbook(path,data_only=False)
assert math.isclose(values['Tong_hop']['F16'].value,p['time'],rel_tol=1e-12,abs_tol=1e-10)
assert math.isclose(values['Tong_hop']['G16'].value,p['distance'],rel_tol=1e-12,abs_tol=1e-9)
assert len(trajectory)>0
assert len({name.lower() for name in forms.defined_names})==len(forms.defined_names), 'Excel names must be unique ignoring case'
last_excel=5+len(trajectory)
assert abs(values['Tang_toc_chi_tiet'].cell(last_excel,fields.index('t')+1).value-p['time'])<1e-10
assert abs(values['Tang_toc_chi_tiet'].cell(last_excel,fields.index('S')+1).value-p['distance'])<1e-9
errors=[]
for sh in values:
    for row in sh:
        for cell in row:
            if cell.data_type=='e':errors.append((sh.title,cell.coordinate,cell.value))
assert not errors,errors
checks={'file':str(path),'bytes':path.stat().st_size,'sheets':values.sheetnames,'trajectory_rows':len(trajectory),'final_time_s':values['Tong_hop']['F16'].value,'final_distance_m':values['Tong_hop']['G16'].value,'formula_count':sum(c.data_type=='f' for sh in forms for row in sh for c in row),'cached_errors':errors,'charts':len(forms['Do_thi']._charts),'normalization_relative':model['checks']['source_torque_relative_difference'],'input_workbook_modified':False}
(ROOT/'workbook_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
