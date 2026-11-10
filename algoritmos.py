from lista import ListaEncadeada


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