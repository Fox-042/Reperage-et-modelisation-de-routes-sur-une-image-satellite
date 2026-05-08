from math import sqrt, pi, exp
from matplotlib import pyplot as plt
import cv2

def triangularise (S : list[list[float]], X: list[float]) -> list[float]:
    n = len(S)
    m = len(S[0])
    for i in range (m-1):
        a = S[i][i]
        for j in range (i+1, n):
            b = S[j][i]
            for k in range(m):
                S[j][k] = b*S[i][k] - a*S[j][k]
            X[j] = b*X[i] - a*X[j]

def back_substitution (S, X):
    n = len(S)
    m = len(S[0])
    for i in range(n-1,0,-1):
        X[i] = sum([S[i][j]*X[j] for j in range(m)])/X[i]

def print_matrix(M):
    for i in M:
        for j in i:
            print(str(j), end = " ")
        print("\n")

def gaussian_system (S,X):
    triangularise(S, X)
    back_substitution(S,X)
    print_matrix(S)
    print(X)
    return X
    
#gaussian_system([[1.,2.],[3.,1.]],[1.,2.])

def splines_cubiques(x, y):
    intervalles = []
    n=len(x)
    for i in range(n-1):
        intervalles.append(x[i+1]-x[i])
    alpha = [0]
    for i in range(1,n-1):
        alpha.append((3/intervalles[i])*(y[i+1]-y[i])-(3/intervalles[i-1])*(y[i]-y[i-1]))
    alpha.append(0)
    l=[1]
    mu = [0]
    z=[0]
    for i in range(1,n-1):
        
        l.append(2*(x[i+1]-x[i-1])-intervalles[i-1]*mu[i-1])
        mu.append(intervalles[i]/l[i])
        z.append((alpha[i]-intervalles[i-1]*z[i-1])/l[i])
    l.append(1)
    z.append(0)
    
    a=y[:]
    b=[0]*n
    c=[0]*n
    d=[0]*n
    for i in range(n-2,-1,-1):
        c[i]=z[i]-mu[i]*c[i+1]
        b[i] = (y[i+1] - y[i])/intervalles[i] - intervalles[i]*(c[i+1] + 2*c[i]) / 3
        d[i] = (c[i+1] - c[i]) / (3*intervalles[i])
    return [(a[i],b[i],c[i],d[i]) for i in range(n-1)]


def spline(a,b,c,d,xi,x):
    return a+ b*(x - xi) + c*(x - xi)**2 + d*(x - xi)**3
 

def interpole(points, N, deb, fin):
    points.sort()# jai un doute- semble contraire au pricipe. 17/03/2026
    print(len(points), " : points")
    X = [c[0] for c in points]
    Y = [c[1] for c in points]
    h = (fin-deb)/(N-1)
    courbe = []
    sp = splines_cubiques(X, Y)
    print(sp)
    for i in range(N):
        x = deb + i*h
        j = 0
        while j<len(X)-1 and X[j+1] < x :
            j+=1
        a,b,c,d = sp[j]
        courbe.append((x,spline(a,b,c,d,X[j],x)))

    print(len(courbe), " : courbe")
    print(x, fin)
    tracer(courbe,"courbe","abcisse")
    return courbe

def splines_parametres(points, N):
    ecart = [sqrt(x**2+y**2) for x, y in points]
    t = [sum(ecart[:i]) for i in range (len(points))]
    x = [(t[i],c[0]) for i,c in enumerate(points)]
    tracer(x,"t","x")
    
    y = [(t[i],c[1]) for i,c in enumerate(points)]
    tracer(y,"t","y")
    xt = interpole(x,N,t[0],t[-1])
    yt = interpole(y,N,t[0],t[-1])

    tracer(xt,"t","x_interpolée")
    print("2")
    tracer(yt,"t","y_interpolée")
    courbe = [(xt[i][1], yt[i][1]) for i in range(N)]
    return courbe

    

            
def tracer(points,xs='x',ys='y', marker = 'o'):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plt.close()

    plt.plot(x, y, marker=marker)
    plt.xlabel(xs)
    plt.ylabel(ys)
    plt.title('Courbe des points')
    plt.grid(True)
    plt.show()










"""
1x+2y=x 
3x+y=2y

2y=x
3x=Y









"""