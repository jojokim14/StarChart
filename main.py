import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import csv
import math

def clamp(x):
    return max(0, min(x, 255))

def starcolor(si):
    #from stackoverflow
    #http://stackoverflow.com/questions/21977786/star-b-v-color-index-to-apparent-rgb-color
    t = 4600 * ((1 / ((0.92 * si) + 1.7)) + (1 / ((0.92 * si) + 0.62)))
    #conversion to si to kelvin
    x = 0
    y = 0
    if (t >= 1667 and t <= 4000):
        x = (((-0.2661239 * math.pow(10, 9)) / math.pow(t, 3)) +
             ((-0.2343580 * math.pow(10, 6)) / math.pow(t, 2)) + ((0.8776956 * math.pow(10, 3)) / t) + 0.179910)
    elif (t > 4000 and t <= 25000):
        x = (((-3.0258469 * math.pow(10, 9)) / math.pow(t, 3)) +
             ((2.1070379 * math.pow(10, 6)) / math.pow(t, 2)) + ((0.2226347 * math.pow(10, 3)) / t) + 0.240390)

    if (t >= 1667 and t <= 2222):
        y = -1.1063814 * math.pow(x, 3) - 1.34811020 * math.pow(x, 2) + 2.18555832 * x - 0.20219683
    elif (t > 2222 and t <= 4000):
        y = -0.9549476 * math.pow(x, 3) - 1.37418593 * math.pow(x, 2) + 2.09137015 * x - 0.16748867
    elif (t > 4000 and t <= 25000):
        y = 3.0817580 * math.pow(x, 3) - 5.87338670 * math.pow(x, 2) + 3.75112997 * x - 0.37001483
    #kevlin to xyZ
    Y = 1
    if (y == 0):
        Y = 0
    X = 0
    if (y != 0):
        X = (x*Y)/y
    Z = 0
    if (y != 0):
        Z = ((1 - x - y) * Y) / y
    # xyZ to XYZ
    r = 3.2406 * X - 1.5372 * Y - 0.4986 * Z
    g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
    b = 0.0557 * X - 0.2040 * Y + 1.0570 * Z
    rgb = [r,g,b]
    #XYZ to rgb
    a = 0.5
    srgb = []
    for u in rgb:
        if u <= 0.0031308:
            u = 12.92*u
        else:
            u = math.pow(u,1/2.4)
            u = (1+a)*u
            u = u-a
        u = u * 255.0
        srgb.append(u)
    rf = srgb[0]
    gf = srgb[1]
    bf = srgb[2]
    hexcode = "#{0:02x}{1:02x}{2:02x}".format(clamp(int(rf)), clamp(int(gf)), clamp(int(bf)))
    return hexcode
    #gamma correction
    #WORST METHOD EVERR

def trans(x, y, z):
    dr = math.pi*2
    x0 = x
    y0 = y*math.cos(dr*x)+z*math.sin(dr*x)
    z0 = z*math.cos(dr*x)-z*math.sin(dr*x)
    #yrotation
    x1 = x0 * math.cos(dr*y) - z0 * math.sin(dr*y)
    y1 = y0
    z1 = z0 * math.cos(dr*y) + x0 * math.sin(dr*y)
    #end
    x2 = x1 * math.cos(dr*z) + y1 * math.sin(dr*z)
    y2 = y1 * math.cos(dr*z) - x1 * math.sin(dr*z)
    return [x2, y2]

fig = plt.figure(figsize=(40,40))
fig2 = plt.figure(figsize=(40,40))
ax = fig.add_subplot(111, projection='3d', axisbg = 'k')
ax2 = fig2.add_subplot(111, axisbg = 'k')
starfile = open("../HYG-Database/hygdata_v3.csv", "r")
reader = csv.reader(starfile)
x = 0
for row in reader:
    xc = float(row[17])
    yc = float(row[18])
    zc = float(row[19])
    secdim = trans(xc, yc, zc)
    color = 'white'
    if row[16] == "":
        color = "White"
    else:
        color = starcolor(float(row[16]))
    ax.scatter(xc, yc, zc, c=color)
    ax2.scatter(secdim[0],secdim[1],c=color)
    """if row[6] != "":
            plt.annotate(
                row[6],
                xy=(secdim[0], secdim[1]), xytext=(-20, 20),
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))"""
    x += 1
    if (x%5000 == 0):
        print ("At number: "+str(x))
starfile.close()
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
fig.savefig("final_3d.png",bbox_inches='tight')
fig2.savefig("final_2d.png",bbox_inches='tight')
fig.show()
