# Importar as funções
import funcoes as funcs

# Carregar o modelo e a imagem (input):
pesos, modelo, classes, imagem = "weights/yolov3.weights", "cfg/yolov3.cfg", "data/coco.names", "images/dog.jpg" # Selecione a imagem desejada alterando o último parâmetro.

threshold_confianca = 0.5 # Selecione um valor entre 0 e 1 (padrão: 0.5). 
# Valores mais altos garantem que as detecções são mais confiáveis, mas detecções corretas podem ser descartadas.

threshold_iou = 0.5 # Selecione um valor entre 0 e 1 (padrão: 0.5). 
# Valores mais baixos evitam que o mesmo objeto seja detectado mais de uma vez, mas detecções corretas podem ser descartadas.

# Foward Propagation:
classes, imagem, outputs = funcs.inferencia_na_rede(pesos,modelo,classes,imagem)

# Non-Max Supression (NMS):
confianca_pred, caixas_pred, classes_pred = funcs.non_max_suppression(outputs, threshold_confianca, imagem, threshold_iou)

# Imagem final (output):
funcs.objetos_detectados(confianca_pred,caixas_pred,classes_pred,classes,imagem)

# Após a execução:
# A imagem do output será aberta em uma nova janela, além de ser salva na pasta "outputs".
# No terminal, serão exibidas as classes e as confianças de cada objeto detectado, além da média das confianças.