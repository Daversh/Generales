import matplotlib.pyplot as plt
import numpy as np
import control

T = 0.2
B = [0.0175, 0.871]
A = [-1.253, 0.253]
m = len(A)
den = [0]
den[0] = 1
den.extend(A)
H = control.tf(B, den, T)
print(H)
[Y, t1] = control.step_response(H)
plt.step(Y, t1)
plt.show()

sumB = np.sum(B)
q = [0]
q[0] = 1/((1 - A[0]) * sumB)
for it in range(0, m, 1):
    q.append((q[0]*(den[it+1]-den[it])) + (den[it]/sumB))
q.append(den[m]*((1/sumB)-q[0]))
print(q)

p = [0]
p[0] = q[0] * B[0]
for it in range(0, m-1, 1):
    p.append((q[0] * (B[it + 1] - B[it])) + (B[it] / sumB))
p.append(-B[m-1]*(q[0]-(1/sumB)))
print(p)

den1 = [0]
den1[0] = 1
den1.extend(p)
D = control.tf(q, den1, T)
print(D)

GW = H*D
print(GW)

Hz = control.feedback(GW, 1, sign=1)
print(Hz)
[Y1, t2] = control.step_response(Hz)
plt.step(Y1, t2)
plt.show()
