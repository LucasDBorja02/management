import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

class EstoqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciar Estoque")
        self.root.geometry("1366x768")
        self.root.configure(bg="#f0f4f7")

        # Configuração de estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure('TFrame', background="#f0f4f7")
        style.configure('TLabel', background="#f0f4f7", font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12), padding=6)
        style.configure('TEntry', font=('Arial', 12), padding=5)
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), background="#f0f4f7")
        style.map('TButton', background=[('!disabled', '#0078d4')], foreground=[('!disabled', 'white')])

        # Layout principal (dividido em duas colunas)
        self.frame_list = ttk.Frame(root, padding="10")
        self.frame_list.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        self.frame_edit = ttk.Frame(root, padding="10")
        self.frame_edit.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        # === Frame Lista de Produtos ===
        self.label_list = ttk.Label(self.frame_list, text="Lista de Produtos", style='Header.TLabel')
        self.label_list.grid(row=0, column=0, pady=10)

        self.listbox_produtos = tk.Listbox(self.frame_list, width=40, height=20, font=('Arial', 12), bg="white", bd=1, selectmode=tk.SINGLE, highlightthickness=1, relief="solid")
        self.listbox_produtos.grid(row=1, column=0, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(self.frame_list, orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.listbox_produtos.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox_produtos.yview)

        # Botões da lista
        self.button_view = ttk.Button(self.frame_list, text="Visualizar Detalhes", command=self.visualizar_detalhes)
        self.button_view.grid(row=2, column=0, pady=10, sticky="ew")

        self.button_delete = ttk.Button(self.frame_list, text="Excluir Produto", command=self.excluir_produto)
        self.button_delete.grid(row=3, column=0, pady=10, sticky="ew")

        self.button_add_stock = ttk.Button(self.frame_list, text="Adicionar Estoque", command=self.adicionar_estoque)
        self.button_add_stock.grid(row=4, column=0, pady=10, sticky="ew")

        self.button_baixo_estoque = ttk.Button(self.frame_list, text="Produtos Abaixo do Estoque", command=self.produtos_abaixo_estoque_minimo)
        self.button_baixo_estoque.grid(row=5, column=0, pady=10, sticky="ew")

        # === Frame Adicionar/Editar Produtos ===
        self.label_edit = ttk.Label(self.frame_edit, text="Editar Produto", style='Header.TLabel')
        self.label_edit.grid(row=0, column=0, columnspan=2, pady=10)

        campos = [
            ("ID do Produto", "entry_id"),
            ("Nome", "entry_nome"),
            ("Preço de Compra", "entry_preco_compra"),
            ("Preço de Venda", "entry_preco_venda"),
            ("Quantidade", "entry_quantidade"),
            ("Fornecedor", "entry_fornecedor"),
            ("Estoque Mínimo", "entry_estoque_minimo")
        ]
        self.entries = {}
        for i, (label_text, entry_name) in enumerate(campos):
            label = ttk.Label(self.frame_edit, text=label_text)
            label.grid(row=i + 1, column=0, sticky="e", pady=5)
            entry = ttk.Entry(self.frame_edit, width=30)
            entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky="ew")
            self.entries[entry_name] = entry

        # Botões do frame de edição
        self.button_save = ttk.Button(self.frame_edit, text="Salvar Produto", command=self.salvar_produto)
        self.button_save.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

        self.button_add = ttk.Button(self.frame_edit, text="Adicionar Novo Produto", command=self.adicionar_produto)
        self.button_add.grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")

        # Configurações adicionais
        self.carregar_produtos()

    def carregar_produtos(self):
        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("SELECT id, nome FROM produtos")
        produtos = c.fetchall()
        conn.close()

        self.listbox_produtos.delete(0, tk.END)
        for produto in produtos:
            self.listbox_produtos.insert(tk.END, f"{produto[0]} - {produto[1]}")
    def visualizar_detalhes(self):
        selecionado = self.listbox_produtos.curselection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um produto para visualizar")
            return

        produto_info = self.listbox_produtos.get(selecionado[0])
        produto_id = produto_info.split(" - ")[0]

        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        produto = c.fetchone()
        conn.close()

        if produto:
            detalhes_window = tk.Toplevel(self.root)
            detalhes_window.title("Detalhes do Produto")
            detalhes_window.geometry("400x350")

            ttk.Label(detalhes_window, text=f"ID: {produto[0]}", font=('Arial', 12)).pack(pady=5)
            ttk.Label(detalhes_window, text=f"Nome: {produto[1]}", font=('Arial', 12)).pack(pady=5)
            ttk.Label(detalhes_window, text=f"Preço de Compra: {produto[2]:.2f}", font=('Arial', 12)).pack(pady=5)
            ttk.Label(detalhes_window, text=f"Preço de Venda: {produto[3]:.2f}", font=('Arial', 12)).pack(pady=5)
            ttk.Label(detalhes_window, text=f"Quantidade: {produto[4]}", font=('Arial', 12)).pack(pady=5)
            ttk.Label(detalhes_window, text=f"Estoque Mínimo: {produto[6]}", font=('Arial', 12)).pack(pady=5)
            ttk.Label(detalhes_window, text=f"Fornecedor: {produto[5]}", font=('Arial', 12)).pack(pady=5)

            button_edit = ttk.Button(detalhes_window, text="Editar Produto", command=lambda: self.editar_produto(produto))
            button_edit.pack(pady=10)

    def editar_produto(self, produto):
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, produto[0])
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, produto[1])
        self.entry_preco_compra.delete(0, tk.END)
        self.entry_preco_compra.insert(0, produto[2])
        self.entry_preco_venda.delete(0, tk.END)
        self.entry_preco_venda.insert(0, produto[3])
        self.entry_quantidade.delete(0, tk.END)
        self.entry_quantidade.insert(0, produto[4])
        self.entry_fornecedor.delete(0, tk.END)
        self.entry_fornecedor.insert(0, produto[5])
        self.entry_estoque_minimo.delete(0, tk.END)
        self.entry_estoque_minimo.insert(0, produto[6])

    def salvar_produto(self):
        id_produto = self.entry_id.get()
        nome = self.entry_nome.get()
        
        # Verifica se os preços e quantidades são válidos
        try:
            preco_compra = float(self.entry_preco_compra.get())
            preco_venda = float(self.entry_preco_venda.get())
            quantidade = int(self.entry_quantidade.get())
            fornecedor = self.entry_fornecedor.get()  # Adicionado aqui
            estoque_minimo = int(self.entry_estoque_minimo.get())

            if preco_compra <= 0 or preco_venda <= 0 or quantidade <= 0 or estoque_minimo <= 0:
                raise ValueError("Os valores devem ser maiores que zero.")
        except ValueError as e:
            messagebox.showerror("Erro", f"Dados inválidos: {e}")
            return

        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute('''UPDATE produtos SET nome=?, preco_compra=?, preco_venda=?, quantidade=?, fornecedor=?, estoque_minimo=? WHERE id=?''',
                (nome, preco_compra, preco_venda, quantidade, fornecedor, estoque_minimo, id_produto))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        self.carregar_produtos()



    def adicionar_produto(self):
        id_produto = self.entry_id.get()
        nome = self.entry_nome.get()
        
        # Verifica se os preços e quantidades são válidos
        try:
            preco_compra = float(self.entry_preco_compra.get())
            preco_venda = float(self.entry_preco_venda.get())
            quantidade = int(self.entry_quantidade.get())
            fornecedor = self.entry_fornecedor.get()  # Adicionado aqui
            estoque_minimo = int(self.entry_estoque_minimo.get())

            if preco_compra <= 0 or preco_venda <= 0 or quantidade <= 0 or estoque_minimo <= 0:
                raise ValueError("Os valores devem ser maiores que zero.")
        except ValueError as e:
            messagebox.showerror("Erro", f"Dados inválidos: {e}")
            return

        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute('''INSERT INTO produtos (id, nome, preco_compra, preco_venda, quantidade, fornecedor, estoque_minimo)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (id_produto, nome, preco_compra, preco_venda, quantidade, fornecedor, estoque_minimo))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        self.carregar_produtos()



    def excluir_produto(self):
        selecionado = self.listbox_produtos.curselection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um produto para excluir")
            return

        produto_info = self.listbox_produtos.get(selecionado[0])
        produto_id = produto_info.split(" - ")[0]

        confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este produto?")
        if confirm:
            conn = sqlite3.connect('estoque.db')
            c = conn.cursor()
            c.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            self.carregar_produtos()

    def adicionar_estoque(self):
        selecionado = self.listbox_produtos.curselection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um produto para adicionar estoque")
            return

        produto_info = self.listbox_produtos.get(selecionado[0])
        produto_id = produto_info.split(" - ")[0]

        # Solicita a quantidade a adicionar
        nova_quantidade = simpledialog.askinteger("Adicionar Estoque", "Quantidade a adicionar:", minvalue=1)
        if nova_quantidade is not None:
            conn = sqlite3.connect('estoque.db')
            c = conn.cursor()
            c.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (nova_quantidade, produto_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso!")
            self.carregar_produtos()


    def produtos_abaixo_estoque_minimo(self):
        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("SELECT id, nome FROM produtos WHERE quantidade < estoque_minimo")
        produtos = c.fetchall()
        conn.close()

        if not produtos:
            messagebox.showinfo("Informação", "Não há produtos abaixo do estoque mínimo.")
            return

        produtos_window = tk.Toplevel(self.root)
        produtos_window.title("Produtos Abaixo do Estoque Mínimo")
        produtos_window.geometry("400x300")

        listbox_produtos_minimo = tk.Listbox(produtos_window, width=60, height=20, border=1)
        listbox_produtos_minimo.pack(padx=10, pady=10)

        for produto in produtos:
            listbox_produtos_minimo.insert(tk.END, f"{produto[0]} - {produto[1]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()
