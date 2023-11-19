#include<stdio.h>

#define MAX 1000

unsigned int busca_motivo ( char s[] , char m[] );

void converter_minusculo(char string[], int tamanho);

int tamanho_string(char string[]);
/*
int tamanho_string(char string[]) {
    int i;
    for (i = 0; (i < MAX) && (string[i] != '\0'); i++);
    return i;
}
*/
int tamanho_string(char string[]) {
    int tam = 0;
    while (string[tam] != '\0') {
        tam++;
    }
    return tam;
}

void converter_minusculo(char string[], int tamanho) {
    for (int i = 0; i < tamanho; i++) {
        if (string[i] <= 90 && string[i] >= 65) {
            string[i] = string[i] + 32;
        }
    }
}

unsigned int busca_motivo(char s[], char m[]) {
    int tamanho_s = tamanho_string(s);
    int tamanho_m = tamanho_string(m);
    converter_minusculo(s, tamanho_s);
    converter_minusculo(m, tamanho_m);
    //int flag_comeca_com_plus;
    //int pos;
    unsigned int resposta = 0; 
   // char s_anterior; 
    char s_posterior; 
    int index_posterior;
    int igual_dps_plus;
    for(int index_s = 0; index_s<tamanho_s; index_s++){ //para cada letra de s
        while (s[index_s] == '\n' || s[index_s] == ' ') {
                index_s++;
            }
       // flag_comeca_com_plus = 0;
       // pos=0;
        int temp_index_s = index_s; //var temporaria para andar as letras dentro de cada loop
        for(int index_m = 0; index_m<=tamanho_m; index_m++){ //para cada caracter de m
            if( index_m == tamanho_m){
                resposta+=1;
                index_s = temp_index_s-1;
                /*
                if ( flag_comeca_com_plus ==1 ) { 
                    index_s = index_s + pos;
                }
                */                
                break;
            }

            while (s[temp_index_s] == '\n' || s[temp_index_s] == ' ') {
                temp_index_s++;
            }

            if( ( index_m == tamanho_m-1 ) && ( m[index_m] == s[temp_index_s] ) ) {
                resposta+=1;
               // index_s++;
                index_s = temp_index_s;
/*  
                if ( flag_comeca_com_plus ==1 ) { 
                    index_s = index_s + pos;
                }
*/ 
                break;
            }
            if ( ( m[index_m] == s[temp_index_s] )){
              //  s_anterior = s[temp_index_s];
                index_posterior=temp_index_s+1;
                s_posterior = s[index_posterior];
                while (s[index_posterior] == '\n' || s[index_posterior] == ' ') {
                    index_posterior++;
                    s_posterior = s[index_posterior];
                }
                if( (m[index_m+1] == '+' )){
                    igual_dps_plus = 0;
                    int m_temp = index_m;
                    while ( ( m_temp < tamanho_m-2 ) && ( ( m[m_temp+2] == s[temp_index_s] ) || ( m[m_temp+2] == '+' ) ) ) {
                        if ( m[m_temp+2] == s[temp_index_s] ) {
                            igual_dps_plus++;
                        }                  
                        m_temp++;    
                    } 

                    /*
                    if ( index_m ==0 ) {
                        
                        if ( ( index_m < tamanho_m-2 ) && ( m[index_m+2] != m[index_m] ) ){
                            if (s[temp_index_s+1]==m[index_m]) {
                        //        flag_comeca_com_plus=1;
                            }
                            while (s[temp_index_s]==m[index_m] || s[temp_index_s] == '\n' || s[temp_index_s] == ' '){
                                temp_index_s++;
                                if (s_anterior==s[temp_index_s] || s[temp_index_s] == '\n' || s[temp_index_s] == ' ') {
                                    pos++;
                                }
                            }
                            temp_index_s++;
                            for (int volta_temp_index_s = 0; volta_temp_index_s< igual_dps_plus; volta_temp_index_s++){
                                temp_index_s--;
                            }
                           // temp_index_s = temp_index_s - igual_dps_plus+1;
                        }
                        else if (s_posterior==s[temp_index_s]){
                            while (s_posterior==s[temp_index_s] || s[temp_index_s] == '\n' || s[temp_index_s] == ' '){
                                temp_index_s++;
                                index_posterior++;
                                s_posterior = s[index_posterior];
                                while (s[s_posterior] == '\n' || s[s_posterior] == ' ') {
                                    index_posterior++;
                                    s_posterior = s[index_posterior];
                                }
                                pos++;
                            }
                            temp_index_s++;
                            for (int volta_temp_index_s = 0; volta_temp_index_s< igual_dps_plus; volta_temp_index_s++){
                                temp_index_s--;
                            }
                           // temp_index_s = temp_index_s - igual_dps_plus+1;
                        }
                        index_m++;
                                                                                        
                    }
                    */
                    if ( ( index_m < tamanho_m-2 ) && (m[index_m+2] != m[index_m] )){
                        while (s[temp_index_s]==m[index_m] || s[temp_index_s] == '\n' || s[temp_index_s] == ' '){
                            temp_index_s++;
                        }
                        //temp_index_s++;
                        for (int volta_temp_index_s = 0; volta_temp_index_s< igual_dps_plus; volta_temp_index_s++){
                            temp_index_s--;
                            while ( s[temp_index_s] == ' ' || s[temp_index_s] == '\n'){
                                temp_index_s--;
                            }
                        }
                        // temp_index_s = temp_index_s - igual_dps_plus+1;
                        index_m++;              
                    }

                    else if (s_posterior==s[temp_index_s] && ( index_m < tamanho_m-2 ) && (m[index_m+2] == m[index_m] )){
                        while (s_posterior==s[temp_index_s]){
                            temp_index_s++;
                            index_posterior++;
                            s_posterior = s[index_posterior];
                            while (s[index_posterior] == '\n' || s[index_posterior] == ' ') {
                                index_posterior++;
                                s_posterior = s[index_posterior];
                            }
                            while (s[temp_index_s] == '\n' || s[temp_index_s] == ' ') {
                                temp_index_s++;
                            }              
                        }
                        index_m++;
                                   
                        temp_index_s++;
                        for (int volta_temp_index_s = 0; volta_temp_index_s< igual_dps_plus; volta_temp_index_s++){
                            temp_index_s--;
                            while ( s[temp_index_s] == ' ' || s[temp_index_s] == '\n'){
                                temp_index_s--;
                            }
                        }
                        // temp_index_s = temp_index_s - igual_dps_plus+1;
                        

                    }

                    else if( index_m == tamanho_m-2 && s[temp_index_s]==m[index_m] ) {
                            
                        resposta+=1;
                            //index_s++;
                        

                        index_s = temp_index_s;

                        while (s[index_s]== m[index_m] || s[index_s] == '\n' || s[index_s] == ' '){
                            index_s++;
                        }
                        index_s--;
                        /*
                        if ( flag_comeca_com_plus ==1 ) { 
                            index_s = index_s + pos;
                        }
                        */
                        break;
                    }                    
                }
                else{
                    temp_index_s++;
                    continue;
                }
            }
            else {
                break;
            }
        }
        
    }
    return resposta;
}

int main(){
    char s[MAX], m[MAX];
    int i = 0;
    scanf("%s ", m);
    do
    {
        s[i] = getchar ();
        if (s[i] != EOF)
        {
        i++;
        s[i] = '0';
        }
    }
    while (s[i] != EOF);
    s[i] = '\0';
    unsigned int resposta;
    resposta = busca_motivo(s, m);
    printf("%u\n",resposta);
    return 0;
}
