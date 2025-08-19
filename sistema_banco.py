saldo = 2000
limite_saque = 500
saques_diarios = 3
saques_realizados = 0
extrato = []

while True:
    print("\n=== Sistema Bancário ===")
    print("1. Depositar")
    print("2. Sacar")
    print("3. Visualizar Extrato")
    print("4. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: R$ "))
        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: +R$ {valor:.2f}")
            print("Depósito realizado com sucesso!")
        else:
            print("Valor inválido para depósito.")

    elif opcao == "2":
        if saques_realizados >= saques_diarios:
            print("Limite diário de saques atingido.")
            continue
        valor = float(input("Informe o valor do saque: R$ "))
        if valor <= 0:
            print("Valor inválido para saque.")
        elif valor > limite_saque:
            print("Valor do saque excede o limite por operação.")
        elif valor > saldo:
            print("Você não possui saldo em conta.")
        else:
            saldo -= valor
            saques_realizados += 1
            extrato.append(f"Saque: -R$ {valor:.2f}")
            print("Saque realizado com sucesso!")

    elif opcao == "3":
        print("\n=== Extrato ===")
        if not extrato:
            print("Não foram realizadas movimentações.")
        else:
            for item in extrato:
                print(item)
        print(f"Saldo atual: R$ {saldo:.2f}")

    elif opcao == "4":
        print("Saindo do sistema. Até logo!")
        break

    else:
        print("Opção inválida. Tente novamente.")