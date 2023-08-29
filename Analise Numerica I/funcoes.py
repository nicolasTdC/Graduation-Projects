import numpy as np
import matplotlib.pyplot as plt
import imageio
from PIL import Image
def read_pgm_file(file_path):
    try:
        image = imageio.imread(file_path, mode='F')
    except:
        image = imageio.imread(file_path,as_gray=True)
    return image

def read_ppm_file(file_path):
    image = Image.open(file_path)
    return image

def extract_channels(image):
    # Split the image into color channels
    r, g, b = image.split()

    # Convert channels to NumPy arrays
    r_array = np.array(r)
    g_array = np.array(g)
    b_array = np.array(b)

    return r_array, g_array, b_array


def erro_comp(X,X_comp):

    err2=np.linalg.norm(X)
    err1=np.linalg.norm(X-X_comp)
    err = err1/err2
    return err

def svd_comp(X,U,S,V,k):

    compressed_U = U[:, :k]
    compressed_S = np.diag(S[:k])
    compressed_V = V[:k, :]
    
    compressed_image_array = np.dot(np.dot(compressed_U, compressed_S), compressed_V)
    
    err = erro_comp(X,compressed_image_array)
            
    return compressed_image_array, err

def taxa_comp(numero_inicial, numero_comprimido):
    taxa = 1- numero_comprimido/numero_inicial
    return taxa

def simulacoes_compressao_svd_gray(file):
    X = read_pgm_file(f'{file}')
    m=X.shape[0]
    n=X.shape[1]
    
    mean=[]#media para cada atributo
    std=[]#std para cada atributo
    for i in range(n):
        mi = np.mean(X[:,i])
        sigma=np.std(X[:,i])
        mean.append(mi)
        std.append(sigma)
    for j in range(n):
        for i in range(m):
            X[i,j]=(X[i,j]-mean[j])/std[j]#z score dos atributos]
    
    plt.figure(1)
    plt.imshow(X,cmap='gray')
    plt.axis('off')
     
    kmax =int(min( m*n/(m+n+1) , m , n ) )
    vetork = [i+1 for i in range(kmax)]
    
    U,S,V=np.linalg.svd(X)
    vetor_erro= []
    vetor_imagens_comprimidas=[]
    vetor_taxa_comp = []
    k_relev = []
    count = 0
    flag=False
    flag2 = False
    for _ in vetork:
        
        k = int(_)
            
        compressed_image_array, err= svd_comp(X,U,S,V,k)
    
        
        if count==0:
        
            vetor_erro.append(err)
            vetor_imagens_comprimidas.append(compressed_image_array)
            numero_comprimido = m * k + k + n * k
            
            vetor_taxa_comp.append(taxa_comp(m*n, numero_comprimido))
            k_relev.append(k)
            count+=1
        
        else:
            if abs(err-vetor_erro[count-1])>=0.1 and flag==False:
                vetor_erro.append(err)
                vetor_imagens_comprimidas.append(compressed_image_array)
                numero_comprimido = m * k + k + n * k
                
                vetor_taxa_comp.append(taxa_comp(m*n, numero_comprimido))
                k_relev.append(k)
                count+=1
 
        if err<=0.1:
            flag=True
            if err<=0.05 and flag2==False:
                vetor_erro.append(err)
                vetor_imagens_comprimidas.append(compressed_image_array)
                numero_comprimido = m * k + k + n * k
                
                vetor_taxa_comp.append(taxa_comp(m*n, numero_comprimido))
                k_relev.append(k)
                count+=1
                flag2=True
                              
           
            if err<=0.01 and flag2==True :
                vetor_erro.append(err)
                vetor_imagens_comprimidas.append(compressed_image_array)
                numero_comprimido = m * k + k + n * k
                
                vetor_taxa_comp.append(taxa_comp(m*n, numero_comprimido))
                k_relev.append(k)
                count+=1
                break
            
            if err<=0.05 and flag2==True :
                
                if abs(err-vetor_erro[count-1])>=0.01:
                    vetor_erro.append(err)
                    vetor_imagens_comprimidas.append(compressed_image_array)
                    numero_comprimido = m * k + k + n * k
                    
                    vetor_taxa_comp.append(taxa_comp(m*n, numero_comprimido))
                    k_relev.append(k)
                    count+=1
                                      
    plt.figure(2)
    plt.plot(vetor_taxa_comp,vetor_erro)
    plt.xlabel('Taxa de compressão')
    plt.ylabel('Erro relativo')

    return k_relev, vetor_erro, vetor_imagens_comprimidas, vetor_taxa_comp

def plot_single_img_gray(array):
    plt.imshow(array,cmap="gray")
    plt.axis('off')
 
def plot_single_img_rgb(array):
    plt.imshow(array)
    plt.axis('off')

def simulacoes_compressao_svd_rgb(file):
    X = read_ppm_file(f'{file}')
    
    r_array, g_array, b_array=extract_channels(X)
    
    X= np.dstack((r_array, g_array, b_array))
   
    X=normalize_image(X)
    m=X.shape[0]
    n=X.shape[1]
    l=X.shape[2]
    plt.figure(1)
    plt.imshow(X)
    plt.axis('off')
   # plt.show()
   
    kmax =int(min( m*n/(m+n+1) , m , n ) ) 
    
    vetork = [i+1 for i in range(kmax)]
    
    vetor_imagens_comprimidas_completo=[[],[],[]]

    count = 0
    flag=False
    flag2=False
    for camada in range(l):
        if count==0:
            U,S,V=np.linalg.svd(X[:,:,camada])
            vetor_erro= []
            vetor_imagens_comprimidas=[]
            vetor_numero_comp = []
            k_relev = []
        
            for _ in vetork:
                
                k = int(_)
                    
                compressed_image_array, err= svd_comp(X[:,:,camada],U,S,V,k)
                
                
                if count==0:
                
                    vetor_erro.append(err)
                    vetor_imagens_comprimidas.append(compressed_image_array)
                    numero_comprimido = m * k + k + n * k
                    vetor_numero_comp.append(numero_comprimido)
                    k_relev.append(k)
                    count+=1
                
                else:
                    if abs(err-vetor_erro[count-1])>=0.1 and flag==False:
                        vetor_erro.append(err)
                        vetor_imagens_comprimidas.append(compressed_image_array)
                        numero_comprimido = m * k + k + n * k
                        vetor_numero_comp.append(numero_comprimido)
                        k_relev.append(k)
                        count+=1
                
                if err<=0.1:
                    flag=True

                    if err<=0.05 and flag2==False:
                        vetor_erro.append(err)
                        vetor_imagens_comprimidas.append(compressed_image_array)
                        numero_comprimido = m * k + k + n * k
                        vetor_numero_comp.append(numero_comprimido)
                        k_relev.append(k)
                        count+=1
                        flag2=True
                
                    if err<=0.01 and flag2==True:
                        vetor_erro.append(err)
                        vetor_imagens_comprimidas.append(compressed_image_array)
                        numero_comprimido = m * k + k + n * k
                        vetor_numero_comp.append(numero_comprimido)
                        k_relev.append(k)
                        count+=1                                           
                        break
                    
                    if err<=0.05 and flag2==True:
                        if abs(err-vetor_erro[count-1])>=0.01:
                            vetor_erro.append(err)
                            vetor_imagens_comprimidas.append(compressed_image_array)
                            numero_comprimido = m * k + k + n * k
                            vetor_numero_comp.append(numero_comprimido)
                            k_relev.append(k)
                            count+=1                                           
               
        else:
            U,S,V=np.linalg.svd(X[:,:,camada])
            vetor_imagens_comprimidas=[]
        
            for _ in k_relev:
                
                k = int(_)  
                compressed_image_array, err= svd_comp(X[:,:,camada],U,S,V,k)     
                vetor_imagens_comprimidas.append(compressed_image_array)

        vetor_imagens_comprimidas_completo[camada]=vetor_imagens_comprimidas

    return k_relev, vetor_imagens_comprimidas_completo, vetor_numero_comp,X

def img_aprox_rgb(array1,array2,array3):#red,green,blue
    img=np.dstack((array1, array2, array3))
    return img
def normalize_image(image):
    # Normalize the image array to the range [0, 1]
    image_min = np.min(image)
    image_max = np.max(image)
    normalized_image = (image - image_min) / (image_max - image_min)

    return normalized_image

def pca_comp(X,X_original,U,k,mean,std):

    compressed_U = U[:,0:k]
    
    Z=X@compressed_U
    
    compressed_image_array = Z@compressed_U.T
    n0 = compressed_image_array.shape[1]
    m0 = compressed_image_array.shape[0]
    
    for j in range(n0):
        for i in range(m0):
            compressed_image_array[i,j]=(compressed_image_array[i,j]*std[j])+mean[j]
     
    err = erro_comp(X_original,compressed_image_array)
            
    return compressed_image_array, err

def simulacoes_compressao_pca_gray(file):
    X = read_pgm_file(f'{file}')
    m0=X.shape[0]
    n0=X.shape[1]
    X_original = X.copy() 
    mean=[]#media para cada atributo
    std=[]#std para cada atributo
    for i in range(n0):
        mi = np.mean(X[:,i])
        sigma=np.std(X[:,i])
        mean.append(mi)
        std.append(sigma)
    for j in range(n0):
        for i in range(m0):
            X[i,j]=(X[i,j]-mean[j])/std[j]#z score dos atributos]
        
    plt.figure(1)
    plt.imshow(X,cmap='gray')
    plt.axis('off')
    
    Sigma=1/m0*X.T@X#matriz corr
    m=Sigma.shape[0]
    n=Sigma.shape[1]
    
    kmax =int(min( m*n/(m+n) , m , n ) )

    vetork = [i+1 for i in range(kmax)]

    U,S,V=np.linalg.svd(Sigma)
    
    vetor_erro= []
    vetor_imagens_comprimidas=[]
    vetor_taxa_comp = []
    k_relev = []
    count = 0
    flag=False
    flag2=False
    for _ in vetork:
        
        k = int(_)
            
        compressed_image_array, err= pca_comp(X,X_original,U,k,mean,std)
        
        if count==0:
        
            vetor_erro.append(err)
            vetor_imagens_comprimidas.append(compressed_image_array)
            numero_comprimido = m0 * k + n0 * k           
            vetor_taxa_comp.append(taxa_comp(m0*n0, numero_comprimido))
            k_relev.append(k)
            count+=1
        
        else:
            if abs(err-vetor_erro[count-1])>=0.1 and flag==False:
                vetor_erro.append(err)
                vetor_imagens_comprimidas.append(compressed_image_array)
                numero_comprimido = m0 * k + n0 * k           
                vetor_taxa_comp.append(taxa_comp(m0*n0, numero_comprimido))
                k_relev.append(k)
                count+=1
         
        if err<=0.1:
            flag=True
            if err<=0.05 and flag2==False:
                vetor_erro.append(err)
                vetor_imagens_comprimidas.append(compressed_image_array)
                numero_comprimido = m0 * k + n0 * k           
                vetor_taxa_comp.append(taxa_comp(m0*n0, numero_comprimido))
                k_relev.append(k)
                count+=1
                flag2=True
        
        
        if err<=0.01 and flag2==True:
            vetor_erro.append(err)
            vetor_imagens_comprimidas.append(compressed_image_array)
            numero_comprimido = m0 * k + n0 * k           
            vetor_taxa_comp.append(taxa_comp(m0*n0, numero_comprimido))
            k_relev.append(k)
            count+=1
            break
        
        if err<=0.05 and flag2==True:
            if abs(err-vetor_erro[count-1])>=0.01:
                vetor_erro.append(err)
                vetor_imagens_comprimidas.append(compressed_image_array)
                numero_comprimido = m0 * k + n0 * k           
                vetor_taxa_comp.append(taxa_comp(m0*n0, numero_comprimido))
                k_relev.append(k)
                count+=1    
   
    plt.figure(2)
    plt.plot(vetor_taxa_comp,vetor_erro)
    plt.xlabel('Taxa de compressão')
    plt.ylabel('Erro relativo')
 
    return k_relev, vetor_erro, vetor_imagens_comprimidas, vetor_taxa_comp

def simulacoes_compressao_pca_rgb(file):
    X = read_ppm_file(f'{file}')
    
    r_array, g_array, b_array=extract_channels(X)
    
    X= np.dstack((r_array, g_array, b_array))

    m0=X.shape[0]
    n0=X.shape[1]
    l=X.shape[2]
    X=normalize_image(X)
    X_original = X.copy()
    plt.figure(1)
    plt.imshow(X_original)
    plt.axis('off')

    mean=[[],[],[]]#media para cada atributo
    std=[[],[],[]]#std para cada atributo
    
    for camada in range(l):

        for i in range(n0):
            mi = np.mean(X[:,i,camada])
            sigma=np.std(X[:,i,camada])
            mean[camada].append(mi)
            std[camada].append(sigma)
        for j in range(n0):
            for i in range(m0):
                X[i,j,camada]=(X[i,j,camada]-mean[camada][j])/std[camada][j]#z score dos atributos]

    kmax =int(min( n0*n0/(n0+n0) , n0 ) )

    vetork = [i+1 for i in range(kmax)]

    vetor_imagens_comprimidas_completo=[[],[],[]]

    count = 0
    flag=False
    flag2=False
    for camada in range(l):
        if count==0:
            Sigma=1/m0*X[:,:,camada].T@X[:,:,camada]#matriz corr

            U,S,V=np.linalg.svd(Sigma)
            vetor_erro= []
            vetor_imagens_comprimidas=[]
            vetor_numero_comp = []
            k_relev = []
        
            for _ in vetork:
                
                k = int(_)

                compressed_image_array, err= pca_comp(X[:,:,camada],X_original[:,:,camada],U,k,mean[camada],std[camada])

                if count==0:
                
                    vetor_erro.append(err)
                    vetor_imagens_comprimidas.append(compressed_image_array)
                    numero_comprimido =  m0 * k + n0 * k  
                    vetor_numero_comp.append(numero_comprimido)
             
                    k_relev.append(k)
                    count+=1
                
                else:
                    if abs(err-vetor_erro[count-1])>=0.1 and flag==False:
                        vetor_erro.append(err)
                        vetor_imagens_comprimidas.append(compressed_image_array)
                        numero_comprimido = m0 * k + n0 * k
                        vetor_numero_comp.append(numero_comprimido)
                        k_relev.append(k)
                        count+=1
                
                if err<=0.1:
                    flag=True
                    if err<=0.05 and flag2==False:
                        vetor_erro.append(err)
                        vetor_imagens_comprimidas.append(compressed_image_array)
                        numero_comprimido = m0 * k + n0 * k
                        vetor_numero_comp.append(numero_comprimido)
                        k_relev.append(k)
                        count+=1
                        flag2=True
                
                
                if err<=0.01 and flag2==True:
                    vetor_erro.append(err)
                    vetor_imagens_comprimidas.append(compressed_image_array)
                    numero_comprimido = m0 * k + n0 * k
                    vetor_numero_comp.append(numero_comprimido)
                    k_relev.append(k)
                    count+=1
                    break        
                
                if err<=0.05 and flag2==True:
                    if abs(err-vetor_erro[count-1])>=0.01:
                        vetor_erro.append(err)
                        vetor_imagens_comprimidas.append(compressed_image_array)
                        numero_comprimido = m0 * k + n0 * k
                        vetor_numero_comp.append(numero_comprimido)
                        k_relev.append(k)
                        count+=1
        else:
            Sigma=1/m0*X[:,:,camada].T@X[:,:,camada]#matriz corr

            U,S,V=np.linalg.svd(Sigma)

            vetor_imagens_comprimidas=[]
        
            for _ in k_relev:
                
                k = int(_)
                    
                compressed_image_array, err= pca_comp(X[:,:,camada],X_original[:,:,camada],U,k,mean[camada],std[camada])

                vetor_imagens_comprimidas.append(compressed_image_array)

        vetor_imagens_comprimidas_completo[camada]=vetor_imagens_comprimidas

        vetor_numero_comp2 = [i+2*n0 for i in vetor_numero_comp]
        
    return k_relev, vetor_imagens_comprimidas_completo, vetor_numero_comp2,X_original