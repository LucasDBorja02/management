import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
import os
from tkinter.filedialog import asksaveasfilename
import subprocess
from database import create_db

class FinanceiroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análise Financeira")
        self.root.geometry("1400x700")
        
        # Adicionando Menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.file_menu)
        self.file_menu.add_command(label="Exportar para PDF", command=self.exportar_pdf)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Imprimir", command=self.imprimir_pdf)
        self.file_menu.add_command(label="Sair", command=self.root.quit)

        # Canvas e Scrollbar
        self.canvas = tk.Canvas(root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.frame_container = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_container, anchor='nw')

        # Frame para período e análise
        self.frame_periodo = tk.Frame(self.frame_container, padx=10, pady=10)
        self.frame_periodo.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.label_periodo = tk.Label(self.frame_periodo, text="Período", font=('Arial', 12))
        self.label_periodo.grid(row=0, column=0, sticky="e")

        self.periodo_var = tk.StringVar(value="Diário")
        self.option_periodo = tk.OptionMenu(self.frame_periodo, self.periodo_var, "Diário", "Semanal", "Mensal", "Anual")
        self.option_periodo.grid(row=0, column=1, padx=5, pady=5)

        self.button_analisar = tk.Button(self.frame_periodo, text="Analisar", command=self.analisar_financeiro)
        self.button_analisar.grid(row=0, column=2, padx=5, pady=5)

        # Frame para gráficos
        self.frame_grafico = tk.Frame(self.frame_container, padx=10, pady=10)
        self.frame_grafico.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.figure, (self.ax1, self.ax2) = plt.subplots(nrows=2, figsize=(9, 6))
        self.canvas_figura = FigureCanvasTkAgg(self.figure, master=self.frame_grafico)
        self.canvas_figura.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Frame para tabela de vendas
        self.frame_tabela = tk.Frame(self.frame_container, padx=10, pady=10)
        self.frame_tabela.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.label_tabela = tk.Label(self.frame_tabela, text="Detalhes das Vendas", font=('Arial', 12))
        self.label_tabela.pack(pady=5)

        self.tree = ttk.Treeview(self.frame_tabela, columns=("Produto", "Quantidade", "Total", "Forma de Pagamento"), show='headings')
        self.tree.heading("Produto", text="Produto")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Forma de Pagamento", text="Forma de Pagamento")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Frame para informações adicionais (lucro, caixa, ranking)
        self.frame_info = tk.Frame(self.frame_container, padx=10, pady=10)
        self.frame_info.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="ns")

        # Label para exibir o lucro total
        self.label_lucro = tk.Label(self.frame_info, text="Lucro Total: R$0,00", font=('Arial', 14))
        self.label_lucro.pack(pady=5)

        # Label para exibir o total de caixa
        self.label_valor_caixa = tk.Label(self.frame_info, text="Caixa Total: R$0,00", font=('Arial', 14))
        self.label_valor_caixa.pack(pady=5)

        # Label para exibir ranking dos produtos mais vendidos
        self.label_ranking = tk.Label(self.frame_info, text="Top 5 Produtos Mais Vendidos:", font=('Arial', 12))
        self.label_ranking.pack(pady=5)

        self.text_ranking = tk.Text(self.frame_info, height=15, width=40)
        self.text_ranking.pack(pady=5)

        # Frame para tabela de contas
        self.frame_contas = tk.Frame(self.frame_container, padx=10, pady=10)
        self.frame_contas.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.label_contas = tk.Label(self.frame_contas, text="Detalhes das Contas", font=('Arial', 12))
        self.label_contas.pack(pady=5)

        self.tree_contas = ttk.Treeview(self.frame_contas, columns=("Descrição", "Valor", "Data"), show='headings')
        self.tree_contas.heading("Descrição", text="Descrição")
        self.tree_contas.heading("Valor", text="Valor")
        self.tree_contas.heading("Data", text="Data")
        self.tree_contas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adiciona um scrollbar ao frame de contas
        self.scrollbar_contas = tk.Scrollbar(self.frame_contas, orient=tk.VERTICAL, command=self.tree_contas.yview)
        self.scrollbar_contas.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_contas.configure(yscrollcommand=self.scrollbar_contas.set)

        # Frame para botões de contas
        self.frame_botoes_contas = tk.Frame(self.frame_contas, padx=10, pady=10)
        self.frame_botoes_contas.pack(pady=10, anchor='w')

        # Botão para adicionar conta
        self.button_adicionar_conta = tk.Button(self.frame_botoes_contas, text="Adicionar Conta", command=self.adicionar_conta)
        self.button_adicionar_conta.pack(pady=5)

        # Botão para deletar conta
        self.button_deletar_conta = tk.Button(self.frame_botoes_contas, text="Deletar Conta", command=self.delete_conta)
        self.button_deletar_conta.pack(pady=5)

        # Adiciona um scrollbar ao frame de contas
        self.scrollbar_contas = tk.Scrollbar(self.frame_contas, orient=tk.VERTICAL, command=self.tree_contas.yview)
        self.scrollbar_contas.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_contas.configure(yscrollcommand=self.scrollbar_contas.set)

        # Frame para gráficos adicionais
        self.frame_graficos_adicionais = tk.Frame(self.frame_container, padx=10, pady=10)
        self.frame_graficos_adicionais.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.figure_adicionais, (self.ax3, self.ax4) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
        self.canvas_figura_adicionais = FigureCanvasTkAgg(self.figure_adicionais, master=self.frame_graficos_adicionais)
        self.canvas_figura_adicionais.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.conectar_db()
        self.update_caixa_total()
        self.update_lucro_total()
        self.update_ranking_produtos()
        self.update_tabela_contas()
        self.update_graficos()

    def exportar_pdf(self):
        # Função para salvar o relatório em PDF
        file_path = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        pdf = SimpleDocTemplate(file_path, pagesize=A4)

        elements = []

        # Tabela de vendas
        data_vendas = [("Produto", "Quantidade", "Total", "Forma de Pagamento")]
        for item in self.tree.get_children():
            data_vendas.append(self.tree.item(item, "values"))

        table_vendas = Table(data_vendas)
        table_vendas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_vendas)

        # Tabela de contas
        data_contas = [("Descrição", "Valor", "Data")]
        for item in self.tree_contas.get_children():
            data_contas.append(self.tree_contas.item(item, "values"))

        table_contas = Table(data_contas)
        table_contas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_contas)

        # Salvar o PDF
        pdf.build(elements)

        messagebox.showinfo("Exportar PDF", f"Relatório salvo em: {file_path}")

    def imprimir_pdf(self):
        # Função para imprimir o PDF
        file_path = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        self.exportar_pdf()

        if os.name == 'nt':  # Para Windows
            os.startfile(file_path, "print")
        else:
            subprocess.run(['lp', file_path])

    def conectar_db(self):
        self.conn = sqlite3.connect('estoque.db')
        self.cursor = self.conn.cursor()

    def update_caixa_total(self):
        self.cursor.execute("SELECT SUM(total) FROM vendas")
        total_vendas = self.cursor.fetchone()[0] or 0
        self.cursor.execute("SELECT SUM(valor) FROM contas")
        total_contas = self.cursor.fetchone()[0] or 0
        caixa_total = total_vendas - total_contas
        self.label_valor_caixa.config(text=f"Caixa Total: R${caixa_total:.2f}")

    def update_lucro_total(self):
        self.cursor.execute("SELECT SUM((vendas.total - produtos.preco_compra * vendas.quantidade)) FROM vendas JOIN produtos ON vendas.produto_id = produtos.id")
        lucro = self.cursor.fetchone()[0] or 0
        self.cursor.execute("SELECT SUM(valor) FROM contas")
        total_contas = self.cursor.fetchone()[0] or 0
        lucro_total = lucro - total_contas
        self.label_lucro.config(text=f"Lucro Total: R${lucro_total:.2f}")

    def update_ranking_produtos(self):
        self.cursor.execute("SELECT produtos.nome, SUM(vendas.quantidade) as total_vendido FROM vendas JOIN produtos ON vendas.produto_id = produtos.id GROUP BY produtos.nome ORDER BY total_vendido DESC LIMIT 5")
        ranking = self.cursor.fetchall()
        self.text_ranking.delete(1.0, tk.END)
        for produto, quantidade in ranking:
            self.text_ranking.insert(tk.END, f"{produto}: {quantidade}\n")

    def update_tabela_contas(self):
        for item in self.tree_contas.get_children():
            self.tree_contas.delete(item)
        self.cursor.execute("SELECT descricao, valor, data_conta FROM contas")
        contas = self.cursor.fetchall()
        for conta in contas:
            self.tree_contas.insert("", "end", values=conta)

    def adicionar_conta(self):
        popup = tk.Toplevel()
        popup.title("Adicionar Conta")
        popup.geometry("400x300")

        frame = tk.Frame(popup, padx=10, pady=10)
        frame.pack(expand=True, fill=tk.BOTH)

        label_descricao = tk.Label(frame, text="Descrição:")
        label_descricao.grid(row=0, column=0, padx=5, pady=5)

        entry_descricao = tk.Entry(frame)
        entry_descricao.grid(row=0, column=1, padx=5, pady=5)

        label_valor = tk.Label(frame, text="Valor:")
        label_valor.grid(row=1, column=0, padx=5, pady=5)

        entry_valor = tk.Entry(frame)
        entry_valor.grid(row=1, column=1, padx=5, pady=5)

        button_adicionar = tk.Button(frame, text="Adicionar", command=lambda: self.salvar_conta(entry_descricao.get(), entry_valor.get(), popup))
        button_adicionar.grid(row=2, column=0, columnspan=2, pady=10)

    def salvar_conta(self, descricao, valor, popup):
        try:
            valor = float(valor)
            if descricao and valor:
                self.cursor.execute("INSERT INTO contas (descricao, valor) VALUES (?, ?)", (descricao, valor))
                self.conn.commit()
                self.update_tabela_contas()
                self.update_caixa_total()
                self.update_lucro_total()
                popup.destroy()
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o campo de valor.")

    def update_graficos(self):
        self.update_grafico_contas()
        self.update_grafico_caixa_lucro()

    def update_grafico_contas(self):
        self.cursor.execute("SELECT descricao, valor FROM contas")
        contas = self.cursor.fetchall()

        if contas:
            descricoes, valores = zip(*contas)
        else:
            descricoes, valores = [], []

        self.ax3.clear()
        self.ax3.bar(descricoes, valores, color='red')
        self.ax3.set_title('Contas por Descrição')
        self.ax3.set_ylabel('Valor')
        self.ax3.set_xlabel('Descrição')
        
        # Defina os ticks e depois os rótulos para garantir que estejam sincronizados
        self.ax3.set_xticks(range(len(descricoes)))
        self.ax3.set_xticklabels(descricoes, rotation=45, ha='right')

        self.canvas_figura_adicionais.draw()


    def update_grafico_caixa_lucro(self):
        self.cursor.execute("SELECT SUM(total) FROM vendas")
        total_vendas = self.cursor.fetchone()[0] or 0

        self.cursor.execute("SELECT SUM((vendas.total - produtos.preco_compra * vendas.quantidade)) FROM vendas JOIN produtos ON vendas.produto_id = produtos.id")
        lucro = self.cursor.fetchone()[0] or 0

        self.cursor.execute("SELECT SUM(valor) FROM contas")
        total_contas = self.cursor.fetchone()[0] or 0

        caixa_total = total_vendas - total_contas

        labels = ['Caixa Total', 'Lucro Total', 'Contas']
        valores = [caixa_total, lucro, total_contas]

        self.ax4.clear()
        self.ax4.bar(labels, valores, color=['green', 'blue', 'red'])
        self.ax4.set_title('Comparativo Financeiro')
        self.ax4.set_ylabel('Valor')
        self.ax4.set_xlabel('Categorias')

        self.canvas_figura_adicionais.draw()


    def analisar_financeiro(self):
        periodo = self.periodo_var.get()
        hoje = datetime.today()

        if periodo == "Diário":
            data_inicio = hoje
        elif periodo == "Semanal":
            data_inicio = hoje - timedelta(days=7)
        elif periodo == "Mensal":
            data_inicio = hoje - timedelta(days=30)
        elif periodo == "Anual":
            data_inicio = hoje - timedelta(days=365)

        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("""
            SELECT produto_id, SUM(quantidade) AS total_vendido, SUM(total) AS total_recebido, forma_pagamento
            FROM vendas
            WHERE data_venda >= ?
            GROUP BY produto_id, forma_pagamento
            ORDER BY produto_id
        """, (data_inicio,))
        resultados = c.fetchall()

        produtos = []
        vendas = []
        lucros = []
        formas_pagamento = []
        formas_pagamento_set = set()

        produto_dict = {}
        total_caixa = 0
        total_lucro = 0

        for resultado in resultados:
            produto_id = resultado[0]
            total_vendido = resultado[1]
            total_recebido = resultado[2]
            forma_pagamento = resultado[3]
            c.execute("SELECT nome, preco_compra FROM produtos WHERE id = ?", (produto_id,))
            produto_data = c.fetchone()
            nome_produto = produto_data[0]
            preco_custo = produto_data[1]
            lucro = total_recebido - (preco_custo * total_vendido)

            if nome_produto not in produto_dict:
                produto_dict[nome_produto] = {'vendas': {}, 'lucro': 0, 'quantidade': 0}

            produto_dict[nome_produto]['vendas'][forma_pagamento] = total_vendido
            produto_dict[nome_produto]['lucro'] += lucro
            produto_dict[nome_produto]['quantidade'] += total_vendido
            formas_pagamento_set.add(forma_pagamento)

            total_caixa += total_recebido
            total_lucro += lucro

        # Despesas com contas
        c.execute("SELECT descricao, valor FROM contas WHERE data_conta >= ?", (data_inicio,))
        contas = c.fetchall()
        total_contas = sum([conta[1] for conta in contas])
        total_caixa -= total_contas
        total_lucro -= total_contas

        conn.close()

        produtos = list(produto_dict.keys())
        vendas = [sum(produto_dict[produto]['vendas'].values()) for produto in produtos]
        lucros = [produto_dict[produto]['lucro'] for produto in produtos]
        formas_pagamento = list(formas_pagamento_set)

        self.ax1.clear()
        self.ax1.bar(produtos, vendas, color='skyblue')
        self.ax1.set_title("Produtos Vendidos")
        self.ax1.set_ylabel("Quantidade Vendida")
        self.ax1.set_xlabel("Produtos")

        self.ax2.clear()
        self.ax2.plot(produtos, lucros, marker='o', linestyle='-', color='green')
        self.ax2.set_title("Lucro por Produto")
        self.ax2.set_ylabel("Lucro (R$)")
        self.ax2.set_xlabel("Produtos")

        self.canvas_figura.draw()

        self.tree.delete(*self.tree.get_children())
        for produto, quantidade in zip(produtos, vendas):
            total = next((item[2] for item in resultados if item[0] == produto), 0)
            self.tree.insert('', 'end', values=(produto, quantidade, total, formas_pagamento))

        self.label_lucro.config(text=f"Lucro Total: R${total_lucro:.2f}")
        self.label_valor_caixa.config(text=f"Caixa Total: R${total_caixa:.2f}")

        ranking_produtos = sorted(produto_dict.items(), key=lambda x: x[1]['quantidade'], reverse=True)
        self.text_ranking.delete('1.0', tk.END)
        for i, (produto, dados) in enumerate(ranking_produtos[:5]):
            self.text_ranking.insert(tk.END, f"{i+1}. {produto} - {dados['quantidade']} unidades vendidas\n")

    def analisar_diario(self):
        hoje = datetime.now().date()
        self.analisar_por_periodo(hoje, hoje)

    def analisar_semanal(self):
        hoje = datetime.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        self.analisar_por_periodo(inicio_semana, fim_semana)

    def analisar_mensal(self):
        hoje = datetime.now().date()
        inicio_mes = hoje.replace(day=1)
        proximo_mes = inicio_mes + timedelta(days=32)
        fim_mes = proximo_mes.replace(day=1) - timedelta(days=1)
        self.analisar_por_periodo(inicio_mes, fim_mes)

    def analisar_anual(self):
        hoje = datetime.now().date()
        inicio_ano = hoje.replace(month=1, day=1)
        fim_ano = hoje.replace(month=12, day=31)
        self.analisar_por_periodo(inicio_ano, fim_ano)

    def analisar_por_periodo(self, inicio, fim):
        self.cursor.execute(""" 
        SELECT produtos.nome, SUM(vendas.quantidade) as total_vendido, 
            SUM(vendas.total) as total_vendas, vendas.forma_pagamento 
        FROM vendas 
        JOIN produtos ON vendas.produto_id = produtos.id 
        WHERE data_venda BETWEEN ? AND ?
        GROUP BY produtos.nome, vendas.forma_pagamento
        ORDER BY total_vendido DESC
        """, (inicio, fim))
        vendas = self.cursor.fetchall()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for venda in vendas:
            # Certifique-se de que 'venda' contém a estrutura correta para o insert
            self.tree.insert("", "end", values=(venda[0], venda[1], venda[2], venda[3]))  # Certifique-se que isso corresponde à sua estrutura


        # Total de vendas no período
        self.cursor.execute("SELECT SUM(total) FROM vendas WHERE data_venda BETWEEN ? AND ?", (inicio, fim))
        total_vendas = self.cursor.fetchone()[0] or 0
        self.label_valor_caixa.config(text=f"Caixa Total: R${total_vendas:.2f}")

        # Lucro no período
        self.cursor.execute("""
        SELECT SUM((vendas.total - produtos.preco_compra * vendas.quantidade)) 
        FROM vendas 
        JOIN produtos ON vendas.produto_id = produtos.id 
        WHERE data_venda BETWEEN ? AND ?
        """, (inicio, fim))
        lucro = self.cursor.fetchone()[0] or 0
        self.label_lucro.config(text=f"Lucro Total: R${lucro:.2f}")

        # Obter dados de vendas por forma de pagamento
        self.cursor.execute("""
        SELECT forma_pagamento, SUM(total) 
        FROM vendas 
        WHERE data_venda BETWEEN ? AND ?
        GROUP BY forma_pagamento
        """, (inicio, fim))
        self.vendas_por_pagamento = self.cursor.fetchall()

        # Atualizar o gráfico de forma de pagamento
        self.update_grafico_pagamento()

        # Atualizar os outros gráficos e rankings
        self.update_ranking_produtos()
        self.update_graficos()

        self.update_grafico_entrada_total(inicio, fim)
        self.update_grafico_comparativo(inicio, fim)


    def update_grafico_pagamento(self, inicio, fim):
        # Obter dados das vendas por forma de pagamento com base no período
        self.cursor.execute(""" 
            SELECT forma_pagamento, SUM(total) 
            FROM vendas 
            WHERE data_venda BETWEEN ? AND ?
            GROUP BY forma_pagamento
        """, (inicio, fim))
        vendas_por_pagamento = self.cursor.fetchall()

        # Extrair dados de pagamentos para o gráfico
        formas_pagamento = [item[0] for item in vendas_por_pagamento]
        valores_pagamento = [item[1] for item in vendas_por_pagamento]

        # Gráfico de barras para valores
        self.ax_pagamento_barras.clear()
        self.ax_pagamento_barras.bar(formas_pagamento, valores_pagamento, color=['blue', 'green', 'red', 'purple'])
        self.ax_pagamento_barras.set_title('Valores das Vendas por Forma de Pagamento')
        self.ax_pagamento_barras.set_ylabel('Valor (R$)')
        self.ax_pagamento_barras.set_xlabel('Forma de Pagamento')

        # Gráfico de pizza para comparação
        self.ax_pagamento_pizza.clear()
        self.ax_pagamento_pizza.pie(valores_pagamento, labels=formas_pagamento, autopct='%1.1f%%', startangle=90)
        self.ax_pagamento_pizza.set_title('Comparativo de Vendas por Forma de Pagamento')

        # Atualizar os gráficos no canvas
        self.canvas_pagamento.draw()
        

    def update_grafico_entrada_total(self, inicio, fim):
    # Obter dados das entradas por forma de pagamento com base no período
        self.cursor.execute("""
            SELECT forma_pagamento, SUM(total) 
            FROM vendas 
            WHERE data_venda BETWEEN ? AND ?
            GROUP BY forma_pagamento
        """, (inicio, fim))
        entradas_por_pagamento = self.cursor.fetchall()

        # Extrair dados para o gráfico
        formas_pagamento = [item[0] for item in entradas_por_pagamento]
        valores_pagamento = [item[1] for item in entradas_por_pagamento]

        # Gráfico de barras para entradas totais
        self.ax_entrada_total.clear()
        self.ax_entrada_total.bar(formas_pagamento, valores_pagamento, color=['blue', 'green', 'red', 'purple'])
        self.ax_entrada_total.set_title('Entrada Total por Forma de Pagamento')
        self.ax_entrada_total.set_ylabel('Valor (R$)')
        self.ax_entrada_total.set_xlabel('Forma de Pagamento')

        # Atualizar o gráfico no canvas
        self.canvas_entrada_total.draw()


    def update_grafico_comparativo(self, inicio, fim):
        # Obter dados de entradas por forma de pagamento
        self.cursor.execute("""
            SELECT forma_pagamento, SUM(total) 
            FROM vendas 
            WHERE data_venda BETWEEN ? AND ?
            GROUP BY forma_pagamento
        """, (inicio, fim))
        entradas_por_pagamento = self.cursor.fetchall()

        # Extrair dados para o gráfico comparativo
        formas_pagamento = [item[0] for item in entradas_por_pagamento]
        valores_pagamento = [item[1] for item in entradas_por_pagamento]

        # Gráfico de pizza para comparação
        self.ax_comparativo.clear()
        self.ax_comparativo.pie(valores_pagamento, labels=formas_pagamento, autopct='%1.1f%%', startangle=90)
        self.ax_comparativo.set_title('Comparativo de Entradas por Forma de Pagamento')

        # Atualizar o gráfico no canvas
        self.canvas_comparativo.draw()
    


    def exibir_totais_pagamento(self):
        # Limpar exibições anteriores
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        # Exibir todos os totais de pagamento
        for item in self.vendas_por_pagamento:
            forma_pagamento, valor = item
            label_text = f"{forma_pagamento.capitalize()}: R${valor:.2f}"
            label = tk.Label(self.root, text=label_text, font=("Arial", 12))
            label.pack()

    def configurar_interface(self):
        # Criar a figura e os eixos para os gráficos de entrada
        fig_entrada, (self.ax_entrada_total, self.ax_comparativo) = plt.subplots(1, 2, figsize=(10, 5))
        fig_entrada.suptitle('Análise das Entradas por Forma de Pagamento')

        # Criar o canvas e adicionar a figura à interface
        self.canvas_entrada_total = FigureCanvasTkAgg(fig_entrada, master=self.root)
        self.canvas_entrada_total.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Chamar update_grafico_entrada_total() e update_grafico_comparativo() para exibir os gráficos com dados iniciais
        hoje = datetime.now().date()
        self.update_grafico_entrada_total(hoje, hoje)  # Gráfico de entrada total
        self.update_grafico_comparativo(hoje, hoje)    # Gráfico comparativo




    def delete_conta(self):
        selected_item = self.tree_contas.selection()
        if selected_item:
            item = self.tree_contas.item(selected_item)
            descricao = item["values"][0]
            valor_str = item["values"][1]

            try:
                # Convertendo o valor para float
                valor = float(valor_str)
            except ValueError:
                messagebox.showerror("Erro", "O valor da conta não é válido.")
                return

            # Confirmar exclusão
            confirm = messagebox.askyesno("Confirmação", f"Tem certeza de que deseja excluir a conta '{descricao}' de valor R${valor:.2f}?")
            if confirm:
                try:
                    # Remover a conta do banco de dados
                    self.cursor.execute("DELETE FROM contas WHERE descricao = ? AND valor = ?", (descricao, valor))
                    self.conn.commit()

                    # Atualizar valores de caixa e lucro
                    self.update_caixa_total()
                    self.update_lucro_total()

                    # Remover o item da árvore
                    self.tree_contas.delete(selected_item)
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao excluir a conta: {str(e)}")
        else:
            messagebox.showwarning("Atenção", "Por favor, selecione uma conta para excluir.")


    def carregar_vendas(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect('C:/path/to/vendas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT produto_id, quantidade, total, forma_pagamento, data_venda FROM vendas")
        vendas = cursor.fetchall()

        for venda in vendas:
            self.tree.insert('', 'end', values=venda)

    def close_connection(self):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    create_db()
    root = tk.Tk()
    app = FinanceiroApp(root)
    root.mainloop()
