import os
from models.db import db
import datetime
from Operecoes.operecoes import Operecoes

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



Oper = Operecoes()




nome = input('Nome: ')
if db.usuario_existe(nome):
    print("continua ...")
else:
    print("Banco BPY")
    print('Cadastra ...')
    nome = input('Nome: ')
    idade = int(input('Idade: '))
    db.db_insert_User(name=nome, age=idade)
    
user = db.db_mostra_user(nome)
user_id = user[0][0]


date = datetime.datetime.now()

if user_id:
    Oper.saldo = db.pegar_saldo_atual(user_id=user_id)
    db.db_insert_Extrato(saldo=Oper.saldo, date=date, user_id=user_id)

while True:
    
    print("Bem Banco BPY ...")
    
    print(f"User:  {user[0][1]:<15}  |  Saldo: R$ {Oper.saldo:,.2f}")
    
    opcoes = input(menu).lower()
    
    
    if opcoes == "d": 
        print("Depositar")
        valor = input('Valor:')
        Oper.Depositar(value=float(valor))
        db.db_insert_Extrato(saldo=Oper.saldo, date=datetime.datetime.now(), user_id=user_id)

        
    if opcoes == "s":
        print("Sacar")
        valor = input('Valor:')
        Oper.Sacar(value=float(valor))
        db.db_insert_Extrato(saldo=Oper.saldo, date=datetime.datetime.now(), user_id=user_id)

        
    
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
