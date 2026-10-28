# Oficina Mecânica — Projeto de Estrutura de Dados

Sistema de gestão de uma oficina mecânica: clientes/veículos, fila de
atendimento, diagnóstico (árvore de componentes), estoque de peças por
lote, ordens de serviço e pagamento.

Disciplina: Estrutura de Dados — Fatec Rio Claro
Linguagem: Python puro (sem bibliotecas built-in para as estruturas de
dados do problema; estruturas implementadas do zero).

## Estrutura do repositório

```
oficina_mecanica/
├── estruturas/           # Estruturas de dados genéricas (sem regra de negócio)
│   ├── lista.py            # Lista encadeada própria
│   ├── fila.py             # Fila (FIFO) própria
│   ├── pilha.py            # Pilha (LIFO) própria
│   └── arvore.py           # Árvore N-ária própria
├── modelos/               # Regras de negócio da oficina (usam as estruturas acima)
│   ├── atendimento.py       # Controle de atendimento (fila guincho + fila normal)
│   ├── cliente.py           # Controle de clientes e veículos (lista + lista)
│   ├── diagnostico.py       # Diagnóstico via árvore de componentes pré-definida
│   ├── estoque.py           # Controle de estoque (lista de produtos + fila de lotes)
│   ├── ordem_servico.py     # Ordem de Serviço (peças, serviços, fechamento)
│   ├── pagamento.py         # Controle de Pagamento
│   └── fechamento.py        # Integra OS + estoque + pagamento + rastreabilidade
├── testes/
│   ├── teste_estruturas.py
│   ├── teste_clientes.py
│   ├── teste_diagnostico.py
│   ├── teste_estoque.py
│   ├── teste_ordem_servico.py
│   └── teste_pagamento.py
├── simulacao.py           # Simulação de atendimento completo ponta a ponta
└── README.md
```

## Status atual — projeto concluído

- [x] Estruturas genéricas: Lista, Fila, Pilha, Árvore N-ária
- [x] Controle de Atendimento (fila guincho + fila normal)
- [x] Controle de Clientes e Veículos (Lista de clientes, cada um com Lista de veículos)
- [x] Árvore de Componentes pré-definida (diagnóstico)
- [x] Controle de Estoque (Lista de produtos, cada um com Fila de lotes)
- [x] Ordem de Serviço
- [x] Controle de Pagamento
- [x] Simulação de atendimento completo (fluxo integrado ponta a ponta)

Rodar a simulação completa: `python -m simulacao` (a partir da raiz do projeto).

## Combinações de estruturas (obrigatório pelo enunciado)

### 1. Atendimento com prioridade para guincho — Fila + Fila
**Classes envolvidas:** `ControleAtendimento` (modelos/atendimento.py),
usando duas instâncias de `Fila` (estruturas/fila.py): `fila_guincho` e
`fila_normal`.
**Método:** `ControleAtendimento.proximo_veiculo()` — consome primeiro
da `fila_guincho`; se vazia, consome da `fila_normal`.
**Justificativa:** separar em duas filas garante O(1) para decidir o
próximo veículo, mantendo a ordem de chegada dentro de cada categoria.
Usar uma única fila exigiria reordenar ou varrer a fila inteira toda
vez que um guincho chegasse, o que é O(n) e quebra a ordem de chegada
dos demais veículos.

### 2. Estoque com vários lotes por produto — Lista + Fila
**Classes envolvidas:** `ControleEstoque` (modelos/estoque.py), que
mantém uma `Lista` de `Produto`; cada `Produto` mantém sua própria
`Fila` de `Lote`.
**Método:** `ControleEstoque.baixar_estoque(codigo, quantidade)` →
`Produto.baixar_estoque(...)` — percorre a lista até achar o produto e
consome a fila de lotes a partir da frente (lote mais antigo), passando
para o próximo lote quando o atual não é suficiente.
**Justificativa:** a Fila garante FIFO nativamente, sem precisar
ordenar os lotes por data a cada baixa — o lote mais antigo já está
sempre na frente. Usar uma única lista de lotes misturada exigiria
ordenação a cada operação ou controle manual de "qual é o mais antigo",
o que é mais custoso e propenso a erro.

### 3. Clientes e seus veículos — Lista + Lista
**Classes envolvidas:** `ControleClientes` (modelos/cliente.py), que
mantém uma `Lista` (estruturas/lista.py) de `Cliente`; cada `Cliente`
mantém sua própria `Lista` de `Veiculo`.
**Método:** `ControleClientes.buscar_veiculo_por_placa(placa)` —
percorre a lista de clientes e, para cada um, percorre sua lista de
veículos até encontrar a placa.
**Justificativa:** cada cliente é dono natural de seus veículos, então
aninhar uma lista dentro da outra reflete o domínio do problema e
permite que cada cliente cresça sua lista de veículos de forma
independente, sem limite pré-definido. Usar uma única lista global de
veículos exigiria guardar uma referência/chave ao cliente em cada
veículo e perderia a relação direta de posse; a remoção de um cliente
também não removeria automaticamente seus veículos.

## Fluxo integrado (simulacao.py)

O arquivo `simulacao.py` reproduz o fluxo completo pedido no
enunciado, chamando os módulos de todos os dias em sequência:

1. **Chegada do veículo** → `ControleAtendimento.chegar_veiculo()`
2. **Box livre, chama o próximo e abre a OS** →
   `ControleAtendimento.proximo_veiculo()` + `ControleOrdensServico.abrir_os()`
3. **Diagnóstico na árvore de componentes** →
   `ControleDiagnostico.marcar_defeito()` + `exibir_diagnostico()`
4. **Inclusão de peças/serviços na OS** →
   `OrdemServico.adicionar_peca()` / `adicionar_servico()`
5. **Fechamento da OS e pagamento** →
   `ControleFechamento.fechar_os_com_pagamento()`, que orquestra, nesta
   ordem: baixa de estoque pelo lote mais antigo (`ControleEstoque`),
   fechamento da OS (valida remontagem concluída), registro do
   pagamento (`ControleFinanceiro`) e registro de rastreabilidade do
   consumo (`RegistroConsumo`, em `modelos/fechamento.py`).

`ControleFechamento` não cria uma nova estrutura de dados — ele integra
as já existentes (Estoque, OS, Pagamento), mantendo a separação de
responsabilidades: cada módulo cuida da sua parte, e o fechamento cuida
apenas da orquestração entre eles.

## Observações sobre a implementação

- Nenhuma estrutura built-in do Python (`list`, `dict`, `queue.Queue`,
  etc.) é usada para resolver as estruturas de dados do problema. Elas
  são implementadas do zero com nós encadeados próprios, em
  `estruturas/`.
- Separação de responsabilidades: `estruturas/` contém apenas
  estruturas de dados puras e reutilizáveis; `modelos/` contém as
  regras específicas da oficina, que usam as estruturas de `estruturas/`.
- Todos os módulos têm testes manuais em `testes/`, cobrindo o caminho
  feliz e casos de borda (dados duplicados, estoque insuficiente,
  fechamento antes da remontagem concluída, forma de pagamento
  inválida, etc.).
