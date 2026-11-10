from lista import ListaEncadeada
from registro import Registro


def buscar_por_titulo(lista: ListaEncadeada, termo: str) -> int:
    """Busca linear por título (case-insensitive). Imprime e retorna o total."""
    termo = termo.lower()
    encontrado = 0
    atual = lista.cabeca
    while atual is not None:
        if termo in atual.dados.titulo.lower():
            print("-" * 50)
            print(atual.dados)
            encontrado += 1
        atual = atual.proximo
    return encontrado


def buscar_por_categoria(lista: ListaEncadeada, termo: str) -> int:
    """Busca linear por categoria (case-insensitive). Imprime e retorna o total."""
    termo = termo.lower()
    encontrado = 0
    atual = lista.cabeca
    while atual is not None:
        if termo in atual.dados.categoria.lower():
            print("-" * 50)
            print(atual.dados)
            encontrado += 1
        atual = atual.proximo
    return encontrado


def _comparar(criterio: str, reg1: Registro, reg2: Registro) -> bool:
    """Retorna True se reg1 deve vir antes de reg2 no critério."""
    if criterio == "titulo":
        return reg1.titulo.lower() < reg2.titulo.lower()
    if criterio == "categoria":
        return reg1.categoria.lower() < reg2.categoria.lower()
    if criterio == "horas":
        return reg1.horas < reg2.horas
    return False


def ordenar_lista(lista: ListaEncadeada, criterio: str) -> None:
    """Ordena a lista encadeada pelo critério (selection sort).

    Troca apenas os dados entre nós, mantendo as referências intactas.
    """
    if lista.cabeca is None or lista.cabeca.proximo is None:
        return

    inicio = lista.cabeca
    while inicio is not None:
        menor = inicio
        atual = inicio.proximo
        while atual is not None:
            if _comparar(criterio, atual.dados, menor.dados):
                menor = atual
            atual = atual.proximo
        if menor is not inicio:                 # troca só os dados
            inicio.dados, menor.dados = menor.dados, inicio.dados
        inicio = inicio.proximo