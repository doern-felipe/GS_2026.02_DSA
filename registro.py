class Registro:
    """Representa um registro do banco de tempo 'Tempo Vale'."""

    def __init__(self, id: int, titulo: str, tipo: str, categoria: str,
                 descricao: str, requisitos: str, local: str,
                 horas: int, responsavel: str) -> None:
        self.id = id                    # identificador único do registro
        self.titulo = titulo            # título da oferta/pedido/projeto
        self.tipo = tipo                # Oferta, Pedido ou Projeto
        self.categoria = categoria      # ex.: Educação, Informática
        self.descricao = descricao      # descrição do que será feito
        self.requisitos = requisitos    # pré-requisitos para participar
        self.local = local              # local onde a ação acontece
        self.horas = horas              # horas de ajuda (1 hora = 1 crédito)
        self.responsavel = responsavel  # pessoa responsável pelo registro

    def __str__(self) -> str:
        """Retorna uma exibição formatada do registro."""
        return (
            f"ID: {self.id}\n"
            f"Título: {self.titulo}\n"
            f"Tipo: {self.tipo}\n"
            f"Categoria: {self.categoria}\n"
            f"Descrição: {self.descricao}\n"
            f"Requisitos: {self.requisitos}\n"
            f"Local: {self.local}\n"
            f"Horas: {self.horas}\n"
            f"Responsável: {self.responsavel}"
        )