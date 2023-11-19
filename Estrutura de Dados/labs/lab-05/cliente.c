/*

  cliente.c - Aplicação principal que utiliza as estruturas de dados 'árvore binária de busca' e 'pilha',
              simulando um cenário de aventura em uma floresta misteriosa, onde estratégias de sobrevivência
              contra monstros são testadas, como parte das atividades do Laboratório 5 de MC202G+H.

  Autor: Nicolas Toledo de Camargo 

  RA: 242524

  MC202G+H - 2º semestre de 2023.

*/

#include "floresta.h"

int main(){
  int NUMERO_MONSTROS; 
  scanf("%d", &NUMERO_MONSTROS);
  
  NoArvore* ARVORE = cria_percursos();

  for ( int MONSTRO = 0; MONSTRO < NUMERO_MONSTROS; MONSTRO++){
    int PODER;
    scanf("%d", &PODER);
    ARVORE = insere_monstro(ARVORE, PODER);
  }

  int VIDA_PERSONAGEM;
  scanf("%d", &VIDA_PERSONAGEM);

  busca_caminhos(ARVORE, VIDA_PERSONAGEM);

  return 0;
}