clientes = [
    ("joao", "1234", "Nome do seu cachorro?", 1500.00),
    ("maria", "abcd", "Cidade onde nasceu?", 3200.50),
    ("carlos", "senha123", "Cor favorita?", 500.75),
    ("ana", "4321", "Nome da escola primária?", 10000.00)
]

# Cria ou sobrescreve o arquivo de usuários
with open("usuarios.txt", "w", encoding="utf-8") as f:
    for usuario, senha, pergunta, saldo in clientes:
        f.write(f"{usuario};{senha};{pergunta}\n")

# Cria os arquivos de saldo e extrato para cada cliente
for usuario, senha, pergunta, saldo in clientes:
    with open(f"dados_{usuario}.txt", "w", encoding="utf-8") as f:
        f.write(f"{saldo:.2f}\n")
    with open(f"extrato_{usuario}.txt", "w", encoding="utf-8") as f:
        pass  # extrato vazio
