import matplotlib.pyplot as plt
import control

num = 1
den = [1, 1, 1.5]
H = control.tf(num, den)
print(H)
[Y, t1] = control.step_response(H)
print(control.step_info(H))
plt.plot(Y, t1)
plt.show()