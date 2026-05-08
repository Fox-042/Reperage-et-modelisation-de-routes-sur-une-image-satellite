import numpy as np
from matplotlib import pyplot as plt
import random
import cv2
import traces as t
import interpolate as i
import canny as c
from math import sqrt

def lit_image_naif(entree, sortie, affiche = False):
    ksize = 5
    img = cv2.imread(entree)
    assert img is not None, "erreur : chemin non trouve"
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


    height, width, _ = img.shape
    white_pixels = []
    f=open(sortie,'w')
    for x in range(width):
        for y in range (height):
            if edges[y, x] == 255:
                white_pixels.append((x,y))
                img[y, x] = [0, 0, 255]
               
                f.write(str(x)+","+str(height-y)+"\n")
    f.close()
#lit_image_naif('batman.jpg',"points.txt")
#lit_image_naif ('Gemini_Generated_Image_road_01_v3.png',"Gemini_Generated_Image_road_01_v3.png.txt")

def parcours(img, x, y, lst):
    
    def aux(x, y):
        if img[y,x] == 255:
            lst.append((x,y))
            img[y,x] =100
            aux(x-1,y)
            aux(x+1,y)
            aux(x,y-1)
            aux(x,y+1)
            aux(x-1,y-1)
            aux(x+1,y-1)
            aux(x-1,y+1)
            aux(x+1,y+1)
    aux(x,y)

def lit_image(entree, sortie, affiche = False):
    ksize = 5
    img = cv2.imread(entree)
    assert img is not None, "erreur : chemin non trouve"
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


    height, width, _ = img.shape
    white_pixels = []
    prev=0
    f=open(sortie,'w')
    for x in range(width):
        for y in range (height):
            if edges[y, x] == 255:
                parcours(edges,x,y,white_pixels)
                #img[y, x] = [0, 0, 255]
                f.write(str(x)+","+str(height-y)+"\n")
    f.close()


def lit_points(nom):
    res = []
    f=open(nom,'r')
    for i in f.readlines():
        a,b = i.split(",")
        res.append((int(a), int(b)))
    f.close()
    #res.sort()
    #print(res)
    return res

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


def staline_filter(points):
    osc = True
    res = []
    for p in points:
        if osc:
            res.append(p)
            osc = False
        else:
            osc = True
    return res


"""print("start")
#points = lit_points("points_road01.txt")
points = lit_points("Gemini_Generated_Image_road_01_v3.png.txt")
print("a lu")
points_t = trie_points_distance(points,affiche= True)
print("premier tri fait")
points_f = filtre_points_isolés(points_t)
print("filtre  fait")


courbes = t.differencie_points(points_t, 20)
points_f = t.filtre_courbes_concat(courbes,70)
points_f = staline_filter(points_f)


plt.close()
plt.plot([i[0] for i in points_f],[i[1] for i in points_f],'o')
plt.show()
print("premiers points")


i.tracer(points_f,"x","y")
plt.show()
courbe = i.splines_parametres(points_f,100000,0,4)
print(courbe)
plt.close()
i.tracer(courbe,marker = '')
print("Done")

"""

img = cv2.imread("road01v2.jpg")
can = c.gradient_magnitude_threshholding(img, 5)
cv2.imshow(can)








      
"""points = [(0,4),(2,8),(3,10),(4,3)]
plt.close()
i.tracer(points,"x","y")
plt.show()
courbe = i.splines_parametres(points,100,0,4)
print(courbe)
plt.close()
i.tracer(courbe)
print("Done")"""

"""x = np.array([i[0] for i in points])
y = np.array([i[1] for i in points])
plt.plot(x, y, 'o', label= 'points')
plt.show()"""




"""plt.close()
fig, axs = plt.subplots(len(diff_f), sharex=True)
fig.suptitle('Différentes sous fonctions identifiées')
for j in range(len(diff_f)):
    x = np.array([i[0] for i in diff_f[j]])
    y = np.array([i[1] for i in diff_f[j]])
    axs[j].plot(x, y)
plt.show()
"""