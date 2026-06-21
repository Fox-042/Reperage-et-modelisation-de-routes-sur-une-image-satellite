from math import pi, exp,sqrt,atan2
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def weight_matrix(n, sigma,show=False):
    k=2*n+1
    m = [[] for i in range(k)]
    s=0
    for i in range(k):
        m[i] = [[] for i in range(k)]
        for j in range(k):
            x=i-n
            y=j-n
            m[i][j] = (1/(2*pi*sigma**2))*exp(-(x**2+y**2)/(2*sigma**2))
            s+=m[i][j]
    for i in range(k):
        for j in range(k):
            m[i][j] = m[i][j]/s
    if show:
        print(m)
    return m

def point_value(i,j,weight_matrix,image,n,I,J):#Attention, il faut ici n<< I et J
    """
    I: width
    J: height
    
    
    """
    k=2*n+1
    s=[0,0,0] 
    for dx in range(k):
        for dy in range(k):
            x=dx-n
            y=dy-n
            ci = i+x
            cj=j+y
            if ci<0 :
                ci = I+ci
            if ci>=I:
                ci=ci-I
            if cj<0 :
                cj = J+cj
            if cj>=J:
                cj=cj-J
            b,g,r = image[cj, ci] 
            b*=weight_matrix[dx][dy]
            g*=weight_matrix[dx][dy]
            r*=weight_matrix[dx][dy]
            s[0]+=b
            s[1]+=g
            s[2]+=r
    return s

def gaussian_blur(img, n, sigma, affiche = False):
    height, width, _ = img.shape
    res = img.copy()
    print("blurr")
    weights = weight_matrix(n, sigma, True)
    for j in range(height):
        for i in range(width):
            res[j,i]=point_value(i,j,weights,img,n,width,height)
    if affiche:
        cv2.imwrite("image floue.png",res)
        print("image floue mise à jour")
    return res

def grayscale(img, affiche = False):
    height, width, _ = img.shape
    res = img.copy()
    for j in range(height):
        for i in range(width):
            b,g,r = img[j,i]
            val=b/3 + g/3 +r/3
            res[j,i] = [val,val,val]
    if affiche:
        cv2.imwrite("image grise.png",res)
        print("image grise mise à jour")
    return res

def grad_matrix(n, sigma):
    k=2*n+1 
    print("grad matrix")
    G = weight_matrix(n, sigma, True)
    Kx = [[0 for _ in range(k)] for _ in range(k)]
    Ky = [[0 for _ in range(k)] for _ in range(k)]
    for i in range(k):
        for j in range(k):
            x=i-n
            y=j-n
            Kx[i][j]=-(x/(sigma*sigma))*G[i][j]
            Ky[i][j]=-(y/(sigma*sigma))*G[i][j]
    print("kX")
    print(Kx)
    print("kY")
    print(Ky)
    return Kx,Ky

def grad_image(img,n, sigma,show=False):
    height, width, _ = img.shape
    grad = [[0 for _ in range(width)] for _ in range(height)]
    theta = [[0 for _ in range(width)] for _ in range(height)]
    Kx,Ky = grad_matrix(n, sigma)
    X=[[0 for _ in range(width)] for _ in range(height)]
    Y=[[0 for _ in range(width)] for _ in range(height)]
    for i in range(width):
        for j in range(height):
            x = point_value(i,j,Kx,img,n,width,height)[1]
            y = point_value(i,j,Ky,img,n,width,height)[1]
            X[j][i]=x
            Y[j][i]=y
            grad[j][i]=sqrt(x**2+y**2)
            theta[j][i]=atan2(y,x)
            if theta[j][i]<0:
                theta[j][i]=theta[j][i]+pi
            n_s = abs(theta[j][i]-pi/2)
            nw_se = abs(theta[j][i]-(3*pi)/4)
            ne_sw = abs(theta[j][i]-pi/4)
            e_w = abs(theta[j][i])
            dir = n_s
            theta[j][i] = "n_s"
            if dir >= nw_se:
                theta[j][i] = "nw_se"
                dir = nw_se
            if dir >= ne_sw:
                theta[j][i] = "ne_sw"
                dir = ne_sw
            if dir >= e_w:
                theta[j][i] = "e_w"
    if show:
        cmap = "RdBu_r" 

        m1=min([min(l)for l in X])
        m2=max([max(l) for l in X])
        print("m1 et m2 : "+str(m1)+ ", "+str(m2))
        norme1 = matplotlib.colors.TwoSlopeNorm(0,m1,m2)
        plt.imsave("gradientX.png", X, cmap=cmap, vmin=m1, vmax=m2)


        m1=min([min(l)for l in Y])
        m2=max([max(l) for l in Y])
        norme1 = matplotlib.colors.TwoSlopeNorm(0,m1,m2)
        plt.imsave("gradientY.png", Y, cmap=cmap, vmin=m1, vmax=m2)
    return grad, theta

def neighbors(i,j,I,J):
    res=[]
    if i<I-1:
        res.append((i+1,j))
        if j>0:
            res.append((i+1,j-1))
        if j<J-1:
            res.append((i+1,j+1))
    if i>0:
        res.append((i-1,j))
        if j>0:
            res.append((i-1,j-1))
        if j<J-1:
            res.append((i-1,j+1))
    if j>0:
        res.append((i,j-1))
    if j<J-1:
        res.append((i,j+1))
    return res    

def gradient_magnitude_threshholding(img,n_gauss, sigma_gauss, n_grad, sigma_grad, affiche = False):
    height, width, _ = img.shape
    gray = grayscale(img,affiche)
    blury = gaussian_blur(gray,n_gauss,sigma_gauss, affiche)
    grad, theta = grad_image(blury,n_grad,sigma_grad, affiche)
    if affiche:
        m1=min([min(l)for l in grad])
        m2=max([max(l) for l in grad])
        plt.imsave("grad.png", grad, cmap="gray_r", vmin=m1, vmax=m2)

        theta2 = [[0 for _ in range(width)] for _ in range(height)]
        for i in range(width):
            for j in range(height):
                if theta[j][i] =="n_s":
                    theta2[j][i]=0
                elif theta[j][i] == "e_w":
                    theta2[j][i]=1
                elif theta[j][i] == "nw_se":
                    theta2[j][i]=2
                elif theta[j][i] == "ne_sw":
                    theta2[j][i]=3

        cmap = matplotlib.colors.ListedColormap(["red", "green", "blue", "yellow"])
        plt.imsave("theta2.png", theta2, cmap=cmap, vmin=0, vmax=3)
        plt.imshow(theta2, cmap=cmap, vmin=0, vmax=3)

        plt.colorbar()
    strength = [[0 if grad[j][i]<0.1 else 1 if grad[j][i]<0.3 else 2 for i in range(width)] for j in range(height)]
    m=max([max(l) for l in grad])
    threshold1=0.1 * m
    threshold2=0.3 * m
    res = img.copy()
    for i in range(width):
        for j in range(height):
            if grad[j][i]>threshold1:
                strength[j][i] = 1
            if grad[j][i]>threshold2:
                strength[j][i]=2
            if theta[j][i] =="n_s":
                if j>0 and j<height-1 and grad[j-1][i]<grad[j][i] and grad[j][i]>grad[j+1][i]:
                    res[j,i] = [255,255,255]
                else:
                    res[j,i] = [0,0,0]
            elif theta[j][i] =="e_w":
                if i>0 and i<width-1 and grad[j][i-1]<grad[j][i] and grad[j][i]>grad[j][i+1]:
                    res[j,i] = [255,255,255]
                else:
                    res[j,i] = [0,0,0]
            elif theta[j][i] =="nw_se":
                if i>0 and i<width-1 and j>0 and j<height-1 and grad[j+1][i-1]<grad[j][i] and grad[j][i]>grad[j-1][i+1]:
                    res[j,i] = [255,255,255]
                else:
                    res[j,i] = [0,0,0]
            elif theta[j][i] =="ne_sw":
                if i>0 and i<width-1 and j>0 and j<height-1 and grad[j+1][i+1]<grad[j][i] and grad[j][i]>grad[j-1][i-1]:
                    res[j,i] = [255,255,255]
                else:
                    res[j,i] = [0,0,0]
            else:
                res[j,i]=[0,0,255] #red = problem, should not actually happen (bgr)
    
    if affiche :
        cmap = matplotlib.colors.ListedColormap(["white", "gray", "black"])
        plt.imsave("strength bzfore.png", strength, cmap=cmap, vmin=0, vmax=2)
        plt.imshow(strength, cmap=cmap, vmin=0, vmax=3)
        plt.colorbar()

    cv2.imwrite("image avant hysterisis.png", res)
    #applying hysterisis with queue method
    q = []
    for i in range(width):
        for j in range(height):
            if strength[j][i]==2:
                q.append((i,j))
    while len(q)>0:
        i,j=q.pop(0)
        neighborhood = neighbors(i,j,width,height)
        for n in neighborhood:
            i_n,j_n=n
            if strength[j_n][i_n]==1 and (res[j_n,i_n]==[255,255,255]).all():
                strength[j_n][i_n]=2
                q.append((i_n,j_n))
    
    for i in range(width):
        for j in range(height):
            if strength[j][i]<2:
                res[j,i]=[0,0,0]
    if affiche:
        cv2.imshow("image resultante", res)

        cv2.imwrite("image resultante.png", res)

        cmap = matplotlib.colors.ListedColormap(["white", "gray", "black"])
        plt.imsave("strength after.png", strength, cmap=cmap, vmin=0, vmax=2)
        plt.imshow(strength, cmap=cmap, vmin=0, vmax=3)
        plt.colorbar()

    return res
            


            
    