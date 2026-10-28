"""
Regra de negocio: Controle do que foi consumido / Fechamento integrado.

Integra, no momento do fechamento da OS:
    1. Baixa no estoque das pecas e fluidos utilizados (ControleEstoque)
    2. Registro do pagamento (ControleFinanceiro)
    3. Registro de qual cliente/veiculo consumiu quais pecas
       (rastreabilidade, com base no valor da OS e na baixa de estoque)

Nao introduz uma nova estrutura de dados: orquestra as ja existentes
(Estoque, Ordem de Servico, Pagamento), mantendo a separacao de
responsabilidades (cada modulo cuida da sua parte; este cuida da
integracao entre eles).
"""

from estruturas.lista import Lista


class RegistroConsumo:
    """
    Registro de rastreabilidade: o que um cliente/veiculo consumiu em
    uma OS, com os lotes efetivamente baixados do estoque.
    """

    def __init__(self, numero_os, placa_veiculo, nome_cliente, lotes_consumidos, valor_os):
        self.numero_os = numero_os
        self.placa_veiculo = placa_veiculo
        self.nome_cliente = nome_cliente
        self.lotes_consumidos = lotes_consumidos  # dict: codigo_produto -> Lista de Lote
        self.valor_os = valor_os

    def __repr__(self):
        return (f"Consumo OS#{self.numero_os} - {self.nome_cliente} ({self.placa_veiculo}) "
                f"- Total: R$ {self.valor_os:.2f}")


class ControleFechamento:
    """
    Orquestra o fechamento de uma OS: baixa de estoque + pagamento +
    rastreabilidade do consumo.
    """

    def __init__(self, controle_estoque, controle_financeiro):
        self.controle_estoque = controle_estoque
        self.controle_financeiro = controle_financeiro
        self.registros_consumo = Lista()

    def fechar_os_com_pagamento(self, ordem_servico, forma_pagamento, data_hora_pagamento, parcelas=1):
        """
        Fecha a OS (exige remontagem concluida), baixa do estoque cada
        peca utilizada (pelo lote mais antigo), registra o pagamento e
        gera o registro de rastreabilidade do consumo.
        """
        from modelos.pagamento import Pagamento

        # 1. Baixa no estoque, pelas pecas registradas na OS
        lotes_consumidos_por_produto = {}
        for item_peca in ordem_servico.pecas.percorrer():
            consumidos = self.controle_estoque.baixar_estoque(
                item_peca.codigo_produto, item_peca.quantidade
            )
            lotes_consumidos_por_produto[item_peca.codigo_produto] = consumidos

        # 2. Fecha a OS (valida remontagem concluida)
        ordem_servico.fechar()

        # 3. Registra o pagamento
        pagamento = Pagamento(
            nome_pagador=ordem_servico.nome_cliente,
            numero_os=ordem_servico.numero,
            forma_pagamento=forma_pagamento,
            valor_pecas=ordem_servico.valor_total_pecas(),
            valor_mao_de_obra=ordem_servico.valor_total_servicos(),
            data_hora_pagamento=data_hora_pagamento,
            parcelas=parcelas,
        )
        self.controle_financeiro.registrar_pagamento(pagamento)

        # 4. Registra rastreabilidade do consumo
        registro = RegistroConsumo(
            numero_os=ordem_servico.numero,
            placa_veiculo=ordem_servico.placa_veiculo,
            nome_cliente=ordem_servico.nome_cliente,
            lotes_consumidos=lotes_consumidos_por_produto,
            valor_os=ordem_servico.valor_total(),
        )
        self.registros_consumo.inserir(registro)

        return pagamento, registro
