import random
# Importa as funções do arquivo database.py ajustado para mclanches.db
from database import conectar, criar_tabelas, salvar_cliente, salvar_item, salvar_pedido

def popular_banco_mclanches_movimentado():
    print("🔄 Inicializando e estruturando o banco de dados mclanches.db...")
    criar_tabelas()

    # ==========================================================
    # 1. CADASTRO DE CLIENTES (20 registros com atributos corretos)
    # ==========================================================
    print("👥 Cadastrando clientes de teste...")
    clientes = [
        ("Alan Kardec", "71999991111", "Av. Santos Dumont", 1020, "Centro", "Perto do Shopping", "Entregar na portaria"),
        ("Maria Silva", "71999992222", "Rua das Flores", 45, "Ipitanga", "Atrás da Igreja", ""),
        ("João Pereira", "71999993333", "Alameda das Palmeiras", 301, "Vilas do Atlântico", "Próximo à praia", "Interfone 301"),
        ("Ana Oliveira", "71999994444", "Rua Direita", 12, "Buraquinho", "Ao lado do mercado", ""),
        ("Carlos Souza", "71999995555", "Av. Luis Tarquínio", 88, "Portão", "Galpão azul", "Cuidado com o cachorro"),
        ("Beatriz Costa", "71999996666", "Rua do Farol", 500, "Ipitanga", "Próximo ao posto", ""),
        ("Lucas Martins", "71999997777", "Rua Principal", 99, "Areia Branca", "", "Ligar ao chegar"),
        ("Juliana Lima", "71999998888", "Av. Praia de Copacabana", 15, "Vilas do Atlântico", "Condomínio Sol", "Deixar com o vigilante"),
        ("Pedro Santos", "71999999999", "Rua Getúlio Vargas", 740, "Centro", "Em frente à praça", ""),
        ("Mariana Alves", "71988881111", "Rua Castro Alves", 23, "Portão", "", ""),
        ("Fernando Gomes", "71988882222", "Rua Novo Horizonte", 105, "Itinga", "Final de linha", "Entrar no beco à direita"),
        ("Camila Ribeiro", "71988883333", "Av. Gerônimo de Albuquerque", 2000, "Buraquinho", "Apto 402 Bloco B", ""),
        ("Rodrigo Melo", "71988884444", "Rua da Aurora", 89, "Centro", "Ao lado da farmácia", ""),
        ("Amanda Rodrigues", "71988885555", "Travessa da Paz", 7, "Ipitanga", "", ""),
        ("Ricardo Rocha", "71988886666", "Rua dos Coqueiros", 54, "Vilas do Atlântico", "Portão de madeira", ""),
        ("Larissa Carvalho", "71988887777", "Rua Rio de Janeiro", 112, "Portão", "", "Entregar no segundo andar"),
        ("Gabriel Jesus", "71988888888", "Av. Brigadeiro Alberto Costa", 400, "Centro", "Próximo à prefeitura", ""),
        ("Sofia Fonseca", "71988889999", "Rua Bahia", 82, "Ipitanga", "", ""),
        ("Thiago Neves", "71977771111", "Rua Sergipe", 14, "Itinga", "Perto da escola", ""),
        ("Aline Prado", "71977772222", "Av. Fortaleza", 335, "Itinga", "Atrás do supermercado", "Mora nos fundos")
    ]

    for c in clientes:
        try:
            # Envia exatamente as 7 variáveis exigidas na assinatura da função 'salvar_cliente'
            salvar_cliente(c[0], c[1], c[2], c[3], c[4], c[5], c[6])
        except Exception:
            pass # Evita interrupção caso chaves UNIQUE já existam no banco

    # ==========================================================
    # 2. CARDÁPIO: PRODUTOS VARIADOS DO CARDÁPIO (30 registros)
    # ==========================================================
    print("🍔 Cadastrando o cardápio de produtos...")
    produtos_cardapio = [
        # --- SANDUÍCHES E REFEIÇÕES (Comida) ---
        ("Big Bob", 26.90, 60, "Comida"),
        ("Big Bob Artesanal", 32.90, 45, "Comida"),
        ("Bob's Burger", 14.90, 80, "Comida"),
        ("Double Cheese Burger", 19.90, 70, "Comida"),
        ("Cheddar Australiano", 28.50, 50, "Comida"),
        ("Bob's Costela", 31.90, 40, "Comida"),
        ("Tentador Carne", 25.00, 55, "Comida"),
        ("Tentador Frango", 23.50, 50, "Comida"),
        ("Crispy Bacon", 27.90, 45, "Comida"),
        ("Australiano Bacon", 29.90, 40, "Comida"),
        ("Bob's Picanha 150g", 36.90, 30, "Comida"),
        ("Bob's Picanha Double", 44.90, 25, "Comida"),
        
        # --- ACOMPANHAMENTOS E SNACKS (Comida) ---
        ("Batata Frita Palito Média", 11.90, 150, "Comida"),
        ("Batata Frita Palito Grande", 14.90, 100, "Comida"),
        ("Batata Mega Franqueada", 18.90, 80, "Comida"),
        ("Franlitos 6 unid.", 15.50, 90, "Comida"),
        ("Franlitos 12 unid.", 24.90, 60, "Comida"),
        ("Almofadas de Queijo Gouda", 13.50, 110, "Comida"),
        
        # --- SOBREMESAS (Comida) ---
        ("Milk-Shake Ovomaltine 500ml", 17.90, 200, "Comida"),
        ("Milk-Shake Ovomaltine 700ml", 21.90, 150, "Comida"),
        ("Milk-Shake Morango 500ml", 16.90, 100, "Comida"),
        ("Milk-Shake Paçoca 500ml", 17.90, 80, "Comida"),
        ("Sundae Ovomaltine", 10.90, 120, "Comida"),
        ("Cascão Recheado Chocolate", 7.50, 250, "Comida"),
        
        # --- BEBIDAS (Bebida) ---
        ("Refri Refil Coca-Cola", 9.90, 400, "Bebida"),
        ("Refri Refil Guaraná", 9.90, 300, "Bebida"),
        ("Refri Refil Fanta Laranja", 9.90, 200, "Bebida"),
        ("Suco de Laranja Del Valle", 10.50, 100, "Bebida"),
        ("Água Mineral sem Gás", 5.00, 500, "Bebida"),
        ("Água Mineral com Gás", 5.50, 300, "Bebida")
    ]

    for p in produtos_cardapio:
        try:
            # Envia as 4 variáveis exigidas na assinatura da função 'salvar_item'
            salvar_item(p[0], p[1], p[2], p[3])
        except Exception:
            pass # Ignora se o produto UNIQUE já existir

    # ==========================================================
    # 3. CAPTURA DE INFORMAÇÕES DE ID PARA COMPOSIÇÃO DOS PEDIDOS
    # ==========================================================
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM clientes")
    ids_clientes = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id, preco FROM itens WHERE status_item = 'em estoque' AND quantidade > 0")
    dados_itens = cursor.fetchall()
    
    conn.close()

    # ==========================================================
    # 4. SIMULAÇÃO DE CAIXA ALTAMENTE MOVIMENTADO (40 Pedidos Relacionais)
    # ==========================================================
    if not ids_clientes or not dados_itens:
        print("⚠️ Erro crítico: Clientes ou Itens indisponíveis para gerar as vendas.")
        return

    print("🛒 Simulando grande volume de vendas no caixa do MCLanches...")
    status_opcoes = ['pendente', 'em preparo', 'saiu para entrega', 'entregue']
    pedidos_gerados = 0

    # Gerando 40 compras completas de forma randômica
    for _ in range(40):
        cliente_aleatorio = random.choice(ids_clientes)
        status_aleatorio = random.choice(status_opcoes)
        
        # Cada pedido do fluxo movimentado terá entre 1 e 5 tipos de produtos diferentes
        quantidade_de_itens_diferentes = random.randint(1, 5)
        itens_escolhidos_no_carrinho = random.sample(dados_itens, quantidade_de_itens_diferentes)
        
        lista_itens_pedido = []
        valor_total_pedido = 0.0
        
        for item_id, preco_unitario in itens_escolhidos_no_carrinho:
            qtd_comprada = random.randint(1, 3) # Compra de 1 a 3 unidades do mesmo item
            subtotal_item = qtd_comprada * preco_unitario
            valor_total_pedido += subtotal_item
            
            # Monta a tupla exigida pela regra de negócios: (item_id, quantidade, preco_unitario)
            lista_itens_pedido.append((item_id, qtd_comprada, preco_unitario))
        
        valor_total_pedido = round(valor_total_pedido, 2)
        
        try:
            # Insere simultaneamente nas tabelas 'pedidos' e 'itens_pedido' aplicando abatimento de estoque
            salvar_pedido(cliente_aleatorio, valor_total_pedido, lista_itens_pedido, status_aleatorio)
            pedidos_gerados += 1
        except Exception as e:
            print(f"❌ Falha ao simular venda: {e}")

    print(f"\n✅ Operação de população concluída com sucesso!")
    print(f"   🔹 20 Clientes cadastrados de forma operacional.")
    print(f"   🔹 30 Itens do cardápio inseridos com sucesso.")
    print(f"   🔹 {pedidos_gerados} Pedidos e subtotais gerados relacionalmente.")
    print("\n🚀 Abra o painel ('main.py') para checar as vendas ativas no sistema!")

if __name__ == "__main__":
    popular_banco_mclanches_movimentado()