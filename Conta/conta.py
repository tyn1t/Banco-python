class Conta:
    def __init__(self, saldo: float = 0):
        self.saldo = saldo
        self.Limite = 500
        
    def Depositar(self, value: float = 0):
        if float(value) > 0:
            self.saldo += float(value)
        else: 
            print('Valor inválido para depósito.')
        
    def Sacar(self, value: float = 0): 
        if float(value) > 0 and self.saldo >= float(value):
            self.saldo -= float(value)
        else:
            print('Saldo insuficiente para saque.')