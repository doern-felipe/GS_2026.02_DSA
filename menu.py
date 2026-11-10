from registro import Registro
from lista import ListaEncadeada
from algoritmos import buscar_por_categoria, buscar_por_titulo, ordenar_lista

TIPOS_VALIDOS = ("Oferta", "Pedido", "Projeto")


class SairPrograma(Exception):
    """Sinaliza que o usuário quer encerrar o programa (Ctrl+C/Ctrl+D)."""


def ler_texto(campo: str) -> str:
    """Lê um texto não vazio do terminal."""
    while True:
        try:
            valor = input(f"{campo}: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma
        if valor == "":
            print(f"O campo '{campo}' não pode ficar vazio.")
            continue
        return valor


def ler_inteiro_positivo(campo: str) -> int:
    """Lê um número inteiro maior que zero."""
    while True:
        try:
            valor = int(input(f"{campo}: ").strip())
        except ValueError:
            print(f"O campo '{campo}' deve ser um número inteiro.")
            continue
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma
        if valor <= 0:
            print(f"O campo '{campo}' deve ser maior que zero.")
            continue
        return valor


def ler_tipo() -> str:
    """Lê o tipo, aceitando apenas Oferta, Pedido ou Projeto."""
    while True:
        valor = ler_texto("Tipo (Oferta/Pedido/Projeto)")
        if valor in TIPOS_VALIDOS:
            return valor
        print("Tipo inválido. Digite Oferta, Pedido ou Projeto.")


def ler_id(lista: ListaEncadeada) -> int:
    """Lê um ID inteiro que ainda não exista na lista."""
    while True:
        try:
            id = int(input("ID: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            continue
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma
        if lista.buscar_por_id(id) is not None:
            print(f"O ID {id} já existe. Escolha outro.")
            continue
        return id


def cadastrar_registro(lista: ListaEncadeada) -> None:
    """Lê os campos, valida e insere; permite cadastrar vários em sequência."""
    while True:
        print("\n--- Cadastro de Registro ---")
        id = ler_id(lista)
        titulo = ler_texto("Título")
        tipo = ler_tipo()
        categoria = ler_texto("Categoria")
        descricao = ler_texto("Descrição")
        requisitos = ler_texto("Requisitos")
        local = ler_texto("Local")
        horas = ler_inteiro_positivo("Horas")
        responsavel = ler_texto("Responsável")

        registro = Registro(id, titulo, tipo, categoria, descricao,
                            requisitos, local, horas, responsavel)
        lista.inserir_fim(registro)
        print(f"Registro '{titulo}' cadastrado com sucesso!")

        try:
            resposta = input("Cadastrar outro? (s/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma
        if resposta != "s":
            break


def ler_inteiro(campo: str) -> int:
    """Lê um número inteiro do terminal."""
    while True:
        try:
            return int(input(f"{campo}: ").strip())
        except ValueError:
            print(f"O campo '{campo}' deve ser um número inteiro.")
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma


def consultar_por_id(lista: ListaEncadeada) -> None:
    """Consulta um registro pelo ID e exibe todos os campos."""
    if len(lista) == 0:                     # lista vazia: avisa antes de pedir
        print("A lista está vazia. Nenhum registro para consultar.")
        return

    id = ler_inteiro("ID para consulta")
    registro = lista.buscar_por_id(id)
    print()
    if registro is None:
        print(f"Registro não encontrado (ID {id}).")
    else:
        print("--- Registro encontrado ---")
        print(registro)                     # usa o __str__ de Registro


def pesquisar(lista: ListaEncadeada) -> None:
    """Submenu de pesquisa por título ou categoria."""
    if len(lista) == 0:                     # lista vazia
        print("A lista está vazia. Nenhum registro para pesquisar.")
        return

    print("\n--- Pesquisar ---")
    print("1 - Por título")
    print("2 - Por categoria")
    print("0 - Voltar")
    opcao = ler_inteiro("Opção")

    if opcao == 0:
        return
    if opcao == 1:
        termo = ler_texto("Título (termo de busca)")
        print("\n--- Resultado da pesquisa por título ---")
        total = buscar_por_titulo(lista, termo)
    elif opcao == 2:
        termo = ler_texto("Categoria (termo de busca)")
        print("\n--- Resultado da pesquisa por categoria ---")
        total = buscar_por_categoria(lista, termo)
    else:
        print("Opção inválida.")
        return

    if total == 0:
        print("Nenhum registro encontrado.")
    else:
        print("-" * 50)
        print(f"Total de registros encontrados: {total}")


def ler_texto_opcional(campo: str, valor_atual: str) -> str:
    """Lê um texto; Enter mantém o valor atual."""
    while True:
        try:
            valor = input(f"{campo} [{valor_atual}]: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma
        if valor == "":
            return valor_atual
        return valor


def ler_tipo_opcional(valor_atual: str) -> str:
    """Lê o tipo; Enter mantém o valor atual."""
    while True:
        try:
            valor = input(f"Tipo (Oferta/Pedido/Projeto) [{valor_atual}]: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma
        if valor == "":
            return valor_atual
        if valor in TIPOS_VALIDOS:
            return valor
        print("Tipo inválido. Digite Oferta, Pedido ou Projeto.")


def ler_inteiro_positivo_opcional(campo: str, valor_atual: int) -> int:
    """Lê um inteiro > 0; Enter mantém o valor atual."""
    while True:
        try:
            valor = input(f"{campo} [{valor_atual}]: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma
        if valor == "":
            return valor_atual
        try:
            numero = int(valor)
        except ValueError:
            print(f"O campo '{campo}' deve ser um número inteiro.")
            continue
        if numero <= 0:
            print(f"O campo '{campo}' deve ser maior que zero.")
            continue
        return numero


def atualizar_registro(lista: ListaEncadeada) -> None:
    """Atualiza os campos de um registro existente, preservando o nó."""
    if len(lista) == 0:                     # lista vazia
        print("A lista está vazia. Nenhum registro para atualizar.")
        return

    id = ler_inteiro("ID do registro a atualizar")
    registro = lista.buscar_por_id(id)
    if registro is None:
        print(f"Registro não encontrado (ID {id}).")
        return

    print("\n--- Registro atual ---")
    print(registro)
    print("\nPressione Enter para manter o valor atual.")

    # altera os campos do próprio registro (o nó e os ponteiros ficam intactos)
    registro.titulo = ler_texto_opcional("Título", registro.titulo)
    registro.tipo = ler_tipo_opcional(registro.tipo)
    registro.categoria = ler_texto_opcional("Categoria", registro.categoria)
    registro.descricao = ler_texto_opcional("Descrição", registro.descricao)
    registro.requisitos = ler_texto_opcional("Requisitos", registro.requisitos)
    registro.local = ler_texto_opcional("Local", registro.local)
    registro.horas = ler_inteiro_positivo_opcional("Horas", registro.horas)
    registro.responsavel = ler_texto_opcional("Responsável", registro.responsavel)

    print("\nRegistro atualizado com sucesso!")
    print(registro)


def excluir_registro(lista: ListaEncadeada) -> None:
    """Exclui um registro após confirmação do usuário."""
    if len(lista) == 0:                     # lista vazia
        print("A lista está vazia. Nenhum registro para excluir.")
        return

    id = ler_inteiro("ID do registro a excluir")
    registro = lista.buscar_por_id(id)
    if registro is None:                    # ID inexistente
        print(f"Registro não encontrado (ID {id}).")
        return

    print("\n--- Registro a excluir ---")
    print(registro)

    try:
        resposta = input("\nConfirmar exclusão? (s/n): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        raise SairPrograma

    if resposta != "s":
        print("Exclusão cancelada.")
        return

    if lista.remover_por_id(id):
        print("Registro excluído com sucesso!")
    else:
        print(f"Não foi possível excluir o registro (ID {id}).")


def ordenar_e_exibir(lista: ListaEncadeada) -> None:
    """Submenu de ordenação e exibição da lista."""
    if len(lista) == 0:                         # lista vazia
        print("A lista está vazia. Nenhum registro para ordenar.")
        lista.imprimir_lista()
        return
    if len(lista) == 1:                         # só um registro
        print("A lista tem apenas um registro; nada a ordenar.")
        lista.imprimir_lista()
        return

    print("\n--- Ordenar e exibir ---")
    print("1 - Título (A-Z)")
    print("2 - Categoria")
    print("3 - Horas (crescente)")
    print("0 - Voltar")
    opcao = ler_inteiro("Opção")

    criterios = {1: "titulo", 2: "categoria", 3: "horas"}
    if opcao == 0:
        return
    if opcao not in criterios:
        print("Opção inválida.")
        return

    ordenar_lista(lista, criterios[opcao])
    print(f"\nLista ordenada por {criterios[opcao]}:")
    lista.imprimir_lista()


def analise(lista: ListaEncadeada) -> None:
    """Percorre a lista e exibe totais e contagem por categoria."""
    if len(lista) == 0:                         # lista vazia
        print("A lista está vazia. Nenhuma análise a fazer.")
        return

    total_registros = 0
    total_horas = 0
    categorias = {}                             # conta categorias só aqui

    atual = lista.cabeca
    while atual is not None:
        total_registros += 1
        total_horas += atual.dados.horas
        categoria = atual.dados.categoria
        categorias[categoria] = categorias.get(categoria, 0) + 1
        atual = atual.proximo

    print("\n--- Análise do banco de tempo ---")
    print(f"Total de registros: {total_registros}")
    print(f"Total de horas (créditos): {total_horas}")
    print("Registros por categoria:")
    for categoria, quantidade in categorias.items():
        print(f"  {categoria}: {quantidade}")


def exibir_menu() -> None:
    """Exibe o menu principal."""
    print("\n" + "=" * 50)
    print("TEMPO VALE - Banco de tempo e serviços comunitários")
    print("=" * 50)
    print("1 - Cadastrar registro")
    print("2 - Consultar por ID")
    print("3 - Pesquisar")
    print("4 - Atualizar registro")
    print("5 - Excluir registro")
    print("6 - Ordenar e exibir")
    print("7 - Análise")
    print("0 - Sair")
    print("=" * 50)


def executar_opcao(lista: ListaEncadeada, opcao: int) -> None:
    """Executa a opção escolhida no menu."""
    if opcao == 1:
        cadastrar_registro(lista)
    elif opcao == 2:
        consultar_por_id(lista)
    elif opcao == 3:
        pesquisar(lista)
    elif opcao == 4:
        atualizar_registro(lista)
    elif opcao == 5:
        excluir_registro(lista)
    elif opcao == 6:
        ordenar_e_exibir(lista)
    elif opcao == 7:
        analise(lista)
    elif opcao == 0:
        print("Encerrando o programa. Obrigado por usar o Tempo Vale!")
    else:
        print("Opção inválida. Tente novamente.")


def main() -> None:
    """Loop principal do menu."""
    lista = ListaEncadeada()
    try:
        while True:
            exibir_menu()
            opcao = ler_inteiro("Opção")
            if opcao == 0:
                executar_opcao(lista, opcao)
                break
            executar_opcao(lista, opcao)
    except SairPrograma:
        print("\nEncerrando o programa. Obrigado por usar o Tempo Vale!")
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando o programa. Obrigado por usar o Tempo Vale!")