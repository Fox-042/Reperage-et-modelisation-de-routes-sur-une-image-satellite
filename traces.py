from matplotlib import pyplot as plt
import numpy as np
from decimal import Decimal as d
from scipy.interpolate import CubicSpline

def trace_points(ax1,points : list):
    liste_x = [(points[3:-3])[i][0] for i in range (len(points[3:-3]))]
    liste_y = [(points[3:-3])[i][1] for i in range (len(points[3:-3]))]
    ax1.scatter(*zip(*points[3:-3]), color="red", label="Data Points")  # Plot given points
    ax1.plot(liste_x, liste_y, color = "black")
    ax1.set_title('Tracé obtenu en reliant les points par segments')
    plt.show()


def lit_points(nom):
    res = []
    f=open(nom,'r')
    for i in f.readlines():
        a,b = i.split(",")
        res.append((int(a), int(b)))
    f.close()
    res.sort()
    #print(res)
    return res

points = lit_points("points_road01.txt")
"""x = np.array([i[0] for i in points])
y = np.array([i[1] for i in points])
plt.plot(x, y, 'o', label= 'points')
plt.show()"""

def L1(points: list, X:float):
    n = len(points)
    s = 0
    for j in range(n):        
        for i in range(n):
            if i!=j:
                t = [d(X)-d(points[i][0]) for i in range(n)]
                b = [d(points[j][0])-d(points[i][0]) for i in range(n)]
                T=np.prod(t)
                B=np.prod(b)
                p=T/B
        s += d(p)*d(points[j][1])
    return s

def L(points: list, X:float):
    n = len(points)
    s = 0
    for j in range(n):        
        t = [d(X)-d(points[i][0]) if i!=j else 1 for i in range(n)]
        b = [d(points[j][0])-d(points[i][0]) if i!=j else 1 for i in range(n)]
        T=np.prod(t)
        B=np.prod(b)
        p=T/B
        s += d(p)*d(points[j][1])
    return s

def genere_points_tchebythchev(a, b,n):
    pts_base = [np.cos(((2*k+1)/(2*n+2)) * np.pi) for k in range (n)]
    return [(a+b)/2 + ((b-a)/2)*xk for xk in pts_base]



def splines(points):
    plt.ylim(-200, 2000)
    points.sort()
    x = np.array([i[0] for i in points])
    y = np.array([i[1] for i in points])

    cs = CubicSpline(x, y)

    x_trace = np.linspace(0,1500,10000)
    y_trace = cs(x_trace)#yavait x_dense variable perdue? j'ai changé il peut y avoir une erreur

    plt.plot(x, y, 'o', label= 'points')
    plt.plot(x_trace, y_trace, label='splines cubiques')
    plt.legend()
    plt.title("Interpolation par splines cubiques")
    plt.grid(True)
    plt.show()

def interpole_par_splines(matrice_points, xmin = 0, xmax = 1400):
    for courbe in matrice_points:
        x = np.array([i[0] for i in courbe])
        y = np.array([i[1] for i in courbe])    

        cs = CubicSpline(x,y)
        x_trace = np.linspace(0,1500,10000)
        y_trace = cs(y)

        plt.plot(x,y)
    plt.title("Interpolation par splines cubiques")
    plt.grid(True)
    plt.show


def lagrange_final():
    x = np.linspace(-2.5, -0., 1000)  
    y = np.array([L(points, xi) for xi in x])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    trace_points(ax1, points)
    ax2.set_title('Tracé obtenu par interpolation de Lagrange')
    ax2.plot(x,y, color="blue", label="Lagrange Interpolation")
    ax2.scatter(*zip(*(points[3:-3])), color="red", label="Data Points")

    ax2.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

#ON VEUT RECUPERER LES POINTS D'UNE IMAGE
