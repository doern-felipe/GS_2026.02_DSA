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

    def inserir_fim(self, registro: Registro) -> bool:
        """Insere o registro no fim da lista. Retorna True se inseriu."""
        novo_no = No(registro)          # cria o nó já com proximo = None
        if self.cabeca is None:         # lista vazia: novo nó vira a cabeça
            self.cabeca = novo_no
        else:                           # percorre até o último nó
            atual = self.cabeca
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no     # último nó aponta para o novo
        self.tamanho += 1
        return True

    def imprimir_lista(self) -> None:
        """Percorre os nós com um laço while e exibe cada registro."""
        if self.cabeca is None:                 # lista vazia
            print("A lista está vazia. Nenhum registro cadastrado.")
            return

        atual = self.cabeca                     # começa no primeiro nó
        print("=" * 50)
        print("REGISTROS CADASTRADOS")
        print("=" * 50)
        while atual is not None:                # enquanto houver nó
            print("-" * 50)
            print(atual.dados)                  # usa o __str__ de Registro
            atual = atual.proximo               # avança para o próximo nó
        print("-" * 50)
        print(f"Total de registros: {self.tamanho}")
        print("=" * 50)

    def remover_por_id(self, id: int) -> bool:
        """Remove o nó com o ID informado. Retorna True se removeu."""
        if self.cabeca is None:                     # lista vazia
            return False

        # Caso 1: remoção da cabeça
        if self.cabeca.dados.id == id:
            removido = self.cabeca
            self.cabeca = self.cabeca.proximo       # cabeça vira o próximo
            removido.proximo = None                 # desliga o nó removido
            self.tamanho -= 1
            return True

        # Caso 2: remoção do meio ou do fim
        anterior = self.cabeca
        atual = self.cabeca.proximo
        while atual is not None:
            if atual.dados.id == id:
                anterior.proximo = atual.proximo    # pula o nó removido
                atual.proximo = None                # desliga o nó removido
                self.tamanho -= 1
                return True
            anterior = atual                        # avança os dois ponteiros
            atual = atual.proximo
        return False                                # ID não encontrado

    def limpar(self) -> None:
        """Zera a lista, desligando cada nó antes de descartá-lo."""
        atual = self.cabeca
        while atual is not None:
            proximo = atual.proximo     # guarda o próximo antes de desligar
            atual.proximo = None        # desliga o nó corrente
            atual = proximo             # avança
        self.cabeca = None              # lista vazia
        self.tamanho = 0

    def __len__(self) -> int:
        """Retorna a quantidade de nós da lista."""
        return self.tamanho


if __name__ == "__main__":
    lista = ListaEncadeada()
    for i in range(1, 6):
        lista.inserir_fim(Registro(i, f"Registro {i}", "Oferta", "Educação",
                                   "Descrição", "Requisitos", "Local", i,
                                   f"Responsável {i}"))

    print("Lista inicial:")
    lista.imprimir_lista()                          # 1 2 3 4 5
    print("Tamanho (__len__):", len(lista))         # 5

    print("\nRemovendo a CABEÇA (id 1):", lista.remover_por_id(1))
    lista.imprimir_lista()                          # 2 3 4 5

    print("\nRemovendo o MEIO (id 3):", lista.remover_por_id(3))
    lista.imprimir_lista()                          # 2 4 5

    print("\nRemovendo o FIM (id 5):", lista.remover_por_id(5))
    lista.imprimir_lista()                          # 2 4

    print("\nRemovendo ID inexistente (id 99):", lista.remover_por_id(99))

    print("\nLimpando a lista:")
    lista.limpar()
    lista.imprimir_lista()                          # lista vazia
    print("Tamanho após limpar:", len(lista))       # 0