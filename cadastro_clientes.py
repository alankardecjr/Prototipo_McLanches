import tkinter as tk
from tkinter import messagebox
import sqlite3
import database  # Utiliza o banco de dados relacional refatorado

class JanelaCadastroClientes(tk.Toplevel):
    def __init__(self, master, dados_cliente=None, callback_pedido=None):
        super().__init__(master)
        self.title("***** Sistema JAD - McLanches Delivery *****")
        
        # AJUSTE: Tamanho reduzido para a janela ficar mais compacta e elegante
        self.geometry("500x550") 
        self.resizable(False, False)
        
        # Paleta de cores padronizada com a Main
        self.bg_fundo = "#f4f6f9"
        self.bg_card = "#ffffff"
        self.cor_borda = "#2c3e50"  # Borda sólida escura para as caixas
        self.cor_texto = "#2c3e50"
        self.cor_lbl = "#2c3e50"
        
        self.configure(bg=self.bg_fundo)
        self.cliente_id = None
        self.callback_pedido = callback_pedido 

        self.criar_widgets()
        
        # Se receber dados da Main (Edição), preenche os campos automaticamente
        if dados_cliente:
            self.preencher_dados(dados_cliente)            
     
        # Prende o foco nesta janela até que ela seja fechada
        self.grab_set()

    def criar_widgets(self):
        # -------------------------------------------------------------
        # PAINEL FORMULÁRIO (LabelFrame com bordas bem marcadas igual à Main)
        # -------------------------------------------------------------
        main_frame = tk.LabelFrame(self, text=" Gerenciamento de Clientes ", bg=self.bg_fundo,
                                   font=("Arial", 11, "bold"), bd=2, relief="solid", padx=20, pady=5)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Função auxiliar simples para criar os campos de entrada padronizados
        def criar_campo(parent, texto, row, col=0, colspan=2, width=None):
            tk.Label(parent, text=texto, bg=self.bg_fundo, fg=self.cor_lbl, 
                     font=("Arial", 9, "bold")).grid(row=row, column=col, sticky="w", pady=(5, 1))
            
            # Entry com borda sólida nativa para melhor legibilidade
            ent = tk.Entry(parent, font=("Arial", 11), bg=self.bg_card, fg=self.cor_texto,
                           relief="solid", bd=1)
            
            if width: 
                ent.config(width=width)
            
            ent.grid(row=row+1, column=col, columnspan=colspan, sticky="ew", ipady=3, padx=(0, 5) if colspan==1 else 0)
            return ent

        # --- CAMPOS DO FORMULÁRIO (Espaçamentos internos reduzidos) ---
        self.ent_nome = criar_campo(main_frame, "NOME COMPLETO", 1)
        self.ent_tel = criar_campo(main_frame, "TELEFONE", 3)
        self.ent_logra = criar_campo(main_frame, "LOGRADOURO (Rua/Av)", 5, col=0, colspan=1)
        self.ent_num = criar_campo(main_frame, "Nº", 5, col=1, colspan=1, width=5)
        self.ent_bairro = criar_campo(main_frame, "BAIRRO", 7)
        self.ent_ref = criar_campo(main_frame, "PONTO DE REFERÊNCIA", 9)
        self.txt_obs = criar_campo(main_frame, "OBSERVAÇÕES DO ENDEREÇO", 11)

        # --- STATUS DO CLIENTE ---
        tk.Label(main_frame, text="STATUS DO CLIENTE", bg=self.bg_fundo, fg=self.cor_lbl, 
                 font=("Arial", 9, "bold")).grid(row=13, column=0, sticky="w", pady=(8, 1))
        
        self.var_status = tk.StringVar(value="Ativo")
        self.opt_status = tk.OptionMenu(main_frame, self.var_status, "Ativo", "Inativo", "Vip", "PCD/Idoso")
        self.opt_status.config(bg=self.bg_card, fg=self.cor_texto, relief="solid", bd=1, 
                               font=("Arial", 10), cursor="hand2", highlightthickness=0)
        self.opt_status.grid(row=14, column=0, columnspan=2, sticky="ew", ipady=1)

        # -------------------------------------------------------------
        # AJUSTE: PAINEL DE BOTÕES TOTALMENTE ALINHADOS LADO A LADO
        # -------------------------------------------------------------
        btn_frame = tk.Frame(main_frame, bg=self.bg_fundo)
        btn_frame.grid(row=15, column=0, columnspan=2, pady=(15, 5), sticky="ew")

        # Configura as 3 colunas do frame de botões para terem tamanhos iguais
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        btn_style = {
            "font": ("Arial", 9, "bold"), "relief": "solid", "bd": 1, "cursor": "hand2"
        }

        # Botão Salvar / Atualizar (Coluna 0)
        self.btn_salvar = tk.Button(btn_frame, text="💾 SALVAR", bg="#ffffff", fg="#27ae60", 
                                    command=self.salvar_e_sair, **btn_style)
        self.btn_salvar.grid(row=0, column=0, padx=4, ipady=6, sticky="ew")

        # Botão Pedir (Coluna 1)
        self.btn_pedido = tk.Button(btn_frame, text="🛒 PEDIR", bg="#ffffff", fg="#2980b9", 
                                    command=self.salvar_e_pedir, **btn_style)
        self.btn_pedido.grid(row=0, column=1, padx=4, ipady=6, sticky="ew")

        # Botão Fechar Janela (Coluna 2)
        self.btn_sair_janela = tk.Button(btn_frame, text="🚪 FECHAR", bg="#ffffff", fg="#7f8c8d", 
                                        command=self.fechar_limpar, **btn_style)
        self.btn_sair_janela.grid(row=0, column=2, padx=4, ipady=6, sticky="ew")

        # Configuração de pesos das colunas do formulário
        main_frame.columnconfigure(0, weight=4)
        main_frame.columnconfigure(1, weight=1)

    def fechar_limpar(self):
        """Libera o foco do sistema e fecha a janela"""
        self.grab_release()
        self.destroy()

    def coletar_dados(self):
        """Coleta as strings limpas digitadas nos campos"""
        return {
            "nome": self.ent_nome.get().strip(),
            "tel": self.ent_tel.get().strip(),
            "logra": self.ent_logra.get().strip(),
            "num": self.ent_num.get().strip(),
            "bairro": self.ent_bairro.get().strip(),
            "ref": self.ent_ref.get().strip(),
            "obs": self.txt_obs.get().strip(),
            "status": self.var_status.get()
        }

    def validar_e_salvar(self):
        """Valida campos obrigatórios e salva as alterações no SQLite"""
        d = self.coletar_dados()
        if not d["nome"] or not d["tel"] or not d["logra"]:
            messagebox.showwarning("Atenção", "Os campos Nome, Telefone e Logradouro são obrigatórios.")
            return False
        
        try:
            if self.cliente_id:
                database.atualizar_cliente(self.cliente_id, d["nome"], d["tel"], d["logra"], 
                                          d["num"], d["bairro"], d["ref"], d["obs"], d["status"])
            else:
                database.salvar_cliente(d["nome"], d["tel"], d["logra"], d["num"], 
                                       d["bairro"], d["ref"], d["obs"], d["status"])
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este número de telefone já está cadastrado para outro cliente.")
            return False

    def salvar_e_sair(self):
        """Salva o cliente e apenas fecha a janela retornando para a Main"""
        if self.validar_e_salvar():
            self.fechar_limpar()

    def salvar_e_pedir(self):
        """Salva/Atualiza o cliente e dispara o callback abrindo a tela de PDV já com o nome dele"""
        d = self.coletar_dados()
        if self.validar_e_salvar():
            self.fechar_limpar()  # Fecha a janela atual primeiro
            if self.callback_pedido:
                # Dispara a abertura do PDV levando o nome como parâmetro inicial de busca automática
                self.callback_pedido(d["nome"])

    def preencher_dados(self, dados):
        """Preenche o formulário ao abrir em modo de edição (Duplo clique na Main)"""
        self.cliente_id = dados[0]
        self.ent_nome.insert(0, str(dados[1]))
        self.ent_tel.insert(0, str(dados[2]))
        
        if len(dados) > 3:
            try:
                self.ent_logra.insert(0, str(dados[3]))
                self.ent_num.insert(0, str(dados[4]))
                self.ent_bairro.insert(0, str(dados[5]))
                self.ent_ref.insert(0, str(dados[6]))
                self.txt_obs.insert(0, str(dados[7]))
                self.var_status.set(dados[8])
            except IndexError:
                pass
                
        self.btn_salvar.config(text="🔄 ATUALIZAR")

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw() 
    JanelaCadastroClientes(root)
    root.mainloop()