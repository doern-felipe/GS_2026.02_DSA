#include "lista.h"
#include <stdlib.h>

// Cria uma lista vazia.
Lista criar_lista(void) {
    Lista lista;
    lista.cabeca = NULL;
    lista.tamanho = 0;
    return lista;
}

// Cria um no solto com o registro; retorna NULL se malloc falhar.
No *criar_no(Registro dados) {
    No *novo = (No *)malloc(sizeof(No));
    if (novo == NULL) {
        return NULL;
    }
    novo->dados = dados;
    novo->proximo = NULL;
    return novo;
}