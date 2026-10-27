"""
Regra de negocio: Ordem de Servico (OS).

Cada veiculo atendido recebe uma OS, que acumula pecas e servicos ao
longo do diagnostico/atendimento. A OS so pode ser fechada depois que
a remontagem estiver concluida (flag 'remontagem_concluida').

Peças e serviços usados na OS: Lista propria (quantidade variavel,
adicionados/removidos ao longo do atendimento).
"""

from estruturas.lista import Lista


class ItemPeca:
    """Peca utilizada na OS (associada a um produto do estoque)."""

    def __init__(self, codigo_produto, nome, quantidade, preco_unitario):
        self.codigo_produto = codigo_produto
        self.nome = nome
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def valor_total(self):
        return self.quantidade * self.preco_unitario

    def __repr__(self):
        return f"{self.nome} x{self.quantidade} (R$ {self.valor_total():.2f})"


class ItemServico:
    """Servico de mao de obra realizado na OS (ex.: troca de pastilhas, alinhamento)."""

    def __init__(self, descricao, valor):
        self.descricao = descricao
        self.valor = valor

    def __repr__(self):
        return f"{self.descricao} (R$ {self.valor:.2f})"


class OrdemServico:
    """
    Representa uma Ordem de Servico aberta para um veiculo.

    Estado:
        aberta -> em andamento, pecas/servicos podem ser adicionados ou
                  removidos, remontagem ainda nao concluida
        fechada -> remontagem concluida e OS fechada (ponto de corte
                   para pagamento, dia 6)
    """

    _proximo_numero = 1  # contador simples para gerar numero de OS

    def __init__(self, placa_veiculo, nome_cliente, mecanico_responsavel, data_hora_abertura):
        self.numero = OrdemServico._proximo_numero
        OrdemServico._proximo_numero += 1

        self.placa_veiculo = placa_veiculo
        self.nome_cliente = nome_cliente
        self.mecanico_responsavel = mecanico_responsavel
        self.data_hora_abertura = data_hora_abertura

        self.pecas = Lista()
        self.servicos = Lista()

        self.remontagem_concluida = False
        self.fechada = False

    # --- Pecas ---

    def adicionar_peca(self, item: ItemPeca):
        if self.fechada:
            raise ValueError(f"OS #{self.numero} ja esta fechada, nao e possivel adicionar pecas")
        self.pecas.inserir(item)

    def remover_peca(self, codigo_produto):
        """Remove uma peca da OS (ex.: cliente nao autorizou o servico)."""
        if self.fechada:
            raise ValueError(f"OS #{self.numero} ja esta fechada, nao e possivel remover pecas")
        return self.pecas.remover(lambda p: p.codigo_produto == codigo_produto)

    # --- Servicos ---

    def adicionar_servico(self, item: ItemServico):
        if self.fechada:
            raise ValueError(f"OS #{self.numero} ja esta fechada, nao e possivel adicionar servicos")
        self.servicos.inserir(item)

    def remover_servico(self, descricao):
        if self.fechada:
            raise ValueError(f"OS #{self.numero} ja esta fechada, nao e possivel remover servicos")
        return self.servicos.remover(lambda s: s.descricao == descricao)

    # --- Totais ---

    def valor_total_pecas(self):
        total = 0.0
        for peca in self.pecas.percorrer():
            total += peca.valor_total()
        return total

    def valor_total_servicos(self):
        total = 0.0
        for servico in self.servicos.percorrer():
            total += servico.valor
        return total

    def valor_total(self):
        return self.valor_total_pecas() + self.valor_total_servicos()

    # --- Ciclo de vida ---

    def concluir_remontagem(self):
        self.remontagem_concluida = True

    def fechar(self):
        """So pode fechar depois que a remontagem estiver concluida."""
        if not self.remontagem_concluida:
            raise ValueError(
                f"OS #{self.numero} nao pode ser fechada: remontagem ainda nao concluida"
            )
        self.fechada = True

    def __repr__(self):
        status = "FECHADA" if self.fechada else "ABERTA"
        return (f"OS #{self.numero} [{status}] - {self.placa_veiculo} "
                f"- {self.nome_cliente} - Total: R$ {self.valor_total():.2f}")


class ControleOrdensServico:
    """
    Gerencia a Lista de ordens de servico abertas/fechadas na oficina.
    """

    def __init__(self):
        self.ordens = Lista()

    def abrir_os(self, placa_veiculo, nome_cliente, mecanico_responsavel, data_hora_abertura):
        os_nova = OrdemServico(placa_veiculo, nome_cliente, mecanico_responsavel, data_hora_abertura)
        self.ordens.inserir(os_nova)
        return os_nova

    def buscar_por_numero(self, numero):
        return self.ordens.buscar(lambda os: os.numero == numero)

    def buscar_por_placa(self, placa_veiculo):
        """Retorna a OS aberta mais recente para a placa (busca simples)."""
        encontrada = None
        for os_atual in self.ordens.percorrer():
            if os_atual.placa_veiculo == placa_veiculo and not os_atual.fechada:
                encontrada = os_atual
        return encontrada


if __name__ == "__main__":
    # Teste rapido manual
    controle = ControleOrdensServico()

    os1 = controle.abrir_os("ABC1234", "Joao Silva", "Mecanico Carlos", "26/10 09:00")
    os1.adicionar_peca(ItemPeca("PST001", "Pastilha dianteira", 1, 120.0))
    os1.adicionar_servico(ItemServico("Troca de pastilhas", 80.0))
    os1.adicionar_servico(ItemServico("Alinhamento", 60.0))

    print(os1)
    print("Pecas:", list(os1.pecas.percorrer()))
    print("Servicos:", list(os1.servicos.percorrer()))

    # cliente nao autorizou o alinhamento
    os1.remover_servico("Alinhamento")
    print("\nApos remover alinhamento:")
    print(os1)

    try:
        os1.fechar()
        print("ERRO: deveria ter lancado excecao (remontagem nao concluida)!")
    except ValueError as e:
        print("\nExcecao esperada capturada:", e)

    os1.concluir_remontagem()
    os1.fechar()
    print("\nApos concluir remontagem e fechar:")
    print(os1)
