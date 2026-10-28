"""
Simulacao de atendimento completo da Oficina Mecanica.

Segue exatamente o fluxo pedido no enunciado:
    1. Chegada do veiculo e entrada na espera (normal ou guincho).
    2. Chamada do proximo veiculo quando um box fica livre e abertura da OS.
    3. Diagnostico na arvore de componentes, marcando as pecas com defeito.
    4. Inclusao de pecas e servicos na OS, com baixa no estoque pelo lote
       mais antigo.
    5. Fechamento da OS e pagamento.

Integra os modulos de todos os dias:
    Dia 1: estruturas genericas + ControleAtendimento
    Dia 2: ControleClientes (clientes e veiculos)
    Dia 3: ControleDiagnostico (arvore de componentes)
    Dia 4: ControleEstoque + ControleOrdensServico
    Dia 5: ControleFinanceiro + ControleFechamento
"""

from modelos.atendimento import ControleAtendimento, VeiculoEspera
from modelos.cliente import ControleClientes, Cliente, Veiculo
from modelos.diagnostico import ControleDiagnostico
from modelos.estoque import ControleEstoque, Produto, Lote
from modelos.ordem_servico import ControleOrdensServico, ItemPeca, ItemServico
from modelos.pagamento import ControleFinanceiro
from modelos.fechamento import ControleFechamento


def preparar_cadastros():
    """Prepara os cadastros iniciais: clientes, veiculos e estoque de pecas."""
    controle_clientes = ControleClientes()
    controle_clientes.cadastrar_cliente(Cliente("Joao Silva", "111.111.111-11", "19999990000"))
    controle_clientes.cadastrar_veiculo("111.111.111-11", Veiculo("ABC1234", "Onix", "Chevrolet", 2020))

    controle_estoque = ControleEstoque()

    pastilha = Produto("Pastilha dianteira", "PST001", "Fornecedor A", preco_venda=120.0, estoque_minimo=3)
    controle_estoque.cadastrar_produto(pastilha)
    controle_estoque.adicionar_lote("PST001", Lote("2026-09-01", 60.0, 5))
    controle_estoque.adicionar_lote("PST001", Lote("2026-10-10", 65.0, 5))

    vela = Produto("Vela de ignicao", "VLA001", "Fornecedor B", preco_venda=35.0, estoque_minimo=2)
    controle_estoque.cadastrar_produto(vela)
    controle_estoque.adicionar_lote("VLA001", Lote("2026-08-15", 15.0, 4))

    return controle_clientes, controle_estoque


def main():
    print("=" * 70)
    print("SIMULACAO DE ATENDIMENTO COMPLETO - OFICINA MECANICA")
    print("=" * 70)

    controle_clientes, controle_estoque = preparar_cadastros()
    controle_atendimento = ControleAtendimento()
    controle_os = ControleOrdensServico()
    controle_financeiro = ControleFinanceiro()
    controle_fechamento = ControleFechamento(controle_estoque, controle_financeiro)

    # --- 1. Chegada do veiculo e entrada na espera ---
    print("\n[1] CHEGADA DO VEICULO")
    veiculo_espera = VeiculoEspera(
        placa="ABC1234",
        nome_cliente="Joao Silva",
        data_hora_chegada="27/10 08:30",
        queixa="Barulho ao frear",
        guincho=False,
    )
    controle_atendimento.chegar_veiculo(veiculo_espera)
    print(f"  Veiculo {veiculo_espera.placa} entrou na fila de espera (normal).")

    # --- 2. Chamada do proximo veiculo + abertura da OS ---
    print("\n[2] BOX LIVRE -> CHAMANDO PROXIMO VEICULO")
    proximo = controle_atendimento.proximo_veiculo()
    print(f"  Chamado: {proximo}")

    os_atual = controle_os.abrir_os(
        placa_veiculo=proximo.placa,
        nome_cliente=proximo.nome_cliente,
        mecanico_responsavel="Mecanico Carlos",
        data_hora_abertura="27/10 08:35",
    )
    print(f"  {os_atual}")

    # --- 3. Diagnostico na arvore de componentes ---
    print("\n[3] DIAGNOSTICO (arvore de componentes)")
    diagnostico = ControleDiagnostico()
    diagnostico.marcar_defeito("PST001")  # confirma defeito na pastilha
    print("  Arvore apos diagnostico:")
    diagnostico.exibir_diagnostico()

    pecas_defeituosas = diagnostico.listar_pecas_com_defeito()
    print("\n  Pecas com defeito encontradas no diagnostico:")
    for peca in pecas_defeituosas.percorrer():
        print(f"   -> {peca.nome} ({peca.codigo_peca})")

    # --- 4. Inclusao de pecas e servicos na OS ---
    print("\n[4] INCLUSAO DE PECAS E SERVICOS NA OS")
    os_atual.adicionar_peca(ItemPeca("PST001", "Pastilha dianteira", quantidade=2, preco_unitario=120.0))
    os_atual.adicionar_servico(ItemServico("Troca de pastilhas dianteiras", 90.0))
    print(f"  Pecas na OS: {list(os_atual.pecas.percorrer())}")
    print(f"  Servicos na OS: {list(os_atual.servicos.percorrer())}")
    print(f"  Valor total parcial: R$ {os_atual.valor_total():.2f}")

    print(f"\n  Estoque de pastilhas ANTES da baixa: {controle_estoque.buscar_produto('PST001').quantidade_total()}")

    # --- 5. Fechamento da OS e pagamento ---
    print("\n[5] FECHAMENTO DA OS E PAGAMENTO")
    os_atual.concluir_remontagem()
    pagamento, registro = controle_fechamento.fechar_os_com_pagamento(
        ordem_servico=os_atual,
        forma_pagamento="CARTAO",
        data_hora_pagamento="27/10 10:15",
        parcelas=2,
    )

    print(f"  {pagamento}")
    print(f"  {registro}")
    print(f"  Estoque de pastilhas APOS a baixa: {controle_estoque.buscar_produto('PST001').quantidade_total()}")
    print(f"  Lotes consumidos (rastreabilidade): {list(registro.lotes_consumidos['PST001'].percorrer())}")

    print("\n" + "=" * 70)
    print(f"Faturamento total da oficina: R$ {controle_financeiro.faturamento_total():.2f}")
    print("Simulacao concluida com sucesso.")
    print("=" * 70)


if __name__ == "__main__":
    main()
