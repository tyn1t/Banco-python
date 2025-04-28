import os
from models.db import db
from datetime import datetime
from Conta.conta import Conta
from Conta.contatype import User


conta = Conta()
usuario = User()
now = datetime.now()

menu = """
    [D] => depositar 
    [S] => Sacar 
    [E] => Extrato
    [M] => Mostra Conta
    [L] => Limpar Terminal 
    [0] => Sair 
=== > 
"""

def limpar_terminal():
    return os.system("cls" if os.name == "nt" else "clear")

def dedenho(desenho: str = None, num: int = None):
    print(desenho * num)

def digite_input(title: str = ""):
    """ Função para capturar entrada numérica """
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
        
        # Verifica se o usuário existe
        if db.usuario_existe(nome):
            print("Usuário encontrado. Continuando...")
            continu = True
        else:
            print("Banco BPY")
            print('Cadastro de novo usuário...')
            print("____________________")
            
            usuario.nome = input('Nome: ')
            usuario.idade = digite_input('Idade')
            cpf = input("CPF: ")
            usuario.set_cpf(cpf)
            usuario.typeconta = digite_input('Tipo de Conta')
            
            print("____________________")
            
            cpf = usuario.get_cpf()
        
            if not cpf:
                print("Erro: CPF inválido.")
                continue
            
            if usuario.idade is not None and cpf is not None and usuario.conta is not None:
                
                
                usuario.type_conta(usuario.typeconta)
                db.insert_conta(usuario.conta, usuario.typeconta)
                
                id_conta = db.get_id_conta(usuario.conta)
                
                db.db_insert_User(name=usuario.nome, age=usuario.idade, cpf=usuario.get_cpf(), conta_id=id_conta[0])
                
                continu = True
            else:
                print("Erro: dados inválidos. Tente novamente.")
        
        print("+++++++++++++++++++++++++++++++++++")
        if continu:
            if not nome:
                nome = input('Nome: ')
                
            user = db.db_mostra_user(nome)
            if user:  
                
                
                Conta.saldo = db.pegar_saldo_atual(user_id=user[0])
                
                date = now.strftime("%Y-%m-%d %H:%M:%S")
                db.db_insert_Extrato(saldo=Conta.saldo, date=date, user_id=user[0])  # Corrigido para user[0]
                
                return user
        
        break


def mostra_conta(user):
    
    dedenho(desenho="_", num=35)
    print(f' Conta '.center(35, '='))
    for result in user:
        print(f"Conta: {result[1]} | idade: {result[2]}  | cpf: {result[3]}")
    dedenho(desenho="_", num=35)
    
date = now.strftime("%Y-%m-%d %H:%M:%S")



user = tela_inicial()
user_id = user[0][0]
conta.saldo = db.pegar_saldo_atual(user_id)

while True:
    
    
    print("Bem Banco BPY ...")
    print(f"User:  {user[0][1]}  |  Saldo: R$ {conta.saldo}")
    print('_' * 35)
    
    opcoes = input(menu).lower()
    limpar_terminal()
    
    dedenho(desenho="-", num=35)
    
    if opcoes == "d": 
        print("Depositar")
        valor = input('Valor:')
        conta.Depositar(value=float(valor))
        db.db_insert_Extrato(saldo=conta.saldo, deposito=valor, date=date, user_id=user_id)

        
    if opcoes == "s":
        print("Sacar")
        valor = input('Valor:')
        conta.Sacar(value=float(valor))
        db.db_insert_Extrato(saldo=conta.saldo, saque=valor, date=date, user_id=user_id)

        
    
    if opcoes == "e": 
        print("Extrato")
        extratos = db.mostra_extrato(user_id=user_id) 
        for extrato in extratos:
            print(f'ID: {extrato[0]} | Saldo: {extrato[1]}  | Date: {extrato[2]}')
    
    if opcoes == "m":
        mostra_conta(user)
        
    if opcoes == "0":
        print("Sair ...")
        break
    
    if opcoes == "1":
        limpar_terminal()
        
    dedenho(desenho="+", num=35)
