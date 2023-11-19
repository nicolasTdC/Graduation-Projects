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
  int numero_fichas;
  char* string_numero;
  p_no fichario;
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
      destroi_fichas(fichario);
      free(comando);
      return 0;
    }
    else if ( comando[0] == 'N'){
      fichario = cria_fichario ();
    }
    else if ( comando[0] == 'I'){
      tamanho_comando = strlen(comando);
      string_numero = malloc(( tamanho_comando + 1 - 2) *sizeof(char));
      for (int _ = 2;_<tamanho_comando ;_++){
          string_numero[_-2] = comando[_];
      }
      string_numero[tamanho_comando - 2] = '\0';
      numero_fichas = atoi(string_numero);
      free(string_numero );
      for (int _ = 0 ; _ < numero_fichas; _++){
        fichario = insere_ficha (fichario, le_ficha());
        if (fichario->prox->doi == NULL){
          free(fichario->prox);
          fichario->prox = NULL;
        }
      }
    }
    else if ( comando[0] == 'P'){
      imprime_ficha(fichario);
    }
    else if ( comando[0] == 'B'){
      tamanho_comando = strlen(comando);
      string_numero = malloc(( tamanho_comando +1 -2) *sizeof(char));//doi
      for (int _ = 2;_<tamanho_comando ;_++){
          string_numero[_-2] = comando[_];
      }
      string_numero[tamanho_comando -2] = '\0';
      p_no flag_busca = busca_ficha(fichario, string_numero);
      if (flag_busca == NULL){
        string_numero[strcspn(string_numero, "\n")] = '\0';
        string_numero[strcspn(string_numero, "\r")] = '\0';
        printf("DOI %s inexistente\n", string_numero);
      }
      else if (flag_busca != NULL){
        if (flag_busca->n_autores>3){
          printf("%s %s %s et al. (%d) %d\n", flag_busca->autor[0], flag_busca->autor[1],
                  flag_busca->autor[2], flag_busca->ano,flag_busca->volume);
          }
        else if (flag_busca->n_autores==3){
          printf("%s %s %s (%d) %d\n", flag_busca->autor[0], flag_busca->autor[1],
                  flag_busca->autor[2], flag_busca->ano,flag_busca->volume);
        }
        else if (flag_busca->n_autores==2){
          printf("%s %s (%d) %d\n", flag_busca->autor[0], flag_busca->autor[1],
                  flag_busca->ano,flag_busca->volume);
        }
        else if (flag_busca->n_autores==2){
          printf("%s (%d) %d\n", flag_busca->autor[0],
                flag_busca->ano,flag_busca->volume);
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
      fichario = remove_ficha(fichario, string_numero);
      free(string_numero );
    }
    free(comando);
  }
}