import tkinter as tk
from tkinter import messagebox
import sqlite3
import database  # Utiliza o banco de dados relacional refatorado

class JanelaCadastroProdutos(tk.Toplevel):
    def __init__(self, master, dados_produto=None):
        super().__init__(master)
        self.title("***** Sistema JAD - McLanches Delivery *****")
        
        # AJUSTE: Tamanho reduzido para manter o mesmo padrão compacto da janela de clientes
        self.geometry("500x420") 
        self.resizable(False, False)
        
        # Paleta de Cores unificada com a Main e Cadastro de Clientes
        self.bg_fundo = "#f4f6f9"
        self.bg_card = "#ffffff"
        self.cor_borda = "#2c3e50"  # Borda sólida escura
        self.cor_texto = "#2c3e50"
        self.cor_lbl = "#2c3e50"

        self.configure(bg=self.bg_fundo)
        self.produto_id = None

        self.criar_widgets()

        # Se receber dados do Main (Edição ao duplo clique), preenche os inputs automaticamente
        if dados_produto:
            self.preencher_dados(dados_produto)
            
        # Prende o foco do sistema nesta janela de diálogo até ser fechada
        self.grab_set()

    def criar_widgets(self):
        # -------------------------------------------------------------
        # PAINEL FORMULÁRIO (LabelFrame com bordas bem marcadas)
        # -------------------------------------------------------------
        main_frame = tk.LabelFrame(self, text=" Gerenciamento de Produtos ", bg=self.bg_fundo,
                                   font=("Arial", 11, "bold"), bd=2, relief="solid", padx=20, pady=5)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Função interna simples para criar campos de entrada textuais padronizados
        def criar_campo(parent, texto, row, col=0, colspan=2, width=None):
            tk.Label(parent, text=texto, bg=self.bg_fundo, fg=self.cor_lbl, 
                     font=("Arial", 9, "bold")).grid(row=row, column=col, sticky="w", pady=(5, 1))
            
            # Entry com borda sólida nativa para fácil compreensão do professor
            ent = tk.Entry(parent, font=("Arial", 11), bg=self.bg_card, fg=self.cor_texto,
                           relief="solid", bd=1)
            
            if width: 
                ent.config(width=width)
                
            ent.grid(row=row+1, column=col, columnspan=colspan, sticky="ew", ipady=3, padx=(0, 5) if colspan==1 else 0)
            return ent

        # --- CAMPOS DO FORMULÁRIO (Otimizados para a redução de tamanho) ---
        self.ent_produto = criar_campo(main_frame, "NOME DO PRODUTO / ITEM", 1)

        # Campo do tipo Categoria (Comida, Bebida, etc)
        tk.Label(main_frame, text="CATEGORIA", bg=self.bg_fundo, fg=self.cor_lbl, 
                 font=("Arial", 9, "bold")).grid(row=3, column=0, sticky="w", pady=(5, 1))
        
        self.var_categoria = tk.StringVar(value="Comida")
        self.opt_categoria = tk.OptionMenu(main_frame, self.var_categoria, "Comida", "Bebida")
        self.opt_categoria.config(bg=self.bg_card, fg=self.cor_texto, relief="solid", bd=1, 
                                   font=("Arial", 10), cursor="hand2", highlightthickness=0)
        self.opt_categoria.grid(row=4, column=0, columnspan=2, sticky="ew", ipady=1)

        # Preço e Quantidade lado a lado
        self.ent_preco = criar_campo(main_frame, "PREÇO REAL (R$)", 5, col=0, colspan=1)
        self.ent_qtd = criar_campo(main_frame, "QTD EM ESTOQUE", 5, col=1, colspan=1)

        # Campo de Status do Item
        tk.Label(main_frame, text="STATUS DO ESTOQUE", bg=self.bg_fundo, fg=self.cor_lbl, 
                 font=("Arial", 9, "bold")).grid(row=7, column=0, sticky="w", pady=(5, 1))
        
        self.var_status = tk.StringVar(value="em estoque")
        self.opt_status = tk.OptionMenu(main_frame, self.var_status, "em estoque", "sem estoque")
        self.opt_status.config(bg=self.bg_card, fg=self.cor_texto, relief="solid", bd=1, 
                                font=("Arial", 10), cursor="hand2", highlightthickness=0)
        self.opt_status.grid(row=8, column=0, columnspan=2, sticky="ew", ipady=1)

        # -------------------------------------------------------------
        # AJUSTE: PAINEL DE BOTÕES ALINHADOS LADO A LADO (Esquema Cad Cliente)
        # -------------------------------------------------------------
        btn_frame = tk.Frame(main_frame, bg=self.bg_fundo)
        btn_frame.grid(row=9, column=0, columnspan=2, pady=(15, 5), sticky="ew")

        # Configura as colunas do sub-frame de botões para preencherem igualmente o espaço
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        btn_style = {
            "font": ("Arial", 9, "bold"), "relief": "solid", "bd": 1, "cursor": "hand2"
        }

        # Botão Salvar (Lado Esquerdo)
        self.btn_salvar = tk.Button(btn_frame, text="💾 SALVAR", bg="#ffffff", fg="#27ae60", 
                                    command=self.salvar, **btn_style)
        self.btn_salvar.grid(row=0, column=0, padx=5, ipady=6, sticky="ew")

        # Botão Fechar Janela (Lado Direito)
        self.btn_fechar = tk.Button(btn_frame, text="🚪 FECHAR", bg="#ffffff", fg="#7f8c8d", 
                                    command=self.destroy, **btn_style)
        self.btn_fechar.grid(row=0, column=1, padx=5, ipady=6, sticky="ew")

        # Equaliza o peso das colunas internas para o Preço e Estoque ficarem simétricos
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def coletar_dados(self):
        """Captura e sanitiza os inputs digitados na janela"""
        # Limpa espaços e ajusta vírgulas para ponto no preço float
        preco_limpo = self.ent_preco.get().replace(',', '.').strip()
        return {
            "produto": self.ent_produto.get().strip(),
            "preco": preco_limpo,
            "quantidade": self.ent_qtd.get().strip(),
            "categoria": self.var_categoria.get(),
            "status": self.var_status.get()
        }

    def salvar(self):
        """Valida os tipos e persiste os dados do produto no SQLite"""
        d = self.coletar_dados()
        if not d["produto"] or not d["preco"]:
            messagebox.showwarning("Atenção", "O Nome do produto e o Preço são campos obrigatórios.")
            return

        try:
            # Tenta converter os dados para garantir integridade numérica do BD
            preco_float = float(d["preco"])
            qtd_int = int(d["quantidade"]) if d["quantidade"] else 0
            
            if self.produto_id:
                database.atualizar_item(self.produto_id, d["produto"], preco_float, 
                                       qtd_int, d["categoria"], d["status"])
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            else:
                database.salvar_item(d["produto"], preco_float, qtd_int, 
                                    d["categoria"], d["status"])
                messagebox.showinfo("Sucesso", "Novo produto cadastrado no cardápio!")
            
            self.destroy() # Fecha a janela após salvar para atualizar a grid principal

        except ValueError:
            messagebox.showerror("Erro de Tipo", "Digite valores numéricos válidos.\nEx: Preço: 24.90 | Estoque: 50")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível processar a operação: {e}")

    def preencher_dados(self, dados):
        """Injeta as variáveis caso a janela seja aberta a partir de um duplo clique no Main"""
        self.produto_id = dados[0]
        self.ent_produto.insert(0, dados[1])
        
        # Limpa o texto "R$" caso venha formatado da grid do Main
        preco_limpo = str(dados[2]).replace("R$", "").strip()
        self.ent_preco.insert(0, preco_limpo)
        
        self.ent_qtd.insert(0, str(dados[3]))
        self.var_categoria.set(dados[4])
        self.var_status.set(dados[5])
        
        self.btn_salvar.config(text="🔄 ATUALIZAR")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    JanelaCadastroProdutos(root)
    root.mainloop()