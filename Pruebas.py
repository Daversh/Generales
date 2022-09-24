import matplotlib.pyplot as plt
import numpy as np
import control
T = 1
t = np.arange(0, 7, T)
n = 2
alpha = 1000
u = np.array([0, 1, 1, 1, 1, 1, 1])
y = np.array([0, 0.73, 1.26, 1.55, 1.73, 1.84, 1.91])
l = len(y) - 1
Theta = np.zeros(shape=(2*n,1))
L = np.zeros(shape=(2*n,1))
ThetaT = Theta.transpose()
P = alpha*np.identity(2*n)
Error = np.zeros(7-1)
#F = np.zeros(2*n)
for i in range(l):
    F = np.array([-y[i+1], -y[i], u[i+1], u[i]])
    Ft = F.transpose()
    Error[i] = y[i+1] - F.dot(Theta)
    L1= np.array([P.dot(F)/(1 + Ft.dot(P.dot(F)))])
    L = L1.transpose()
    ThetaT = ThetaT + Error[i]*L[:,0]
    P = np.identity(2*n) - L.dot(np.array([F.dot(P)]))
    Theta = ThetaT[0,:]
print(Theta)

plt.plot(t, y)
#Construcción de la función de transferencia
num = [Theta[2], Theta[3]]
den = [1, Theta[0], Theta[1]]
Hz = control.tf(num, den, T)
(y, t) = control.step_response(Hz, t)

plt.step(y, t)
plt.show()


print(Hz)