import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkfont
import database  # Módulo de banco de dados relacional refatorado anteriormente

# Importação dos módulos das janelas secundárias
try:
    from cadastro_clientes import JanelaCadastroClientes
except ImportError:
    from cadastro_clientes import JanelaCadastroClientes as JanelaCadastroClientes

from cadastro_produtos import JanelaCadastroProdutos
from cadastro_pedidos import JanelaCadastroPedidos

class SistemaJAD:
    def __init__(self, root):
        self.root = root
        self.root.title("***** Sistema JAD - McLanches Delivery *****")
        
        # -------------------------------------------------------------
        # INICIAR A JANELA MAXIMIZADA (Multiplataforma)
        # -------------------------------------------------------------
        try:
            # Funciona nativamente no Windows e na maioria das distribuições Linux
            self.root.state('zoomed')
        except tk.TclError:
            # Caso falhe (ex: macOS), maximiza capturando as dimensões físicas da tela
            largura = self.root.winfo_screenwidth()
            altura = self.root.winfo_screenheight()
            self.root.geometry(f"{largura}x{altura}+0+0")
            
        self.root.configure(bg="#f4f6f9")
        
        self.modo_atual = "clientes" 
        self.setup_ui()
        
        # Configuração de Tags de Cores para as Linhas da Tabela
        self.tree.tag_configure('inativo', background="#e0e0e0", foreground='#424242')
        self.tree.tag_configure('finalizado', background="#bdc3c7", foreground='white') 
        self.tree.tag_configure('prioridade', foreground="#d32f2f") # Destaca prioridades em vermelho discreto
        
        # Inicia o sistema listando os clientes cadastrados
        self.exibir_clientes()

    def setup_ui(self):
        # Título Principal do Sistema (Identidade do MCLanches)
        tk.Label(self.root, text="🍔 MCLanches Delivery System 🍟", 
                 font=("Arial", 22, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=15)

        # -------------------------------------------------------------
        # 1. CAMPO DE BUSCA AMPLIADO COM BORDAS SÓLIDAS E FOCUS E HOVER
        # -------------------------------------------------------------
        frame_busca = tk.LabelFrame(self.root, text=" Painel de Pesquisa ", bg="#f4f6f9", 
                                    font=("Arial", 10, "bold"), bd=2, relief="solid")
        frame_busca.pack(fill="x", padx=40, pady=10, ipady=8)
        
        tk.Label(frame_busca, text="Digite para buscar:", bg="#f4f6f9", font=("Arial", 11, "bold")).pack(side="left", padx=15)
        
        # Caixa de busca maior (font 13) com bordas sólidas
        self.ent_busca = tk.Entry(frame_busca, font=("Arial", 13), bd=1, relief="solid", highlightthickness=1, highlightbackground="#2c3e50")
        self.ent_busca.pack(side="left", padx=10, fill="x", expand=True, ipady=4)
        self.ent_busca.bind("<KeyRelease>", self.filtrar_dados) 
        
        # --- APLICAÇÃO DE FOCUS E HOVER NO CAMPO DE TEXTO ---
        self.ent_busca.bind("<Enter>", lambda e: e.widget.config(highlightbackground="#3498db") if e.widget != self.root.focus_get() else None)
        self.ent_busca.bind("<Leave>", lambda e: e.widget.config(highlightbackground="#2c3e50") if e.widget != self.root.focus_get() else None)
        self.ent_busca.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground="#27ae60", highlightthickness=2))
        self.ent_busca.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground="#2c3e50", highlightthickness=1))

        # -------------------------------------------------------------
        # 2. MENU DE BOTÕES COM ESTILO, BORDAS E HOVER PADRONIZADO
        # -------------------------------------------------------------
        frame_menu = tk.LabelFrame(self.root, text=" Operações do Sistema ", bg="#f4f6f9",
                                   font=("Arial", 10, "bold"), bd=2, relief="solid")
        frame_menu.pack(fill="x", padx=40, pady=10, ipady=5)
        
        # Botões estilizados no padrão iniciante (usando propriedades nativas do Tkinter)
        btn_style = {
            "width": 16, "height": 2, "bg": "#ffffff", "fg": "#2c3e50", 
            "font": ("Arial", 10, "bold"), "relief": "solid", "bd": 1, "cursor": "hand2"
        }

        botoes = [
            ("Novo Pedido", self.abrir_pedido_vazio),
            ("Novo Cliente", self.abrir_cadastro),
            ("Ver Clientes", self.exibir_clientes),
            ("Ver Produtos", self.editar_produtos),
            ("Ver Pedidos", self.exibir_pedidos),
            ("Sair", self.confirmar_saida)
        ]

        # Posiciona os botões lado a lado proporcionalmente aplicando hover estruturado
        for i, (texto, comando) in enumerate(botoes):
            btn = tk.Button(frame_menu, text=texto, command=comando, **btn_style)
            btn.grid(row=0, column=i, padx=12, pady=5, sticky="nsew")
            frame_menu.grid_columnconfigure(i, weight=1) # Distribui espaço igualmente
            
            # --- APLICAÇÃO DE HOVER EM TODOS OS BOTÕES DO MENU ---
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2c3e50", fg="#ffffff"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#ffffff", fg="#2c3e50"))

        # -------------------------------------------------------------
        # 3. LISTA (TREEVIEW) COM FONTES GRANDES E BORDAS SÓLIDAS
        # -------------------------------------------------------------
        self.tree_frame = tk.LabelFrame(self.root, text=" Visualização dos Dados (Duplo clique para Detalhar/Editar) ", 
                                        bg="white", font=("Arial", 10, "bold"), bd=2, relief="solid")
        self.tree_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # Customização do tamanho das fontes globais da tabela via ttk.Style
        style = ttk.Style()
        style.theme_use("default")
        
        # Configura a fonte do cabeçalho da tabela
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#e2e6ea", foreground="#2c3e50")
        
        # Configura a fonte das linhas da tabela e aumenta o espaço vertical entre elas (rowheight)
        style.configure("Treeview", font=("Arial", 11), rowheight=28) 

        self.tree = ttk.Treeview(self.tree_frame, selectmode="browse", show="headings")
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Vincula ação de DUPLO CLIQUE para abrir edição/visualização de dados
        self.tree.bind("<Double-1>", lambda e: self.editar_selecionado())
        # Vincula ação de clique esquerdo para exibir o aviso rápido do pedido
        self.tree.bind("<Button-1>", self._on_tree_left_click)
       
        # Menu de contexto para alterar status do pedido via clique direito
        self.menu_status_pedido = tk.Menu(self.root, tearoff=0)
        for status in ["pendente", "em preparo", "saiu para entrega", "entregue"]:
            self.menu_status_pedido.add_command(
                label=f"Alterar para '{status}'",
                command=lambda s=status: self._alterar_status_selecionado(s)
            )
        self.tree.bind("<Button-3>", self.mostrar_menu_status_pedido)
        self.tree.bind("<Leave>", lambda e: self._fechar_info_popup())
        self.info_popup = None
        self.info_popup_item = None
        
        # Barra de rolagem lateral da tabela
        scrol = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrol.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrol.set)

        # Exibição do Rodapé de Totens/Vendas
        self.lbl_total = tk.Label(self.root, text="", font=("Arial", 13, "bold"), bg="#f4f6f9", fg="#16a085")
        self.lbl_total.pack(pady=10)

    def preparar_colunas(self, colunas):
        """Limpa a tabela e redefine as colunas necessárias"""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = colunas
        for col in colunas:
            header = col.replace("_", " ").title()
            self.tree.heading(col, text=header, anchor="center")
            self.tree.column(col, width=150, anchor="center")
        self.tree.column(colunas[0], width=60) # Mantém coluna ID sempre menor

    def exibir_clientes(self):
        """Carrega e exibe os clientes do Banco de Dados"""
        self.modo_atual = "clientes"
        self.lbl_total.config(text="")
        self.preparar_colunas(("id", "nome", "telefone", "endereco", "status"))
        
        dados = sorted(database.listar_clientes(), key=lambda x: str(x[1]).lower())
        for c in dados:
            endereco = f"{c[3]}, {c[4]} - {c[5]}".strip().replace(" ,", "")
            status = str(c[8])
            tag = "inativo" if status == "Inativo" else "prioridade" if status in ["Idoso", "PCD", "PCD/Idoso"] else ""
            self.tree.insert("", "end", values=(c[0], c[1], c[2], endereco, status), tags=(tag,))

    def exibir_pedidos(self):
        """Carrega e exibe o histórico de pedidos"""
        self.modo_atual = "pedidos"
        self.preparar_colunas(("id", "cliente", "valor", "data", "status_pedido"))
        
        dados = database.listar_pedidos_detalhados()
        total = 0.0
        for p in dados:
            try: 
                total += float(p[2])
            except: 
                pass
            
            tag = "finalizado" if p[4] in ["finalizado", "entregue"] else ""
            self.tree.insert("", "end", values=(p[0], p[1], f"R$ {p[2]:.2f}", p[3], p[4]), tags=(tag,))
            
        self.lbl_total.config(text=f"Faturamento Total das Vendas: R$ {total:.2f}")

    def editar_produtos(self):
        """Carrega e exibe la lista de produtos no cardápio"""
        self.modo_atual = "produtos"
        self.lbl_total.config(text="")
        self.preparar_colunas(("id", "produto", "preco", "quantidade", "categoria", "status_item"))
        
        dados = sorted(database.listar_itens(), key=lambda x: str(x[1]).lower())
        for item in dados:
            tag = "inativo" if item[5] in ["Fora de estoque", "sem estoque"] else ""
            self.tree.insert("", "end", values=(item[0], item[1], f"R$ {item[2]:.2f}", item[3], item[4], item[5]), tags=(tag,))

    # -----------------------------------------------------------------
    # CORREÇÃO CRÍTICA: ABRE O PDV CASO O CLIQUE SEJA EM UM PEDIDO EXISTENTE
    # -----------------------------------------------------------------
    def editar_selecionado(self):
        """Abre a respectiva janela de edição/visualização de acordo com a aba atual"""
        item = self.tree.selection()
        if not item: 
            return
        
        dados = self.tree.item(item)["values"]
        
        if self.modo_atual == "clientes":
            janela = JanelaCadastroClientes(self.root, dados_cliente=dados, callback_pedido=self.abrir_pedido)
            self.root.wait_window(janela)
            self.exibir_clientes()
            
        elif self.modo_atual == "produtos":
            janela = JanelaCadastroProdutos(self.root, dados_produto=dados)
            self.root.wait_window(janela)
            self.editar_produtos()
            
        elif self.modo_atual == "pedidos":
            # Captura o ID do pedido e o nome do cliente para abrir o PDV em modo de edição
            pedido_id = dados[0]
            nome_cliente_vinculado = dados[1]
            self.abrir_pedido(nome_cliente=nome_cliente_vinculado, pedido_id=pedido_id)

    def mostrar_menu_status_pedido(self, event):
        """Exibe o menu de contexto para mudar o status do pedido via clique direito."""
        if self.modo_atual != "pedidos":
            return

        item = self.tree.identify_row(event.y)
        if not item:
            return

        self.tree.selection_set(item)
        self.menu_status_pedido.post(event.x_root, event.y_root)

    def _on_tree_left_click(self, event):
        """Mostra o aviso rápido apenas no primeiro clique esquerdo sobre um pedido."""
        if self.modo_atual != "pedidos":
            return

        item = self.tree.identify_row(event.y)
        if not item:
            return

        if self.info_popup_item == item:
            return

        self.tree.selection_set(item)
        self._mostrar_info_popup(event, "Ação rápida: clique com o botão direito neste pedido para mudar o status.")
        self.info_popup_item = item

    def _mostrar_info_popup(self, event, texto):
        self._fechar_info_popup()
        popup = tk.Toplevel(self)
        popup.overrideredirect(True)
        popup.configure(bg="#fff8dc", padx=10, pady=6)
        label = tk.Label(popup, text=texto, bg="#fff8dc", fg="#2c3e50", font=("Arial", 10), justify="left")
        label.pack()
        x = event.x_root + 10
        y = event.y_root + 10
        popup.geometry(f"+{x}+{y}")
        self.info_popup = popup

    def _fechar_info_popup(self):
        if self.info_popup is not None:
            try:
                self.info_popup.destroy()
            except Exception:
                pass
            self.info_popup = None
            self.info_popup_item = None

    def _alterar_status_selecionado(self, novo_status):
        """Altera o status do pedido selecionado após confirmação."""
        item = self.tree.selection()
        if not item:
            return

        dados = self.tree.item(item)["values"]
        if not dados:
            return

        pedido_id = dados[0]
        pergunta = f"Deseja realmente mudar o status do pedido {pedido_id} para '{novo_status}'?"
        if messagebox.askyesno("Confirmar alteração", pergunta):
            database.atualizar_status_pedido(pedido_id, novo_status)
            messagebox.showinfo("Status atualizado", f"O status do pedido {pedido_id} foi alterado para '{novo_status}'.")
            self.exibir_pedidos()

    def filtrar_dados(self, event):
        """Mecanismo simplificado de busca em tempo real"""
        termo = self.ent_busca.get().lower()
        self.tree.delete(*self.tree.get_children())
        
        if self.modo_atual == "clientes":
            dados_raw = database.listar_clientes()
            for d in dados_raw:
                if termo in str(d[1]).lower() or termo in str(d[2]).lower():
                    endereco = f"{d[3]}, {d[4]} - {d[5]}".strip().replace(" ,", "")
                    tag = "inativo" if d[8] == "Inativo" else "prioridade" if d[8] in ["Idoso", "PCD"] else ""
                    self.tree.insert("", "end", values=(d[0], d[1], d[2], endereco, d[8]), tags=(tag,))
                    
        elif self.modo_atual == "produtos":
            dados_raw = database.listar_itens()
            for d in dados_raw:
                if termo in str(d[1]).lower() or termo in str(d[4]).lower():
                    tag = "inativo" if d[5] in ["sem estoque", "Fora de estoque"] else ""
                    self.tree.insert("", "end", values=(d[0], d[1], f"R$ {d[2]:.2f}", d[3], d[4], d[5]), tags=(tag,))
                    
        else:
            dados_raw = database.listar_pedidos_detalhados()
            for d in dados_raw:
                if termo in str(d[1]).lower() or termo in str(d[4]).lower():
                    tag = "finalizado" if d[4] in ["finalizado", "entregue"] else ""
                    self.tree.insert("", "end", values=(d[0], d[1], f"R$ {d[2]:.2f}", d[3], d[4]), tags=(tag,))

    def abrir_cadastro(self):
        """Abre janela para cadastrar novo cliente"""
        janela = JanelaCadastroClientes(self.root, callback_pedido=self.abrir_pedido)
        self.root.wait_window(janela)
        self.exibir_clientes()

    def abrir_pedido_vazio(self):
        """Abre a tela de pedidos sem cliente pré-selecionado"""
        self.abrir_pedido(None)

    def abrir_pedido(self, nome_cliente=None, pedido_id=None):
        """Abre a tela de vendas/PDV trazendo os dados do cliente selecionado e, opcionalmente, o pedido existente."""
        janela = JanelaCadastroPedidos(self.root, nome_cliente_inicial=nome_cliente, pedido_id_existente=pedido_id)
        if hasattr(janela, 'top'): 
            self.root.wait_window(janela.top)
        self.exibir_pedidos()

    def confirmar_saida(self):
        """Confirmação amigável de encerramento"""
        if messagebox.askyesno("Sair do Sistema", "Deseja realmente fechar o sistema MCLanches?"): 
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaJAD(root)
    root.mainloop()