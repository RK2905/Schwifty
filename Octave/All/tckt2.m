close all;
clear all;
clc;

z0=50;
l1=127*10^(-9);
c1=0.199*10^(-12);
l2=0.726*10^(-9);
c2=34.91*10^(-12);
l3=l1;
c3=c1;

f=0.6*10^9:10^4:1.4*10^9;

for i=1:1:length(f)
  w=2*pi*f(i);
  
  t1=[1 j*w*l1;0 1];
  t2=[1 1/(j*w*c1); 0 1];
  t3=[1 0;1/(j*w*l2) 1];
  t4=[1 0;j*w*c2 1];
  t5=[1 j*w*l3;0 1];
  t6=[1 1/(j*w*c3);0 1];
  
  t=t1*t2*t3*t4*t5*t6;
  
  a=t(1,1);
  b=t(1,2);
  c=t(2,1);
  d=t(2,2);
  
  s21(i)=2/(a+ b/z0 + c*z0 +d);
  s11(i)=(a + b/z0 - c*z0 - d)/(a*b/z0+c*z0+d);
  i=i+1;
 end 

subplot(2,1,1);
plot(f,abs(s11),'r-',f,abs(s21),'b-');
title('Magnitude Response');
xlabel('Frequency-->');
ylabel('Magnitude-->');
subplot(2,1,2);
plot(f,angle(s11),'r-',f,angle(s21),'b-');
axis([f(1) f(length(f)) -pi pi]);
title('Phase Response');
xlabel('Frequency-->');
ylabel('Phase');
 
  
  
