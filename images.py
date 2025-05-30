import numpy as np
import cv2
from matplotlib import pyplot as plt
 
img = cv2.imread('batman.jpg')
assert img is not None, "file could not be read, check with os.path.exists()"
edges = cv2.Canny(img,100,200)


height, width, color = img.shape
white_pixels = []
prev=0
f=open("points.txt",'w')
for x in range(width):
    for y in range (height):
        if edges[y, x] == 255:
            white_pixels.append((x,y))
            img[y, x] = [0, 0, 255]
            prev = x
            f.write(str(x)+","+str(height-y)+"\n")
f.close()

"""plt.subplot(121)
plt.imshow(img)
plt.title('Original Image'), 
plt.subplot(122)
plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image')
 
plt.show()"""

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

points = lit_points("points.txt")
"""x = np.array([i[0] for i in points])
y = np.array([i[1] for i in points])
plt.plot(x, y, 'o', label= 'points')
plt.show()"""

def differencie_points(points):
    fonctions = []
    nb_f = 0
    for p in points:
        if nb_f == 0:
            fonctions.append([p])
            nb_f+=1
        else:
            i=0
            trouve = False
            min_d = float('inf')
            fonctions_logiques = [float('inf') for i in range (nb_f)]
            while i < nb_f:
                f = fonctions[i]
                y = abs(p[1] -f[-1][1])
                x = abs(p[0] -f[-1][0])
                m=x+y
                if p[0] != f[-1][0]:
                    fonctions_logiques[i] = m
                    trouve = True
                    if m < min_d:
                        min_d = m
                elif m < 30:
                    trouve = True #le point est inutile, on ne le met nulle part
                    if m < min_d:
                        min_d = m
                i+=1
            if trouve and min_d < 120:
                j=fonctions_logiques.index(min(fonctions_logiques))
                fonctions[j].append(p)
            elif min_d>30:
                fonctions.append([p])
                nb_f+=1
    return fonctions

diff_f = differencie_points(points)

diff_f = [f for f in diff_f if len(f)>100]

print(diff_f[1])
print(len(diff_f))
plt.close()
fig, axs = plt.subplots(len(diff_f), sharex=True)
fig.suptitle('Différentes sous fonctions identifiées')
for j in range(len(diff_f)):
    x = np.array([i[0] for i in diff_f[j]])
    y = np.array([i[1] for i in diff_f[j]])
    axs[j].plot(x, y)
plt.show()
