"""
Testes manuais do Controle de Pagamento.
Rodar com: python -m testes.teste_pagamento (a partir da raiz do projeto)
"""

from modelos.pagamento import ControleFinanceiro, Pagamento


def testar_registro_pagamento():
    print("== Registro de pagamento (PIX) ==")
    controle = ControleFinanceiro()
    pagamento = Pagamento(
        nome_pagador="Maria Souza",
        numero_os=5,
        forma_pagamento="PIX",
        valor_pecas=0.0,
        valor_mao_de_obra=60.0,
        data_hora_pagamento="27/10 09:00",
    )
    controle.registrar_pagamento(pagamento)
    print(pagamento)
    assert pagamento.valor_total_pago() == 60.0


def testar_parcelamento_invalido():
    print("\n== Parcelamento fora do cartao (deve lancar erro) ==")
    try:
        Pagamento(
            nome_pagador="Pedro Costa",
            numero_os=6,
            forma_pagamento="DINHEIRO",
            valor_pecas=50.0,
            valor_mao_de_obra=20.0,
            data_hora_pagamento="27/10 09:10",
            parcelas=3,
        )
        print("ERRO: deveria ter lancado excecao!")
    except ValueError as e:
        print("Excecao esperada capturada:", e)


def testar_forma_pagamento_invalida():
    print("\n== Forma de pagamento invalida (deve lancar erro) ==")
    try:
        Pagamento(
            nome_pagador="Ana",
            numero_os=7,
            forma_pagamento="BOLETO",
            valor_pecas=10.0,
            valor_mao_de_obra=10.0,
            data_hora_pagamento="27/10 09:20",
        )
        print("ERRO: deveria ter lancado excecao!")
    except ValueError as e:
        print("Excecao esperada capturada:", e)


def testar_faturamento_total():
    print("\n== Faturamento total com varios pagamentos ==")
    controle = ControleFinanceiro()
    controle.registrar_pagamento(Pagamento("Cliente A", 1, "PIX", 100.0, 50.0, "27/10 10:00"))
    controle.registrar_pagamento(Pagamento("Cliente B", 2, "DINHEIRO", 30.0, 20.0, "27/10 11:00"))
    print("Faturamento total:", controle.faturamento_total())
    assert controle.faturamento_total() == 200.0


if __name__ == "__main__":
    testar_registro_pagamento()
    testar_parcelamento_invalido()
    testar_forma_pagamento_invalida()
    testar_faturamento_total()
    print("\nTodos os testes passaram.")
