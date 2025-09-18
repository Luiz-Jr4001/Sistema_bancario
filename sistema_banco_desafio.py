import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import os

# --- Classes para Cliente e Conta Bancária ---

class Cliente:
    def __init__(self, usuario, senha, pergunta):
        self.usuario = usuario
        self.senha = senha
        self.pergunta = pergunta

class ContaBancaria:
    def __init__(self, cliente, saldo=2000.0):
        self.cliente = cliente
        self.saldo = saldo
        self.extrato = []
        self.limite_saque = 500.0
        self.saques_diarios = 3
        self.saques_realizados = 0
        self.transacoes_diarias = 0
        self.limite_transacoes = 10

    def depositar(self, valor):
        if valor > 0 and self.transacoes_diarias < self.limite_transacoes:
            self.saldo += valor
            self.transacoes_diarias += 1
            self.extrato.append((horario_formatado(), "Depósito", f"+R$ {valor:.2f}"))
            return True
        return False

    def sacar(self, valor):
        if (valor > 0 and valor <= self.limite_saque and
            self.saques_realizados < self.saques_diarios and
            self.transacoes_diarias < self.limite_transacoes and
            valor <= self.saldo):
            self.saldo -= valor
            self.saques_realizados += 1
            self.transacoes_diarias += 1
            self.extrato.append((horario_formatado(), "Saque", f"-R$ {valor:.2f}"))
            return True
        return False

    def registrar_extrato(self, tipo, valor):
        self.extrato.append((horario_formatado(), tipo, valor))

# --- Funções de persistência usando objetos ---

def carregar_clientes():
    clientes = {}
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(";")
                if len(partes) == 3:
                    usuario, senha, pergunta = partes
                    clientes[usuario] = Cliente(usuario, senha, pergunta)
    return clientes

def carregar_conta(cliente):
    saldo = 2000.0
    extrato = []
    if os.path.exists(f"dados_{cliente.usuario}.txt"):
        with open(f"dados_{cliente.usuario}.txt", "r", encoding="utf-8") as f:
            saldo = float(f.readline().strip())
    conta = ContaBancaria(cliente, saldo)
    if os.path.exists(f"extrato_{cliente.usuario}.txt"):
        with open(f"extrato_{cliente.usuario}.txt", "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(";")
                if len(partes) == 3:
                    conta.extrato.append(tuple(partes))
    return conta

def salvar_conta(conta):
    with open(f"dados_{conta.cliente.usuario}.txt", "w", encoding="utf-8") as f:
        f.write(f"{conta.saldo:.2f}\n")
    with open(f"extrato_{conta.cliente.usuario}.txt", "w", encoding="utf-8") as f:
        for data, tipo, valor in conta.extrato:
            f.write(f"{data};{tipo};{valor}\n")

def adicionar_cliente(usuario, senha, pergunta):
    with open("usuarios.txt", "a", encoding="utf-8") as f:
        f.write(f"{usuario};{senha};{pergunta}\n")
    with open(f"dados_{usuario}.txt", "w", encoding="utf-8") as f:
        f.write("2000.00\n")
    with open(f"extrato_{usuario}.txt", "w", encoding="utf-8") as f:
        pass

def remover_cliente(usuario):
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
        with open("usuarios.txt", "w", encoding="utf-8") as f:
            for linha in linhas:
                if not linha.startswith(usuario + ";"):
                    f.write(linha)
    if os.path.exists(f"dados_{usuario}.txt"):
        os.remove(f"dados_{usuario}.txt")
    if os.path.exists(f"extrato_{usuario}.txt"):
        os.remove(f"extrato_{usuario}.txt")

# --- Função para formatar data/hora ---
def horario_formatado():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

# --- Função para cadastrar novos usuários ---
def cadastrar_usuario():
    def salvar_usuario():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        pergunta = entry_pergunta.get().strip()
        clientes = carregar_clientes()
        if not usuario or not senha or not pergunta:
            messagebox.showerror("Erro", "Preencha todos os campos.")
        elif usuario in clientes:
            messagebox.showerror("Erro", "Usuário já existe.")
        else:
            adicionar_cliente(usuario, senha, pergunta)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            cadastro_window.destroy()

    cadastro_window = tk.Toplevel()
    cadastro_window.title("Cadastro de Usuário")
    cadastro_window.geometry("320x250")

    tk.Label(cadastro_window, text="Usuário:").pack(pady=5)
    entry_usuario = tk.Entry(cadastro_window)
    entry_usuario.pack(pady=5)

    tk.Label(cadastro_window, text="Senha:").pack(pady=5)
    entry_senha = tk.Entry(cadastro_window, show="*")
    entry_senha.pack(pady=5)

    tk.Label(cadastro_window, text="Pergunta secreta (ex: Nome da mãe):").pack(pady=5)
    entry_pergunta = tk.Entry(cadastro_window)
    entry_pergunta.pack(pady=5)

    tk.Button(cadastro_window, text="Salvar", command=salvar_usuario, bg="#4CAF50", fg="white", font=("Arial", 11)).pack(pady=10)

# --- Função para recuperação de senha ---
def recuperar_senha():
    usuario = simpledialog.askstring("Recuperar Senha", "Digite seu usuário:")
    clientes = carregar_clientes()
    if not usuario or usuario not in clientes:
        messagebox.showerror("Erro", "Usuário não encontrado.")
        return
    resposta = simpledialog.askstring("Pergunta Secreta", f"Responda: {clientes[usuario].pergunta}")
    if resposta and resposta.strip().lower() == clientes[usuario].pergunta.strip().lower():
        messagebox.showinfo("Senha", f"Sua senha é: {clientes[usuario].senha}")
    else:
        messagebox.showerror("Erro", "Resposta incorreta.")

def verificar_login():
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()
    clientes = carregar_clientes()
    if usuario in clientes and clientes[usuario].senha == senha:
        abrir_sistema(clientes[usuario])
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def tela_login():
    global entry_usuario, entry_senha, login_window

    login_window = tk.Tk()
    login_window.title("LJ BANK - Login")
    login_window.geometry("420x340")
    login_window.configure(bg="#FF6600")  # Laranja Itaú

    # Topo azul escuro
    tk.Label(login_window, text="LJ BANK", bg="#003366", fg="#FF6600", font=("Segoe UI", 22, "bold"), width=30, pady=10).pack(pady=(0, 10))

    frame = tk.Frame(login_window, bg="#ffffff", bd=0, relief="flat")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=230)

    tk.Label(frame, text="Acesso ao Internet Banking", bg="#ffffff", fg="#003366", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 15))

    tk.Label(frame, text="Usuário:", bg="#ffffff", fg="#003366", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entry_usuario = tk.Entry(frame, font=("Segoe UI", 11), bg="#f5f5f5", relief="flat")
    entry_usuario.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Senha:", bg="#ffffff", fg="#003366", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entry_senha = tk.Entry(frame, show="*", font=("Segoe UI", 11), bg="#f5f5f5", relief="flat")
    entry_senha.grid(row=2, column=1, padx=10, pady=5)

    frame_botoes = tk.Frame(frame, bg="#ffffff")
    frame_botoes.grid(row=3, column=0, columnspan=2, pady=15)

    tk.Button(frame_botoes, text="Entrar", command=verificar_login, bg="#003366", fg="white", font=("Segoe UI", 11, "bold"), width=10, relief="flat", activebackground="#002244").grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Cadastrar", command=cadastrar_usuario, bg="#FF6600", fg="white", font=("Segoe UI", 11, "bold"), width=10, relief="flat", activebackground="#FF8500").grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Recuperar Senha", command=recuperar_senha, bg="#003366", fg="white", font=("Segoe UI", 11, "bold"), width=22, relief="flat", activebackground="#002244").grid(row=1, column=0, columnspan=2, pady=5)

    login_window.mainloop()

def abrir_sistema(cliente):
    login_window.destroy()

    conta = carregar_conta(cliente)

    def depositar():
        try:
            valor = float(entry_valor.get())
            if conta.depositar(valor):
                salvar_conta(conta)
                atualizar_tabela()
                atualizar_status()
                messagebox.showinfo("Sucesso", f"Depósito de R$ {valor:.2f} realizado.")
            else:
                messagebox.showerror("Erro", "Não foi possível depositar. Verifique limites e valor.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico.")

    def sacar():
        try:
            valor = float(entry_valor.get())
            if conta.sacar(valor):
                salvar_conta(conta)
                atualizar_tabela()
                atualizar_status()
                messagebox.showinfo("Sucesso", f"Saque de R$ {valor:.2f} realizado.")
            else:
                messagebox.showerror("Erro", "Não foi possível sacar. Verifique limites, saldo e valor.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico.")

    def transferir():
        destino_usuario = simpledialog.askstring("Transferência", "Usuário de destino:")
        valor_str = simpledialog.askstring("Transferência", "Valor a transferir:")
        clientes = carregar_clientes()
        if not destino_usuario or destino_usuario == cliente.usuario:
            messagebox.showerror("Erro", "Usuário de destino inválido.")
            return
        if destino_usuario not in clientes:
            messagebox.showerror("Erro", "Usuário de destino não existe.")
            return
        try:
            valor = float(valor_str)
            if valor <= 0:
                messagebox.showerror("Erro", "Valor inválido.")
                return
            if conta.transacoes_diarias >= conta.limite_transacoes:
                messagebox.showwarning("Limite", "Limite diário de transações atingido.")
                return
            if valor > conta.saldo:
                messagebox.showwarning("Saldo", "Saldo insuficiente.")
                return
            conta.saldo -= valor
            conta.transacoes_diarias += 1
            conta.registrar_extrato("Transferência Enviada", f"-R$ {valor:.2f} para {destino_usuario}")
            salvar_conta(conta)
            # Credita no destinatário
            destino_cliente = clientes[destino_usuario]
            destino_conta = carregar_conta(destino_cliente)
            destino_conta.saldo += valor
            destino_conta.registrar_extrato("Transferência Recebida", f"+R$ {valor:.2f} de {cliente.usuario}")
            salvar_conta(destino_conta)
            atualizar_tabela()
            atualizar_status()
            messagebox.showinfo("Sucesso", f"Transferência de R$ {valor:.2f} para {destino_usuario} realizada.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico.")

    def excluir_conta():
        if messagebox.askyesno("Excluir Conta", "Tem certeza que deseja excluir sua conta? Esta ação é irreversível."):
            remover_cliente(cliente.usuario)
            messagebox.showinfo("Conta Excluída", "Sua conta foi excluída.")
            janela.destroy()

    def atualizar_tabela():
        for item in tabela.get_children():
            tabela.delete(item)
        for data, tipo, valor in conta.extrato:
            tabela.insert("", "end", values=(data, tipo, valor))

    def atualizar_status():
        label_status.config(text=f"Usuário: {cliente.usuario} | Saldo: R$ {conta.saldo:.2f} | Transações: {conta.transacoes_diarias}/{conta.limite_transacoes} | Saques: {conta.saques_realizados}/{conta.saques_diarios}")

    def sair():
        janela.destroy()

    janela = tk.Tk()
    janela.title("LJ BANK - Sistema Bancário")
    janela.geometry("900x540")
    janela.configure(bg="#FF6600")  # Laranja Itaú

    # Topo azul escuro
    tk.Label(janela, text="LJ BANK", bg="#003366", fg="#FF6600", font=("Segoe UI", 28, "bold"), width=60, pady=10).pack(pady=(0, 5))

    frame_top = tk.Frame(janela, bg="#003366")
    frame_top.pack(fill="x")
    tk.Label(frame_top, text=f"Bem-vindo, {cliente.usuario}!", bg="#003366", fg="white", font=("Segoe UI", 16, "bold")).pack(pady=10)

    frame_main = tk.Frame(janela, bg="#ffffff", bd=0, relief="flat")
    frame_main.place(relx=0.5, rely=0.53, anchor="center", width=800, height=400)

    frame_entrada = tk.Frame(frame_main, bg="#ffffff")
    frame_entrada.grid(row=0, column=0, columnspan=5, pady=10, padx=10, sticky="w")
    tk.Label(frame_entrada, text="Valor (R$):", bg="#ffffff", fg="#003366", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, padx=5)
    entry_valor = tk.Entry(frame_entrada, font=("Segoe UI", 12), width=15, bg="#f5f5f5", relief="flat")
    entry_valor.grid(row=0, column=1, padx=5)

    frame_botoes = tk.Frame(frame_main, bg="#ffffff")
    frame_botoes.grid(row=1, column=0, columnspan=5, pady=10)
    tk.Button(frame_botoes, text="Depositar", command=depositar, bg="#003366", fg="white", width=15, font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#002244").grid(row=0, column=0, padx=7)
    tk.Button(frame_botoes, text="Sacar", command=sacar, bg="#FF6600", fg="white", width=15, font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#FF8500").grid(row=0, column=1, padx=7)
    tk.Button(frame_botoes, text="Transferir", command=transferir, bg="#003366", fg="white", width=15, font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#002244").grid(row=0, column=2, padx=7)
    tk.Button(frame_botoes, text="Excluir Conta", command=excluir_conta, bg="#FF6600", fg="white", width=15, font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#FF8500").grid(row=0, column=3, padx=7)
    tk.Button(frame_botoes, text="Sair", command=sair, bg="#003366", fg="white", width=15, font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#002244").grid(row=0, column=4, padx=7)

    label_status = tk.Label(frame_main, text="", bg="#ffffff", fg="#003366", font=("Segoe UI", 12, "bold"))
    label_status.grid(row=2, column=0, columnspan=5, pady=10)
    atualizar_status()

    tabela = ttk.Treeview(frame_main, columns=("Data", "Tipo", "Valor"), show="headings", height=10)
    tabela.heading("Data", text="Data")
    tabela.heading("Tipo", text="Tipo")
    tabela.heading("Valor", text="Valor")
    tabela.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
    frame_main.grid_rowconfigure(3, weight=1)
    frame_main.grid_columnconfigure(0, weight=1)
    atualizar_tabela()

    janela.mainloop()

tela_login()
