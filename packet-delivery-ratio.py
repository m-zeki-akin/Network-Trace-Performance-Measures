import matplotlib.pyplot as plt
from lib.PerformanceMeasures import PerformanceMeasures

packet_delivery_ratio = PerformanceMeasures().packet_delivery_ratio()

x = []
y = []

for i in packet_delivery_ratio:
    x.append(i[0])
    y.append(i[1])

plt.plot(x, y)
plt.xlabel('Time(seconds)')
plt.ylabel('Packet Delivery Ratio(Percent)')
plt.title('Total Packet Delivery Ratio')
plt.show()