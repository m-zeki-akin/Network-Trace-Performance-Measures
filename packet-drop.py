import matplotlib.pyplot as plt
from lib.PerformanceMeasures import PerformanceMeasures

packet_drop = PerformanceMeasures().packet_drop()

x = []
y = []

for i in packet_drop:
    x.append(i[0])
    y.append(i[1])

plt.plot(x, y)
plt.xlabel('Time(seconds)')
plt.ylabel('Packet Drop')
plt.title('Total Packet Drop')
plt.show()
