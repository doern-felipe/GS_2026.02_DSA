from registro import Registro


class No:
    """Nó da lista encadeada simples."""

    def __init__(self, dados: Registro) -> None:
        self.dados = dados      # registro guardado neste nó
        self.proximo = None     # referência para o próximo nó (None no fim)


class ListaEncadeada:
    """Lista encadeada simples sem ponteiro para a cauda."""

    def __init__(self) -> None:
        self.cabeca = None      # primeiro nó (None se a lista estiver vazia)
        self.tamanho = 0        # quantidade de nós na lista