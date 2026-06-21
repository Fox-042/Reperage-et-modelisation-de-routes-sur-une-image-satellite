from matplotlib import pyplot as plt
import cv2

import canny as c


def lit_image(entree, sortie, affiche = False):
    ksizeblurr = 5
    ksizecanny = 5
    img = cv2.imread(entree)
    assert img is not None, "erreur : chemin non trouve"
    edges = c.gradient_magnitude_threshholding(img,ksizeblurr,ksizecanny,affiche)

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


