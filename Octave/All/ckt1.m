%%%% Microwave LPF %%%%
clear all;
close all;
clc;
%% Characteristic Impedance %%
Z0 = 50;
C1 = 0.984*10^(-12);
L2 = 6.438*10^(-9);
C3 = 3.183*10^(-12);
L4 = L2;
C5 = C1;
f=1:0.1*10^9:10*10^9;
for i=1:1:length(f)
  w = 2*pi*f(i);
  %% ABCD Matrix of individual elements %%
  T1 = [1 0; j*w*C1 1];
  T2 = [1 j*w*L2; 0 1];
  T3 = [1 0; j*w*C3 1];
  T4 = [1 j*w*L4; 0 1];
  T5 = [1 0; j*w*C5 1];
  %% Cascading %%
  T = T1*T2*T3*T4*T5;
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
plot(f,angle(S11),'r*',f,angle(S21),'bx');
axis([f(1) f(length(f)) -pi pi]);
title('Phase Response');
xlabel('Freqency --->');
ylabel('Phase ---->');