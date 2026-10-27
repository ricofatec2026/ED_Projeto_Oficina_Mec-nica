"""
Testes manuais da Ordem de Servico.
Rodar com: python -m testes.teste_ordem_servico (a partir da raiz do projeto)
"""

from modelos.ordem_servico import ControleOrdensServico, ItemPeca, ItemServico


def testar_fluxo_completo():
    print("== Fluxo completo: abrir, adicionar, remover, fechar ==")
    controle = ControleOrdensServico()
    os1 = controle.abrir_os("XYZ9999", "Maria Souza", "Mecanico Bruno", "26/10 10:00")

    os1.adicionar_peca(ItemPeca("AMT001", "Amortecedor", 2, 150.0))
    os1.adicionar_servico(ItemServico("Troca de amortecedores", 100.0))

    print("Total antes do fechamento:", os1.valor_total())
    assert os1.valor_total() == 400.0

    os1.concluir_remontagem()
    os1.fechar()
    assert os1.fechada is True
    print("OS fechada com sucesso:", os1)


def testar_bloqueio_apos_fechamento():
    print("\n== Bloqueio de edicao apos fechamento (deve lancar erro) ==")
    controle = ControleOrdensServico()
    os1 = controle.abrir_os("QWE4321", "Pedro Costa", "Mecanico Bruno", "26/10 11:00")
    os1.concluir_remontagem()
    os1.fechar()

    try:
        os1.adicionar_servico(ItemServico("Troca de oleo", 50.0))
        print("ERRO: deveria ter lancado excecao!")
    except ValueError as e:
        print("Excecao esperada capturada:", e)


def testar_busca_por_placa():
    print("\n== Busca de OS aberta por placa ==")
    controle = ControleOrdensServico()
    controle.abrir_os("AAA1111", "Cliente A", "Mecanico C", "26/10 08:00")
    os_encontrada = controle.buscar_por_placa("AAA1111")
    print("OS encontrada:", os_encontrada)
    assert os_encontrada is not None


if __name__ == "__main__":
    testar_fluxo_completo()
    testar_bloqueio_apos_fechamento()
    testar_busca_por_placa()
    print("\nTodos os testes passaram.")
