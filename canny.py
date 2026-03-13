from math import pi, exp,sqrt,atan2


def weight_matrix(n):
    k=2*n+1
    sigma = k/6
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

def gaussian_blur(img, n):
    height, width, _ = img.shape
    res = img.copy()
    weights = weight_matrix(n)
    for j in range(height):
        for i in range(width):
            res[j,i]=point_value(i,j,weights,img,n,width,height)
    return res

def grayscale(img):
    height, width, _ = img.shape
    res = img.copy()
    for j in range(height):
        for i in range(width):
            b,g,r = img[j,i]
            res[j,i] = [(b+g+r)/3,(b+g+r)/3,(b+g+r)/3]
    return res

def grad_matrix(n):
    k=2*n+1 
    sigma = k/6
    G = weight_matrix(n)
    Kx = [[0 for _ in range(k)] for _ in range(k)]
    Ky = [[0 for _ in range(k)] for _ in range(k)]
    for i in range(k):
        for j in range(k):
            x=i-n
            y=j-n
            Kx[i][j]=-(x/(sigma*sigma))*G[i][j]
            Ky[i][j]=-(y/(sigma*sigma))*G[i][j]
    return Kx,Ky

def grad_image(img,n):
    height, width, _ = img.shape
    grad = [[0 for _ in range(width)] for _ in range(height)]
    theta = [[0 for _ in range(width)] for _ in range(height)]
    Kx,Ky = grad_matrix(n)
    for i in range(width):
        for j in range(height):
            x = point_value(i,j,Kx,img,n,width,height)[1]
            y = point_value(i,j,Ky,img,n,width,height)[1]
            grad[j,i]=sqrt(x**2+y**2)
            theta[j][i]=atan2(y,x)
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
    return grad, theta

def gradient_magnitude_threshholding(img, n):
    height, width, _ = img.shape
    gray = grayscale(img)
    blury = gaussian_blur(gray,10)
    grad, theta = grad_image(blury,n)
    strength = [[0 if grad[j][i]<0.1 else 1 if grad[j][i]<0.3 else 2 for i in range(width)] for j in range(height)]
    res = img.copy()
    for i in range(width):
        for j in range(height):
            kept = True
            if strength[j][i]==0:
                kept = False
            else if


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
                if i>0 and i<height-1 and j>0 and j<width-1 and grad[j+1][i-1]<grad[j][i] and grad[j][i]>grad[j-1][i+1]:
                    res[j,i] = [255,255,255]
                else:
                    res[j,i] = [0,0,0]
            elif theta[j][i] =="ne_sw":
                if i>0 and i<height-1 and j>0 and j<width-1 and grad[j+1][i+1]<grad[j][i] and grad[j][i]>grad[j-1][i-1]:
                    res[j,i] = [255,255,255]
                else:
                    res[j,i] = [0,0,0]
            else :
                res[j,i]=[0,0,255]
    return res
            


            
    