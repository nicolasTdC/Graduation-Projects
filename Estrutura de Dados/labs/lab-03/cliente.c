/*

  cliente.c - Programa cliente para testar o tipo e os operadores
              para solucionar labirintos no Trabalho de MC202GH.

  Autor: Nicolas Toledo de Camargo RA242524

  MC202GH - 2 semestre de 2023.

*/

#include <stdlib.h>
#include <stdio.h>
#include "labirinto.h"
int main ()
{
  char* dim_linha = malloc ((100)*sizeof(char));
  char* dim_coluna = malloc ((100)*sizeof(char));
  int i = 0;
  while (1) {
    int ch = getchar();
    if (ch == '\n' || ch == EOF || ch == 'x') {
        break;
    }
    dim_linha[i] = (char) ch;
    i++;
  }
  dim_linha[i] = '\0';
  i = 0;
  while (1) {
    int ch = getchar();
    if (ch == '\n' || ch == EOF || ch == 'x') {
      break;
    }
    dim_coluna[i] = (char) ch;
    i++;
  }
  dim_coluna[i] = '\0';
  int linhas = atoi(dim_linha), colunas = atoi(dim_coluna);

  labirinto* l = criar_labirinto(linhas, colunas);
  ler_labirinto(l); 
  int** coords_iniciais = malloc((2)*sizeof(int*));
  for ( int eixo = 0; eixo < 2; eixo++ ) { 
    coords_iniciais[eixo] = malloc(linhas*2*colunas*sizeof(int));
  }
  int index_coords_inciais_x = 0;
  int index_coords_inciais_y = 0;
  for ( int i = 0 ; i < linhas ; i++) {
    for ( int j = 0 ; j < 2* colunas - 1 ; j++) {
      if ( (l->matriz)[i][j] == 'P' ) {
        coords_iniciais[1][index_coords_inciais_y] = i;
        coords_iniciais[0][index_coords_inciais_x] = j;
        index_coords_inciais_y++;
        index_coords_inciais_x++;
      }
    }
  }
  labirinto* labirinto_copia = criar_labirinto(linhas, colunas);
  for ( int pessoa = 0 ; pessoa<index_coords_inciais_y; pessoa++) {
    for (int i = 0; i < linhas; i++) {
      for (int j = 0; j < 2*colunas - 1; j++) {
        (labirinto_copia->matriz)[i][j] = (l->matriz)[i][j];
      }
      (labirinto_copia->matriz)[i][2*colunas - 1] = '\0';
    }
    for ( int ja_resgatado = 0; ja_resgatado < pessoa; ja_resgatado++){
      (labirinto_copia->matriz)[coords_iniciais[1][ja_resgatado]][coords_iniciais[0][ja_resgatado]] = '0';
    }
    labirinto_copia = buscar_saida(labirinto_copia, coords_iniciais[0][pessoa],coords_iniciais[1][pessoa]);
    imprimir_labirinto(labirinto_copia);
    if ( pessoa < index_coords_inciais_y -1 ) {
      printf("\n");
    }
  }
  destruir_labirinto(labirinto_copia);
  for (int _ = 0; _ < 2; _++) {
    free(coords_iniciais[_]);
  }
  free(coords_iniciais);
  free(dim_linha);
  free(dim_coluna);
  destruir_labirinto(l);
  return 0;
}


