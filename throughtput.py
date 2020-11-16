import matplotlib.pyplot as plt
from lib.PerformanceMeasures import PerformanceMeasures

throughtput = PerformanceMeasures().throughtput()

x = []
y = []

for i in throughtput:
    x.append(i[0])
    y.append(i[1])

plt.plot(x, y)
plt.xlabel('Time(seconds)')
plt.ylabel('Kbps')
plt.title('Average Throughtput')
plt.show()
