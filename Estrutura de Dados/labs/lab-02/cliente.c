/*

  cliente.c - Programa cliente para testar o tipo e os operadores
              para manipulação de fichas de referências bibliográficas
              do Laboratório 2 de MC202GH.

  MC202G+H - 2 semestre de 2023.

  Autor: Nicolas Toledo de Camargo RA 242524

*/

#include "ficha.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 1000

int main ()
{
  int tamanho_comando;
  int tamanho_fichario = 0;
  int numero_fichas;
  char* string_numero;
  ficha ** fichario;
  while (1){
    char *comando = malloc(MAX*sizeof(char));
    int i = 0;
    while (1) {
      int ch = getchar();

      if (ch == '\n' || ch == EOF) {
        break;
      }

      if (i < MAX - 1) { 
        comando[i] = (char) ch;
        i++;
      }

    }
    comando[i] = '\0';
    if ( comando[0] == 'F'){
      if (tamanho_fichario != 0){
        for (int _ = 0 ; _ < tamanho_fichario ; _++){
          destroi_ficha(fichario[_]);
        }
        free(fichario);
      }
      free(comando);
      return 0;
    }
    else if ( comando[0] == 'N'){
      tamanho_comando = strlen(comando);
      string_numero = malloc(( tamanho_comando +1 -2 ) *sizeof(char));//
      for (int _ = 2;_<tamanho_comando ;_++){
        string_numero[_-2] = comando[_];
      }
      string_numero[tamanho_comando -2] = '\0';
      tamanho_fichario = atoi(string_numero);
      free(string_numero );
      fichario = cria_fichario (tamanho_fichario);
    }
    else if ( comando[0] == 'I'){
      tamanho_comando = strlen(comando);
      string_numero = malloc(( tamanho_comando +1 -2) *sizeof(char));
      for (int _ = 2;_<tamanho_comando ;_++){
          string_numero[_-2] = comando[_];
      }
      string_numero[tamanho_comando - 2] = '\0';
      numero_fichas = atoi(string_numero);
      free(string_numero );

      for (int _ = 0 ; _ < numero_fichas; _++){
        insere_ficha (fichario, tamanho_fichario, le_ficha());
      }
    }
    else if ( comando[0] == 'P'){
      for (int _ = 0 ; _ < tamanho_fichario; _++){
        if ( (fichario[_])->doi   != NULL){
          imprime_ficha(fichario[_]);
        }
      }
    }
    else if ( comando[0] == 'B'){
      tamanho_comando = strlen(comando);
      string_numero = malloc(( tamanho_comando +1 -2) *sizeof(char));//doi
      for (int _ = 2;_<tamanho_comando ;_++){
          string_numero[_-2] = comando[_];
      }
      string_numero[tamanho_comando -2] = '\0';
      int flag_busca = busca_ficha (fichario, tamanho_fichario, string_numero);
      if (flag_busca == -1){
        //printf("DOI %s inexistente\n",string_numero);
        printf("DOI %.*s inexistente\n", (int)strlen(string_numero) -1, string_numero);
        
      }
      else if (flag_busca != -1){
        if (fichario[flag_busca]->n_autores>3){
          printf("%s %s %s et al. (%d) %d\n", fichario[flag_busca]->autor[0], fichario[flag_busca]->autor[1],
                  fichario[flag_busca]->autor[2], fichario[flag_busca]->ano,fichario[flag_busca]->volume);
          }
        else if (fichario[flag_busca]->n_autores==3){
          printf("%s %s %s (%d) %d\n", fichario[flag_busca]->autor[0], fichario[flag_busca]->autor[1],
                  fichario[flag_busca]->autor[2], fichario[flag_busca]->ano,fichario[flag_busca]->volume);
        }
        else if (fichario[flag_busca]->n_autores==2){
          printf("%s %s (%d) %d\n", fichario[flag_busca]->autor[0], fichario[flag_busca]->autor[1],
                  fichario[flag_busca]->ano,fichario[flag_busca]->volume);
        }
        else if (fichario[flag_busca]->n_autores==2){
          printf("%s (%d) %d\n", fichario[flag_busca]->autor[0],
                fichario[flag_busca]->ano,fichario[flag_busca]->volume);
        }
      }
      free(string_numero );
    }
    else if ( comando[0] == 'R'){
      tamanho_comando = strlen(comando);
      string_numero = malloc(( tamanho_comando +1 -2) *sizeof(char));//doi
      for (int _ = 2;_<tamanho_comando ;_++){
        string_numero[_-2] = comando[_];
      }
      string_numero[tamanho_comando - 2] = '\0';
      remove_ficha (fichario, tamanho_fichario, string_numero);
      free(string_numero );
    }
    free(comando);
  }
}
