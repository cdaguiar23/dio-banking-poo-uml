from abc import ABC, abstractmethod

# -----------------------------
# Classes de Transações e Histórico
# -----------------------------
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        saldo_disponivel = conta.saldo
        if hasattr(conta, "limite"):
            saldo_disponivel += conta.limite

        if saldo_disponivel >= self.valor:
            conta.saldo -= self.valor
            # A lógica de contagem de saques foi movida para ContaCorrente.realizar_transacao
            conta.historico.adicionar_transacao(self)
            return True
        return False


class Transferencia(Transacao):
    def __init__(self, valor, destino):
        self.valor = valor
        self.destino = destino

    def registrar(self, origem):
        saldo_disponivel_origem = origem.saldo
        if hasattr(origem, "limite"):
            saldo_disponivel_origem += origem.limite

        if saldo_disponivel_origem >= self.valor:
            origem.saldo -= self.valor
            self.destino.saldo += self.valor
            origem.historico.adicionar_transacao(self)
            self.destino.historico.adicionar_transacao(
                Deposito(self.valor)  # registra como depósito na conta destino
            )
            return True
        return False


# -----------------------------
# Classes de Conta
# -----------------------------
class Conta:
    contas = []

    def __init__(self, cliente, numero):
        self.cliente = cliente
        self.numero = numero
        self.saldo = 0.0
        self.historico = Historico()
        Conta.contas.append(self)

    def realizar_transacao(self, transacao):
        resultado = transacao.registrar(self)
        return resultado if isinstance(resultado, bool) else True

    def registrar_transacao(self, transacao):
        self.historico.adicionar_transacao(transacao)

    def resumo(self):
        resumo_str = f"Conta {self.numero} - Saldo: R${self.saldo:.2f}"
        if hasattr(self, "limite"):
            resumo_str += f" (Limite: R${self.limite:.2f})"
        return resumo_str

    def extrato(self):
        print(f"\nExtrato da Conta {self.numero}")
        if not self.historico.transacoes:
            print("Nenhuma transação registrada.")
        else:
            for t in self.historico.transacoes:
                tipo = t.__class__.__name__
                valor = t.valor
                print(f"{tipo}: R${valor:.2f}")
        print(f"Saldo atual: R${self.saldo:.2f}")

    @classmethod
    def buscar_conta(cls, numero):
        """Busca uma conta pelo número na lista de contas da classe."""
        return next((c for c in cls.contas if c.numero == numero), None)


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def realizar_transacao(self, transacao):
        if isinstance(transacao, Saque):
            if self.saques_realizados >= self.limite_saques:
                print("Limite de saques atingido.")
                return False
            if super().realizar_transacao(transacao):
                self.saques_realizados += 1
                return True
            return False
        return super().realizar_transacao(transacao)

    def resumo(self):
        resumo_base = super().resumo()
        resumo_base += f" | Saques: {self.saques_realizados}/{self.limite_saques}"
        return resumo_base


# -----------------------------
# Classes de Cliente
# -----------------------------
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        return conta.realizar_transacao(transacao)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


# -----------------------------
# Menu Interativo
# -----------------------------
def menu():
    clientes = []

    while True:
        print("\n=== MENU BANCÁRIO ===")
        print("1. Criar cliente")
        print("2. Criar conta corrente")
        print("3. Depositar")
        print("4. Sacar")
        print("5. Ver resumo da conta")
        print("6. Ver extrato da conta")
        print("7. Transferir entre contas")
        print("8. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            nascimento = input("Data de nascimento: ")
            endereco = input("Endereço: ")
            cliente = PessoaFisica(cpf, nome, nascimento, endereco)
            clientes.append(cliente)
            print("Cliente criado com sucesso!")

        elif opcao == "2":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if cliente:
                numero = int(input("Número da conta: "))
                limite_credito = float(input("Limite de crédito (ex: 500.00): "))
                limite_saques = int(input("Limite de saques (ex: 3): "))
                conta = ContaCorrente(cliente, numero, limite=limite_credito, limite_saques=limite_saques)
                cliente.adicionar_conta(conta)
                print("Conta criada com sucesso!")
            else:
                print("Cliente não encontrado.")

        elif opcao == "3":
            numero = int(input("Número da conta: "))
            conta = Conta.buscar_conta(numero)
            if conta:
                valor = float(input("Valor do depósito: "))
                deposito = Deposito(valor)
                conta.realizar_transacao(deposito)
                print("Depósito realizado!")
            else:
                print("Conta não encontrada.")

        elif opcao == "4":
            numero = int(input("Número da conta: "))
            conta = Conta.buscar_conta(numero)
            if conta:
                valor = float(input("Valor do saque: "))
                saque = Saque(valor)
                if conta.realizar_transacao(saque):
                    print("Saque realizado!")
                else:
                    print("Saque não autorizado.")
            else:
                print("Conta não encontrada.")

        elif opcao == "5":
            numero = int(input("Número da conta: "))
            conta = Conta.buscar_conta(numero)
            if conta:
                print(conta.resumo())
            else:
                print("Conta não encontrada.")

        elif opcao == "6":
            numero = int(input("Número da conta: "))
            conta = Conta.buscar_conta(numero)
            if conta:
                conta.extrato()
            else:
                print("Conta não encontrada.")

        elif opcao == "7":
            origem_num = int(input("Número da conta de origem: "))
            destino_num = int(input("Número da conta de destino: "))
            valor = float(input("Valor da transferência: "))

            origem = Conta.buscar_conta(origem_num)
            destino = Conta.buscar_conta(destino_num)

            if origem and destino:
                transferencia = Transferencia(valor, destino)
                if origem.realizar_transacao(transferencia):
                    print("Transferência realizada com sucesso!")
                else:
                    print("Saldo insuficiente para transferência.")
            else:
                print("Conta de origem ou destino não encontrada.")

        elif opcao == "8":
            print("Encerrando o sistema.")
            break

        else:
            print("Opção inválida. Tente novamente.")


# -----------------------------
# Execução do Programa
# -----------------------------
if __name__ == "__main__":
    menu()