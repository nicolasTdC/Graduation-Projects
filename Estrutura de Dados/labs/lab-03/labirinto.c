/*

  labirinto.c - Implementação dos operadores para manipulação de labirintos 
                no Trabalho de MC202GH.

 Autores: Nicolas Toledo de Camargo RA242524

  MC202GH - 2 semestre de 2023.

*/
#include <stdlib.h>
#include <stdio.h>
#include "labirinto.h"

labirinto* criar_labirinto(int linhas, int colunas){
  labirinto* new_labirinto = malloc(sizeof(labirinto));
  new_labirinto->colunas = colunas;
  new_labirinto->linhas = linhas;
  new_labirinto->matriz = malloc(linhas*(sizeof(char*)));
  for (int _ = 0 ; _ < linhas ; _++) {
    (new_labirinto->matriz)[_] = malloc ( (1+2*colunas)*sizeof(char));
  }
  return new_labirinto;
}

void ler_labirinto(labirinto *l){
  for ( int row = 0; row<l->linhas;row++){
    int col = 0;
    char c;
    while (1) {
      c = getchar();
      if (c == '\n' || c == '\0') {
        (l->matriz)[row][col] = '\0';
        break; 
      }
      (l->matriz)[row][col] = (char) c;
      col++;
    }
  }
}

void imprimir_labirinto(labirinto *l){
 for (int i = 0; i < l->linhas; i++) {
    printf("%s\n", (l->matriz)[i]);
  }
}

void destruir_labirinto(labirinto *l){
  for (int i = 0; i < l->linhas; i++) {
    free((l->matriz)[i]);
  }
  free(l->matriz);
  free(l);
}

int buscar_saida_recursivamente(char **matriz, int linhas, int colunas, int x_atual, int y_atual){
  if ( matriz[y_atual][x_atual] == 'P' || matriz[y_atual][x_atual] == 'X' ){
    static int movimentos[4][2] = { {2,0} , {0,1} , {-2,0}, {0,-1} };
    int prox_x, prox_y;
    for (int opcao = 0; opcao < 4; opcao++) { 
      prox_x = x_atual + movimentos[opcao][0];
      prox_y = y_atual + movimentos[opcao][1];
      if((prox_y >= 0) && (prox_y < linhas) && (prox_x >= 0) && (prox_x < 2*colunas)){
        if (matriz[prox_y][prox_x] == '0' || matriz[prox_y][prox_x] == 'S' ) {
          if ( matriz[prox_y][prox_x] == 'S' ) {
            matriz[prox_y][prox_x] = 'X';
            return 1;
          }            
          matriz[prox_y][prox_x] = 'X';
          if ( buscar_saida_recursivamente(matriz, linhas, colunas, prox_x, prox_y) ) {
            return 1;
          }
          matriz[prox_y][prox_x] = '0';
        }       
      }
    }
  }
  return 0;
} 

labirinto* buscar_saida(labirinto *l, int x, int y) { 
  buscar_saida_recursivamente(l->matriz, l->linhas, l->colunas, x, y);
  return l;
}