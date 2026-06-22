# Reperage-et-modelisation-de-routes-sur-une-image-satellite

Le but de ce projet est de detecter les routes sur les images satellites.

Contenu:

- main.py : contient en début de ficher les paramètres à faire varier. Pour faire tourner le code, lancer ce ficher A PARTIR DE SON DOSSIER PARENT, donc de la racine du projet.

 - images_a_traiter : dossier de rangement des images sur lesquelles je travaille, dont des images experimentales traitées par IA pour voir la réaction de mon code à des situations avec plus ou moins de bruit.

 - resultats : dossier dans lequel sont sauvegardées toutes les images générées par le code - ATTENTION, elles sont remplacées à chaque exécution du main, à moins de les renomer en prolongeant les noms ou de les sauvgarder ailleurs.

 - textes : dossier qui contient les fichiers textes représentant soit des informations sauvgardées, soit des fuchuers de communication utilisés entre le c et le python. Ils peuvent être réecrits à tout moment, il faut donc encore ici les renommer ou les sauvegarder ailleurs si l'on souhaite les conserver.

- scripts : contient des fichiers codes 
    - interpolate.py : plus utilisé, code python d'interpolation par splines cubiques
    - splines.c, splines.exe : effectue maintenant l'interpolation par splines cubiques
    - canny.py : code des traitements d'image pour la détection des bords
    - traces.py : contient les petits codes autres, notemment les tris et filtres des points



