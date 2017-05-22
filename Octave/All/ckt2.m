%%%% Microwave BPF %%%%
clear all;
close all;
clc;
%% Characteristic Impedance %%
Z0 = 50;
L1 = 127*10^(-9);
C1 = 0.199*10^(-12);
L2 = 0.726*10^(-9);
C2 = 34.91*10^(-12);
L3 = L1;
C3 = C1;
f=0.6*10^9:10^5:1.4*10^9;

for i=1:1:length(f)
  w = 2*pi*f(i);
  %% ABCD Matrix of individual elements %%
  T1 = [1 j*w*L1; 0 1];
  T2 = [1 1/(j*w*C1); 0 1];
  T3 = [1 0; 1/(j*w*L2) 1];
  T4 = [1 0; j*w*C2 1];
  T5 = [1 j*w*L3; 0 1];
  T6 = [1 1/(j*w*C3); 0 1];
  %% Cascading %%
  T = T1*T2*T3*T4*T5*T6;
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
plot(f,angle(S11),'r-',f,angle(S21),'b-');
axis([f(1) f(length(f)) -pi pi]);
title('Phase Response');
xlabel('Freqency --->');
ylabel('Phase ---->');