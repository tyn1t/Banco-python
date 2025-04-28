import uuid

class TypeConta:
    def __init__(self):
        self.conta_corrente = 0
        self.conta_poupanca = 1

class User(TypeConta):
    def __init__(self, nome: str = None, idade: int = 0, cpf: str = None):
        super().__init__() 
        self.nome = nome
        self.idade = idade
        
        if cpf:
            self.set_cpf(cpf)
        else:
            self.__cpf = None

        self.conta = self.iu_conta()

    def type_conta(self, conta):
        if conta == self.conta_corrente:
            self.typeconta = "Corrente"
        elif conta == self.conta_poupanca:
            self.typeconta = "Poupança"
        else:
            self.typeconta = "Tipo Desconhecido"
    
    def set_cpf(self, cpf: str):
        if self.validar_cpf(cpf):  # Valide o CPF antes de atribuí-lo
            self.__cpf = cpf
        else:
            print("Erro: CPF inválido.")
    
    def validar_cpf(self, cpf: str) -> bool:
        if len(cpf) == 11 and cpf.isdigit():
            return True
        return False
    
    def get_cpf(self):
        return self.__cpf
    
    def iu_conta(self):
        return int(str(uuid.uuid4().int)[0:8])