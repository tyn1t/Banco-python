import uuid

class TypeConta:
    def __init__(self):
        self.conta_corrente = 0
        self.conta_poupanca = 1

class User(TypeConta):
    def __init__(self, nome: str = None, idade: int = 0, cpf: str = None):
        super().__init__() 
        self.nome = nome
        self.__cpf = cpf
        self.idade = idade
        self.conta = self.iu_conta()

    def type_conta(self, conta):
        if conta == self.conta_corrente:
            self.typeconta = "Corrente"
        elif conta == self.conta_poupanca:
            self.typeconta = "Poupança"
        else:
            self.typeconta = "Tipo Desconhecido"
    
    def confirma_cpf(self):
        cpf = int(self.__cpf.split("-", ""))
        if len(cpf) == 11:
            self.__cpf = cpf
        return None
    
    def iu_conta(self):
        return int(str(uuid.uuid4().int)[0:8])