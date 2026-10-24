"""
Testes manuais do Diagnostico (Arvore de Componentes).
Rodar com: python -m testes.teste_diagnostico (a partir da raiz do projeto)
"""

from modelos.diagnostico import ControleDiagnostico


def testar_exibicao_inicial():
    print("== Exibicao inicial (tudo OK) ==")
    d = ControleDiagnostico()
    d.exibir_diagnostico()


def testar_marcacao_defeito():
    print("\n== Marcando defeitos ==")
    d = ControleDiagnostico()
    d.marcar_defeito("DSC001")  # Disco dianteiro
    d.marcar_defeito("AMT001")  # Amortecedor
    d.exibir_diagnostico()

    pecas = list(d.listar_pecas_com_defeito().percorrer())
    print("\nTotal de pecas com defeito:", len(pecas))
    for p in pecas:
        print(" ->", p.nome, p.codigo_peca, p.estado)


def testar_codigo_invalido():
    print("\n== Codigo invalido (deve lancar erro) ==")
    d = ControleDiagnostico()
    try:
        d.marcar_defeito("CODIGO_INEXISTENTE")
        print("ERRO: deveria ter lancado excecao!")
    except ValueError as e:
        print("Excecao esperada capturada:", e)


def testar_reverter_estado():
    print("\n== Marcar defeito e depois reverter para OK ==")
    d = ControleDiagnostico()
    d.marcar_defeito("VLA001")
    print("Pecas com defeito apos marcar:", len(list(d.listar_pecas_com_defeito().percorrer())))
    d.marcar_ok("VLA001")
    print("Pecas com defeito apos reverter:", len(list(d.listar_pecas_com_defeito().percorrer())))


if __name__ == "__main__":
    testar_exibicao_inicial()
    testar_marcacao_defeito()
    testar_codigo_invalido()
    testar_reverter_estado()
