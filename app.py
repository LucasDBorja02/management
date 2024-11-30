import tkinter as tk
from tkinter import ttk
from tkinter import font
from estoque import EstoqueApp
from vendas import VendasApp
from controle import ControleVendasApp 
from financeiro import FinanceiroApp
from funcionarios import FuncionarioApp
from database import create_db

class MainApp:
    def __init__(self, root, user_role):
        self.root = root
        self.root.title("Sistema de Gestão de Comércio")
        self.root.geometry("550x500")
        self.root.resizable(False, False)
        self.user_role = user_role

        # Configuração do estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton',
                        padding=10,
                        relief='flat',
                        background='#2C3E50',
                        foreground='white',
                        font=('Helvetica', 12),
                        borderwidth=2)
        style.map('TButton',
                  background=[('active', '#1ABC9C')],
                  foreground=[('active', 'white')],
                  relief=[('pressed', 'sunken')],
                  bordercolor=[('active', '#16A085')])

        # Fonte do título
        title_font = font.Font(family='Helvetica', size=18, weight='bold')

        # Frame Principal
        self.frame_main = tk.Frame(root, padx=20, pady=20, bg='#ECF0F1')
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        # Título
        self.label_title = tk.Label(self.frame_main, text="Sistema de Gestão de Comércio", font=title_font, bg='#ECF0F1')
        self.label_title.pack(pady=20)

        # Adicionar Botões Baseados no Papel do Usuário
        self.create_buttons()

    def create_buttons(self):
        button_config = {
            'Admin': [('Gerenciar Estoque', '📦'), ('Gerenciar Vendas', '💵'), ('Vendas Online', '🛒'), ('Análise Financeira', '📊'), ('Gerenciar Funcionários', '👥')],
            'Estoque': [('Gerenciar Estoque', '📦')],
            'Caixa': [('Gerenciar Vendas', '💵')],
            'Financeiro': [('Análise Financeira', '📊'), ('Gerenciar Funcionários', '👥')]
        }

        for (text, icon) in button_config.get(self.user_role, []):
            button = ttk.Button(self.frame_main, text=f"{icon} {text}", command=lambda t=text: self.open_window(t))
            button.pack(pady=10, fill=tk.X)

    def open_window(self, title):
        top = tk.Toplevel(self.root)
        top.title(title)
        if title == 'Gerenciar Estoque':
            EstoqueApp(top)
        elif title == 'Gerenciar Vendas':
            VendasApp(top)
        elif title == 'Vendas Online':
            ControleVendasApp(top)  # Chamando a nova funcionalidade ControleApp
        elif title == 'Análise Financeira':
            FinanceiroApp(top)
        elif title == 'Gerenciar Funcionários':
            FuncionarioApp(top)

if __name__ == "__main__":
    create_db()
    from login import LoginApp  # Importar aqui para evitar importação circular
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()
