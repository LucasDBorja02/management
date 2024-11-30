import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# Configuração do caminho do banco de dados
DB_PATH = os.path.join(os.path.expanduser('~'), 'Desktop/management/site/pages/vendas.db')

# Função para criar o banco de dados e a tabela de vendas
def create_vendas_db():
    with sqlite3.connect(DB_PATH) as conn:
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

class ControleVendasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Vendas")
        self.root.geometry("1200x600")
        self.root.resizable(True, True)

        # Configuração do estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#ECF0F1')
        style.configure('TLabel', background='#ECF0F1', font=('Helvetica', 12))
        style.configure('TButton', background='#2C3E50', foreground='white', font=('Helvetica', 12), padding=5)
        style.map('TButton', background=[('active', '#1ABC9C')])

        # Título
        self.label_title = ttk.Label(self.root, text="Controle de Vendas", font=('Helvetica', 18, 'bold'), anchor='center')
        self.label_title.pack(pady=10)

        # Configuração dos frames principais
        self.frame_main = ttk.Frame(self.root, padding="10")
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        # Configuração dos frames para as listas
        self.frames = {
            "Em Preparo": self.create_list_frame("Em Preparo"),
            "Em Entrega": self.create_list_frame("Em Entrega"),
            "Pedido Concluído": self.create_list_frame("Pedido Concluído"),
        }

        # Configuração do frame para controle de status
        self.frame_status = ttk.Frame(self.root, padding="10")
        self.frame_status.pack(fill=tk.X)
        self.setup_status_controls()

        self.carregar_vendas()

    def create_list_frame(self, title):
        frame = ttk.Frame(self.frame_main, padding="10")
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        label = ttk.Label(frame, text=title, font=('Helvetica', 14))
        label.pack(pady=5)

        listbox = tk.Listbox(frame, width=40, height=20, border=1, selectmode=tk.SINGLE)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)

        return {"frame": frame, "listbox": listbox}

    def setup_status_controls(self):
        label_status = ttk.Label(self.frame_status, text="Alterar Status da Venda", font=('Helvetica', 14))
        label_status.pack(pady=5)

        self.status_opcoes = ['Em Preparo', 'Em Entrega', 'Pedido Concluído']
        self.status_combo = ttk.Combobox(self.frame_status, values=self.status_opcoes, state="readonly", font=('Helvetica', 12))
        self.status_combo.pack(pady=5)

        button_status = ttk.Button(self.frame_status, text="Alterar Status", command=self.alterar_status)
        button_status.pack(pady=10)

    def carregar_vendas(self):
        # Limpar todas as listas antes de adicionar os itens
        for key in self.frames:
            self.frames[key]["listbox"].delete(0, tk.END)

        # Consultar vendas
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT id, nome_produto, quantidade, total, status FROM vendas")
            vendas = c.fetchall()

        # Distribuir vendas nas listas correspondentes
        for venda in vendas:
            texto_venda = f"ID: {venda[0]} | Produto: {venda[1]} | Qtde: {venda[2]} | Total: R${venda[3]:.2f}"
            status = venda[4]
            if status in self.frames:
                self.frames[status]["listbox"].insert(tk.END, texto_venda)

    def alterar_status(self):
        venda_selecionada = None
        status_atual = None

        for status, frame_info in self.frames.items():
            listbox = frame_info["listbox"]
            if listbox.curselection():
                venda_selecionada = listbox.get(listbox.curselection()[0])
                status_atual = status
                break

        if not venda_selecionada:
            messagebox.showerror("Erro", "Selecione uma venda para alterar o status")
            return

        venda_id = int(venda_selecionada.split("|")[0].split(":")[1].strip())
        novo_status = self.status_combo.get()

        if not novo_status:
            messagebox.showerror("Erro", "Selecione um status para alterar")
            return

        # Atualizar status no banco de dados
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("UPDATE vendas SET status = ? WHERE id = ?", (novo_status, venda_id))
            conn.commit()

        messagebox.showinfo("Sucesso", "Status da venda alterado com sucesso!")
        self.carregar_vendas()

if __name__ == "__main__":
    root = tk.Tk()
    create_vendas_db()  # Criar a tabela de vendas se ainda não existir
    app = ControleVendasApp(root)
    root.mainloop()
