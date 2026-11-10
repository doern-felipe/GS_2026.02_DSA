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
        """Percorre os nos com um laço while e exibe cada registro."""
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


if __name__ == "__main__":
    lista = ListaEncadeada()

    r1 = Registro(1, "Aula de reforço", "Oferta", "Educação",
                  "Reforço de matemática", "Saber ler", "Biblioteca", 2, "Ana")
    r2 = Registro(2, "Consertar torneira", "Pedido", "Manutenção",
                  "Torneira da cozinha vazando", "Trazer chave", "Casa da Maria",
                  1, "Maria")
    r3 = Registro(3, "Horta comunitária", "Projeto", "Horta",
                  "Plantio coletivo", "Disponibilidade aos sábados",
                  "Praça Central", 4, "Carlos")

    print(lista.inserir_fim(r1))  # True
    print(lista.inserir_fim(r2))  # True
    print(lista.inserir_fim(r3))  # True
    print("Tamanho:", lista.tamanho)  # 3

    atual = lista.cabeca
    while atual is not None:
        print(atual.dados.titulo)
        atual = atual.proximo