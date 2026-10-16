% TRICH MA PHU LUC III: Chuong trinh Matlab tinh toan suc keo o to.
% Nguon: Bai tap Ly thuyet o to, Dao Manh Hung - Vu Van Tan - Ta Thi Thanh Huyen.
% Trang in 222-232; trang 223-233 trong PDF do nguoi dung cung cap.
% Ban trich: bo dau/cuoi trang, noi dong bi ngat khi dan trang PDF,
% them chu thich nguon va moc trang; giu cong thuc va so lieu cua tai lieu.
% CAN Symbolic Math Toolbox. Doc README.md truoc khi chay.
% LUU Y: o nhap G(N) trong ban goc thuc te can nhap KHOI LUONG (kg).
% Day la vi du cua tai lieu, KHONG phai bo so lieu BTL Nhom 2.

%% Trang in 222 | Trang PDF 223
format bank

clear
    %Nhap cac thong so dong co
    AddOpts.Resize='on';

AddOpts.WindowStyle='normal';
    AddOpts.Interpreter='tex';
    dongnhac1 = {'So vong quay toi thieu (vong/phut)','So vong quay n_e_M (vong/phut)','Momen M_e_m_a_x (Nm)','So vong quay n_e_N (vong/phut)','Cong suat N_e_m_a_x (Kw)','So diem lay so lieu: n'};
    tieude1='Nhap Thong so Dong co o to';
    sodong1 = 1;
    macdinh1={'500','1800','383','3200','114','100'};
    giatrinhap1=inputdlg(dongnhac1,tieude1,sodong1,macdinh1,AddOpts);
    nemin=str2num(char(giatrinhap1(1)));
    neM=str2num(char(giatrinhap1(2)));
    Memax=str2num(char(giatrinhap1(3)));
    neN=str2num(char(giatrinhap1(4)));
    MeN=30*1000*str2num(char(giatrinhap1(5)))/(neN*pi);
    n =str2num(char(giatrinhap1(6)));
    %----------------------------------------------------------------------
    Km=Memax/MeN;
    Kc=neN/neM;
    Md=(Km-1)*100;

    %======================================================================
    %Nhap cac he so a-b-c trong cong thuc Laydecman
    AddOpts.Resize='on';

AddOpts.WindowStyle='normal';
    AddOpts.Interpreter='tex';
    dongnhac3 = {'He so a','He so b','He so c'};
    tieude3='Nhap cac he so a-b-c trong cong thuc Laydecman';
    sodong3 = 1;
    macdinh3={'1','1','1'};
    giatrinhap3=inputdlg(dongnhac3,tieude3,sodong3,macdinh3,AddOpts);
    a=str2num(char(giatrinhap3(1)));
    b=str2num(char(giatrinhap3(2)));
    c=str2num(char(giatrinhap3(3)));
    %====================================================================
%     a=1;
%     b=1;

%% Trang in 223 | Trang PDF 224
%     c=1;
    %=====================================================
    % DUNG SYMBOLIC
    syms n_e

    Me=MeN*(a+b*(n_e/neN)-c*((n_e/neN)^2)); %Nm
    Ne=Me*n_e*pi/30;%W
    Omega_e = linspace(nemin,3200,n);
    M_e = subs(Me,Omega_e);
    N_e = subs(Ne,Omega_e);

    %=====================================================
    % Nhap cac thong so ket cau

AddOpts.Resize='on';

AddOpts.WindowStyle='normal';
    AddOpts.Interpreter='tex';
    dongnhac = {'Ma tran TY SO TRUYEN cua HS: i_h_s','Ty so truyen cau xe: i_0','Ma tran HIEU SUAT cua HS: eta_h_s','Ban kinh tinh toan: r_k (m)','Chieu rong Oto: B(m)','Chieu cao lon nhat Oto: H(m)','Trong luong Oto: G(N)'};
    tieude='Nhap Thong so cua o to';
    sodong = 1;
    macdinh={'5.38 3.028 1.70 1 0.722','8.8','0.85 0.85 0.85 0.85 0.85','0.55','2.035','2.755','6600'};
    giatrinhap=inputdlg(dongnhac,tieude,sodong,macdinh,AddOpts);
    I_hs=str2num(char(giatrinhap(1)));
    I_0=str2num(char(giatrinhap(2)));
    Eta_tl=str2num(char(giatrinhap(3)));
    R_k=str2num(char(giatrinhap(4)));

B=str2num(char(giatrinhap(5)));

H=str2num(char(giatrinhap(6)));

G=9.81*str2num(char(giatrinhap(7)));
    I_tl=I_hs*I_0;
   %===================================
    AddOpts.Resize='on';

AddOpts.WindowStyle='normal';
    AddOpts.Interpreter='tex';
    dongnhac2 = {'He so can khong khi: K(N.s^2/m^4)','He so can lan duong: fcl'};
    tieude2='Nhap Thong so cua dieu kien ben ngoai';
    sodong2 = 1;
    macdinh2={'0.45','0.015'};
     giatrinhap2=inputdlg(dongnhac2,tieude2,sodong2,macdinh2,AddOpts);
     K=str2num(char(giatrinhap2(1)));
     fcl0=str2num(char(giatrinhap2(2)));

%% Trang in 224 | Trang PDF 225
%=====================================================
 % Tinh cac gia tri VAN TOC va LUC KEO va NHAN TO DONG LUC HOC

 % Tinh VAN TOC va LUC KEO
 for i=1:5
   for j=1:n
        V(i,j)=pi*Omega_e(j)*R_k/(30*I_tl(i));
        P_k(i,j)=N_e(j)*Eta_tl(i)/V(i,j);


D(i,j)=(P_k(i,j)-K*B*H*(V(i,j))^2)/G;
   end
 end

% Tinh NHAN TO DONG LUC HOC



V1=V(1,:);
    P_k1=P_k(1,:);
    D1=D(1,:);


V2=V(2,:);
    P_k2=P_k(2,:);
    D2=D(2,:);



V3=V(3,:);

P_k3=P_k(3,:);
    D3=D(3,:);


V4=V(4,:);

P_k4=P_k(4,:);
    D4=D(4,:);


V5=V(5,:);

P_k5=P_k(5,:);
    D5=D(5,:);

 %=====================================================

 % DAC TINH NGOAI DONG CO
   Dth = figure;
   set(Dth,'Numbertitle','off');
   set(Dth,'Color',[0.4 0.6 0.8]);
   set(Dth,'Name','Dac tinh ngoai cua dong co');
 % Ve dac tinh ngoai cua dong co

%% Trang in 225 | Trang PDF 226
plot(Omega_e,M_e*200,Omega_e,N_e)
   grid on
   zoom on
   legend('Me','Ne')
   xlabel('ne(v/ph)')
   ylabel('200*Me(Nm); Ne(W)')
 %=====================================================
 % VE DAC TINH DLH
 dtdl = figure;
        set(dtdl,'Numbertitle','off');

    set(dtdl,'Color',[.4 .6 .8]);
        set(dtdl,'Name','DAC TINH DONG LUC HOC');
 %Ve Dac tinh DLH
   plot(3.6*V1,D1,3.6*V2,D2,3.6*V3,D3,3.6*V4,D4,3.6*V5,D5);
   grid on
   zoom on
   legend('Tay so 1','Tay so 2','Tay so 3','Tay so 4','Tay so 5')
   xlabel('Van toc Oto: V(Km/h)')
   ylabel('Nhan to dong luc hoc: D')
 %=====================================================
 %VE DAC TINH KEO
   dtk = figure;
   set(dtk,'Numbertitle','off');
   set(dtk,'Color',[0.4 0.6 0.8]);
   set(dtk,'Name','DO THI CAN BANG LUC KEO');
%TINH HE SO CAN
  % fcl0 = 0.015;
   alpha = 5*pi/180;
   Vgd=[0:0.05:V5(n)];
   fcl=fcl0 + 0.000007*Vgd.^2;
   Pf = fcl*G*cos(alpha);
   Pi = G*sin(alpha);
   Ptc = Pf+Pi+K*B*H*Vgd.^2;
% Ve Dac tinh keo
   plot(3.6*V1,P_k1,3.6*V2,P_k2,3.6*V3,P_k3,3.6*V4,P_k4,3.6*V5,P_k5)
   grid on
   zoom on
   legend('P_k_1','P_k_2','P_k_3','P_k_4','P_k_5')
   xlabel('Van toc Oto: V(km/h)')
   ylabel('Luc keo theo dong co: P_k(N)')
 %=====================================================
% THOI GIAN TANG TOC

%% Trang in 226 | Trang PDF 227
%Sy=0.02;
   Sy=fcl0;
   Denta=1+0.05*(1+I_hs.*I_hs);

   for i=1:5
      for j=1:n


gt(i,j)=9.81*(D(i,j)-Sy)/Denta(i);
      end
   end


   for i=1:5
      for j=1:n
         gtn(i,j)=1/gt(i,j);
      end
   end

   gtn1=gtn(1,:);
   gtn2=gtn(2,:);
   gtn3=gtn(3,:);
   gtn4=gtn(4,:);
   gtn5=gtn(5,:);
   % Noi suy cac duong gia toc nguoc
   bac=2;
   p1=polyfit(V1,gtn1,bac);
   p2=polyfit(V2,gtn2,bac);
   p3=polyfit(V3,gtn3,bac);
   p4=polyfit(V4,gtn4,bac);
   p5=polyfit(V5,gtn5,bac);

   %=====================================================
   v_1=linspace(V1(1),V1(n),100);
   gtn_1=polyval(p1,v_1);
   for k=1:99
      Dt1(1)=0;
      Dt1(k+1)=(v_1(k+1)-v_1(k))*(gtn_1(k)+gtn_1(k+1))/2;
   end
   for k=1:99
      T1(1)=Dt1(1);
      T1(k+1)=T1(k)+Dt1(k+1);
   end
   ts1 = 1.2; vs1 = 9.3*ts1*Sy;
   %=====================================================

%% Trang in 227 | Trang PDF 228
v_2=linspace(v_1(100)-vs1,V2(n),100);
   gtn_2=polyval(p2,v_2);
   for k=1:99
      Dt2(1)=0;
      Dt2(k+1)=(v_2(k+1)-v_2(k))*(gtn_2(k)+gtn_2(k+1))/2;
   end
   for k=1:99
      T2(1)=Dt2(1);
      T2(k+1)=T2(k)+Dt2(k+1);
   end
   T2=T2+T1(100)+ts1;
   ts2 = 1; vs2 = 9.3*ts2*Sy;
   %=====================================================
   v_3=linspace(v_2(100)-vs2,V3(n),100);
   gtn_3=polyval(p3,v_3);
   for k=1:99
      Dt3(1)=0;
      Dt3(k+1)=(v_3(k+1)-v_3(k))*(gtn_3(k)+gtn_3(k+1))/2;
   end
   for k=1:99
      T3(1)=Dt3(1);
      T3(k+1)=T3(k)+Dt3(k+1);
   end
   T3=T3+T2(100)+ts2;
   ts3 = 1; vs3 = 9.3*ts3*Sy;
   %=====================================================
   v_4=linspace(v_3(100)-vs3,V4(n),100);
   gtn_4=polyval(p4,v_4);
   for k=1:99
      Dt4(1)=0;
      Dt4(k+1)=(v_4(k+1)-v_4(k))*(gtn_4(k)+gtn_4(k+1))/2;
   end
   for k=1:99
      T4(1)=Dt4(1);
      T4(k+1)=T4(k)+Dt4(k+1);
   end
   T4=T4+T3(100)+ts3;
   ts4 = 1; vs4 = 9.3*ts4*Sy;
   %=====================================================
   v_5=linspace(v_4(100)-vs4,V5(n),100);
   gtn_5=polyval(p5,v_5);
   for k=1:99
      Dt5(1)=0;

%% Trang in 228 | Trang PDF 229
Dt5(k+1)=(v_5(k+1)-v_5(k))*(gtn_5(k)+gtn_5(k+1))/2;
   end
   for k=1:99
      T5(1)=Dt5(1);
      T5(k+1)=T5(k)+Dt5(k+1);
   end
   T5=T5+T4(100)+ts4;
   %!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   v=3.6*[v_1 v_2 v_3 v_4 v_5];
   Ttt=[T1 T2 T3 T4 T5];

   dtdl = figure;
   set(dtdl,'Numbertitle','off');
   set(dtdl,'Color',[0.4 0.6 0.8]);
   set(dtdl,'Name','DO THI THOI GIAN TANG TOC');

% Ve DO THI THOI GIAN TANG TOC
   plot(v,Ttt)
   grid on
   zoom on
   hold on
   xlabel('Van toc Oto: V(km/h)')
   ylabel('Thoi gian tang toc: t_t_t(s)')
%=====================================================
% QUANG DUONG TANG TOC

   for i=1:5
      for j=1:n
         gtn(i,j)=1/gt(i,j);
      end
   end

   gtn1=gtn(1,:);
   gtn2=gtn(2,:);
   gtn3=gtn(3,:);
   gtn4=gtn(4,:);
   gtn5=gtn(5,:);
   % Noi suy cac duong gia toc nguoc
   bac=2;
   p1=polyfit(V1,gtn1,bac);
   p2=polyfit(V2,gtn2,bac);
   p3=polyfit(V3,gtn3,bac);
   p4=polyfit(V4,gtn4,bac);

%% Trang in 229 | Trang PDF 230
p5=polyfit(V5,gtn5,bac);

%=====================================================
   v_1=linspace(V1(1),V1(n),100);
   gtn_1=polyval(p1,v_1);
   for k=1:99
      Dt1(1)=0;
      Dt1(k+1)=(v_1(k+1)-v_1(k))*(gtn_1(k)+gtn_1(k+1))/2;
   end
   for k=1:99
      T1(1)=Dt1(1);
      T1(k+1)=T1(k)+Dt1(k+1);
   end
   ts1 = 1; vs1 = 9.3*ts1*Sy;

   for k=1:99
      D_t1(1)=0;
      D_t1(k+1)=(T1(k+1)-T1(k))*(v_1(k)+v_1(k+1))/2;
   end
   for k=1:99
      S1(1)=D_t1(1);
      S1(k+1)=S1(k)+D_t1(k+1);
   end
   ss1 = (v_1(100)-4.73*ts1*Sy)*ts1;

   %=====================================================
   v_2=linspace(v_1(100)-vs1,V2(n),100);
   gtn_2=polyval(p2,v_2);
   for k=1:99
      Dt2(1)=0;
      Dt2(k+1)=(v_2(k+1)-v_2(k))*(gtn_2(k)+gtn_2(k+1))/2;
   end
   for k=1:99
      T2(1)=Dt2(1);
      T2(k+1)=T2(k)+Dt2(k+1);
   end
   T2=T2+T1(100)+ts1;
   ts2 = 1; vs2 = 9.3*ts2*Sy;

   for k=1:99
      D_t2(1)=0;
      D_t2(k+1)=(T2(k+1)-T2(k))*(v_2(k)+v_2(k+1))/2;
   end

%% Trang in 230 | Trang PDF 231
for k=1:99
      S2(1)=D_t2(1);
      S2(k+1)=S2(k)+D_t2(k+1);
   end
   S2 = S2+S1(100)+ss1;
   ss2 = (v_2(100)-4.73*ts2*Sy)*ts2;

   %=====================================================
   v_3=linspace(v_2(100)-vs2,V3(n),100);
   gtn_3=polyval(p3,v_3);
   for k=1:99
      Dt3(1)=0;
      Dt3(k+1)=(v_3(k+1)-v_3(k))*(gtn_3(k)+gtn_3(k+1))/2;
   end
   for k=1:99
      T3(1)=Dt3(1);
      T3(k+1)=T3(k)+Dt3(k+1);
   end
   T3=T3+T2(100)+ts2;
   ts3 = 1; vs3 = 9.3*ts3*Sy;

   for k=1:99
      D_t3(1)=0;
      D_t3(k+1)=(T3(k+1)-T3(k))*(v_3(k)+v_3(k+1))/2;
   end
   for k=1:99
      S3(1)=D_t3(1);
      S3(k+1)=S3(k)+D_t3(k+1);
   end
   S3 = S3+S2(100)+ss2;
   ss3 = (v_3(100)-4.73*ts3*Sy)*ts3;

   %=====================================================
   v_4=linspace(v_3(100)-vs3,V4(n),100);
   gtn_4=polyval(p4,v_4);
   for k=1:99
      Dt4(1)=0;
      Dt4(k+1)=(v_4(k+1)-v_4(k))*(gtn_4(k)+gtn_4(k+1))/2;
   end
   for k=1:99
      T4(1)=Dt4(1);
      T4(k+1)=T4(k)+Dt4(k+1);
   end

%% Trang in 231 | Trang PDF 232
T4=T4+T3(100)+ts3;
   ts4 = 1; vs4 = 9.3*ts4*Sy;

   for k=1:99
      D_t4(1)=0;
      D_t4(k+1)=(T4(k+1)-T4(k))*(v_4(k)+v_4(k+1))/2;
   end
   for k=1:99
      S4(1)=D_t4(1);
      S4(k+1)=S4(k)+D_t4(k+1);
   end
   S4 = S4+S3(100)+ss3;
   ss4 = (v_4(100)-4.73*ts4*Sy)*ts4;
   %=====================================================
   v_5=linspace(v_4(100)-vs4,V5(n),100);
   gtn_5=polyval(p5,v_5);
   for k=1:99
      Dt5(1)=0;
      Dt5(k+1)=(v_5(k+1)-v_5(k))*(gtn_5(k)+gtn_5(k+1))/2;
   end
   for k=1:99
      T5(1)=Dt5(1);
      T5(k+1)=T5(k)+Dt5(k+1);
   end
   T5=T5+T4(100)+ts4;

   for k=1:99
      D_t5(1)=0;
      D_t5(k+1)=(T5(k+1)-T5(k))*(v_5(k)+v_5(k+1))/2;
   end
   for k=1:99
      S5(1)=D_t5(1);
      S5(k+1)=S5(k)+D_t5(k+1);
   end
   S5 = S5+S4(100)+ss4;
   %!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   v=3.6*[v_1 v_2 v_3 v_4 v_5];
   T=[T1 T2 T3 T4 T5];
   Stt = [S1 S2 S3 S4 S5];

   dtdl = figure;
   set(dtdl,'Numbertitle','off');
   set(dtdl,'Color',[0.4 0.6 0.8]);

%% Trang in 232 | Trang PDF 233
set(dtdl,'Name','DO THI QUANG DUONG TANG TOC');

% Ve DO THI QUANG DUONG TANG TOC
   plot(v,Stt)
   grid on
   zoom on
   hold on
   xlabel('Van toc Oto: V(km/h)')
   ylabel('Quang duong tang toc: S_t_t(m)')
%=====================================================
% GIA TOC CUA XE

  % Sy = 0.02 He so can cua duong tinh ca he so can doc ;
  Sy=fcl0;
  Denta=1+0.05*(1+I_hs.^2);

   for i=1:5
       for j=1:n
           gt(i,j)=9.81*(D(i,j)-Sy)/Denta(i);
       end

end

   gt1=gt(1,:);
   gt2=gt(2,:);
   gt3=gt(3,:);
   gt4=gt(4,:);
   gt5=gt(5,:);

  dtdl = figure;
  set(dtdl,'Numbertitle','off');
  set(dtdl,'Color',[0.4 0.6 0.8]);
  set(dtdl,'Name','DO THI GIA TOC');

% Ve DO THI GA TOC
   plot(3.6*V1,gt1,3.6*V2,gt2,3.6*V3,gt3,3.6*V4,gt4,3.6*V5,gt5)
   grid on
   zoom on
   legend('Tay so 1','Tay so 2','Tay so 3','Tay so 4','Tay so 5')
   xlabel('Van toc Oto: V(Km/h)')
   ylabel('Gia toc Oto: j(m/s^2)')
 %===================THE END===============================
