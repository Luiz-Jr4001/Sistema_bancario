import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

# Função para carregar usuários do arquivo
def carregar_usuarios():
    usuarios = {}
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r", encoding="utf-8") as f:
            for linha in f:
                usuario, senha = linha.strip().split(";")
                usuarios[usuario] = senha
    return usuarios

# Função para adicionar novo usuário ao arquivo
def adicionar_usuario(usuario, senha):
    with open("usuarios.txt", "a", encoding="utf-8") as f:
        f.write(f"{usuario};{senha}\n")

# Dados da conta
saldo = 2000.00
limite_saque = 500.00
saques_diarios = 3
saques_realizados = 0
transacoes_diarias = 0
limite_transacoes = 10
extrato = []

# Função para formatar data/hora
def horario_formatado():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

# Função para cadastrar novos usuários
def cadastrar_usuario():
    def salvar_usuario():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        usuarios = carregar_usuarios()
        if not usuario or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        elif usuario in usuarios:
            messagebox.showerror("Erro", "Usuário já existe.")
        else:
            adicionar_usuario(usuario, senha)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            cadastro_window.destroy()

    cadastro_window = tk.Toplevel()
    cadastro_window.title("Cadastro de Usuário")
    cadastro_window.geometry("300x200")

    tk.Label(cadastro_window, text="Usuário:").pack(pady=5)
    entry_usuario = tk.Entry(cadastro_window)
    entry_usuario.pack(pady=5)

    tk.Label(cadastro_window, text="Senha:").pack(pady=5)
    entry_senha = tk.Entry(cadastro_window, show="*")
    entry_senha.pack(pady=5)

    tk.Button(cadastro_window, text="Salvar", command=salvar_usuario, bg="#4CAF50", fg="white", font=("Arial", 11)).pack(pady=10)

# Tela principal do sistema bancário
def abrir_sistema():
    login_window.destroy()

    def depositar():
        global saldo, transacoes_diarias
        try:
            valor = float(entry_valor.get())
            if valor > 0:
                if transacoes_diarias >= limite_transacoes:
                    messagebox.showwarning("Limite", "Limite diário de transações atingido.")
                    return
                saldo += valor
                transacoes_diarias += 1
                extrato.append((horario_formatado(), "Depósito", f"+R$ {valor:.2f}"))
                atualizar_tabela()
                atualizar_status()
                messagebox.showinfo("Sucesso", f"Depósito de R$ {valor:.2f} realizado.")
            else:
                messagebox.showerror("Erro", "Valor inválido.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico.")

    def sacar():
        global saldo, saques_realizados, transacoes_diarias
        try:
            valor = float(entry_valor.get())
            if transacoes_diarias >= limite_transacoes:
                messagebox.showwarning("Limite", "Limite diário de transações atingido.")
                return
            if saques_realizados >= saques_diarios:
                messagebox.showwarning("Limite", "Limite diário de saques atingido.")
            elif valor <= 0:
                messagebox.showerror("Erro", "Valor inválido.")
            elif valor > limite_saque:
                messagebox.showwarning("Limite", "Valor excede o limite por operação.")
            elif valor > saldo:
                messagebox.showwarning("Saldo", "Saldo insuficiente.")
            else:
                saldo -= valor
                saques_realizados += 1
                transacoes_diarias += 1
                extrato.append((horario_formatado(), "Saque", f"-R$ {valor:.2f}"))
                atualizar_tabela()
                atualizar_status()
                messagebox.showinfo("Sucesso", f"Saque de R$ {valor:.2f} realizado.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico.")

    def atualizar_tabela():
        for item in tabela.get_children():
            tabela.delete(item)
        for data, tipo, valor in extrato:
            tabela.insert("", "end", values=(data, tipo, valor))

    def atualizar_status():
        label_status.config(text=f"💰 Saldo: R$ {saldo:.2f} | 📌 Transações: {transacoes_diarias}/{limite_transacoes} | 🏧 Saques: {saques_realizados}/{saques_diarios}")

    def sair():
        janela.destroy()

    janela = tk.Tk()
    janela.title("💳 Sistema Bancário")
    janela.geometry("600x400")
    janela.configure(bg="#f0f4f7")

    tk.Label(janela, text="Valor (R$):", bg="#f0f4f7", font=("Arial", 12)).pack(pady=5)
    entry_valor = tk.Entry(janela, font=("Arial", 12))
    entry_valor.pack(pady=5)

    frame_botoes = tk.Frame(janela, bg="#f0f4f7")
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="💰 Depositar", command=depositar, bg="#4CAF50", fg="white", width=15, font=("Arial", 11)).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="🏧 Sacar", command=sacar, bg="#f44336", fg="white", width=15, font=("Arial", 11)).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="📄 Sair", command=sair, bg="#607D8B", fg="white", width=15, font=("Arial", 11)).grid(row=0, column=2, padx=5)

    label_status = tk.Label(janela, text="", bg="#f0f4f7", font=("Arial", 11), fg="blue")
    label_status.pack(pady=10)
    atualizar_status()

    tabela = ttk.Treeview(janela, columns=("Data", "Tipo", "Valor"), show="headings")
    tabela.heading("Data", text="Data")
    tabela.heading("Tipo", text="Tipo")
    tabela.heading("Valor", text="Valor")
    tabela.pack(pady=10, fill="x")

    janela.mainloop()

# Tela de login
login_window = tk.Tk()
login_window.title("🔐 Login Bancário")
login_window.geometry("300x200")
login_window.configure(bg="#e8f0fe")

tk.Label(login_window, text="Usuário:", bg="#e8f0fe", font=("Arial", 11)).pack(pady=5)
entry_usuario = tk.Entry(login_window)
entry_usuario.pack()

tk.Label(login_window, text="Senha:", bg="#e8f0fe", font=("Arial", 11)).pack(pady=5)
entry_senha = tk.Entry(login_window, show="*")
entry_senha.pack()

def verificar_login():
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()
    usuarios = carregar_usuarios()
    if usuario in usuarios and usuarios[usuario] == senha:
        abrir_sistema()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

tk.Button(login_window, text="Entrar", command=verificar_login, bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=10)

# Botão de cadastro de usuário
tk.Button(login_window, text="Cadastrar", command=cadastrar_usuario, bg="#4CAF50", fg="white", font=("Arial", 11)).pack(pady=5)

login_window.mainloop()