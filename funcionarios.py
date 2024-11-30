import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib

class FuncionarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Funcionários")
        self.root.geometry("1400x700")

        # Frame para lista de funcionários
        self.frame_list = tk.Frame(root, padx=10, pady=10)
        self.frame_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.label_list = tk.Label(self.frame_list, text="Lista de Funcionários", font=('Arial', 14))
        self.label_list.pack(pady=5)

        self.listbox_funcionarios = tk.Listbox(self.frame_list, width=60, height=20, border=1, selectmode=tk.SINGLE)
        self.listbox_funcionarios.pack(padx=5, pady=5)

        self.scrollbar = tk.Scrollbar(self.frame_list, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_funcionarios.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox_funcionarios.yview)

        self.button_view = tk.Button(self.frame_list, text="Visualizar Detalhes", command=self.visualizar_detalhes)
        self.button_view.pack(pady=10)

        self.button_delete = tk.Button(self.frame_list, text="Excluir Funcionário", command=self.excluir_funcionario)
        self.button_delete.pack(pady=10)

        # Frame para adicionar e editar funcionários
        self.frame_edit = tk.Frame(root, padx=10, pady=10)
        self.frame_edit.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Labels e Entrys
        self.label_nome = tk.Label(self.frame_edit, text="Nome")
        self.label_nome.grid(row=0, column=0, sticky="e")
        self.entry_nome = tk.Entry(self.frame_edit, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        self.label_telefone = tk.Label(self.frame_edit, text="Telefone")
        self.label_telefone.grid(row=1, column=0, sticky="e")
        self.entry_telefone = tk.Entry(self.frame_edit, width=30)
        self.entry_telefone.grid(row=1, column=1, padx=5, pady=5)

        self.label_endereco = tk.Label(self.frame_edit, text="Endereço")
        self.label_endereco.grid(row=2, column=0, sticky="e")
        self.entry_endereco = tk.Entry(self.frame_edit, width=30)
        self.entry_endereco.grid(row=2, column=1, padx=5, pady=5)

        self.label_cargo = tk.Label(self.frame_edit, text="Cargo")
        self.label_cargo.grid(row=3, column=0, sticky="e")
        self.entry_cargo = tk.Entry(self.frame_edit, width=30)
        self.entry_cargo.grid(row=3, column=1, padx=5, pady=5)

        self.label_salario = tk.Label(self.frame_edit, text="Salário")
        self.label_salario.grid(row=4, column=0, sticky="e")
        self.entry_salario = tk.Entry(self.frame_edit, width=30)
        self.entry_salario.grid(row=4, column=1, padx=5, pady=5)

        self.label_nivel = tk.Label(self.frame_edit, text="Nível")
        self.label_nivel.grid(row=5, column=0, sticky="e")
        self.combo_nivel = ttk.Combobox(self.frame_edit, values=["Admin", "Financeiro", "Caixa", "Estoque"], width=28)
        self.combo_nivel.grid(row=5, column=1, padx=5, pady=5)

        self.label_cpf = tk.Label(self.frame_edit, text="CPF")
        self.label_cpf.grid(row=6, column=0, sticky="e")
        self.entry_cpf = tk.Entry(self.frame_edit, width=30)
        self.entry_cpf.grid(row=6, column=1, padx=5, pady=5)

        self.label_senha = tk.Label(self.frame_edit, text="Senha")
        self.label_senha.grid(row=7, column=0, sticky="e")
        self.entry_senha = tk.Entry(self.frame_edit, width=30, show="*")
        self.entry_senha.grid(row=7, column=1, padx=5, pady=5)

        self.button_save = tk.Button(self.frame_edit, text="Salvar", command=self.salvar_funcionario)
        self.button_save.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

        self.button_add = tk.Button(self.frame_edit, text="Adicionar Novo", command=self.adicionar_funcionario)
        self.button_add.grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")

        # Carregar funcionários na lista
        self.carregar_funcionarios()

    def carregar_funcionarios(self):
        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("SELECT id, nome, cargo FROM funcionarios")
        funcionarios = c.fetchall()
        conn.close()

        self.listbox_funcionarios.delete(0, tk.END)
        for func in funcionarios:
            self.listbox_funcionarios.insert(tk.END, f"{func[1]} - {func[2]}")

    def visualizar_detalhes(self):
        selected = self.listbox_funcionarios.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um funcionário para visualizar os detalhes.")
            return
        func_index = selected[0]
        func_nome = self.listbox_funcionarios.get(func_index).split(" - ")[0]

        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("SELECT * FROM funcionarios WHERE nome = ?", (func_nome,))
        func = c.fetchone()
        conn.close()

        if func:
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, func[1])

            self.entry_telefone.delete(0, tk.END)
            self.entry_telefone.insert(0, func[2])

            self.entry_endereco.delete(0, tk.END)
            self.entry_endereco.insert(0, func[3])

            self.entry_cargo.delete(0, tk.END)
            self.entry_cargo.insert(0, func[4])

            self.entry_salario.delete(0, tk.END)
            self.entry_salario.insert(0, func[5])

            self.combo_nivel.set(func[7])

            self.entry_cpf.delete(0, tk.END)
            self.entry_cpf.insert(0, func[8])

    def excluir_funcionario(self):
        selected = self.listbox_funcionarios.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir.")
            return
        func_index = selected[0]
        func_nome = self.listbox_funcionarios.get(func_index).split(" - ")[0]

        if messagebox.askyesno("Confirmação", f"Tem certeza de que deseja excluir o funcionário '{func_nome}'?"):
            conn = sqlite3.connect('estoque.db')
            c = conn.cursor()
            c.execute("DELETE FROM funcionarios WHERE nome = ?", (func_nome,))
            conn.commit()
            conn.close()

            self.carregar_funcionarios()
            messagebox.showinfo("Sucesso", f"Funcionário '{func_nome}' excluído com sucesso.")

    def salvar_funcionario(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        endereco = self.entry_endereco.get()
        cargo = self.entry_cargo.get()
        salario = self.entry_salario.get()
        senha = self.entry_senha.get()
        nivel = self.combo_nivel.get()
        cpf = self.entry_cpf.get()

        if not nome or not telefone or not endereco or not cargo or not salario or not senha or not nivel:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        c.execute('''
        INSERT INTO funcionarios (nome, telefone, endereco, cargo, salario, senha, nivel, cpf)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, telefone, endereco, cargo, salario, senha_hash, nivel, cpf))
        conn.commit()
        conn.close()

        self.carregar_funcionarios()
        messagebox.showinfo("Sucesso", f"Funcionário '{nome}' salvo com sucesso.")

    def adicionar_funcionario(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_endereco.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)
        self.entry_salario.delete(0, tk.END)
        self.combo_nivel.set('')
        self.entry_cpf.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_nome.focus_set()
