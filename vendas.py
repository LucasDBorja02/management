import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VendasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciar Vendas")
        self.root.geometry("1400x700")
        self.root.configure(bg='#2c3e50')

        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12), padding=6)
        self.style.configure('TLabel', font=('Arial', 12), background='#2c3e50', foreground='#ecf0f1')
        self.style.configure('TCombobox', font=('Arial', 12))
        self.style.configure('Treeview', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.map('TButton', background=[('active', '#3498db')])

        # Frame para pesquisa de produtos
        self.frame_search = tk.Frame(root, padx=10, pady=10, bg='#34495e')
        self.frame_search.pack(side=tk.TOP, fill=tk.X)

        self.label_search_nome = tk.Label(self.frame_search, text="Buscar por Nome", bg='#34495e', fg='#ecf0f1')
        self.label_search_nome.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_search_nome = tk.Entry(self.frame_search, width=30, font=('Arial', 12), fg='#a0a0a0')
        self.entry_search_nome.grid(row=0, column=1, padx=5, pady=5)
        self.entry_search_nome.insert(0, "Digite o nome do produto")

        # Vincula os eventos FocusIn e FocusOut para o placeholder
        self.entry_search_nome.bind("<FocusIn>", self.limpar_placeholder)
        self.entry_search_nome.bind("<FocusOut>", self.adicionar_placeholder)

        self.button_search = ttk.Button(self.frame_search, text="Pesquisar", command=self.pesquisar_produtos)
        self.button_search.grid(row=0, column=2, padx=5, pady=5)

        # Frame para detalhes do produto
        self.frame_details = tk.Frame(root, padx=10, pady=10, bg='#34495e')
        self.frame_details.pack(side=tk.TOP, fill=tk.X)
        # Campo para valor entregue
        self.label_valor_entregue = tk.Label(self.frame_details, text="Valor Entregue (Dinheiro)", bg='#34495e', fg='#ecf0f1')
        self.label_valor_entregue.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_valor_entregue = tk.Entry(self.frame_details, width=20, font=('Arial', 12))
        self.entry_valor_entregue.grid(row=3, column=1, padx=5, pady=5)


        self.label_quantidade = tk.Label(self.frame_details, text="Quantidade", bg='#34495e', fg='#ecf0f1')
        self.label_quantidade.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_quantidade = tk.Entry(self.frame_details, width=20, font=('Arial', 12))
        self.entry_quantidade.grid(row=0, column=1, padx=5, pady=5)

        self.label_desconto = tk.Label(self.frame_details, text="Desconto (%)", bg='#34495e', fg='#ecf0f1')
        self.label_desconto.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_desconto = tk.Entry(self.frame_details, width=20, font=('Arial', 12))
        self.entry_desconto.grid(row=1, column=1, padx=5, pady=5)

        self.label_pagamento = tk.Label(self.frame_details, text="Forma de Pagamento", bg='#34495e', fg='#ecf0f1')
        self.label_pagamento.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.combo_pagamento = ttk.Combobox(self.frame_details, values=["Débito", "Crédito", "Pix", "Dinheiro"], width=17, font=('Arial', 12))
        self.combo_pagamento.grid(row=2, column=1, padx=5, pady=5)

        self.button_add_to_cart = ttk.Button(self.frame_details, text="Adicionar ao Carrinho", command=self.adicionar_carrinho)
        self.button_add_to_cart.grid(row=3, column=0, columnspan=2, pady=10)

        # Frame para exibição do carrinho
        self.frame_cart = tk.Frame(root, padx=10, pady=10, bg='#ecf0f1')
        self.frame_cart.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.label_cart = tk.Label(self.frame_cart, text="Carrinho", font=('Arial', 14, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        self.label_cart.pack(pady=5)

        self.tree_cart = ttk.Treeview(self.frame_cart, columns=("Produto", "Quantidade", "Preço", "Subtotal"), show='headings')
        self.tree_cart.heading("Produto", text="Produto")
        self.tree_cart.heading("Quantidade", text="Quantidade")
        self.tree_cart.heading("Preço", text="Preço")
        self.tree_cart.heading("Subtotal", text="Subtotal")
        self.tree_cart.pack(fill=tk.BOTH, expand=True)

        self.tree_cart.bind("<ButtonRelease-1>", self.selecionar_produto)

        self.button_finalize = ttk.Button(root, text="Finalizar Compra", command=self.finalizar_compra)
        self.button_finalize.pack(pady=10)

        # Frame para exibir vendas e gerenciar status
        self.frame_sales = tk.Frame(root, padx=10, pady=10, bg='#2c3e50')
        self.frame_sales.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.label_sales = tk.Label(self.frame_sales, text="Vendas Realizadas", font=('Arial', 14, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        self.label_sales.pack(pady=5)

        self.tree_sales = ttk.Treeview(self.frame_sales, columns=("ID Venda", "Produto", "Quantidade", "Total", "Pagamento", "Status"), show='headings')
        self.tree_sales.heading("ID Venda", text="ID Venda")
        self.tree_sales.heading("Produto", text="Produto")
        self.tree_sales.heading("Quantidade", text="Quantidade")
        self.tree_sales.heading("Total", text="Total")
        self.tree_sales.heading("Pagamento", text="Pagamento")
        self.tree_sales.heading("Status", text="Status")
        self.tree_sales.pack(fill=tk.BOTH, expand=True)

        # Botão para alterar status de venda
        self.button_update_status = ttk.Button(self.frame_sales, text="Alterar Status", command=self.alterar_status)
        self.button_update_status.pack(pady=10)

        self.carrinho = []

        # Carregar vendas
        self.carregar_vendas()

    
    def limpar_placeholder(self, event):
        if self.entry_search_nome.get() == "Digite o nome do produto":
            self.entry_search_nome.delete(0, tk.END)
            self.entry_search_nome.config(fg='#34495e')  # Define a cor padrão

    # Função para restaurar o placeholder
    def adicionar_placeholder(self, event):
        if not self.entry_search_nome.get():
            self.entry_search_nome.insert(0, "Digite o nome do produto")
            self.entry_search_nome.config(fg='#a0a0a0')  # Cor do placeholder

    def calcular_troco(self, total_compra):
        try:
            valor_entregue = float(self.entry_valor_entregue.get())
            if valor_entregue < total_compra:
                messagebox.showwarning("Valor Insuficiente", "O valor entregue é menor que o total da compra.")
                return False

            troco = valor_entregue - total_compra

            # Lista de valores de notas e moedas disponíveis em reais
            notas_moedas = [100, 50, 20, 10, 5, 2, 1, 0.50, 0.25, 0.10, 0.05, 0.01]
            distribuicao = {}

            # Cálculo da quantidade mínima de notas e moedas
            for valor in notas_moedas:
                quantidade, troco = divmod(troco, valor)
                if quantidade > 0:
                    distribuicao[valor] = int(quantidade)

            # Monta a mensagem com o valor do troco e a distribuição de notas e moedas
            mensagem_troco = f"O troco é R$ {valor_entregue - total_compra:.2f}\n\nDistribuição de notas e moedas:\n"
            for valor, quantidade in distribuicao.items():
                mensagem_troco += f"{quantidade} x R$ {valor:.2f}\n"

            # Exibe a mensagem final com o troco e a distribuição
            messagebox.showinfo("Troco", mensagem_troco)
            return True

        except ValueError:
            messagebox.showerror("Erro", "Insira um valor válido para o valor entregue.")
            return False



    def carregar_vendas(self):
        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("SELECT v.id, p.nome, v.quantidade, v.total, v.forma_pagamento, v.status FROM vendas v JOIN produtos p ON v.produto_id = p.id")
        vendas = c.fetchall()
        conn.close()

        # Preencher a treeview com as vendas
        for venda in vendas:
            self.tree_sales.insert("", tk.END, values=venda)

    def alterar_status(self):
        selected_item = self.tree_sales.selection()[0]
        venda_id = self.tree_sales.item(selected_item, 'values')[0]

        new_status = tk.simpledialog.askstring("Alterar Status", "Digite o novo status (Preparo, Entregando, Concluído):")
        if new_status not in ["Preparo", "Entregando", "Concluído"]:
            messagebox.showerror("Erro", "Status inválido. Use: Preparo, Entregando ou Concluído.")
            return

        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("UPDATE vendas SET status = ? WHERE id = ?", (new_status, venda_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Status atualizado com sucesso!")
        self.tree_sales.item(selected_item, values=(*self.tree_sales.item(selected_item, 'values')[:-1], new_status))

    def pesquisar_produtos(self):
        nome = self.entry_search_nome.get()
        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("SELECT id, nome, preco_venda FROM produtos WHERE nome LIKE ?", ('%' + nome + '%',))
        produtos = c.fetchall()
        conn.close()

        if produtos:
            self.tree_cart.delete(*self.tree_cart.get_children())
            for produto in produtos:
                self.tree_cart.insert("", tk.END, values=(produto[1], "", produto[2], ""))
        else:
            messagebox.showinfo("Nenhum produto encontrado", "Não foi encontrado nenhum produto com esse nome.")

    def selecionar_produto(self, event):
        selected_item = self.tree_cart.selection()[0]
        self.selected_product = self.tree_cart.item(selected_item, 'values')[0]

    def adicionar_carrinho(self):
        try:
            produto = self.selected_product
        except AttributeError:
            messagebox.showwarning("Nenhum Produto Selecionado", "Selecione um produto na lista de resultados antes de adicionar ao carrinho.")
            return

        try:
            quantidade = int(self.entry_quantidade.get())
            desconto = float(self.entry_desconto.get())
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira valores válidos para quantidade e desconto.")
            return

        forma_pagamento = self.combo_pagamento.get()

        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("SELECT id, preco_venda FROM produtos WHERE nome = ?", (produto,))
        produto_data = c.fetchone()
        conn.close()

        if not produto_data:
            messagebox.showwarning("Produto Não Encontrado", "Produto não encontrado no banco de dados.")
            return

        produto_id = produto_data[0]
        preco = produto_data[1]
        subtotal = preco * quantidade * (1 - desconto / 100)

        self.carrinho.append((produto, quantidade, preco, subtotal))

        self.tree_cart.delete(*self.tree_cart.get_children())

        for item in self.carrinho:
            self.tree_cart.insert("", tk.END, values=item)

        messagebox.showinfo("Produto Adicionado", f"{produto} foi adicionado ao carrinho com sucesso!")

    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showwarning("Carrinho Vazio", "O carrinho está vazio. Adicione produtos antes de finalizar a compra.")
            return

        forma_pagamento = self.combo_pagamento.get()
        total_compra = sum(item[3] for item in self.carrinho)  # Soma dos subtotais no carrinho

        # Se a forma de pagamento for dinheiro, solicitar o valor entregue e calcular o troco
        if forma_pagamento == "Dinheiro":
            valor_entregue = simpledialog.askfloat("Valor Entregue", "Digite o valor entregue pelo cliente:")
            if valor_entregue is None:
                return  # Cancela a operação se o usuário não inserir um valor
            if valor_entregue < total_compra:
                messagebox.showwarning("Valor Insuficiente", "O valor entregue é menor que o total da compra.")
                return
            # Calcular o troco e exibir as notas necessárias
            troco, notas_usadas = self.calcular_troco(valor_entregue - total_compra)
            messagebox.showinfo("Troco", f"O troco é R$ {troco:.2f}. \nDistribuição: {notas_usadas}")

        # Procedimento de finalização da compra
        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()

        for item in self.carrinho:
            produto, quantidade, preco, subtotal = item
            c.execute("SELECT id FROM produtos WHERE nome = ?", (produto,))
            produto_id = c.fetchone()[0]
            c.execute("INSERT INTO vendas (produto_id, quantidade, total, data_venda, forma_pagamento, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (produto_id, quantidade, subtotal, datetime.now(), forma_pagamento, "Preparo"))
            c.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))

        conn.commit()
        conn.close()

        self.carrinho.clear()
        self.tree_cart.delete(*self.tree_cart.get_children())
        messagebox.showinfo("Compra Finalizada", "Compra realizada com sucesso!")
        self.carregar_vendas()



if __name__ == "__main__":
    root = tk.Tk()
    app = VendasApp(root)
    root.mainloop()
