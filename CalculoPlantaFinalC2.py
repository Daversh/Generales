import matplotlib.pyplot as plt
import numpy as np
import control
import math

T = 0.1
Th = T*math.sqrt(5)/2
t = np.arange(0, 20, T)

a = -2/3
b = ((2/3)*math.exp(-0.5*T)*math.cos(Th)) - (math.exp(-0.5*T)*2*math.sin(Th)*math.sqrt(5)/15)
c = -2*math.exp(-0.5*T)*math.cos(Th)
d = math.exp(-T)

A = 2/3
B = a+(c*2/3)
C = b-a+(2*d/3)
D = -b
E = c-1
F = d-c
G = -d

num = [A, B-A, C-B, D-C, -D]
den = [1, E, F, G, 0]
Hz = control.tf(num, den, T)
print(Hz)
(t1, y1) = control.step_response(Hz, t)
#plt.step(t1, y1)

Hs = control.tf([1], [1, 1, 1.5])
print(Hs)
(t2, y2) = control.step_response(Hs, t)
plt.plot(t2, y2)
print(control.pole(Hs))

HZ = Hs.sample(T, method='zoh')
print(HZ)
(t3, y3) = control.step_response(HZ, t)
plt.step(t3, y3)
plt.show()

