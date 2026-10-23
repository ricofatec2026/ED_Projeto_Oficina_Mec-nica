"""
Testes manuais do Controle de Clientes e Veiculos.
Rodar com: python -m testes.teste_clientes (a partir da raiz do projeto)
"""

from modelos.cliente import ControleClientes, Cliente, Veiculo


def testar_cadastro_e_busca():
    print("== Cadastro e busca ==")
    controle = ControleClientes()

    controle.cadastrar_cliente(Cliente("Joao Silva", "111.111.111-11", "19999990000"))
    controle.cadastrar_veiculo("111.111.111-11", Veiculo("ABC1234", "Onix", "Chevrolet", 2020))
    controle.cadastrar_veiculo("111.111.111-11", Veiculo("XYZ9999", "HB20", "Hyundai", 2019))

    controle.cadastrar_cliente(Cliente("Maria Souza", "222.222.222-22", "19988887777"))
    controle.cadastrar_veiculo("222.222.222-22", Veiculo("QWE4321", "Civic", "Honda", 2021))

    cliente = controle.buscar_cliente_por_cpf("222.222.222-22")
    print("Cliente encontrado:", cliente)

    dono, veiculo = controle.buscar_veiculo_por_placa("ABC1234")
    print("Veiculo ABC1234 pertence a:", dono.nome, "->", veiculo)


def testar_remocao():
    print("\n== Remocao ==")
    controle = ControleClientes()
    controle.cadastrar_cliente(Cliente("Pedro Costa", "333.333.333-33", "19977776666"))
    controle.cadastrar_veiculo("333.333.333-33", Veiculo("JJJ0001", "Gol", "Volkswagen", 2015))

    removido = controle.remover_veiculo_por_placa("JJJ0001")
    print("Veiculo removido:", removido)

    dono, veiculo = controle.buscar_veiculo_por_placa("JJJ0001")
    print("Apos remover, busca retorna:", veiculo)

    cliente_removido = controle.remover_cliente("333.333.333-33")
    print("Cliente removido:", cliente_removido)
    print("Busca apos remover cliente:", controle.buscar_cliente_por_cpf("333.333.333-33"))


def testar_cpf_duplicado():
    print("\n== CPF duplicado (deve lancar erro) ==")
    controle = ControleClientes()
    controle.cadastrar_cliente(Cliente("Ana", "444.444.444-44", "19955554444"))
    try:
        controle.cadastrar_cliente(Cliente("Ana Duplicada", "444.444.444-44", "19900001111"))
        print("ERRO: deveria ter lancado excecao!")
    except ValueError as e:
        print("Excecao esperada capturada:", e)


if __name__ == "__main__":
    testar_cadastro_e_busca()
    testar_remocao()
    testar_cpf_duplicado()
