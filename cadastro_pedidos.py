import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import database  # Utiliza o arquivo database.py refatorado

class JanelaCadastroPedidos(tk.Toplevel):
    def __init__(self, master, nome_cliente_inicial=None, pedido_id_existente=None):
        super().__init__(master)
        self.title("***** Sistema JAD - McLanches Delivery *****")
        
        # -------------------------------------------------------------
        # INICIAR A JANELA DO PDV MAXIMIZADA (Multiplataforma)
        # -------------------------------------------------------------
        try:
            self.state('zoomed')
        except tk.TclError:
            largura = self.winfo_screenwidth()
            altura = self.winfo_screenheight()
            self.geometry(f"{largura}x{altura}+0+0")
            
        self.configure(bg="#f4f6f9")
        
        # Cores padronizadas com a tela principal (Main)
        self.bg_fundo = "#f4f6f9"
        self.bg_card = "#ffffff"
        self.cor_texto = "#2c3e50"
        
        self.cliente_selecionado = None
        self.pedido_id_existente = pedido_id_existente  # Armazena se for edição/visualização
        self.total_pedido = 0.0
        self.carrinho_itens_ids = [] 

        self.criar_widgets()
        
        # Caso venha um cliente automático da janela de clientes, faz a busca
        if nome_cliente_inicial:
            self.ent_busca_cliente.insert(0, nome_cliente_inicial)
            self.buscar_cliente()
            
        # Se for um pedido já existente, carrega as informações dele
        if self.pedido_id_existente:
            self.carregar_pedido_existente()

    def criar_widgets(self):
        # Título da Janela
        tk.Label(self, text="🛒 MCLanches Ponto de Venda (PDV) 🍟", 
                 font=("Arial", 18, "bold"), bg=self.bg_fundo, fg=self.cor_texto).pack(pady=10)

        # -----------------------------------------------------------------
        # 1. PAINEL DE BUSCA DE CLIENTE
        # -----------------------------------------------------------------
        frame_busca = tk.LabelFrame(self, text=" Passo 1: Identificar o Cliente ", bg=self.bg_fundo, 
                                    font=("Arial", 10, "bold"), bd=2, relief="solid")
        frame_busca.pack(fill="x", padx=30, pady=5, ipady=5)

        tk.Label(frame_busca, text="Buscar por Nome ou Tel:", bg=self.bg_fundo, font=("Arial", 11, "bold")).pack(side="left", padx=10)
        
        # Campo de busca ampliado com FOCUS e HOVER
        self.ent_busca_cliente = tk.Entry(frame_busca, font=("Arial", 13), bd=1, relief="solid", highlightthickness=1, highlightbackground="#2c3e50")
        self.ent_busca_cliente.pack(side="left", padx=5, fill="x", expand=True, ipady=4)
        
        # Eventos do Campo de Busca
        self.ent_busca_cliente.bind("<Enter>", lambda e: e.widget.config(highlightbackground="#3498db") if e.widget != self.focus_get() else None)
        self.ent_busca_cliente.bind("<Leave>", lambda e: e.widget.config(highlightbackground="#2c3e50") if e.widget != self.focus_get() else None)
        self.ent_busca_cliente.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground="#27ae60", highlightthickness=2))
        self.ent_busca_cliente.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground="#2c3e50", highlightthickness=1))

        # Botão Buscar com Hover
        btn_buscar = tk.Button(frame_busca, text="BUSCAR", command=self.buscar_cliente, bg="#ffffff", 
                               fg=self.cor_texto, font=("Arial", 10, "bold"), relief="solid", bd=1, cursor="hand2")
        btn_buscar.pack(side="left", padx=10, ipady=2, ipadx=10)
        btn_buscar.bind("<Enter>", lambda e: e.widget.config(bg="#2c3e50", fg="#ffffff"))
        btn_buscar.bind("<Leave>", lambda e: e.widget.config(bg="#ffffff", fg=self.cor_texto))

        # Listbox de clientes
        result_frame = tk.Frame(frame_busca, bg=self.bg_card, highlightbackground="#ccc", highlightthickness=1)
        result_frame.pack(side="left", padx=5, fill="both", expand=True)

        self.scroll_lista = tk.Scrollbar(result_frame, orient="vertical")
        self.lista_clientes = tk.Listbox(result_frame, font=("Arial", 10), height=3, relief="flat", 
                                         yscrollcommand=self.scroll_lista.set, bg=self.bg_card, fg=self.cor_texto,
                                         selectbackground="#e2e6ea", selectforeground="black", bd=0, highlightthickness=0)
        self.scroll_lista.config(command=self.lista_clientes.yview)
        self.lista_clientes.pack(side="left", fill="both", expand=True)
        self.scroll_lista.pack(side="right", fill="y")
        self.lista_clientes.bind('<<ListboxSelect>>', self.selecionar_cliente_lista)

        # -----------------------------------------------------------------
        # 2. ÁREA CENTRAL (Divisão em Esquerda e Direita)
        # -----------------------------------------------------------------
        corpo_frame = tk.Frame(self, bg=self.bg_fundo)
        corpo_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # --- ESQUERDA: CARDÁPIO EM GRADE (Ajustado para expandir e ocupar a tela) ---
        prod_container = tk.LabelFrame(corpo_frame, text=" Passo 2: Clique nos Itens do Cardápio ", 
                                       bg=self.bg_fundo, fg=self.cor_texto, font=("Arial", 10, "bold"), bd=2, relief="solid")
        prod_container.pack(side="left", fill="both", expand=True, padx=(0, 15))

        self.canvas = tk.Canvas(prod_container, bg=self.bg_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(prod_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_fundo)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Permite rolar o cardápio com a roda do mouse mesmo quando o cursor não está sobre a barra de rolagem
        self.canvas.bind("<Enter>", lambda e: [
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel),
            self.canvas.bind_all("<Button-4>", self._on_mousewheel),
            self.canvas.bind_all("<Button-5>", self._on_mousewheel)
        ])
        self.canvas.bind("<Leave>", lambda e: [
            self.canvas.unbind_all("<MouseWheel>"),
            self.canvas.unbind_all("<Button-4>"),
            self.canvas.unbind_all("<Button-5>")
        ])

        self.carregar_produtos_grade()

        # --- DIREITA: CARRINHO EQUILIBRADO (Travado para não esticar na largura) ---
        resumo_frame = tk.LabelFrame(corpo_frame, text=" Passo 3: Resumo, Status e Fechamento ", 
                                     bg=self.bg_card, fg=self.cor_texto, font=("Arial", 10, "bold"), bd=2, relief="solid")
        resumo_frame.pack(side="right", fill="both", expand=False, ipadx=40)  # ipadx controla a largura de forma limpa

        # Exibição mais legível e completa dos dados do cliente selecionado
        self.frame_detalhe_cliente = tk.Frame(resumo_frame, bg="#e2e6ea", bd=1, relief="solid")
        self.frame_detalhe_cliente.pack(fill="x", padx=15, pady=10, ipady=5)
        
        self.lbl_nome_cli = tk.Label(self.frame_detalhe_cliente, text="Nenhum cliente selecionado", bg="#e2e6ea", font=("Arial", 11, "bold"), fg="#7f8c8d")
        self.lbl_nome_cli.pack(anchor="w", padx=10, pady=2)
        self.lbl_tel_cli = tk.Label(self.frame_detalhe_cliente, text="Telefone: --", bg="#e2e6ea", font=("Arial", 10), fg="#34495e")
        self.lbl_tel_cli.pack(anchor="w", padx=10)
        self.lbl_status_cli = tk.Label(self.frame_detalhe_cliente, text="Status Cadastro: --", bg="#e2e6ea", font=("Arial", 10), fg="#34495e")
        self.lbl_status_cli.pack(anchor="w", padx=10)

        # Painel de Controle do Status do Pedido Atual
        self.frame_status_pedido = tk.Frame(resumo_frame, bg=self.bg_card)
        self.frame_status_pedido.pack(fill="x", padx=15, pady=5)
        
        tk.Label(self.frame_status_pedido, text="Status do Pedido:", bg=self.bg_card, font=("Arial", 10, "bold"), fg=self.cor_texto).pack(side="left")
        self.var_status_pedido = tk.StringVar(value="pendente")
        self.opt_status_pedido = tk.OptionMenu(self.frame_status_pedido, self.var_status_pedido, 'pendente', 'em preparo', 'saiu para entrega', 'entregue')
        self.opt_status_pedido.config(bg="#ffffff", fg=self.cor_texto, relief="solid", bd=1, font=("Arial", 10), highlightthickness=0)
        self.opt_status_pedido.pack(side="left", padx=10, fill="x", expand=True)

        # Tabela do Carrinho ajustada de forma simétrica para a nova proporção da barra
        style = ttk.Style()
        style.configure("PDV.Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("PDV.Treeview", font=("Arial", 11), rowheight=26)

        self.tree = ttk.Treeview(resumo_frame, columns=("Prod", "Preco"), show="headings", height=8, style="PDV.Treeview")
        self.tree.heading("Prod", text="Produto")
        self.tree.heading("Preco", text="Preço Unit.")
        self.tree.column("Prod", width=180, anchor="w")   # Retornado para dimensão simétrica ideal
        self.tree.column("Preco", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=5)

        # Exibição do Valor Total
        self.lbl_total = tk.Label(resumo_frame, text="TOTAL: R$ 0.00", bg=self.bg_card, 
                                  font=("Arial", 16, "bold"), fg="#16a085")
        self.lbl_total.pack(pady=5)

        # --- BOTÕES DE AÇÃO COM HOVER PADRONIZADO ---
        btn_style = {
            "width": 24, "font": ("Arial", 10, "bold"), "relief": "solid", "bd": 1, "cursor": "hand2"
        }

        self.btn_pagar = tk.Button(resumo_frame, text="✔️ SALVAR PEDIDO", bg="#ffffff", fg="#27ae60", command=self.finalizar_e_salvar_pedido, **btn_style)
        self.btn_pagar.pack(pady=3, ipady=3)
        self.btn_pagar.bind("<Enter>", lambda e: e.widget.config(bg="#27ae60", fg="#ffffff"))
        self.btn_pagar.bind("<Leave>", lambda e: e.widget.config(bg="#ffffff", fg="#27ae60"))


        self.btn_remover = tk.Button(resumo_frame, text="❌ REMOVER ITEM", bg="#ffffff", fg="#c0392b", command=self.remover_item, **btn_style)
        self.btn_remover.pack(pady=3, ipady=3)
        self.btn_remover.bind("<Enter>", lambda e: e.widget.config(bg="#c0392b", fg="#ffffff"))
        self.btn_remover.bind("<Leave>", lambda e: e.widget.config(bg="#ffffff", fg="#c0392b"))

        self.btn_cancelar = tk.Button(resumo_frame, text="🗑️ CANCELAR PEDIDO", bg="#ffffff", fg="#d35400", command=self.cancelar_pedido, **btn_style)
        self.btn_cancelar.pack(pady=3, ipady=3)
        self.btn_cancelar.bind("<Enter>", lambda e: e.widget.config(bg="#d35400", fg="#ffffff"))
        self.btn_cancelar.bind("<Leave>", lambda e: e.widget.config(bg="#ffffff", fg="#d35400"))

        btn_sair = tk.Button(resumo_frame, text="🚪 SAIR DO PDV", bg="#ffffff", fg="#7f8c8d", command=self.destroy, **btn_style)
        btn_sair.pack(pady=3, ipady=3)
        btn_sair.bind("<Enter>", lambda e: e.widget.config(bg="#7f8c8d", fg="#ffffff"))
        btn_sair.bind("<Leave>", lambda e: e.widget.config(bg="#ffffff", fg="#7f8c8d"))

    def _on_mousewheel(self, event):
        """Rola o cardápio pelo canvas quando o cursor está sobre ele."""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def carregar_produtos_grade(self):
        """Monta os botões dinâmicos do cardápio"""
        try:
            itens = database.listar_itens() 
            col, row = 0, 0
            for item in itens:
                if item[5] == "em estoque":
                    texto = f"{item[1]}\nR$ {item[2]:.2f}"
                    btn = tk.Button(self.scrollable_frame, text=texto, width=22, height=4, bg="white", 
                                   fg=self.cor_texto, relief="solid", bd=1, font=("Arial", 11, "bold"),
                                   command=lambda i=item: self.adicionar_item(i))
                    btn.grid(row=row, column=col, padx=8, pady=8)
                    
                    btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2c3e50", fg="#ffffff"))
                    btn.bind("<Leave>", lambda e, b=btn: b.config(bg="white", fg=self.cor_texto))
                    
                    col += 1
                    if col > 3:  # Como o espaço da esquerda aumentou, agora comporta até 4 colunas de produtos por linha!
                        col, row = 0, row + 1
        except Exception as e:
            print(f"Erro ao carregar cardápio: {e}")

    def buscar_cliente(self):
        """Pesquisa clientes pelo nome ou telefone informados"""
        termo = self.ent_busca_cliente.get().strip()
        if not termo: return
        
        self.lista_clientes.delete(0, tk.END)
        self.dados_clientes_lista = []

        conn = database.conectar()
        cursor = conn.cursor()
        with conn:
            cursor.execute("""
                SELECT id, nome, telefone, logradouro, numero, bairro, status_cliente 
                FROM clientes 
                WHERE nome LIKE ? OR telefone = ?""", (f'%{termo}%', termo))
            resultados = cursor.fetchall()

        if resultados:
            for res in resultados:
                linha = f"{res[1].upper()} ({res[2]})"
                self.lista_clientes.insert(tk.END, linha)
                self.dados_clientes_lista.append(res)
            
            if len(resultados) == 1:
                self.lista_clientes.select_set(0)
                self.selecionar_cliente_lista(None)
        else:
            self.lbl_nome_cli.config(text="CLIENTE NÃO ENCONTRADO", fg="#c0392b")
            messagebox.showwarning("Busca", "Nenhum cliente localizado no banco de dados.")

    def selecionar_cliente_lista(self, event):
        """Confirma a seleção do cliente da lista e exibe seus dados legíveis"""
        selecao = self.lista_clientes.curselection()
        if selecao:
            indice = selecao[0]
            self.cliente_selecionado = self.dados_clientes_lista[indice]
            
            self.lbl_nome_cli.config(text=f"👤 {self.cliente_selecionado[1].upper()}", fg="#2c3e50")
            self.lbl_tel_cli.config(text=f"📞 Telefone: {self.cliente_selecionado[2]}")
            self.lbl_status_cli.config(text=f"📋 Tipo/Status: {self.cliente_selecionado[6]}")
            self.frame_detalhe_cliente.config(bg="#d5dbdb")

    def carregar_pedido_existente(self):
        """Caso o pedido já exista, preenche o status e os itens salvos nele"""
        try:
            conn = database.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT status_pedido, cliente_id FROM pedidos WHERE id = ?", (self.pedido_id_existente,))
            p_info = cursor.fetchone()
            
            if p_info:
                self.var_status_pedido.set(p_info[0])
                cursor.execute("SELECT id, nome, telefone, logradouro, numero, bairro, status_cliente FROM clientes WHERE id = ?", (p_info[1],))
                cli = cursor.fetchone()
                if cli:
                    self.cliente_selecionado = cli
                    self.lbl_nome_cli.config(text=f"👤 {cli[1].upper()}", fg="#2c3e50")
                    self.lbl_tel_cli.config(text=f"📞 Telefone: {cli[2]}")
                    self.lbl_status_cli.config(text=f"📋 Tipo/Status: {cli[6]}")
            
            itens_salvos = database.obter_produtos_do_pedido(self.pedido_id_existente)
            for item in itens_salvos:
                item_id, produto, qtd, preco_unitario, subtotal = item
                self.tree.insert("", "end", values=(produto, f"R$ {preco_unitario:.2f}"))
                self.carrinho_itens_ids.append((item_id, qtd, preco_unitario))
                self.total_pedido += subtotal
                
            self.lbl_total.config(text=f"TOTAL: R$ {self.total_pedido:.2f}")
            conn.close()
        except Exception as e:
            print(f"Erro ao carregar pedido: {e}")

    def adicionar_item(self, item):
        """Adiciona o produto selecionado ao carrinho visual e lógico"""
        if not self.cliente_selecionado:
            messagebox.showwarning("Aviso", "Identifique e selecione o cliente no Passo 1 primeiro.")
            return
            
        self.tree.insert("", "end", values=(item[1], f"R$ {item[2]:.2f}"))
        self.carrinho_itens_ids.append((item[0], 1, item[2]))
        
        self.total_pedido += item[2]
        self.lbl_total.config(text=f"TOTAL: R$ {self.total_pedido:.2f}")

    def remover_item(self):
        """Remove o item marcado na lista e desconta do preço total"""
        sel = self.tree.selection()
        if sel:
            for i in sel:
                indice_item = self.tree.index(i)
                self.tree.delete(i)
                if indice_item < len(self.carrinho_itens_ids):
                    item_removido = self.carrinho_itens_ids.pop(indice_item)
                    preco_desconto = item_removido[2] * item_removido[1]
                    self.total_pedido -= preco_desconto
                
            self.lbl_total.config(text=f"TOTAL: R$ {self.total_pedido:.2f}")

    def cancelar_pedido(self):
        """Cancela e remove o pedido de forma segura se ele já existia no banco"""
        if not self.pedido_id_existente:
            self.destroy()
            return
            
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja EXCLUIR/CANCELAR permanentemente este pedido?"):
            try:
                conn = database.conectar()
                cursor = conn.cursor()
                with conn:
                    cursor.execute("DELETE FROM pedidos WHERE id = ?", (self.pedido_id_existente,))
                conn.close()
                messagebox.showinfo("Sucesso", "Pedido cancelado com sucesso!")
                self.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao cancelar: {e}")

    def finalizar_e_salvar_pedido(self):
        """Abre a janela de pagamento antes de salvar o pedido no banco."""
        if not self.cliente_selecionado:
            messagebox.showwarning("Atenção", "Selecione o cliente antes de fechar.")
            return

        if not self.carrinho_itens_ids and not self.pedido_id_existente:
            messagebox.showwarning("Atenção", "O carrinho está vazio.")
            return

        self.abrir_janela_pagamento()

    def abrir_janela_pagamento(self):
        """Abre uma janela de pagamento modal com opções e confirmação."""
        janela_pagamento = tk.Toplevel(self)
        janela_pagamento.title("McLanches Delivery - Pagamento")
        janela_pagamento.configure(bg=self.bg_fundo)
        janela_pagamento.grab_set()
        janela_pagamento.transient(self)

        largura = 520
        altura = 380
        x = (self.winfo_screenwidth() - largura) // 2
        y = (self.winfo_screenheight() - altura) // 2
        janela_pagamento.geometry(f"{largura}x{altura}+{x}+{y}")
        janela_pagamento.resizable(False, False)

        pedido_texto = f"Pedido: {self.pedido_id_existente if self.pedido_id_existente else 'novo'}"
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')

        header = tk.Label(janela_pagamento, text=f" {data_hora} | {pedido_texto}",
                          font=("Arial", 12, "bold"), bg=self.bg_fundo, fg=self.cor_texto, anchor="w")
        header.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(janela_pagamento, text="🧾 Total do Pedido", font=("Arial", 16, "bold"), bg=self.bg_fundo, fg=self.cor_texto).pack(pady=(10, 4))
        tk.Label(janela_pagamento, text=f"R$ {self.total_pedido:.2f}", font=("Arial", 20, "bold"), bg=self.bg_fundo, fg="#16a085").pack(pady=(0, 15))

        frame_pagamento = tk.LabelFrame(janela_pagamento, text=" Escolha a forma de pagamento ", bg=self.bg_fundo, fg=self.cor_texto,
                                       font=("Arial", 11, "bold"), bd=2, relief="solid", padx=20, pady=12)
        frame_pagamento.pack(fill="x", padx=30, pady=10)

        self.var_pagamento = tk.StringVar(value="Dinheiro")
        opcoes = ["Dinheiro", "Cartão", "PIX", "Voucher"]
        for idx, opcao in enumerate(opcoes):
            tk.Radiobutton(frame_pagamento, text=opcao, variable=self.var_pagamento, value=opcao,
                           bg=self.bg_fundo, fg=self.cor_texto, font=("Arial", 11), selectcolor="#d5dbdb",
                           activebackground=self.bg_fundo, activeforeground=self.cor_texto).grid(row=0, column=idx, padx=10, pady=4)

        tk.Label(janela_pagamento, text="Confirme o pagamento para finalizar o pedido ou cancele para voltar.",
                 bg=self.bg_fundo, fg="#7f8c8d", font=("Arial", 11)).pack(pady=(10, 6))

        btn_frame = tk.Frame(janela_pagamento, bg=self.bg_fundo)
        btn_frame.pack(pady=10)

        btn_finalizar = tk.Button(btn_frame, text="✔️ Finalizar Pedido", bg="#27ae60", fg="#ffffff",
                                  font=("Arial", 11, "bold"), relief="solid", bd=1,
                                  command=lambda: self._confirmar_pagamento(janela_pagamento))
        btn_finalizar.grid(row=0, column=0, padx=10, ipadx=10, ipady=8)

        btn_cancelar = tk.Button(btn_frame, text="✖️ Cancelar Pagamento", bg="#ffffff", fg="#c0392b",
                                 font=("Arial", 11, "bold"), relief="solid", bd=1,
                                 command=janela_pagamento.destroy)
        btn_cancelar.grid(row=0, column=1, padx=10, ipadx=10, ipady=8)

        janela_pagamento.wait_window()

    def _confirmar_pagamento(self, janela_pagamento):
        """Salva o pedido após o usuário confirmar o pagamento."""
        try:
            id_cliente = self.cliente_selecionado[0]
            total_arredondado = round(self.total_pedido, 2)
            novo_status = self.var_status_pedido.get()
            metodo_pagamento = self.var_pagamento.get() if hasattr(self, 'var_pagamento') else 'Dinheiro'

            if self.pedido_id_existente:
                database.atualizar_status_pedido(self.pedido_id_existente, novo_status)
                messagebox.showinfo("Sucesso", f"Pedido atualizado e pagamento confirmado ({metodo_pagamento}).")
            else:
                database.salvar_pedido(id_cliente, total_arredondado, self.carrinho_itens_ids, status=novo_status)
                messagebox.showinfo("Sucesso", f"Pedido de R$ {total_arredondado:.2f} registrado com sucesso com pagamento em {metodo_pagamento}.")

            janela_pagamento.destroy()
            self.limpar_para_proxima_venda()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar a operação: {e}")

    def limpar_para_proxima_venda(self):
        """Reseta o carrinho para permitir uma nova venda no mesmo PDV."""
        self.tree.delete(*self.tree.get_children())
        self.carrinho_itens_ids.clear()
        self.total_pedido = 0.0
        self.lbl_total.config(text="TOTAL: R$ 0.00")
        self.pedido_id_existente = None
        self.var_status_pedido.set('pendente')

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    janela = JanelaCadastroPedidos(root)
    root.mainloop()