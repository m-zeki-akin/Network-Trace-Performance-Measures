import matplotlib.pyplot as plt
from lib.PerformanceMeasures import PerformanceMeasures

end_to_end_delay = PerformanceMeasures().end_to_end_delay()

x = []
y = []

for i in end_to_end_delay:
    x.append(i[0])
    y.append(i[1])

plt.plot(x, y)
plt.xlabel('Time(seconds)')
plt.ylabel('End to End Delay(ms)')
plt.title('Average End to End Delay')
plt.show()
