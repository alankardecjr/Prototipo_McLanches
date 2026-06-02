import sqlite3

def conectar():
    """Conecta ao banco de dados mclanches.db e ativa chaves estrangeiras"""
    conn = sqlite3.connect("mclanches.db")
    # Garante que o SQLite respeite rigorosamente as regras de FOREIGN KEY
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    with conn:
        # 1. Tabela de Produtos (itens)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT UNIQUE NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER DEFAULT 0,
            categoria TEXT,
            status_item TEXT DEFAULT 'em estoque'
        )""")

        # 2. Tabela de Clientes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT UNIQUE NOT NULL,
            logradouro TEXT NOT NULL,
            numero INTEGER NOT NULL,
            bairro TEXT,
            ponto_referencia TEXT,
            observacao TEXT,
            status_cliente TEXT DEFAULT 'Ativo'
        )""")

        # 3. Tabela de Pedidos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            valor_total REAL NOT NULL,
            data TEXT DEFAULT (datetime('now', 'localtime')),
            status_pedido TEXT DEFAULT 'pendente',
            FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
        )""")

        # 4. Tabela de Itens do Pedido (Relação Muitos-para-Muitos)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos (id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES itens (id)
        )""")
        
    conn.close()

# --- GESTÃO DE CLIENTES ---

def salvar_cliente(nome, telefone, logradouro, numero, bairro, referencia, obs, status='Ativo'):
    conn = conectar()
    cursor = conn.cursor()
    with conn:
        cursor.execute("""
            INSERT INTO clientes (nome, telefone, logradouro, numero, bairro, ponto_referencia, observacao, status_cliente) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
            (nome, telefone, logradouro, numero, bairro, referencia, obs, status))    
    conn.close()

def listar_clientes():
    """Retorna todos os clientes em ordem alfabética"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY nome ASC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_cliente(id_cliente, nome, telefone, logra, num, bairro, ref, obs, status):
    conn = conectar()
    cursor = conn.cursor()
    with conn:
        cursor.execute("""
            UPDATE clientes SET nome=?, telefone=?, logradouro=?, numero=?, bairro=?, 
            ponto_referencia=?, observacao=?, status_cliente=? WHERE id=?""",
            (nome, telefone, logra, num, bairro, ref, obs, status, id_cliente))
    conn.close()

# --- GESTÃO DE PRODUTOS (ITENS) ---

def salvar_item(produto, preco, quantidade, categoria, status='em estoque'):
    conn = conectar()
    cursor = conn.cursor()
    with conn:
        cursor.execute("""
            INSERT INTO itens (produto, preco, quantidade, categoria, status_item) 
            VALUES (?, ?, ?, ?, ?)""", (produto, preco, quantidade, categoria, status))
    conn.close()

def atualizar_item(id_item, produto, preco, quantidade, categoria, status):
    conn = conectar()
    cursor = conn.cursor()
    with conn:
        cursor.execute("""
            UPDATE itens SET produto=?, preco=?, quantidade=?, categoria=?, status_item=? 
            WHERE id=?""", (produto, preco, quantidade, categoria, status, id_item))
    conn.close()

def listar_itens():
    """Retorna todos os itens em ordem alfabética"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itens ORDER BY produto ASC")
    dados = cursor.fetchall()
    conn.close()
    return dados

# --- GESTÃO DE PEDIDOS ---

def salvar_pedido(cliente_id, valor_total, lista_itens, status='pendente'):
    """
    Salva um novo pedido e os seus itens associados.
    lista_itens deve vir no formato: [(item_id, quantidade, preco_unitario), ...]
    """
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        with conn: # Transação atômica segura
            # Insere o cabeçalho do pedido
            cursor.execute("""
                INSERT INTO pedidos (cliente_id, valor_total, status_pedido) 
                VALUES (?, ?, ?)""", (cliente_id, valor_total, status))
            
            # Recupera o ID gerado automaticamente para este pedido
            pedido_id = cursor.lastrowid
            
            # Insere os produtos vinculados ao pedido
            for item_id, qtd, preco_un in lista_itens:
                cursor.execute("""
                    INSERT INTO itens_pedido (pedido_id, item_id, quantidade, preco_unitario)
                    VALUES (?, ?, ?, ?)""", (pedido_id, item_id, qtd, preco_un))
                
                # Abate de forma segura a quantidade vendida do estoque atual
                cursor.execute("""
                    UPDATE itens SET quantidade = MAX(0, quantidade - ?) WHERE id = ?
                """, (qtd, item_id))
    finally:
        conn.close()

def listar_pedidos_detalhados():
    """Retorna pedidos com informações detalhadas do cliente e status"""
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT p.id, c.nome, p.valor_total, p.data, p.status_pedido, 
           c.status_cliente, c.logradouro, c.bairro
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id 
    ORDER BY p.id DESC
    """
    cursor.execute(query)
    dados = cursor.fetchall()
    conn.close()
    return dados

def obter_produtos_do_pedido(pedido_id):
    """Retorna quais produtos foram comprados em um pedido específico"""
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT i.id, i.produto, ip.quantidade, ip.preco_unitario, 
           (ip.quantidade * ip.preco_unitario) as subtotal
    FROM itens_pedido ip
    JOIN itens i ON ip.item_id = i.id
    WHERE ip.pedido_id = ?
    """
    cursor.execute(query, (pedido_id,))
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_status_pedido(id_pedido, novo_status):
    """Atualiza o status do pedido de forma imediata"""
    conn = conectar()
    cursor = conn.cursor()
    with conn:
        cursor.execute("UPDATE pedidos SET status_pedido = ? WHERE id = ?", (novo_status, id_pedido))
    conn.close()

def deletar_pedido(id_pedido):
    """Remove um pedido do sistema (limpa cascata via chave estrangeira)"""
    conn = conectar()
    cursor = conn.cursor()
    with conn:
        cursor.execute("DELETE FROM pedidos WHERE id = ?", (id_pedido,))
    conn.close()

# --- INICIALIZAÇÃO ---

if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados mclanches.db estruturado e atualizado com sucesso!")