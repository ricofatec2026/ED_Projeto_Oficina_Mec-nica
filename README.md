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
├── estruturas/        # Estruturas de dados genéricas (sem regra de negócio)
│   ├── lista.py        # Lista encadeada própria
│   ├── fila.py          # Fila (FIFO) própria
│   ├── pilha.py         # Pilha (LIFO) própria
│   └── arvore.py        # Árvore N-ária própria
├── modelos/            # Regras de negócio da oficina (usam as estruturas acima)
│   └── atendimento.py   # Controle de atendimento (fila guincho + fila normal)
├── testes/
│   └── teste_estruturas.py
└── README.md
```

## Status atual (em desenvolvimento)

- [x] Estruturas genéricas: Lista, Fila, Pilha, Árvore N-ária
- [x] Controle de Atendimento (fila guincho + fila normal)
- [ ] Controle de Clientes e Veículos (Lista de clientes, cada um com Lista de veículos)
- [ ] Árvore de Componentes pré-definida (diagnóstico)
- [ ] Controle de Estoque (Lista de produtos, cada um com Fila de lotes)
- [ ] Ordem de Serviço
- [ ] Controle de Pagamento
- [ ] Simulação de atendimento completo (fluxo integrado ponta a ponta)

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
*(a implementar)* Lista de produtos, cada produto contendo uma Fila de
lotes. A baixa de estoque percorre a lista até achar o produto e
consome a fila do lote mais antigo (FIFO).

### 3. Clientes e seus veículos — Lista + Lista
*(a implementar)* Lista de clientes, cada cliente contendo uma Lista de
veículos. Busca por placa percorre as duas listas.

## Cronograma de desenvolvimento (commits diários)

| Dia | Data | Entrega |
|---|---|---|
| 1 | 22/10 (qui) | Estruturas genéricas (Lista, Fila, Pilha, Árvore) + Controle de Atendimento |
| 2 | 23/10 (sex) | Controle de Clientes e Veículos (Lista + Lista) |
| 3 | 24/10 (sáb) | Árvore de Componentes pré-definida + exibição indentada |
| 4 | 25/10 (dom) | Controle de Estoque (Lista + Fila de lotes) + alerta de mínimo |
| 5 | 26/10 (seg) | Ordem de Serviço (criação, adicionar/remover peças e serviços) |
| 6 | 27/10 (ter) | Controle de Pagamento + baixa de estoque no fechamento da OS |
| 7 | 28/10 (qua) | Simulação completa ponta a ponta + revisão geral + ajustes no README |
| — | 29/10 (qui) | Apresentação (10 min) |

## Observações sobre a implementação

- Nenhuma estrutura built-in do Python (`list`, `dict`, `queue.Queue`,
  etc.) é usada para resolver as estruturas de dados do problema. Elas
  podem aparecer apenas internamente, encapsuladas (ex.: não se aplica
  no momento — tudo via nós encadeados próprios).
- Separação de responsabilidades: `estruturas/` contém apenas
  estruturas de dados puras e reutilizáveis; `modelos/` contém as
  regras específicas da oficina, que usam as estruturas de `estruturas/`.
