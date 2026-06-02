# 🍔 Estudo de Caso Prático: Protótipo McLanches

[![License](https://img.shields.io/github/license/alankardecjr/Prototipo_McLanches?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

> **Nota:** Este projeto foi desenvolvido exclusivamente como um **exercício de caso prático** para fins de estudo, aplicação de lógica de programação, gerenciamento de estados e design de interface (UI/UX).

O **Protótipo McLanches** é uma simulação de um sistema de autoatendimento (totem) de fast-food. O objetivo principal deste estudo de caso foi estruturar a jornada de compra de um usuário, desde a navegação pelo cardápio até a customização de produtos e finalização do pedido no carrinho.

---

## 🎯 Objetivos do Exercício

O desenvolvimento deste projeto guiou-se pelos seguintes desafios práticos:
1. **Modelagem de Dados Dinâmica:** Estruturar um cardápio flexível dividido por categorias (Lanches, Acompanhamentos, Bebidas e Sobremesas).
2. **Lógica de Customização:** Permitir que o usuário configure o tamanho dos itens ou adicione/remova ingredientes de um produto.
3. **Gerenciamento de Estado do Carrinho:** Controlar a adição, remoção, alteração de quantidades e o cálculo em tempo real do valor total e dos subtotais.
4. **Interface Intuitiva (UX/UI):** Replicar o fluxo visual limpo e rápido característico de totens de atendimento reais.

---

## 🚀 Funcionalidades Implementadas

- [x] **Navegação por Abas/Categorias:** Filtro rápido de produtos sem necessidade de recarregar a página.
- [x] **Modal de Customização:** Opções para personalizar combos (ex: escolha do refrigerante e da batata inclusa).
- [x] **Carrinho de Compras Interativo:** Atualização dinâmica de valores ao alterar a quantidade de itens.
- [x] **Design Responsivo:** Interface adaptável para resoluções de tablets e telas de totens verticais.

---

## 🛠️ Tecnologias Utilizadas

*Selecione e mantenha apenas as tecnologias que você realmente usou no exercício:*
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Frameworks/Bibliotecas:** *(Ex: React / Vue.js / Bootstrap / Tailwind CSS - se aplicável)*
- **Versionamento:** Git e GitHub

---

## 📁 Estrutura de Arquivos Simplificada

```text
Prototipo_McLanches/
├── assets/               # Imagens e ícones dos produtos
├── src/                  # Código-fonte do projeto
│   ├── data/             # Mock de dados do cardápio (JSON ou JS)
│   ├── styles/           # Arquivos de estilização (CSS/SASS)
│   └── main.js           # Lógica principal do carrinho e interações
├── index.html            # Estrutura de visualização principal
└── README.md             # Documentação do estudo de caso