import numpy as np
from matplotlib import pyplot as plt
import random
import cv2
import traces

def lit_image(entree, sortie, affiche = False):
    ksize = 5
    img = cv2.imread(entree)
    assert img is not None, "erreur - chemin non trouvé"
    gaussian_blurr = cv2.GaussianBlur(img, (ksize,ksize),0)
    edges = cv2.Canny(gaussian_blurr,100,200)
    if affiche:
        plt.subplot(121)
        plt.imshow(gaussian_blurr)
        plt.title('Gaussian Image')
        plt.subplot(122)
        plt.imshow(edges,cmap = 'gray')
        plt.title('Edge Image')
        plt.show()


    height, width, color = img.shape
    white_pixels = []
    prev=0
    f=open(sortie,'w')
    for x in range(width):
        for y in range (height):
            if edges[y, x] == 255:
                white_pixels.append((x,y))
                img[y, x] = [0, 0, 255]
                prev = x
                f.write(str(x)+","+str(height-y)+"\n")
    f.close()
#lit_image('batman.jpg',"points.txt")
lit_image('road01.jpg',"points_road01.txt")


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

#points = lit_points("points.txt")
points = lit_points("points_road01.txt")

"""x = np.array([i[0] for i in points])
y = np.array([i[1] for i in points])
plt.plot(x, y, 'o', label= 'points')
plt.show()"""


def differencie_points(points):
    courbes = [[points[0]]]
    for p in points[1:]:
        indice = 0
        d_min = float('inf')
        for i, courbe in enumerate(courbes):
            y = abs(p[1] -courbe[-1][1])
            x = abs(p[0] -courbe[-1][0])
            dist=x+y
            if dist<d_min:
                d_min = dist
                indice = i
        if p[0]!=courbes[indice][-1][0]:
            if d_min < 50:
                courbes[indice].append(p)
            else:
                courbes.append([p])
        elif d_min>90:
            courbes.append([p])
    return courbes
                
def trace_courbes(courbes):
    plt.figure(figsize=(8, 6))
    
    for courbe in courbes:
        x = [p[0] for p in courbe]
        y = [p[1] for p in courbe]
        couleur = (random.random(), random.random(), random.random())  # couleur aléatoire
        plt.plot(x, y, marker='o', linestyle='-', color=couleur)
    
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


diff_f = differencie_points(points)
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
traces.interpole_par_splines(courbes_derivables)
#trace_courbes(diff_f)

"""plt.close()
fig, axs = plt.subplots(len(diff_f), sharex=True)
fig.suptitle('Différentes sous fonctions identifiées')
for j in range(len(diff_f)):
    x = np.array([i[0] for i in diff_f[j]])
    y = np.array([i[1] for i in diff_f[j]])
    axs[j].plot(x, y)
plt.show()
"""