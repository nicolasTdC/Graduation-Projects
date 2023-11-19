/*

  floresta.c - Implementação do TAD para manipulação de uma árvore de busca binária (BST) 
               e pilha, utilizados no contexto de um jogo em uma floresta de monstros.

  Autor: Nicolas Toledo de Camargo 

  RA: 242524

  MC202G+H - 2 semestre de 2023.

*/

#include "floresta.h"

p_no_arvore cria_percursos(){
  NoArvore* NEW_ARVORE = malloc(sizeof(NoArvore));
  NEW_ARVORE->poder = -1;
  NEW_ARVORE->dir = NULL;
  NEW_ARVORE->esq = NULL;
  return NEW_ARVORE;
}

p_no_arvore insere_monstro(p_no_arvore raiz, int poder){
  if (raiz->poder == -1){
    raiz->poder = poder;
    return raiz;
  }

  NoArvore* NO_ATUAL = raiz;
  int PODER_ATUAL = NO_ATUAL->poder;

  NoArvore* NEW_NO = cria_percursos();

  while (1){
    while ( poder < PODER_ATUAL){
      if (NO_ATUAL->esq != NULL){
        NO_ATUAL = NO_ATUAL->esq;
        PODER_ATUAL = NO_ATUAL->poder;
      }
      else{
        NEW_NO->poder = poder;
        NO_ATUAL->esq = NEW_NO;
        return raiz;
      }
    }
    while ( poder > PODER_ATUAL){
      if (NO_ATUAL->dir != NULL){
        NO_ATUAL = NO_ATUAL->dir;
        PODER_ATUAL = NO_ATUAL->poder;
      }
      else{
        NEW_NO->poder = poder;
        NO_ATUAL->dir = NEW_NO;
        return raiz;
      }
    }
  }  
}

void busca_caminhos(p_no_arvore raiz, int vida_personagem) {
  NoPilha* TOPO_PILHA = cria_pilha();
  TOPO_PILHA->poder = raiz->poder;

  NoArvore* NO_ATUAL = raiz;

  int VIDA = vida_personagem;
  VIDA = VIDA - raiz->poder;

  int NUMERO_CAMINHOS = 0;
  NoPilha** GUARDAR_CAMINHOS = malloc(vida_personagem*sizeof(NoPilha*));

  NoArvore** CAMINHOS_NOS = malloc(vida_personagem*sizeof(NoArvore*));
  int CONTADOR_NOS = 0;
  int CONTADOR_NOS_TOTAL = 0;
  CAMINHOS_NOS[0] = raiz;

  int* NUMERO_MONSTROS_ABATIDOS = malloc(vida_personagem*sizeof(int));
  int INDICE_NUMERO_MONSTROS_ABATIDOS = 0;

  if ( VIDA <= 0 ){
    destroi_pilha(TOPO_PILHA);
    free(NUMERO_MONSTROS_ABATIDOS);
    free(GUARDAR_CAMINHOS);
    destroi_percursos(CAMINHOS_NOS[0]);
    free(CAMINHOS_NOS);
    printf("0");
    return;
  }

  while (TOPO_PILHA != NULL) {
    NoArvore* NO_ESQUERDA = NO_ATUAL->esq;
    while (NO_ESQUERDA != NULL && NO_ESQUERDA->poder != -1 && VIDA - NO_ESQUERDA->poder > 0 ) {
      int PODER = NO_ESQUERDA->poder;
      TOPO_PILHA = insere_na_pilha(TOPO_PILHA, PODER);
      VIDA = VIDA - PODER;
      CONTADOR_NOS++;
      CONTADOR_NOS_TOTAL++;
      CAMINHOS_NOS[CONTADOR_NOS] = NO_ESQUERDA;
      NO_ATUAL = NO_ESQUERDA;
      NO_ESQUERDA = NO_ATUAL->esq;
    }
    NoArvore* NO_DIREITA = NO_ATUAL->dir;
    if (NO_DIREITA != NULL && NO_DIREITA->poder != -1 &&  VIDA - NO_DIREITA->poder > 0 ) {
      int PODER = NO_DIREITA->poder;
      TOPO_PILHA = insere_na_pilha(TOPO_PILHA, PODER);
      VIDA = VIDA - PODER;
      CONTADOR_NOS++;
      CONTADOR_NOS_TOTAL++;
      CAMINHOS_NOS[CONTADOR_NOS] = NO_DIREITA;
      NO_ATUAL = NO_DIREITA;
    }
    else if ( NO_ESQUERDA == NULL &&  NO_DIREITA == NULL ) {

      NoPilha* TEMP_PILHA = cria_pilha();
      NoPilha* TOPO_ORIGINAL = TOPO_PILHA;
      NoPilha* TOPO_COPIA = TEMP_PILHA;

      while (TOPO_ORIGINAL != NULL) {
          TOPO_COPIA->poder = TOPO_ORIGINAL->poder;
          if (TOPO_ORIGINAL->prox != NULL) {
              TOPO_COPIA->prox = malloc(sizeof(NoPilha));
              TOPO_COPIA = TOPO_COPIA->prox;
          }
          TOPO_COPIA->prox = NULL;
          TOPO_ORIGINAL = TOPO_ORIGINAL->prox;
      }
      GUARDAR_CAMINHOS[NUMERO_CAMINHOS] = TEMP_PILHA;
      NUMERO_CAMINHOS++;
      int* PODER_REMOVIDO = malloc(sizeof(int));
      TOPO_PILHA = remove_da_pilha(TOPO_PILHA, PODER_REMOVIDO);
      VIDA = VIDA + *PODER_REMOVIDO;
      NO_ATUAL->poder = -1;
      NUMERO_MONSTROS_ABATIDOS[INDICE_NUMERO_MONSTROS_ABATIDOS] = CONTADOR_NOS;
      INDICE_NUMERO_MONSTROS_ABATIDOS++;
      CONTADOR_NOS--;
      NO_ATUAL = CAMINHOS_NOS[CONTADOR_NOS];
      free(PODER_REMOVIDO);
    }
    else {
      int* PODER_REMOVIDO = malloc(sizeof(int));
      TOPO_PILHA = remove_da_pilha(TOPO_PILHA, PODER_REMOVIDO);
      if (TOPO_PILHA == NULL) {
        NUMERO_MONSTROS_ABATIDOS[INDICE_NUMERO_MONSTROS_ABATIDOS] = '\0';

        int MAX = NUMERO_MONSTROS_ABATIDOS[0];
        int* INDICE_MAXIMO_MONSTROS = malloc((INDICE_NUMERO_MONSTROS_ABATIDOS+1)*sizeof(int));
        
        int _ = 0;
        int __ = 0;
        INDICE_MAXIMO_MONSTROS[__] = 0;

        while (NUMERO_MONSTROS_ABATIDOS[_] != '\0') {
          if (NUMERO_MONSTROS_ABATIDOS[_] > MAX) {
            MAX = NUMERO_MONSTROS_ABATIDOS[_];
            __ = 0;
            INDICE_MAXIMO_MONSTROS[__] = _;
          }
          else if (NUMERO_MONSTROS_ABATIDOS[_] == MAX) {
            INDICE_MAXIMO_MONSTROS[__] = _;
            __++;
          }
          _++;
        }
        _ = 0;
        if ( __ == 0 && NUMERO_MONSTROS_ABATIDOS[0] != 0) {
          __ ++;
        }
        INDICE_MAXIMO_MONSTROS[__] = '\0';
        printf("%d\n", __);
        for ( int CAMINHO = 0 ; CAMINHO < NUMERO_CAMINHOS ; CAMINHO++){
          if ( CAMINHO == INDICE_MAXIMO_MONSTROS[_] && _ < __ + 1){
            imprime_pilha(GUARDAR_CAMINHOS[CAMINHO]);
            if ( INDICE_MAXIMO_MONSTROS[ _+1 ] != '\0' ){
              printf("\n");
            }
            _ ++;
          }
          destroi_pilha(GUARDAR_CAMINHOS[CAMINHO]);
        }
        destroi_pilha(TOPO_PILHA);
        free(GUARDAR_CAMINHOS);
        destroi_percursos(CAMINHOS_NOS[0]);
        free(CAMINHOS_NOS);
        free(NUMERO_MONSTROS_ABATIDOS);
        free(INDICE_MAXIMO_MONSTROS);
        free(PODER_REMOVIDO);
        return;
      }
      VIDA = VIDA + *PODER_REMOVIDO;
      free(PODER_REMOVIDO);
      NO_ATUAL->poder = -1;
      CONTADOR_NOS--;
      NO_ATUAL = CAMINHOS_NOS[CONTADOR_NOS];
    }
  }
  destroi_pilha(TOPO_PILHA);
}
  
void destroi_percursos(p_no_arvore raiz){
  if (raiz == NULL) {
    return;
  }
  destroi_percursos(raiz->esq);
  destroi_percursos(raiz->dir);
  free(raiz);
}

p_no_pilha cria_pilha() {
  NoPilha* NEW_PILHA = malloc(sizeof(NoPilha));
  NEW_PILHA->poder = -1;
  NEW_PILHA->prox = NULL;
  return NEW_PILHA;
}

void imprime_pilha(p_no_pilha topo) { 
  NoPilha* TOPO_ATUAL = topo;
  while ( TOPO_ATUAL->prox != NULL) {
    printf("%d, " , TOPO_ATUAL->poder);
    TOPO_ATUAL = TOPO_ATUAL->prox;
  }
 
  printf("%d" , TOPO_ATUAL->poder);
}

p_no_pilha insere_na_pilha(p_no_pilha topo, int poder) {
  NoPilha* NEW_TOPO = malloc(sizeof(NoPilha));
  NEW_TOPO->poder = poder;
  NEW_TOPO->prox = topo;
  return NEW_TOPO;
}

p_no_pilha remove_da_pilha(p_no_pilha topo, int *poder) { 
  if (topo->prox == NULL){
    free(topo);
    return NULL;
  }
  NoPilha* NEW_TOPO = topo->prox;
  topo->prox = NULL;
  poder[0] = topo->poder;
  free(topo);
  return NEW_TOPO;
}

void destroi_pilha(p_no_pilha topo) {
  
  if ( topo == NULL) {
    return;
  }

  while (topo != NULL) {
    NoPilha* proximo = topo->prox;
    free(topo);
    topo = proximo;
  }
}