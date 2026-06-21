from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline #utilisé avant que je ne code ma propre version
import random
from math import sqrt


def trace_points(ax1,points : list):
    ax1.set_ylim(0,3)
    
    liste_x = [points[i][0] for i in range (len(points))]
    liste_y = [points[i][1] for i in range (len(points))]
    ax1.scatter(*zip(*points), color="red", label="Data Points")  # Plot given points
    ax1.plot(liste_x, liste_y, color = "black")
    ax1.set_title('Tracé obtenu en reliant les points par segments')
    


#*****************Tests du début; je n'avais pas encore mon propre code de splines cubiques*******************

points_test = [(0.00428,1.8274),(-0.4,1.8),(-0.63046,2.40734),(-0.8348,0.77841),(-1.20369,0.67881),
               (-1.40584,0.65775),(-1.60777,0.67993),(-1.81702,0.76222),
 (-1.99101,0.88918),(-2.1744,1.11724),(-2.32722,1.39938),(-2.40481,1.69798),(-2.46902,2.20356),
 (-2.83352,2.12509),(-3.17796,2.04253),(-3.60058,1.90563)
]




def splines(points):
    plt.ylim(0,3)
    points.sort()
    x = np.array([i[0] for i in points])
    y = np.array([i[1] for i in points])

    cs = CubicSpline(x, y)

    x_trace = np.linspace(-3.7,0.1,1000)
    y_trace = cs(x_trace)

    plt.plot(x, y, 'o')
    plt.plot(x_trace, y_trace)
    plt.legend()
    plt.title("Interpolation par splines cubiques")
    plt.grid(True)
    plt.show()



def Lagrange(points: list, X:float):
    n = len(points)
    s = 0
    for j in range(n):        
        t = [X-points[i][0]  if i!=j else 1 for i in range(n)]
        b = [points[j][0] -points[i][0] if i!=j else 1 for i in range(n)]
        T=np.prod(t)
        B=np.prod(b)
        p=T/B
        s += p*points[j][1]
    return s

def lagrange_final(points):
    x = np.linspace(-3.7, +0.1, 1000)  
    y = np.array([Lagrange(points, xi) for xi in x])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    trace_points(ax1, points)
    ax2.set_ylim(0,3)
    ax2.set_title('Tracé obtenu par interpolation de Lagrange')
    ax2.plot(x,y, color="blue", label="Lagrange Interpolation")
    ax2.scatter([p[0] for p in points], [p[1] for p in points], color="red", label="Data Points")

    ax2.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()
    

#******************************************************************

def lit_points(nom):
    f = open(nom)
    res = []
    for l in f.readlines():
        x,y = l.split(',')
        res.append((int(x),int(y)))
    return res

def differencie_points(points, D):
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
            if d_min < D:
                courbes[indice].append(p)
            else:
                courbes.append([p])
        elif d_min>2*D:
            courbes.append([p])
    return courbes

def trie_recolle(courbes,D):
    res = []
    for courbe in courbes:

        mode = ""
        d_min = float('inf')
        j=0
        for i, f in enumerate(res):
            #print(f)
            y_f = abs(f[0][1] - courbe[-1][1])
            x_f = abs(f[0][0] - courbe[-1][0])
            dist_f=x_f+y_f
            if dist_f<d_min:
                d_min = dist_f
                j = i
                mode = "fdcf"
            y_d = abs(f[-1][1] - courbe[0][1])
            x_d = abs(f[-1][0] - courbe[0][0])
            dist_d=x_d+y_d
            if dist_d<d_min:
                d_min = dist_d
                j = i
                mode = "ffcd"
            y_gg = abs(f[0][1] - courbe[0][1])
            x_gg = abs(f[0][0] - courbe[0][0])
            dist_gg = x_gg + y_gg

            if dist_gg < d_min:
                d_min = dist_gg
                j = i
                mode = "fdcd"

            y_dd = abs(f[-1][1] - courbe[-1][1])
            x_dd = abs(f[-1][0] - courbe[-1][0])
            dist_dd = x_dd + y_dd

            if dist_dd < d_min:
                d_min = dist_dd
                j = i
                mode = "ffcf"
        if d_min<D:
            if mode == "fdcf":
                res[j] = courbe + res[j]

            elif mode == "ffcd":
                res[j] = res[j] + courbe

            elif mode == "fdcd":
                res[j] = courbe[::-1] + res[j]

            elif mode == "ffcf":
                res[j] = res[j] + courbe[::-1]
        else:
            res.append(courbe)
    return res




def filtre_courbes(courbes, taille_min):
    res = []
    for c in courbes:
        if len(c)>taille_min:
            res.append(c)
    return res    
                
def trace_courbes(courbes, marker = 'o', linestyle = '-', titre = "Tracé des courbes",linewidth=1.5):
    plt.figure(figsize=(8, 6))
    
    for courbe in courbes:
        x = [p[0] for p in courbe]
        y = [p[1] for p in courbe]
        couleur = (random.random(), random.random(), random.random())  # couleur aléatoire
        plt.plot(x, y, marker=marker, linestyle=linestyle, color=couleur,linewidth=linewidth)
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(titre)
    plt.grid(True)
    plt.show()

def separe_euler(courbe):
    courbes = [[]]
    liens = []
    n = len(courbe)
    j = 0
    for i in range(n):
        if i != 0 and i !=n-1 and courbe[i][0] - courbe[i-1][0]!=0 and courbe[i+1][0] - courbe[i][0]!=0:
            b_euler = (courbe[i][1] - courbe[i-1][1])/(courbe[i][0] - courbe[i-1][0])
            f_euler = (courbe[i+1][1] - courbe[i][1])/(courbe[i+1][0] - courbe[i][0])
            diff = abs(f_euler - b_euler)
            prod = f_euler * b_euler
            #print(prod, diff)
            if diff < 40 and prod>-0.25:
                courbes[j].append(courbe[i])
                #print(diff)
            else:
                courbes.append([]) 
                j+=1
                courbes[j].append(courbe[i])
                liens.append(courbe[i])
    return courbes,liens


def trie_points_distance(p, affiche = False):
    points = p.copy()
    res = [points[0]]
    n = len(points)
    dernier= points[0]
    for _ in range(1,n):
        # print(dernier)
        dist = sqrt((abs(dernier[0]-points[0][0]))**2+(abs(dernier[1]-points[0][1]))**2)
        j_min = 0
        for j,pt in enumerate(points):
            x,y = pt
            if sqrt(abs(dernier[0]-x)**2+abs(dernier[1]-y)**2)<dist:
                dist = sqrt(abs(dernier[0]-x)**2+abs(dernier[1]-y)**2)
                j_min = j
        dernier = points[j_min]
        res.append(dernier)
        points.pop(j_min)
    if affiche:
        plt.close()
        plt.plot([i[0] for i in res],[i[1] for i in res],'o')
        plt.show()
    return res[:-2 ]


def filtre_points_isolés(p):
    points = p.copy()
    res = [points[0]]
    dernier = points[0]
    n = len(points) 
    prev_dist = 0
    for _ in range(1,n):
        dist = sqrt((dernier[0]-points[0][0])**2+(dernier[1]-points[0][1])**2)
        jump = dist - prev_dist
        print(dist, jump)
        if jump<50:
            dernier=points[0]
            res.append(dernier)
            prev_dist = dist
        points.pop(0)
    return res

import subprocess

def splines_illustration():
    plt.figure(figsize=(8, 6))
    points=[(0,0),(1,3),(2,1),(3,2),(4,5),(5,1)]
    f=open("../textes/entree.txt",'w')
    f.write(str(len(points))+"\n")
    f.write(str(1000)+"\n")
    X=[p[0] for p in points]
    colors = ["pink", "blue", "orange", "green", "purple"]

    for i in range(len(points)):
        f.write(str(points[i][0])+","+str(points[i][1])+"\n")
    f.close()
    result = subprocess.run(["./splines.exe"], capture_output=True,text=True)
    f2= open("../textes/sortie.txt",'r')
    courbe = []
    for i in f2.readlines():
        a,b = i.split(",")
        courbe.append((float(a), float(b)))
    X = [p[0] for p in courbe]
    Y = [p[1] for p in courbe]
    S=[[],[],[],[],[],[]]

    for x,y in zip(X,Y):
        i = 0
        while i < 5 and x > points[i][0]:
            i+=1
        S[i].append((x,y))

        
    for i in [1,2,3,4,5]:
        couleur = (random.random(), random.random(), random.random())  # couleur aléatoire
        x = [p[0] for p in S[i]]
        y = [p[1] for p in S[i]]
        plt.plot(x, y, marker='', linestyle='-', color=couleur,linewidth=2, label=f"S{i}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Splines cubiques")
    plt.scatter([p[0] for p in points], [p[1] for p in points], color="red", label="Points à interpoler")
    plt.legend()
    plt.show()
