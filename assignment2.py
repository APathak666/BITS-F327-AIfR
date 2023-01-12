import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.animation as an
import numpy as np
import math

length = 20
breadth = 10
theta = np.pi/4

dx = 0.1

deltaX = []
x_vals = []

deltaY = []
y_vals = []

deltaTheta = []
theta_vals = []

time = []

sensor_l1 = []
sensor_l2 = []

car_center = [0, 2]
car_x = car_center[0] - length/2*np.cos(np.pi/4) - breadth/2*np.sin(np.pi/4)
car_y = car_center[1] - length/2*np.sin(np.pi/4) + breadth/2*np.cos(np.pi/4)

fig = plt.figure()
plt.axis('equal')
plt.grid()
axis = plt.axes(xlim=(0, 200), ylim=(0, 200))
rect = plt.Rectangle((car_x, car_y), width=10, height=20, angle=math.degrees(theta)-90, facecolor='blue')
sensor = plt.Circle(car_center, 1, facecolor='red')

l1 = (np.random.randint(125, 200), np.random.randint(0, 125))
l2 = (np.random.randint(0, 75), np.random.randint(100, 200))

axis.add_patch(rect)
axis.add_patch(sensor)

coeffs = [2, 1, 0.001, 0.00001]    
x_arr = np.arange(0, 145)
y_arr = []
rects = [rect]
sensors = [sensor]

patches = sensors + rects

def calculateY(x, coeffs):
    """ Returns a polynomial for ``x`` values for the ``coeffs`` provided.

    The coefficients must be in ascending order (``x**0`` to ``x**o``).
    """
    order = len(coeffs)
    y = 0
    for i in range(order):
        y += coeffs[i]*x**i
    return y

def animate(i):
    global car_x, car_y, car_center, theta
    old_center_x = car_center[0]
    old_center_y = car_center[1]
    car_center[0] += dx
    car_center[1] = calculateY(car_center[0], coeffs)

    dy = (car_center[1]-old_center_y)
    theta_old = theta
    # print('old theta: ', theta_old)
    theta = math.atan(dy/dx)
    # print('new theta: ', theta)
    dtheta = theta - theta_old

    car_x_new = car_center[0] - length/2*np.cos(theta) - breadth/2*np.sin(theta)
    car_y_new = car_center[1] - length/2*np.sin(theta) + breadth/2*np.cos(theta)

    patches[1].set_angle(math.degrees(theta)-90)
    patches[1].set_xy([car_x_new, car_y_new])
    patches[0].center = (car_center[0] + length/2*np.cos(theta), car_center[1] + length/2*np.sin(theta))

    noise = np.random.normal(0, 5, 2)
    l1_dist = np.sqrt((patches[0].center[0] - l1[0])**2 + (patches[0].center[1] - l1[1])**2)
    l1_noise = l1_dist + noise[0]
    l2_dist = np.sqrt((patches[0].center[0] - l2[0])**2 + (patches[0].center[1] - l2[1])**2)
    l2_noise = l2_dist + noise[0]

    sensor_l1.append(l1_noise)
    sensor_l2.append(l2_noise)

    print('Noisy data... Dist from l1: ', l1_noise)
    print('Noisy data... Dist from l2: ', l2_noise)

    time.append(i+1)
    deltaX.append(dx)
    deltaY.append(dy)
    deltaTheta.append(dtheta)

    if i == 1449:
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig1 = plt.figure("Figure 1")
        plt.title("deltaX vs time")
        plt.plot(time, deltaX, color='black')
        fig2 = plt.figure("Figure 2")
        plt.title("deltaY vs time")
        plt.plot(time, deltaY, color='black')
        fig3 = plt.figure("Figure 3")
        plt.title("deltaTheta vs time")
        plt.plot(time, deltaTheta, color='black')

        plt.show()


    return patches

for x in x_arr:
    y = calculateY(x, coeffs)
    y_arr.append(y)

plt.xlim((0, 200))
plt.ylim((0, 200))

plt.plot(l1[0], l1[1], marker="o", markersize=5, markeredgecolor='black', markerfacecolor='black')
plt.plot(l2[0], l2[1], marker="o", markersize=5, markeredgecolor='black', markerfacecolor='black')
plt.plot(x_arr, y_arr, color='black')
# plt.axis('off')

animation = an.FuncAnimation(fig, animate, frames=1450, interval=0.1)
plt.show()
