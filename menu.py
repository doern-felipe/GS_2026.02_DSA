from registro import Registro
from lista import ListaEncadeada
from algoritmos import (buscar_por_categoria, buscar_por_titulo,
                        normalizar_texto, ordenar_lista)

TIPOS_VALIDOS = ("Oferta", "Pedido", "Projeto")

# limites de tamanho dos campos de texto
MAX_TITULO = 100
MAX_TIPO = 10
MAX_CATEGORIA = 50
MAX_DESCRICAO = 200
MAX_REQUISITOS = 150
MAX_LOCAL = 100
MAX_RESPONSAVEL = 60


class SairPrograma(Exception):
    """Sinaliza que o usuário quer encerrar o programa (Ctrl+C/Ctrl+D)."""


def ler_texto(prompt: str, obrigatorio: bool = True,
              max_len: int | None = None) -> str:
    """Lê um texto do terminal, validando vazio e tamanho máximo."""
    while True:
        try:
            valor = input(f"{prompt}: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma
        if obrigatorio and valor == "":
            print(f"O campo '{prompt}' não pode ficar vazio.")
            continue
        if max_len is not None and len(valor) > max_len:
            print(f"O texto deve ter no máximo {max_len} caracteres.")
            continue
        return valor


def ler_inteiro(prompt: str, minimo: int | None = None,
                maximo: int | None = None) -> int:
    """Lê um número inteiro, validando texto, vazio e faixa."""
    while True:
        try:
            valor = int(input(f"{prompt}: ").strip())
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            continue
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma
        if minimo is not None and valor < minimo:
            print(f"O valor deve ser no mínimo {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"O valor deve ser no máximo {maximo}.")
            continue
        return valor


def _normalizar_tipo(valor: str) -> str | None:
    """Converte o texto em um dos tipos válidos, ou None se inválido."""
    normalizado = normalizar_texto(valor)
    for tipo in TIPOS_VALIDOS:
        if normalizar_texto(tipo) == normalizado:
            return tipo
    return None


def ler_tipo() -> str:
    """Lê o tipo, aceitando Oferta, Pedido ou Projeto em qualquer caixa."""
    while True:
        valor = ler_texto("Tipo (Oferta/Pedido/Projeto)", max_len=MAX_TIPO)
        tipo = _normalizar_tipo(valor)
        if tipo is not None:
            return tipo
        print("Tipo inválido. Digite Oferta, Pedido ou Projeto.")


def ler_tipo_opcional(valor_atual: str) -> str:
    """Lê o tipo; Enter mantém o valor atual."""
    while True:
        valor = ler_texto(f"Tipo (Oferta/Pedido/Projeto) [{valor_atual}]",
                          obrigatorio=False, max_len=MAX_TIPO)
        if valor == "":
            return valor_atual
        tipo = _normalizar_tipo(valor)
        if tipo is not None:
            return tipo
        print("Tipo inválido. Digite Oferta, Pedido ou Projeto.")


def ler_id(lista: ListaEncadeada) -> int | None:
    """Lê um ID inteiro que ainda não exista na lista. None cancela."""
    while True:
        id = ler_inteiro("ID (0 para cancelar)", minimo=0)
        if id == 0:                             # cancela o cadastro
            print("Cadastro cancelado.")
            return None
        existente = lista.buscar_por_id(id)
        if existente is not None:               # ID duplicado
            print(f"O ID {id} já é usado pelo registro abaixo:")
            print(existente)
            print("Tente outro ID ou digite 0 para cancelar.")
            continue
        return id


def cadastrar_registro(lista: ListaEncadeada) -> None:
    """Lê os campos, valida e insere; permite cadastrar vários em sequência."""
    while True:
        print("\n--- Cadastro de Registro ---")
        id = ler_id(lista)
        if id is None:                          # cancelou o cadastro
            return
        titulo = ler_texto("Título", max_len=MAX_TITULO)
        tipo = ler_tipo()
        categoria = ler_texto("Categoria", max_len=MAX_CATEGORIA)
        descricao = ler_texto("Descrição", max_len=MAX_DESCRICAO)
        requisitos = ler_texto("Requisitos", max_len=MAX_REQUISITOS)
        local = ler_texto("Local", max_len=MAX_LOCAL)
        horas = ler_inteiro("Horas", minimo=1)
        responsavel = ler_texto("Responsável", max_len=MAX_RESPONSAVEL)

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


def consultar_por_id(lista: ListaEncadeada) -> None:
    """Consulta um registro pelo ID e exibe todos os campos."""
    if len(lista) == 0:                         # lista vazia
        print("A lista está vazia. Nenhum registro para consultar.")
        return

    id = ler_inteiro("ID para consulta")
    registro = lista.buscar_por_id(id)
    print()
    if registro is None:
        print(f"Registro não encontrado (ID {id}).")
    else:
        print("--- Registro encontrado ---")
        print(registro)                         # usa o __str__ de Registro


def pesquisar(lista: ListaEncadeada) -> None:
    """Submenu de pesquisa por título ou categoria."""
    if len(lista) == 0:                         # lista vazia
        print("A lista está vazia. Nenhum registro para pesquisar.")
        return

    print("\n--- Pesquisar ---")
    print("1 - Por título")
    print("2 - Por categoria")
    print("0 - Voltar")
    opcao = ler_inteiro("Opção", 0, 2)

    if opcao == 0:
        return
    if opcao == 1:
        termo = ler_texto("Título (termo de busca)")
        print("\n--- Resultado da pesquisa por título ---")
        total = buscar_por_titulo(lista, termo)
    else:
        termo = ler_texto("Categoria (termo de busca)")
        print("\n--- Resultado da pesquisa por categoria ---")
        total = buscar_por_categoria(lista, termo)

    if total == 0:
        print("Nenhum registro encontrado.")
    else:
        print("-" * 50)
        print(f"Total de registros encontrados: {total}")


def ler_texto_opcional(campo: str, valor_atual: str, max_len: int) -> str:
    """Lê um texto; Enter mantém o valor atual."""
    valor = ler_texto(f"{campo} [{valor_atual}]", obrigatorio=False,
                      max_len=max_len)
    return valor if valor != "" else valor_atual


def ler_inteiro_positivo_opcional(campo: str, valor_atual: int) -> int:
    """Lê um inteiro > 0; Enter mantém o valor atual."""
    while True:
        valor = ler_texto(f"{campo} [{valor_atual}]", obrigatorio=False)
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
    if len(lista) == 0:                         # lista vazia
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
    registro.titulo = ler_texto_opcional("Título", registro.titulo, MAX_TITULO)
    registro.tipo = ler_tipo_opcional(registro.tipo)
    registro.categoria = ler_texto_opcional("Categoria", registro.categoria,
                                            MAX_CATEGORIA)
    registro.descricao = ler_texto_opcional("Descrição", registro.descricao,
                                            MAX_DESCRICAO)
    registro.requisitos = ler_texto_opcional("Requisitos", registro.requisitos,
                                             MAX_REQUISITOS)
    registro.local = ler_texto_opcional("Local", registro.local, MAX_LOCAL)
    registro.horas = ler_inteiro_positivo_opcional("Horas", registro.horas)
    registro.responsavel = ler_texto_opcional("Responsável", registro.responsavel,
                                              MAX_RESPONSAVEL)

    print("\nRegistro atualizado com sucesso!")
    print(registro)


def excluir_registro(lista: ListaEncadeada) -> None:
    """Exclui um registro após confirmação do usuário."""
    if len(lista) == 0:                         # lista vazia
        print("A lista está vazia. Nenhum registro para excluir.")
        return

    id = ler_inteiro("ID do registro a excluir")
    registro = lista.buscar_por_id(id)
    if registro is None:                        # ID inexistente
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
    opcao = ler_inteiro("Opção", 0, 3)

    criterios = {1: "titulo", 2: "categoria", 3: "horas"}
    if opcao == 0:
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
    categorias: dict[str, tuple[str, int]] = {}  # conta categorias só aqui

    atual = lista.cabeca
    while atual is not None:
        total_registros += 1
        total_horas += atual.dados.horas
        categoria = atual.dados.categoria
        chave = normalizar_texto(categoria)
        if chave in categorias:
            nome, quantidade = categorias[chave]
            categorias[chave] = (nome, quantidade + 1)
        else:
            categorias[chave] = (categoria, 1)
        atual = atual.proximo

    print("\n--- Análise do banco de tempo ---")
    print(f"Total de registros: {total_registros}")
    print(f"Total de horas (créditos): {total_horas}")
    print("Registros por categoria:")
    for nome, quantidade in categorias.values():
        print(f"  {nome}: {quantidade}")


def exibir_menu() -> None:
    """Exibe o menu principal."""
    print("\n" + "=" * 50)
    print("COLABRE - Banco de tempo e serviços comunitários")
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


def ler_opcao_menu() -> int:
    """Lê a opção do menu principal, aceitando apenas 0 a 7."""
    while True:
        try:
            valor = int(input("Opção: ").strip())
        except ValueError:
            print("Opção inválida. Digite um número de 0 a 7.")
            continue
        except (EOFError, KeyboardInterrupt):
            raise SairPrograma
        if valor < 0 or valor > 7:
            print("Opção inválida. Digite um número de 0 a 7.")
            continue
        return valor


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
    else:  # opcao == 0
        print("Encerrando o programa. Obrigado por usar o Colabre!")


def main() -> None:
    """Loop principal do menu."""
    lista = ListaEncadeada()
    try:
        while True:
            exibir_menu()
            opcao = ler_opcao_menu()
            if opcao == 0:
                executar_opcao(lista, opcao)
                break
            executar_opcao(lista, opcao)
    except SairPrograma:
        print("\nEncerrando o programa. Obrigado por usar o Colabre!")
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando o programa. Obrigado por usar o Colabre!")