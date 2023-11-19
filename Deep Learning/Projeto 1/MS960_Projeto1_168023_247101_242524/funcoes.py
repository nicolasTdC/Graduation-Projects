import numpy as np
import cv2
import random
import datetime
from PIL import Image

def inferencia_na_rede(pesos,modelo,classes,imagem): 
    """
    Função que realiza o forward propagation

    Input: 
        pesos -- file com os pesos pre-treinados -- arquivo .weights
        modelo -- file com a arquitetura da rede -- arquivo .cgf
        classes -- file com as classes treinadas -- arquivo .names
        imagem -- imagem RGB a ser analisada -- array de inteiros shape (altura, largura, 3)
        
    Output: 
        outputs -- outputs de cada camada de saída da rede -- tupla de arrays shape (altura_grid*largura_grid*numero_anchor_boxes , 5 + numero_classes)
    """

    # Carregar a rede yolov3
    rede = cv2.dnn.readNet(pesos, modelo) 
    
    # Carregas as classes treinadas
    with open(classes, "r") as f:
        classes = f.read().strip().split("\n")
    
    # Carregar a imagem
    imagem = cv2.imread(imagem)
    
    # Redimensionalisar a imagem para ser input da rede
    blob = cv2.dnn.blobFromImage(imagem, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    
    # Prepara as camadas de saída e o input
    camadas_saida = rede.getUnconnectedOutLayersNames()
    rede.setInput(blob)
    
    # Foward Propagation
    outputs = rede.forward(camadas_saida) 
    
    return classes, imagem, outputs

def iou(caixa1, caixa2):
    """
    Função que faz o cálculo do Intersection over Union (IoU) entre duas caixas

    Input: 
        caixa1 -- coordenadas dos cantos -- lista de inteiros (caixa1_x_esquerda, caixa1_y_cima, caixa1_x_direita, caixa1_y_baixo) 
        caixa2 -- coordenadas dos cantos -- lista de inteiros (caixa2_x_esquerda, caixa2_y_cima, caixa2_x_direita, caixa2_y_baixo)
        
    Output: 
        iou -- IoU entre as caixas -- inteiro
    """

    # Extrai os cantos
    (caixa1_x_esquerda, caixa1_y_cima, caixa1_x_direita, caixa1_y_baixo) = caixa1
    (caixa2_x_esquerda, caixa2_y_cima, caixa2_x_direita, caixa2_y_baixo) = caixa2
    
    # Acha os cantos da interseccao
    x_inter_esquerda = max(caixa1_x_esquerda, caixa2_x_esquerda)
    y_inter_cima = max(caixa1_y_cima, caixa2_y_cima)
    x_inter_direita = min(caixa1_x_direita, caixa2_x_direita)
    y_inter_baixo = min(caixa1_y_baixo, caixa2_y_baixo)
    
    # Acha area da interseccao
    largura_inter = x_inter_direita-x_inter_esquerda
    altura_inter = y_inter_baixo-y_inter_cima
    area_inter = largura_inter* altura_inter
    if area_inter < 0 :    
        area_inter = 0 
    
    # Area da uniao
    caixa1_area = (caixa1_x_direita - caixa1_x_esquerda) * (caixa1_y_baixo - caixa1_y_cima)
    caixa2_area = (caixa2_x_direita - caixa2_x_esquerda) * (caixa2_y_baixo - caixa2_y_cima)
    uniao_area = caixa1_area + caixa2_area - area_inter
    
    # IoU
    iou = area_inter/uniao_area
    
    return iou

def filtrar_confianca(outputs, threshold_confianca, imagem):
    """
    Função para filtrar caixas com pouca probabilidade de ter objetos

    Input:
        outputs -- outputs de cada camada de saída da rede -- tupla de arrays shape (altura_grid*largura_grid*numero_anchor_boxes , 5 + numero_classes)
        threshold_confianca -- threshold para descartar caixas com pouca prob de ter objeto -- float
        imagem -- imagem RGB a ser analisada -- array de inteiros shape (altura, largura, 3)

    Output:
        confiancas -- probabilidade de cada objeto apos filtragem -- array shape (numero classes,)
        caixas -- caixas que podem conter objetos apos filtragem -- lista de lista de inteiros com as coordenadas dos cantos das caixas
        ids_classes -- classe respectiva para cada prob e classe apos filtragem -- lista de inteiros que representam cada classe
    """

    caixas = []
    confiancas = []
    ids_classes = []
    
    # Para cada quadro da grid de cada camada de saida, descarta as caixas com baixa probabilidade de ter objeto
    for output in outputs:
        for deteccao in output:
            probs = deteccao[5:]
            class_id = np.argmax(probs)
            confianca = probs[class_id] * deteccao[4]            
            if confianca > threshold_confianca: # eliminar caixas com probablidade baixa de ter objeto
                centro_x, centro_y, largura, altura = (deteccao[:4] * np.array([imagem.shape[1], imagem.shape[0], imagem.shape[1], imagem.shape[0]])).astype(int)
                coord_esquerda_x = int(centro_x - largura / 2)
                coord_direita_x = int(centro_x + largura / 2)
                coord_cima_y = int(centro_y - altura / 2)      
                coord_baixo_y = int(centro_y + altura / 2)  
                caixas.append([coord_esquerda_x, coord_cima_y, coord_direita_x, coord_baixo_y ])
                confiancas.append(float(confianca))
                ids_classes.append(class_id)
                
    return confiancas, caixas, ids_classes

def non_max_suppression(outputs, threshold_confianca, imagem, threshold_iou):
    """
    Função que realiza o Non-Max Supression dos outputs da rede

    Input:
        outputs -- outputs de cada camada de saída da rede -- tupla de arrays shape (altura_grid*largura_grid*numero_anchor_boxes , 5 + numero_classes)
        threshold_confianca -- threshold para descartar caixas com pouca prob de ter objeto -- float
        imagem -- imagem RGB a ser analisada -- array de inteiros shape (altura, largura, 3)
        threshold_iou -- threshold para descartar caixas com base no IoU -- float
        
    Output:
        confiancas_pred -- probabilidade de cada objeto apos NMS -- array shape (numero classes,)
        caixas_pred -- caixas que podem conter objetos apos NMS -- lista de lista de inteiros com as coordenadas dos cantos das caixas
        classes_pred -- classe respectiva para cada prob e classe apos NMS -- lista de inteiros que representam cada classe
    """

    # Faz a filtragem com relacao ao threshold de confianca
    probs, caixas, classes = filtrar_confianca(outputs, threshold_confianca, imagem)
    
    # Para cada classe, realiza o teste de IoU e descarta caixas conforme o threshold
    classes_detectadas = set(classes)
    for classe in classes_detectadas:
        indexes = []
        for i in range(len(classes)):
            if classes[i] == classe:
                indexes.append(i)
                
        confianca_classe = [probs[i] for i in indexes]
        confianca_classe_ordenada = sorted(confianca_classe, reverse=True)
        temp = confianca_classe_ordenada.copy()
        while True:
            for confianca in confianca_classe_ordenada:
                if confianca != -1:
                    confianca_index = probs.index(confianca)
                    caixa_max_prob = caixas[confianca_index]
                    for index in indexes:
                        if caixas[index] != -1:
                            if caixa_max_prob == caixas[index]:
                                continue
                            IOU = iou(caixa_max_prob, caixas[index])
                            if IOU > threshold_iou:
                                confianca_index= confianca_classe_ordenada.index(probs[index])
                                confianca_classe_ordenada[confianca_index]=-1
                                caixas[index] = -1 # Sinaliza para descartar    
            if confianca_classe_ordenada == temp:
                break
            temp = confianca_classe_ordenada.copy()
               
    indexes_descarte = []
    for i in range(len(caixas)):
        if caixas[i] == -1:
            indexes_descarte.append(i)
    confiancas_pred = [probs[i] for i in range(len(probs)) if i not in indexes_descarte]
    caixas_pred = [caixas[i] for i in range(len(caixas)) if i not in indexes_descarte]
    classes_pred = [classes[i] for i in range(len(classes)) if i not in indexes_descarte]
    
    return confiancas_pred, caixas_pred, classes_pred

def objetos_detectados(confiancas_pred, caixas_pred, classes_pred, classes,imagem):
    """
    Função que exibe e salva a imagem com a bounding box e confianca de cada objeto detectado

    Input:
        confiancas_pred -- predicao das confiancas -- lista de float
        caixas_pred -- caixas com os objetos -- lista de lista de inteiros
        classes_pred -- identificacao de cada classe com relacao a predicao e caixa -- lista de inteiros
        classes -- lista das classes treinadas -- lista de string
        imagem -- imagem RGB a ser analisada -- array de inteiros shape (altura, largura, 3)
        
    Output:
        imagem com bounding boxes, classes e confiancas é aberta em uma nova janela, além de ser salva na pasta "outputs" e nomeada com o momento da execução.
    """

    # Se for detectado pelo menos um objeto, é desenhada a bounding box com a confianca com uma cor aleatoria para cada classe
    if len(confiancas_pred) > 0:
        classes_detectadas = list(set(classes_pred))
        cores = []
        for classe in classes_detectadas:
            cores.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        for i in range(len(confiancas_pred)):
            label = str(classes[classes_pred[i]])
            confianca = confiancas_pred[i]
            print(f"Objeto: {label}, Confiança: {confianca:.3f}") # Exibição no terminal da classe do objeto detectado e sua respectiva confiança
            classes_detectadas_index = classes_detectadas.index(classes_pred[i])
            color = cores[classes_detectadas_index]
            cv2.rectangle(imagem, (caixas_pred[i][0], caixas_pred[i][1]), (caixas_pred[i][2], caixas_pred[i][3]), color, 2)
            label_x = caixas_pred[i][0]
            label_y = caixas_pred[i][1] - 10
            if label_y < 10:
                label_y = 20
            # Exibição na imagem final dos labels e seus contornos para facilitar a leitura:
            cv2.putText(imagem, f"{label} {confianca:.3f}", (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 10)
            cv2.putText(imagem, f"{label} {confianca:.3f}", (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 6)  
            cv2.putText(imagem, f"{label} {confianca:.3f}", (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)  
        
        # Exibição no terminal da quantidade de objetos e da média das suas confianças
        print("Quantidade de objetos:", len(confiancas_pred))
        media = sum(confiancas_pred)/len(confiancas_pred)
        print("Média das confianças:", f"{media:.3f}")

        # Imagem final é salva na pasta "outputs" e nomeada com o momento da execução
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output = f"outputs/{time}.jpg"
        cv2.imwrite(output, imagem)

        # Imagem final é aberta em uma nova janela
        img = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        im_pil.show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print("Nenhum objeto detectado.")