"""
Regra de negocio: Controle de Pagamento.

Pagamento e feito no fechamento da OS, via PIX, cartao (avista ou
parcelado) ou dinheiro. Cada pagamento registra quem pagou, a OS
referente, forma de pagamento, parcelas (quando cartao), valores de
pecas/mao de obra/total e data/hora.
"""

from estruturas.lista import Lista

FORMAS_PAGAMENTO = ("PIX", "CARTAO", "DINHEIRO")


class Pagamento:
    """Representa um pagamento realizado no fechamento de uma OS."""

    def __init__(self, nome_pagador, numero_os, forma_pagamento,
                 valor_pecas, valor_mao_de_obra, data_hora_pagamento,
                 parcelas=1):
        if forma_pagamento not in FORMAS_PAGAMENTO:
            raise ValueError(f"Forma de pagamento invalida: {forma_pagamento}")
        if forma_pagamento != "CARTAO" and parcelas != 1:
            raise ValueError("Parcelamento so e valido para pagamento no cartao")

        self.nome_pagador = nome_pagador
        self.numero_os = numero_os
        self.forma_pagamento = forma_pagamento
        self.parcelas = parcelas
        self.valor_pecas = valor_pecas
        self.valor_mao_de_obra = valor_mao_de_obra
        self.data_hora_pagamento = data_hora_pagamento

    def valor_total_pago(self):
        return self.valor_pecas + self.valor_mao_de_obra

    def __repr__(self):
        parc = f" ({self.parcelas}x)" if self.forma_pagamento == "CARTAO" else ""
        return (f"Pagamento OS#{self.numero_os} - {self.nome_pagador} - "
                f"{self.forma_pagamento}{parc} - R$ {self.valor_total_pago():.2f}")


class ControleFinanceiro:
    """
    Gerencia a Lista de pagamentos realizados na oficina.
    """

    def __init__(self):
        self.pagamentos = Lista()

    def registrar_pagamento(self, pagamento: Pagamento):
        self.pagamentos.inserir(pagamento)

    def buscar_por_os(self, numero_os):
        return self.pagamentos.buscar(lambda p: p.numero_os == numero_os)

    def faturamento_total(self):
        total = 0.0
        for pagamento in self.pagamentos.percorrer():
            total += pagamento.valor_total_pago()
        return total


if __name__ == "__main__":
    # Teste rapido manual
    controle = ControleFinanceiro()

    pagamento = Pagamento(
        nome_pagador="Joao Silva",
        numero_os=1,
        forma_pagamento="CARTAO",
        valor_pecas=120.0,
        valor_mao_de_obra=80.0,
        data_hora_pagamento="26/10 14:30",
        parcelas=3,
    )
    controle.registrar_pagamento(pagamento)

    print(pagamento)
    print("Faturamento total:", controle.faturamento_total())
