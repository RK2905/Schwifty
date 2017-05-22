clear all;
close all;
clc;
%% Characteristic Impedances %%
Z0 = 50;
Z01 = 64.9;
Z02 = 217.5;
Z03 = 70.3;
Z04 = Z02;
Z05 = Z01;
%% l is fixed, f is varying %%
f = [3:0.000001:3.06]*10^9;
l = 10;
c = 3*10^8;
for i=1:1:length(f)
  theta = 2*pi*f(i)*l/c;
  T1 = [1 0; j*(1/Z01)*tan(theta) 1];
  T2 = [cos(theta) j*Z02*sin(theta); j*(1/Z02)*sin(theta) cos(theta)];
  T3 = [1 0; j*(1/Z03)*tan(theta) 1];
  T4 = [cos(theta) j*Z04*sin(theta); j*(1/Z04)*sin(theta) cos(theta)];
  T5 = [1 0; j*(1/Z05)*tan(theta) 1];
  
  T=T1*T2*T3*T4*T5;
  
  A = T(1,1);
  B = T(1,2);
  C = T(2,1);
  D = T(2,2);
  
  S21(i) = 2/(A + B/Z0 + C*Z0 + D);
  S11(i) = (A + B/Z0 - C*Z0 - D)/(A + B/Z0 + C*Z0 + D);
  i = i+1;
end
subplot(2,1,1);
plot(f,abs(S11),'r-',f,abs(S21),'b-');
title('Magnitude Response');
xlabel('Freqency --->');
ylabel('Magnitude ---->');
subplot(2,1,2);
plot(f,angle(S11),'r',f,angle(S21),'b');
axis([f(1) f(length(f)) -pi pi]);
title('Phase Response');
xlabel('Freqency --->');
ylabel('Phase ---->');