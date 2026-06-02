# 🍔 MCLanches Delivery System - Desktop PDV & CRUD

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg?style=flat-square&logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/github/license/alankardecjr/Prototipo_McLanches?style=flat-square)](LICENSE)

> **Destaque Técnico:** Este repositório é um **Estudo de Caso de Engenharia de Software** focado no desenvolvimento de uma aplicação Desktop utilizando Programação Orientada a Objetos (POO), persistência relacional local (SQLite) e arquitetura modular de componentes. 

O sistema simula de forma robusta as operações de um **Ponto de Venda (PDV/Checkout)** e o gerenciamento de Retaguarda (CRUDs de Clientes e Produtos) para o ecossistema **MCLanches Delivery**, aplicando os princípios fundamentais de **Transações ACID** e **Clean Code**.

---

## 🎯 Requisitos Técnicos & Arquitetura de Solução

O projeto foi desenhado para resolver desafios comuns no desenvolvimento de aplicações comerciais:

1. **Modelagem de Dados Relacional Avançada:** Implementação de relacionamento **Muitos-para-Muitos (NxN)** através da tabela associativa `itens_pedido`, garantindo o histórico do preço unitário no momento da venda e o cálculo matemático exato de subtotais e totais.
2. **Robustez Transacional (Princípios ACID):** Utilização de Context Managers do Python (`with conn:`) para assegurar atomicidade. A gravação do pedido e o abate físico no estoque de produtos ocorrem de forma síncrona; em caso de falha de hardware ou exceção de execução, é efetuado o *rollback* automático para prevenir a corrupção de dados.
3. **Padrão de Arquitetura de Software:** Separação estrita de responsabilidades:
   * **Camada de Dados (`database.py`):** Encapsula todas as operações de CRUD e persistência via SQL puro.
   * **Camada de Interface (`main.py`, `cadastro_*.py`):** Componentização da interface gráfica em janelas independentes (`Toplevel`), desacopladas da regra de persistência.
4. **Comunicação por Inversão de Controle (Callbacks):** Passagem de funções como argumento para ligar componentes visuais de forma assíncrona. O botão "PEDIR" no formulário de Clientes fecha a janela atual e dispara o carregamento automático do PDV com o estado do cliente injetado.

---

## 🚀 Funcionalidades Implementadas

- [x] **Painel Principal (`main.py`):** Interface otimizada (inicia automaticamente maximizada) com busca global em tempo real e tabelas (`Treeview`) parametrizadas com fontes ampliadas para melhor usabilidade e leitura.
- [x] **Gestão Comercial de Clientes (`cadastro_clientes.py`):** Cadastro completo com suporte a marcação de status especiais (Prioridades como PCD/Idoso) e validação de chaves únicas (Unique Telefone).
- [x] **Módulo PDV Touch-Friendly (`cadastro_pedidos.py`):** Grade dinâmica de produtos com botões expandidos para facilitar o clique, carrinho interativo (adição/remoção de itens em tempo real) e controle de fluxo operacional.
- [x] **PDV Otimizado:** A tela de checkout abre maximizada, o cardápio no PDV suporta rolagem por roda do mouse, e o fechamento de pedido exibe uma janela de pagamento com opções de `Dinheiro`, `Cartão`, `PIX` e `Voucher` antes da confirmação.
- [x] **Gestão de Ciclo de Vida do Pedido:** Recursos em tempo real para **atualizar o status** da produção (Pendente, Em preparo, Saiu para entrega, Entregue) ou efetuar o **cancelamento seguro** do registro.
- [x] **Ação Rápida de Status por Menu de Contexto:** Na lista de pedidos, clique esquerdo em um item exibe um aviso contextual rápido; clique direito abre um menu para mudar o status com confirmação antes da alteração.
- [x] **Engine de Seed (`populardb.py`):** Gerador automático de dados em massa que simula um ambiente real sob carga, injetando 30 produtos variados do cardápio, 20 clientes e mais de 40 pedidos calculados de forma relacional para testes imediatos.

---

## 🧭 Guia Rápido de Uso

1. Abra o sistema executando `python main.py`.
2. Use a barra de busca para localizar clientes, produtos ou pedidos rapidamente.
3. No PDV:
   - o cardápio abre maximizado;
   - a rolagem dos produtos funciona com a roda do mouse;
   - clique nos itens para adicioná-los ao carrinho;
   - ao salvar o pedido, a janela de pagamento exibe opções de `Dinheiro`, `Cartão`, `PIX` e `Voucher`.
4. Na lista de pedidos:
   - clique esquerdo em um pedido para ver a dica de ação rápida;
   - clique direito no pedido para abrir o menu de contexto e alterar o status.
5. Ao alterar o status, confirme a mudança para que o pedido seja atualizado no banco.

---

## 🛠️ Stack Tecnológica

- **Linguagem:** Python 3 (Utilizando conceitos de POO, polimorfismo e encapsulamento).
- **Interface Gráfica (GUI):** Tkinter & ttk (Componentes nativos refinados com tratamento visual de estados `Hover` e `Focus`).
- **Engine de Banco de Dados:** SQLite3.

---

## 📁 Estrutura de Arquivos e Componentes

```text
Prototipo_McLanches/
│
├── mclanches.db           # Banco de dados relacional gerado localmente
│
├── database.py            # Camada de Persistência (Regras SQL, CRUD, Transactions)
├── populardb.py           # Utilitário Data Seed (Simulação de carga de dados e stress)
├── main.py                # Ponto de Entrada da Aplicação (Dashboard Central)
│
├── cadastro_clientes.py   # Componente Visual: CRUD de Clientes
├── cadastro_produtos.py   # Componente Visual: CRUD do Cardápio
└── cadastro_pedidos.py    # Componente Visual: Motor de Checkout / PDV & Status