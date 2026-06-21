import cv2
import subprocess

import traces as t
import canny as c

def lit_image(entree, sortie, affiche = False):
    nsize_blurr = 4 # k vaut 2*n +1
    nsize_grad = 4

    sigma_blurr = 5 #prev:3
    sigma_grad = 13

    img = cv2.imread(entree)
    assert img is not None, "erreur : chemin non trouve"
    edges = c.gradient_magnitude_threshholding(img,nsize_blurr,sigma_blurr,nsize_grad,sigma_grad, affiche)

    height, width, _ = img.shape
    white_pixels = []
    f=open(sortie,'w')
    for x in range(width):
        for y in range (height):
            if (edges[y, x] == [255,255,255]).all():
                white_pixels.append((x,y))
                img[y, x] = [0, 0, 255]
               
                f.write(str(x)+","+str(height-y)+"\n")
    f.close()

#nom de l'image SANS EXTENSION pour plus facilement creer les fichiers coorects ensuite
nom = "road01" 
extension = ".jpg"

#lit_image(nom + extension, nom +".txt", True)
points = t.lit_points(nom + ".txt")




#***********************************************************************
#On trie les points:

#1) on enlève ce qui ne fait pas partie d'une courbe lisse ou homogène:
courbes = t.differencie_points(points, 20)
#t.trace_courbes(courbes, linestyle='')
for _ in range(5):
    courbes = t.trie_recolle(courbes,20)
#2) on sépare les "segments de routes"
#print("here py")
#print(courbes)
routes_bruttes0, jonctions_bruttes = [],[]
for c in courbes:
    r,l = t.separe_euler(c)
    routes_bruttes0+=r
    jonctions_bruttes+=l
routes_bruttes = t.filtre_courbes(routes_bruttes0,50)
#print("here py1")
t.trace_courbes(routes_bruttes, linestyle='')


#***********************************************************************

#======================================================================
# On "lisse" les routes; on interpole chacune selon une valeur donnée. 
# Or, on a un executable codé en C qui fait cette opération en prenant 
# les données dans un fichier format .txt; 
# il faut le faire pour chaque route individuelle.

N=1000

routes = []

#print(len(routes_bruttes))
for r in routes_bruttes:
    
    f=open("entree.txt",'w')
    f.write(str(len(r))+"\n")
    f.write(str(N)+"\n")

    for i in range(len(r)):
        f.write(str(r[i][0])+","+str(r[i][1])+"\n")
    f.close()
    result = subprocess.run(["./splines.exe"], capture_output=True,text=True)
    
    print("stdout:")
    print(result.stdout)

    print("stderr:")
    print(result.stderr)

    print("return code:")
    print(result.returncode)
        

    f2= open("sortie.txt",'r')
    route = []
    for i in f2.readlines():
        a,b = i.split(",")
        route.append((float(a), float(b)))
    routes.append(route)
    f2.close()
t.trace_courbes(routes,marker='', linewidth = 5)

#======================================================================