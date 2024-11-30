import tkinter as tk
from tkinter import ttk, messagebox
from database import register_employee, check_login
from app import MainApp

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("350x250")
        self.root.resizable(False, False)
        self.root.configure(bg='#2C3E50')

        # Frame Principal
        self.frame_login = tk.Frame(self.root, padx=20, pady=20, bg='#2C3E50')
        self.frame_login.pack(fill=tk.BOTH, expand=True)

        # Título
        self.label_title = tk.Label(self.frame_login, text="Bem-vindo", font=('Helvetica', 16, 'bold'), bg='#2C3E50', fg='white')
        self.label_title.pack(pady=(0, 20))

        # Nome de Usuário
        self.label_username = tk.Label(self.frame_login, text="Nome de Usuário:", bg='#2C3E50', fg='white')
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(self.frame_login, font=('Helvetica', 10), bg='#ECF0F1')
        self.entry_username.pack(pady=5)

        # Senha
        self.label_password = tk.Label(self.frame_login, text="Senha:", bg='#2C3E50', fg='white')
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(self.frame_login, show='*', font=('Helvetica', 10), bg='#ECF0F1')
        self.entry_password.pack(pady=5)

        # Botão de Login
        self.button_login = ttk.Button(self.frame_login, text="Login", command=self.login)
        self.button_login.pack(pady=(15, 5))
        self.root.bind('<Return>', lambda event: self.login())

        # Botão de Registrar
        self.button_register = ttk.Button(self.frame_login, text="Registrar", command=self.register)
        self.button_register.pack(pady=5)

    def login(self):
        nome = self.entry_username.get()
        senha = self.entry_password.get()
        result = check_login(nome, senha)
        if result:
            self.root.destroy()  # Fecha a janela de login
            main_app = tk.Tk()
            app = MainApp(main_app, user_role=result[7])  # Passa o nível do usuário
            main_app.mainloop()
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos.")
            self.clear_entries()

    def register(self):
        nome = self.entry_username.get()
        senha = self.entry_password.get()
        telefone = "123456789"
        endereco = "Endereço"
        cargo = "Cargo"
        salario = "Salário"
        nivel = "Nível"
        cpf = "CPF"

        register_employee(nome, telefone, endereco, cargo, salario, senha, nivel, cpf)
        messagebox.showinfo("Sucesso", "Registrado com sucesso!")
        self.clear_entries()

    def clear_entries(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
