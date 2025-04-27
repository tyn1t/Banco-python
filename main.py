import os
from models.db import db
from datetime import datetime
from Conta.conta import Conta
from Conta.contatype import User


conta = Conta()
usuario = User()
now = datetime.now()

menu = """
    [d] => depositar 
    [S] => Sacar 
    [E] => Extrato
    [1] => Limpar Terminal 
    [0] => Sair 
    
=== > 
"""

def limpar_terminal():
    return os.system("cls" if os.name == "nt" else "clear")


def digite_input(title: str = ""):
    try:
        Int = int(input(title + ": "))
        return Int
    except ValueError:
        print("Erro: o valor deve ser um número inteiro!")
        return None

def tela_inicial():
    
    continu = False
    while True:
        nome = input('Nome: ')
        if db.usuario_existe(nome):
            print("Usuário encontrado. Continuando...")
            continu = True
        else:
            print("Banco BPY")
            print('Cadastro de novo usuário...')
            
            usuario.nome = input('Nome: ')
            usuario.idade = digite_input('Idade')
            usuario.cpf = digite_input('CPF')
            usuario.typeconta = digite_input('Tipo de Conta')
            
            if usuario.idade is not None and usuario.cpf is not None and usuario.conta is not None:
                
                usuario.type_conta(usuario.typeconta)
                
                db.db_insert_User(name=nome, age=usuario.idade)
                continu = True
            else:
                print("Erro: dados inválidos. Tente novamente.")

        if continu:
            user = db.db_mostra_user(nome)
            user_id = user[0][0]
            
            if user_id:
                Conta.saldo = db.pegar_saldo_atual(user_id=user_id)
                
                date = now.strftime("%Y-%m-%d %H:%M:%S")
                db.db_insert_Extrato(saldo=Conta.saldo, date=date, user_id=user_id)
                return user
        
        break


date = now.strftime("%Y-%m-%d %H:%M:%S")


user = tela_inicial()
user_id = user[0][0]

while True:
    
    
    print("Bem Banco BPY ...")
    print(f"User:  {user[0][1]:<15}  |  Saldo: R$ {Conta.saldo:,.2f}")
    
    opcoes = input(menu).lower()
    
    
    if opcoes == "d": 
        print("Depositar")
        valor = input('Valor:')
        conta.Depositar(value=float(valor))
        db.db_insert_Extrato(saldo=conta.saldo, date=datetime.datetime.now(), user_id=user_id)

        
    if opcoes == "s":
        print("Sacar")
        valor = input('Valor:')
        conta.Sacar(value=float(valor))
        db.db_insert_Extrato(saldo=conta.saldo, date=datetime.datetime.now(), user_id=user_id)

        
    
    if opcoes == "e": 
        print("Extrato")
        extratos = db.mostra_extrato(user_id=user_id)  # Atualiza!
        for extrato in extratos:
            print(f'ID: {extrato[0]} | Saldo: {extrato[1]}  | Date: {extrato[2]}')
    
    if opcoes == "0":
        print("Sair ...")
        break
    
    if opcoes == "1":
        limpar_terminal()
