/*

  gerenciador.c - Implementação do TAD para manipulação de uma árvore de busca binária (ABB) 
                  utilizada no contexto de gerenciamento de estoque de uma loja de elementos químicos.

  Autor: Nicolas Toledo de Camargo

  RA: 242524

  MC202G+H - 2º semestre de 2023.

*/

#include "gerenciador.h"

p_no criar_arvore(){
  p_no NOVA_ARVORE = malloc(sizeof(No));
  NOVA_ARVORE->numero_atomico = -1;
  NOVA_ARVORE->simbolo[0] = '\0';
  NOVA_ARVORE->esq = NULL;
  NOVA_ARVORE->dir = NULL;
  return NOVA_ARVORE;
}

p_no inserir(p_no raiz, int numero_atomico, char *simbolo){
  if ( raiz == NULL ){
    raiz = criar_arvore();
    raiz->numero_atomico = numero_atomico;
    strcpy(raiz->simbolo, simbolo);  
  }
  else if ( numero_atomico < raiz->numero_atomico ){
    raiz->esq = inserir(raiz->esq, numero_atomico, simbolo);
  }
  else if ( numero_atomico > raiz->numero_atomico ) {
    raiz->dir = inserir(raiz->dir, numero_atomico, simbolo);
  }
  return raiz;
}

p_no minimo(p_no raiz) {
  if (raiz == NULL || raiz->esq == NULL){
    return raiz;
  }
  return minimo(raiz->esq);
}

p_no buscar(p_no raiz, int numero_atomico) {

  if ( raiz == NULL || raiz->numero_atomico == numero_atomico) {
    return raiz;
  }
  else if ( numero_atomico < raiz->numero_atomico ) {
    return buscar(raiz->esq, numero_atomico);
  }
  else {
    return buscar(raiz->dir, numero_atomico);
  }
}

p_no remover(p_no raiz, char *simbolo){
  if (raiz == NULL) {
    return raiz;
  }
 
  if (strcmp(simbolo, raiz->simbolo) != 0) {
    raiz->esq = remover(raiz->esq, simbolo);
  } 
  if (strcmp(simbolo, raiz->simbolo) != 0) {
    raiz->dir = remover(raiz->dir, simbolo);
  } 
  else {
    if (raiz->esq == NULL) {
      p_no temp = raiz->dir;
      free(raiz);
      return temp;
    } 
    else if (raiz->dir == NULL) {
      p_no temp = raiz->esq;
      free(raiz);
      return temp;
    }
    
    p_no temp = minimo(raiz->dir);

    raiz->numero_atomico = temp->numero_atomico;
    strcpy(raiz->simbolo, temp->simbolo);

    raiz->dir = remover(raiz->dir, raiz->simbolo);
  }
  
  return raiz;
}

p_no maximo(p_no raiz){
  if (raiz == NULL || raiz->dir == NULL){
    return raiz;
  }
  return maximo(raiz->dir);
}

void destruir_arvore(p_no raiz) {
  if (raiz == NULL) {
    return;
  }
  destruir_arvore(raiz->esq);
  destruir_arvore(raiz->dir);
  free(raiz);
}

void imprimir( p_no raiz, p_no maximo ) {

  if ( ( raiz == maximo &&  raiz->esq != NULL)) {
    imprimir(raiz->esq, maximo);
    printf("%s\n", raiz->simbolo);
  }

  else if ( (raiz != NULL && raiz != maximo) || ( raiz == maximo &&  raiz->esq != NULL)) {
    imprimir(raiz->esq, maximo);

    int tamanho_string = strlen(raiz->simbolo);
    char ultimo_char = raiz->simbolo[tamanho_string - 1];
    if ( ultimo_char == '\r' || ultimo_char == '\n'){
      printf("%.*s, ", (int)strlen(raiz->simbolo) - 1, raiz->simbolo);

    }
    else {
      printf("%s, ", raiz->simbolo);
    }
    imprimir(raiz->dir, maximo);
  }
  
  else if (raiz == maximo ) {
    printf("%s\n", raiz->simbolo);
  }
}