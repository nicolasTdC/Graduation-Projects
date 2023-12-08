# MS960 - Introdução ao Aprendizado de Máquinas Profundo
# Projeto 2 - Tradução Automática Usando Atenção
# Arquivo de Implementação das Funções Utilizadas no Notebook do Projeto

import numpy as np
import matplotlib.pyplot as plt
import keras.backend as K

from keras.layers import *
from keras.utils import *
from keras.models import *

# Tratamento dos dados:

def string_to_int(string, length, vocab):
  """
    Converts all strings in the vocabulary into a list of integers representing the positions of the
    input string's characters in the "vocab"

    Arguments:
    string -- input string, e.g. 'Wed 10 Jul 2007'
    length -- the number of time steps you'd like, determines if the output will be padded or cut
    vocab -- vocabulary, dictionary used to index every character of your "string"

    Returns:
    rep -- list of integers (or '<unk>') (size = length) representing the position of the string's character in the vocabulary
    """
  #make lower to standardize
  string = string.lower()
  string = string.replace(',', '')

  if len(string) > length:
    string = string[:length]

  rep = list(map(lambda x: vocab.get(x, '<unk>'), string))

  if len(string) < length:
    rep += [vocab['<pad>']] * (length - len(string))

  return rep

def converter_para_one_hot(Tx, Ty, dataset, machine_vocab, human_vocab):
  '''
    Coverte os exemplos para One Hot Vector com base nos indexes dos vocabulários

    Inputs:
    Tx -- Tamanho máximo da frase de entrada
    Ty -- Tamanho máximo da frase de saída
    dataset -- lista de tuplas dos exemplos, tuplas do tipo ( input, output esperado )
    machine_vocab -- dicionario mapeando os caracteres nas datas em formato de maquina para ́ındices inteiros
    human_vocab -- dicionario mapeando os caracteres nas datas em formato humano para ́ındices inteiros.

    Outputs:
    Xoh, Yoh : tensores de One Hot Vectors dos exemplos
    '''
  X, Y = zip(*dataset) # Separa o dataset pros inputs e labels

  # Converte os dados para mapeamento de indexes para os One Hot Vectors
  X = np.array([string_to_int(i, Tx, human_vocab) for i in X])
  Y = [string_to_int(t, Ty, machine_vocab) for t in Y]

  # Converte para One Hot Vector com base nos indices
  Xoh = np.array(
      list(map(lambda x: to_categorical(x, num_classes=len(human_vocab)), X)))
  Yoh = np.array(
      list(map(lambda x: to_categorical(x, num_classes=len(machine_vocab)),
               Y)))

  return Xoh, Yoh

# Mecanismo de Atenção:

def softmax(x, axis=1):
  '''
    Função Softmax

    Inputs:
    x -- Tensor com as energias
    axis -- Eixo para softmax ser aplicada

    Outputs:
    Tensor resultante
    '''
  ndim = K.ndim(x)
  if ndim == 2:
    return K.softmax(x)
  elif ndim > 2:
    e = K.exp(x - K.max(x, axis=axis, keepdims=True))
    s = K.sum(e, axis=axis, keepdims=True)
    return e / s

def ferramentas_atencao(Tx, n_pos, machine_vocab):
  '''
    Preparação dos mecanismos compartilhados no mecanismo de atenção 

    Inputs:
    Tx -- Tamanho máximo da frase de entrada
    n_pos -- numero de ativações pós atenção
    machine_vocab -- dicionario mapeando os caracteres nas datas em formato de maquina para ́ındices inteiros

    Outputs:
    dicionario -- Dicionário com as ferramentas compartilhadas    
    '''
  # Para repetir o estado anterior para todos inputs
  repetidor = RepeatVector(Tx)

  # Para concatenar o estado anterior com as ativações pré-atenção
  concatenador = Concatenate(axis=-1)

  # Para 1a camada da rede de aprendizado de energias
  mecanismo_atencao_camada1 = Dense(10, activation="tanh")

  # Para 2a camada da rede de aprendizado de energias
  mecanismo_atencao_camada2 = Dense(1, activation="relu")

  # Para saída softmax da rede de aprendizado de energias ( obter atenções )
  ativacao = Activation(softmax, name='pesos_atencao')

  # Para fazer a combinação linear dos pesos de atenção e ativações pré-atenção
  dotor = Dot(axes=1)

  #LSTM pros atencao
  LSTM_pos_ativacao = LSTM(n_pos, return_state=True)
  output_layer = Dense(len(machine_vocab), activation=softmax)

  dicionario = {
      'repetidor': repetidor,
      'concatenador': concatenador,
      'mecanismo_atencao_camada1': mecanismo_atencao_camada1,
      'mecanismo_atencao_camada2': mecanismo_atencao_camada2,
      'ativacao': ativacao,
      'dotor': dotor,
      'LSTM_pos_ativacao': LSTM_pos_ativacao,
      'output_layer': output_layer
  }

  return dicionario

# Rede intermediária que calcula os pesos de atenção:

def rede_atencao(a, s_prev, dicionario):
  """    
    Calcula o contexto para um passo temporal

    Inputs:
    a -- ativação da rede pré-atenção
    s_prev -- estado pós-atenção do passo anterior

    Outputs:
    contexto -- vetor com o contexto daquele passo
    """
  # Carrega as ferramentas
  repetidor = dicionario["repetidor"]
  concatenador = dicionario["concatenador"]
  mecanismo_atencao_camada1 = dicionario["mecanismo_atencao_camada1"]
  mecanismo_atencao_camada2 = dicionario["mecanismo_atencao_camada2"]
  ativacao = dicionario["ativacao"]
  dotor = dicionario["dotor"]

  # Repete estado anterior
  s_prev = repetidor(s_prev)

  # Concatena estado anterior com ativações pré-atenção
  concat = concatenador([a, s_prev])

  # Computa pesos de energias para serem usadas para cálculo dos pesos de atenção
  e = mecanismo_atencao_camada1(concat)

  # Computa as energias
  energies = mecanismo_atencao_camada2(e)

  # Compra os pesos de atenção
  alphas = ativacao(energies)

  # Faz a combinação linear das atenções com as ativações pré-atenção para gerar contexto
  contexto = dotor([alphas, a])

  return contexto

# Modelo:

def modelo(Tx, Ty, n_pre, n_pos, human_vocab_size, machine_vocab_size, dicionario):
  """
    Define o modelo principal

    Inputs:
    Tx -- tamanho da sequencia de input
    Ty -- tamanho da sequencia de output
    n_pre -- numero de ativações pré-atenção
    n_pos -- numero de ativações pós-atenção
    human_vocab_size -- tamanho do human_vocab
    machine_vocab_size -- tamanho do  machine_vocab
    dicionario -- dicionario com as ferramentas compartilhadas

    Outputs:
    modelo
    """

  # Define inputs e estados inciais
  X = Input(shape=(Tx, human_vocab_size))
  s0 = Input(shape=(n_pos, ), name='s0')
  c0 = Input(shape=(n_pos, ), name='c0')
  s = s0
  c = c0
  outputs = []

  # LSTM pré - atenção
  a = Bidirectional(LSTM(n_pre, return_sequences=True))(X)

  # LSTM pós - atenção
  LSTM_pos_ativacao = dicionario['LSTM_pos_ativacao']
  output_layer = dicionario['output_layer']

  # Para cada passo de saída, calcula o contexto, estado e output
  for t in range(Ty):

    contexto = rede_atencao(a, s, dicionario)
    s, _, c = LSTM_pos_ativacao(contexto, initial_state=[s, c])
    out = output_layer(s)
    outputs.append(out)

  modelo = Model(inputs=[X, s0, c0], outputs=outputs)

  return modelo

# Treinamento:

def treinamento(Xoh, Yoh, modelo, m, n_pos, n_pre, epocas):
  """
    Treina o modelo

    Inputs:
    Xoh, Yoh -- tensores de One Hot Vectors de todos os exemplos
    modelo -- modelo para treinar
    m -- número de amostras de treino
    n_pre -- numero de ativações pré-atenção
    n_pos -- numero de ativações pós-atenção
    epocas -- numero de epocas para treinar

    Outputs:
    Salva os pesos treinados
    """

  # Separa os dados para treinar
  Xoh = Xoh[:m, :, :]
  Yoh = Yoh[:m, :, :]

  # Inputs para estados e contextos iniciais
  s0 = np.zeros((m, n_pos))
  c0 = np.zeros((m, n_pos))

  # Labels
  outputs = list(Yoh.swapaxes(0, 1))

  # Treinamento
  modelo.fit([Xoh, s0, c0], outputs, epochs=epocas, batch_size=100)

  # Salvar pesos
  modelo.save_weights(
      f'models/model_{epocas}-epocas_{n_pre}-preativacoes_{n_pos}-posativacoes.h5')

# Testes:

def testes(dataset, n_pos, Tx, human_vocab, inv_machine_vocab, modelo):
  """
    Treina o modelo

    Inputs:
    dataset -- lista de tuplas dos exemplos, tuplas do tipo ( input, output esperado )
    n_pos -- numero de ativações pós-atenção
    Tx -- tamanho da sequencia de input
    human_vocab -- dicionario mapeando os caracteres nas datas em formato humano para ́ındices inteiros
    inv_machine_vocab -- dicionario inverso de machine vocab, mapeando devolta dos ́ındices para os caracteres
    modelo -- modelo treinado

    Outputs:
    Mostra os exemplos originais, suas predições e sua versões corretas
    Mostra a acurácia destes testes
    """

  # Carrega os exemplos
  X, Y = zip(*dataset)  # Separa o dataset pros inputs e labels

  # Inicializa os estados, contextos e contador de acertos
  s0 = np.zeros((1, n_pos))
  c0 = np.zeros((1, n_pos))
  acertos = 0

  # Mostra os exemplos originais, suas predições e sua versões corretas
  for _ in range(len(X)):

    # Define o exemplo
    exemplo = X[_]

    # Converte para One Hot ser usado no modelo e ter sua predição
    original = string_to_int(exemplo, Tx, human_vocab)
    original = np.array(
        list(
            map(lambda x: to_categorical(x, num_classes=len(human_vocab)),
                original)))
    original = original.reshape(1, Tx, 37)
    pred = modelo.predict([original, s0, c0])
    pred = np.argmax(pred, axis=-1)
    output = []
    for i in pred:
      output.append(inv_machine_vocab.get(i[0]))
    predito = ''.join(output)

    print("Original:", exemplo)
    print()
    print("Predito:", predito)
    print()
    correto = Y[_]
    print("Correto:", correto)
    print()

    if predito == correto:
      acertos += 1

  acuracia = acertos / len(X)
  print("Acuracia:", acuracia * 100, '%')
  print()

# Mapa de atenção:

def plot_attention_map(modelx,
                       input_vocabulary,
                       inv_output_vocabulary,
                       text,
                       n_pos=128,
                       num=7):
  """
    Plot the attention map.

    """
  attention_map = np.zeros((10, 30))
  layer = modelx.get_layer('pesos_atencao')

  Ty, Tx = attention_map.shape

  human_vocab_size = 37

  # Well, this is cumbersome but this version of tensorflow-keras has a bug that affects the
  # reuse of layers in a model with the functional API.
  # So, I have to recreate the model based on the functional
  # components and connect then one by one.
  # ideally it can be done simply like this:
  # layer = modelx.layers[num]
  # f = Model(modelx.inputs, [layer.get_output_at(t) for t in range(Ty)])
  #

  X = modelx.inputs[0]
  s0 = modelx.inputs[1]
  c0 = modelx.inputs[2]
  s = s0
  c = s0

  a = modelx.layers[2](X)
  outputs = []

  for t in range(Ty):
    s_prev = s
    s_prev = modelx.layers[3](s_prev)
    concat = modelx.layers[4]([a, s_prev])
    e = modelx.layers[5](concat)
    energies = modelx.layers[6](e)
    alphas = modelx.layers[7](energies)
    context = modelx.layers[8]([alphas, a])
    # Don't forget to pass: initial_state = [hidden state, cell state] (≈ 1 line)
    s, _, c = modelx.layers[10](context, initial_state=[s, c])
    outputs.append(energies)

  f = Model(inputs=[X, s0, c0], outputs=outputs)

  s0 = np.zeros((1, n_pos))
  c0 = np.zeros((1, n_pos))
  encoded = np.array(string_to_int(text, Tx, input_vocabulary)).reshape(
      (1, 30))
  encoded = np.array(
      list(
          map(lambda x: to_categorical(x, num_classes=len(input_vocabulary)),
              encoded)))

  r = f([encoded, s0, c0])

  for t in range(Ty):
    for t_prime in range(Tx):
      attention_map[t][t_prime] = r[t][0, t_prime]

  # Normalize attention map
  row_max = attention_map.max(axis=1)
  attention_map = attention_map / row_max[:, None]

  prediction = modelx.predict([encoded, s0, c0])

  predicted_text = []
  for i in range(len(prediction)):
    predicted_text.append(int(np.argmax(prediction[i], axis=1)))

  predicted_text = list(predicted_text)

  for i in range(len(predicted_text)):
    string = inv_output_vocabulary.get(predicted_text[i])
    predicted_text[i] = string

  text_ = list(text)

  # get the lengths of the string
  input_length = len(text)
  output_length = Ty

  # Plot the attention_map
  plt.clf()
  f = plt.figure(figsize=(8, 8.5))
  ax = f.add_subplot(1, 1, 1)

  # add image
  i = ax.imshow(attention_map, interpolation='nearest', cmap='Blues')

  # add colorbar
  cbaxes = f.add_axes([0.2, 0, 0.6, 0.03])
  cbar = f.colorbar(i, cax=cbaxes, orientation='horizontal')
  cbar.ax.set_xlabel('Alpha value (Probability output of the "softmax")',
                     labelpad=2)

  # add labels
  ax.set_yticks(range(output_length))
  ax.set_yticklabels(predicted_text[:output_length])

  ax.set_xticks(range(input_length))
  ax.set_xticklabels(text_[:input_length], rotation=45)

  ax.set_xlabel('Input Sequence')
  ax.set_ylabel('Output Sequence')

  # add grid and legend
  ax.grid()

  #f.show()

  return attention_map