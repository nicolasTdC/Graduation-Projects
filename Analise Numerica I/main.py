
import funcoes as funcs
import numpy as np
import matplotlib.pyplot as plt

decision0 = input(rf'Path dos arquivos? ex: C:\User\Documents\MS512\Projeto\main'+ '\n')

decision1 = input('gray ou rgb? ex: rgb\n')

if decision1 == 'gray':
    
    decision1_1 = input('Arquivo da imagem? ex: fingerprint1.pgm\n')
    file =f'{decision0}\imagens_para_teste\{decision1}\{decision1_1}'
 #   file.replace('\\', '/')
    decision1_2 = input('Compressão por SVD ou PCA? ex: SVD\n')
    
    if decision1_2 == 'SVD':
        k_relev_gray, vetor_erro_svd, vetor_imagens_comprimidas_svd, vetor_taxa_comp_svd= funcs.simulacoes_compressao_svd_gray(file)
        i=0
      #  test=f'{decision0}\save_files\vetor_erro_svd_{decision1_2}_{decision1_1}'
        np.save(rf'{decision0}\save_files\k_relev_gray_{decision1_2}_{decision1_1}',k_relev_gray)
        np.save(rf'{decision0}\save_files\vetor_erro_svd_{decision1_2}_{decision1_1}',vetor_erro_svd)
        np.save(rf'{decision0}\save_files\vetor_imagens_comprimidas_svd_{decision1_2}_{decision1_1}',vetor_imagens_comprimidas_svd)
        np.save(rf'{decision0}\save_files\vetor_taxa_comp_svd_{decision1_2}_{decision1_1}',vetor_taxa_comp_svd)
        
        
        for array in vetor_imagens_comprimidas_svd:
            plt.figure(i+3)
            funcs.plot_single_img_gray(array)
            i+=1
        
        plt.show()
    
    if decision1_2 == 'PCA':
        k_relev_gray_pca, vetor_erro_pca, vetor_imagens_comprimidas_pca, vetor_taxa_comp_pca= funcs.simulacoes_compressao_pca_gray(file)
        i=0
        np.save(rf'{decision0}\save_files\k_relev_gray_pca_{decision1_2}_{decision1_1}',k_relev_gray_pca)
        np.save(rf'{decision0}\save_files\vetor_erro_pca_{decision1_2}_{decision1_1}',vetor_erro_pca)
        np.save(rf'{decision0}\save_files\vetor_imagens_comprimidas_pca_{decision1_2}_{decision1_1}',vetor_imagens_comprimidas_pca)
        np.save(rf'{decision0}\save_files\vetor_taxa_comp_pca_{decision1_2}_{decision1_1}',vetor_taxa_comp_pca)
        
        
        for array in vetor_imagens_comprimidas_pca:
            plt.figure(i+3)
            funcs.plot_single_img_gray(array)
            i+=1
        
        plt.show()
    
if decision1 == 'rgb':
    
    decision1_1 = input('Arquivo da imagem? ex: baboon.ppm\n')
    file = f'{decision0}\imagens_para_teste\{decision1}\{decision1_1}'
   # file.replace('\\', '/')
    decision1_2 = input('Compressão por SVD ou PCA? ex: SVD\n')
    if decision1_2 == 'SVD':
        
        k_relev_rgb, vetor_imagens_comprimidas_completo, vetor_numero_comp_por_camada,X= funcs.simulacoes_compressao_svd_rgb(file)

        vetor_imagens_comprimidas_red = vetor_imagens_comprimidas_completo[0]
        vetor_imagens_comprimidas_green= vetor_imagens_comprimidas_completo[1]
        vetor_imagens_comprimidas_blue = vetor_imagens_comprimidas_completo[2]

        numero_imagens = min(len(vetor_imagens_comprimidas_red),len(vetor_imagens_comprimidas_red),len(vetor_imagens_comprimidas_red))

        vetor_erro_svd=[]
        vetor_taxa_comp_svd=[]
        norma_X=np.linalg.norm(X)
        m=X.shape[0]
        n=X.shape[1]
        l=X.shape[2]
        numero_elementos_iniciais=m*n*l

        for i in range(numero_imagens):
            img = funcs.img_aprox_rgb(vetor_imagens_comprimidas_red[i],vetor_imagens_comprimidas_green[i],vetor_imagens_comprimidas_blue[i])
            err= np.linalg.norm(X-img)/norma_X
            vetor_erro_svd.append(err)
            
            numero_elementos_comprimidos = 3*vetor_numero_comp_por_camada[i]
            taxa_compressao = numero_elementos_comprimidos/numero_elementos_iniciais
            vetor_taxa_comp_svd.append(1-taxa_compressao)
            plt.figure(i+2)
            img=funcs.normalize_image(img)
            funcs.plot_single_img_rgb(img)
        
        np.save(rf'{decision0}\save_files\k_relev_rgb_{decision1_2}_{decision1_1}',k_relev_rgb)
        np.save(rf'{decision0}\save_files\vetor_imagens_comprimidas_completo_{decision1_2}_{decision1_1}',vetor_imagens_comprimidas_completo)
        np.save(rf'{decision0}\save_files\vetor_numero_comp_por_camada_{decision1_2}_{decision1_1}',vetor_numero_comp_por_camada)
        np.save(rf'{decision0}\save_files\X_{decision1_2}_{decision1_1}',X)  
        plt.figure(i+3)
        plt.plot(vetor_taxa_comp_svd,vetor_erro_svd)
        plt.xlabel('Taxa de compressão')
        plt.ylabel('Erro relativo')
        plt.show()
        
    if decision1_2 == 'PCA':
        k_relev_rgb, vetor_imagens_comprimidas_completo, vetor_numero_comp_por_camada,X= funcs.simulacoes_compressao_pca_rgb(file)

        vetor_imagens_comprimidas_red = vetor_imagens_comprimidas_completo[0]
        vetor_imagens_comprimidas_green= vetor_imagens_comprimidas_completo[1]
        vetor_imagens_comprimidas_blue = vetor_imagens_comprimidas_completo[2]

        numero_imagens = min(len(vetor_imagens_comprimidas_red),len(vetor_imagens_comprimidas_red),len(vetor_imagens_comprimidas_red))

        vetor_erro_pca=[]
        vetor_taxa_comp_pca=[]
        norma_X=np.linalg.norm(X)
        m=X.shape[0]
        n=X.shape[1]
        l=X.shape[2]
        numero_elementos_iniciais=m*n*l
        
        np.save(rf'{decision0}\save_files\k_relev_rgb_{decision1_2}_{decision1_1}',k_relev_rgb)
        np.save(rf'{decision0}\save_files\vetor_imagens_comprimidas_completo_{decision1_2}_{decision1_1}',vetor_imagens_comprimidas_completo)
        np.save(rf'{decision0}\save_files\vetor_numero_comp_por_camada_{decision1_2}_{decision1_1}',vetor_numero_comp_por_camada)
        np.save(rf'{decision0}\save_files\X_{decision1_2}_{decision1_1}',X)  
        
        
        for i in range(numero_imagens):
            img = funcs.img_aprox_rgb(vetor_imagens_comprimidas_red[i],vetor_imagens_comprimidas_green[i],vetor_imagens_comprimidas_blue[i])
            err= np.linalg.norm(X-img)/norma_X
            vetor_erro_pca.append(err)
            
            numero_elementos_comprimidos = 3*vetor_numero_comp_por_camada[i]
            taxa_compressao = numero_elementos_comprimidos/numero_elementos_iniciais
            vetor_taxa_comp_pca.append(1-taxa_compressao)
            plt.figure(i+2)
            img=funcs.normalize_image(img)
            funcs.plot_single_img_rgb(img)
        plt.figure(i+3)
        plt.plot(vetor_taxa_comp_pca,vetor_erro_pca)
        plt.xlabel('Taxa de compressão')
        plt.ylabel('Erro relativo')
        plt.show()
    
    
