import matplotlib.pyplot as plt
from lib.PerformanceMeasures import PerformanceMeasures

congestion = PerformanceMeasures().congestion()

x = []
y1 = []
y2 = []

for i in congestion:
    x.append(i[0])
    y1.append(i[1])
    y2.append(i[2])

plt.plot(x, y1)
plt.plot(x, y2)
plt.xlabel('Time(seconds)')
plt.ylabel('Congestion Action')
plt.title('Total Congestion Action')
plt.legend(labels=('sent', 'received'), loc='lower right')
plt.show()
