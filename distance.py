import math
import matplotlib.pyplot as plt
 
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
v = 331
p1 = Point2D(x=0, y=0.26)    # 점1
p2 = Point2D(x=-0.15, y=0)    # 점2
p3 = Point2D(x=0.15, y=0)    # 점3
m = Point2D(x=0.3, y=0.3)  # 타겟
 
Ad = math.sqrt((m.x-p1.x)**2 + (m.y-p1.y)**2)    
Bd = math.sqrt((m.x-p2.x)**2 + (m.y-p2.y)**2)
Cd = math.sqrt((m.x-p3.x)**2 + (m.y-p3.y)**2)

At = Ad / v
Bt = Bd / v
Ct = Cd / v

delay_A = At-Bt 
delay_B = At-Ct 
delay_C = Bt-Ct 


print('{0:.20f}'.format(delay_A))
print('{0:.20f}'.format(delay_B))
print('{0:.20f}'.format(delay_C))

x = [p1.x , p2.x, p3.x, m.x]
y = [p1.y , p2.y, p3.y, m.y]
plt.figure()
plt.scatter(x,y)
plt.xlabel('X-Axis')
plt.ylabel('Y-Axis')
plt.xlim([-1, 1])      # X축의 범위: [xmin, xmax]
plt.ylim([-1, 1])     # Y축의 범위: [ymin, ymax]
plt.show()
