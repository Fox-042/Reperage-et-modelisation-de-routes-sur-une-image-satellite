from matplotlib import pyplot as plt
import numpy as np
from decimal import Decimal as d
from scipy.interpolate import CubicSpline
import random

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




def differencie_points(points, dist_min):
    courbes = [[points[0]]]
    for p in points[1:]:
        indice = 0
        d_min = float('inf')
        for i, courbe in enumerate(courbes):
            y = abs(p[1] - courbe[-1][1])
            x = abs(p[0] - courbe[-1][0])
            dist=x+y
            if dist<d_min:
                d_min = dist
                indice = i
        if p[0]!=courbes[indice][-1][0]:
            if d_min < dist_min:
                courbes[indice].append(p)
            else:
                courbes.append([p])
        elif d_min>2*dist_min:
            courbes.append([p])
    return courbes

def filtre_courbes_concat (courbes, taille_min):
    res = []
    for c in courbes:
        if len(c)>taille_min:
            res+= c
    return res
    
                
def trace_courbes(courbes, marker = 'o'):
    plt.figure(figsize=(8, 6))
    
    for courbe in courbes:
        x = [p[0] for p in courbe]
        y = [p[1] for p in courbe]
        couleur = (random.random(), random.random(), random.random())  # couleur aléatoire
        plt.plot(x, y, marker=marker, linestyle='-', color=couleur)
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Tracé des courbes différenciées")
    plt.grid(True)
    plt.show()

def separe_euler(courbe):
    courbes = [[]]
    n = len(courbe)
    j = 0
    for i in range(n):
        if i != 0 and i !=n-1 :
            b_euler = (courbe[i][1] - courbe[i-1][1])/(courbe[i][0] - courbe[i-1][0])
            f_euler = (courbe[i+1][1] - courbe[i][1])/(courbe[i+1][0] - courbe[i][0])
            diff = abs(f_euler - b_euler)
            prod = f_euler * b_euler
            print(prod, diff)
            if diff < 30 and prod>-0.25:
                courbes[j].append(courbe[i])
                print(diff)
            else:
                courbes.append([]) 
                j+=1
                courbes[j].append(courbe[i])
    return courbes


"""diff_f = differencie_points(points)
diff_f = [f for f in diff_f if len(f)>16]

#print(len(diff_f))
courbes_derivables = []
for c in diff_f:
    d = separe_euler(c)
    for courbe in d:
        if (len(courbe)>18):
            courbes_derivables.append(courbe)
#print(courbes_derivables)
#trace_courbes(courbes_derivables)
interpole_par_splines(courbes_derivables)
#trace_courbes(diff_f)

#ON VEUT RECUPERER LES POINTS D'UNE IMAGE
"""