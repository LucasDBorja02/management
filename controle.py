import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Função para criar o banco de dados e a tabela de vendas
def create_vendas_db():
    db_path = 'C:/Users/ld388/Desktop/management/site/pages/vendas.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_produto TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        total REAL NOT NULL,
        forma_pagamento TEXT NOT NULL,
        data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Em Preparo'
    )
    ''')

    conn.commit()
    conn.close()

class ControleVendasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Vendas")
        
        # Define a janela para tamanho normal
        self.root.geometry("1200x600")  # Define o tamanho inicial da janela
        self.root.resizable(True, True)  # Permite redimensionar a janela

        # Menu para minimizar ou restaurar a janela
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)
        janela_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Janela", menu=janela_menu)
        janela_menu.add_command(label="Minimizar", command=lambda: self.root.iconify())

        # Estilo
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))

        # Frame para lista de vendas - Em Preparo
        self.frame_list_preparo = ttk.Frame(root, padding="10")
        self.frame_list_preparo.grid(row=0, column=0, sticky="nsew")

        self.label_list_preparo = ttk.Label(self.frame_list_preparo, text="Em Preparo", font=('Arial', 14))
        self.label_list_preparo.grid(row=0, column=0, columnspan=2, pady=5)

        self.listbox_preparo = tk.Listbox(self.frame_list_preparo, width=60, height=20, border=1, selectmode=tk.SINGLE)
        self.listbox_preparo.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.scrollbar_preparo = ttk.Scrollbar(self.frame_list_preparo, orient=tk.VERTICAL)
        self.scrollbar_preparo.grid(row=1, column=1, sticky="ns")
        self.listbox_preparo.config(yscrollcommand=self.scrollbar_preparo.set)
        self.scrollbar_preparo.config(command=self.listbox_preparo.yview)

        # Frame para lista de vendas - Em Entrega
        self.frame_list_entrega = ttk.Frame(root, padding="10")
        self.frame_list_entrega.grid(row=0, column=1, sticky="nsew")

        self.label_list_entrega = ttk.Label(self.frame_list_entrega, text="Em Entrega", font=('Arial', 14))
        self.label_list_entrega.grid(row=0, column=0, columnspan=2, pady=5)

        self.listbox_entrega = tk.Listbox(self.frame_list_entrega, width=60, height=20, border=1, selectmode=tk.SINGLE)
        self.listbox_entrega.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.scrollbar_entrega = ttk.Scrollbar(self.frame_list_entrega, orient=tk.VERTICAL)
        self.scrollbar_entrega.grid(row=1, column=1, sticky="ns")
        self.listbox_entrega.config(yscrollcommand=self.scrollbar_entrega.set)
        self.scrollbar_entrega.config(command=self.listbox_entrega.yview)

        # Frame para lista de vendas - Concluído
        self.frame_list_concluido = ttk.Frame(root, padding="10")
        self.frame_list_concluido.grid(row=0, column=2, sticky="nsew")

        self.label_list_concluido = ttk.Label(self.frame_list_concluido, text="Pedido Concluído", font=('Arial', 14))
        self.label_list_concluido.grid(row=0, column=0, columnspan=2, pady=5)

        self.listbox_concluido = tk.Listbox(self.frame_list_concluido, width=60, height=20, border=1, selectmode=tk.SINGLE)
        self.listbox_concluido.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.scrollbar_concluido = ttk.Scrollbar(self.frame_list_concluido, orient=tk.VERTICAL)
        self.scrollbar_concluido.grid(row=1, column=1, sticky="ns")
        self.listbox_concluido.config(yscrollcommand=self.scrollbar_concluido.set)
        self.scrollbar_concluido.config(command=self.listbox_concluido.yview)

        # Frame para alterar o status da venda
        self.frame_status = ttk.Frame(root, padding="10")
        self.frame_status.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.label_status = ttk.Label(self.frame_status, text="Alterar Status da Venda", font=('Arial', 14))
        self.label_status.grid(row=0, column=0, pady=5)

        self.status_opcoes = ['Em Preparo', 'Em Entrega', 'Pedido Concluído']
        self.status_combo = ttk.Combobox(self.frame_status, values=self.status_opcoes, state="readonly")
        self.status_combo.grid(row=1, column=0, padx=5, pady=5)

        self.button_status = ttk.Button(self.frame_status, text="Alterar Status", command=self.alterar_status)
        self.button_status.grid(row=2, column=0, pady=10)

        # Configurações de redimensionamento
        self.frame_list_preparo.columnconfigure(0, weight=1)
        self.frame_list_preparo.rowconfigure(1, weight=1)
        self.frame_list_entrega.columnconfigure(0, weight=1)
        self.frame_list_entrega.rowconfigure(1, weight=1)
        self.frame_list_concluido.columnconfigure(0, weight=1)
        self.frame_list_concluido.rowconfigure(1, weight=1)
        self.frame_status.columnconfigure(0, weight=1)

        # Configurar as linhas e colunas da grade para redimensionamento
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=0)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Carregar vendas na lista
        self.carregar_vendas()

    def carregar_vendas(self):
        conn = sqlite3.connect('C:/Users/ld388/Desktop/management/site/pages/vendas.db')  # Conectar ao banco de dados de vendas
        c = conn.cursor()
        c.execute("SELECT id, nome_produto, quantidade, total, status FROM vendas")
        vendas = c.fetchall()
        conn.close()

        # Limpar todas as listas antes de adicionar os itens
        self.listbox_preparo.delete(0, tk.END)
        self.listbox_entrega.delete(0, tk.END)
        self.listbox_concluido.delete(0, tk.END)

        # Inserir cada venda na lista correspondente ao seu status
        for venda in vendas:
            texto_venda = f"Venda ID: {venda[0]}, Produto: {venda[1]}, Quantidade: {venda[2]}, Total: R${venda[3]:.2f}"
            if venda[4] == "Em Preparo":
                self.listbox_preparo.insert(tk.END, texto_venda)
            elif venda[4] == "Em Entrega":
                self.listbox_entrega.insert(tk.END, texto_venda)
            elif venda[4] == "Pedido Concluído":
                self.listbox_concluido.insert(tk.END, texto_venda)

    def alterar_status(self):
        # Determinar qual lista foi selecionada
        if self.listbox_preparo.curselection():
            selecionado = self.listbox_preparo.curselection()
            status_atual = "Em Preparo"
        elif self.listbox_entrega.curselection():
            selecionado = self.listbox_entrega.curselection()
            status_atual = "Em Entrega"
        elif self.listbox_concluido.curselection():
            selecionado = self.listbox_concluido.curselection()
            status_atual = "Pedido Concluído"
        else:
            messagebox.showerror("Erro", "Selecione uma venda para alterar o status")
            return

        venda_info = self.get_venda_info(status_atual, selecionado)
        venda_id = venda_info.split(",")[0].split(": ")[1]
        novo_status = self.status_combo.get()

        if not novo_status:
            messagebox.showerror("Erro", "Selecione um status para alterar")
            return

        conn = sqlite3.connect('C:/Users/ld388/Desktop/management/site/pages/vendas.db')
        c = conn.cursor()
        c.execute("UPDATE vendas SET status = ? WHERE id = ?", (novo_status, venda_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Status da venda alterado com sucesso!")
        self.carregar_vendas()

    def get_venda_info(self, status_atual, selecionado):
        if status_atual == "Em Preparo":
            return self.listbox_preparo.get(selecionado[0])
        elif status_atual == "Em Entrega":
            return self.listbox_entrega.get(selecionado[0])
        elif status_atual == "Pedido Concluído":
            return self.listbox_concluido.get(selecionado[0])

if __name__ == "__main__":
    root = tk.Tk()
    create_vendas_db()  # Criar a tabela de vendas se ainda não existir
    app = ControleVendasApp(root)
    root.mainloop()
