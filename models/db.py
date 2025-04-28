import sqlite3


class DB:
    
    def __init__(self):
        self.connection = sqlite3.connect('models/database.db')
        self.cursor = self.connection.cursor()

    def db_create(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS Conta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conta_n INTEGER NOT NULL,
                tipo_conta TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                cpf INTEGER NOT NULL UNIQUE,
                conta_id INTEGER,
                FOREIGN KEY (conta_id) REFERENCES Conta(id)
            );

            CREATE TABLE IF NOT EXISTS Extrato (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                saldo DECIMAL(10, 2) NOT NULL,
                deposito DECIMAL(10, 2),
                saque DECIMAL(10, 2),  
                date DATETIME NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES User(id)
            );
                
        '''
    
        self.cursor.executescript(create_table_query)
        
        self.connection.commit()
    
        print("Database created and connected successfully!")
        
    
    def  insert_conta(self, conta, tipo_conta):
        try:
            self.cursor.execute(
                'INSERT INTO Conta (conta_n, tipo_conta) VALUES (?, ?)', (conta, tipo_conta)
            )
            self.connection.commit()
        except sqlite3.Error as e:
            return e
    
    def get_id_conta(self, conta):
        try:
            self.cursor.execute(
                'SELECT id from Conta WHERE conta_n = ?', (conta,)
            )
            return self.cursor.fetchone()
        
        except sqlite3.Error as e:
            return e
        
    def db_insert_User(self, name, age, cpf, conta_id):
        try:
            # Inserir o usuário, associando o conta_id
            self.cursor.execute(
                'INSERT INTO User (name, age, cpf, conta_id) VALUES (?, ?, ?, ?)', (name, age, cpf, conta_id)
            )
            self.connection.commit()
            return "Usuário inserido com sucesso!"
        except sqlite3.Error as e:
            print(f"Erro ao inserir usuário: {e}")
            return f"Erro ao inserir usuário: {e}"  
            
    def db_insert_Extrato(self, saldo, date, user_id, deposito: int = None, saque: int = None):
        try:
            if deposito is not None:
                self.cursor.execute(
                    'INSERT INTO Extrato (saldo, deposito, date, user_id) VALUES (?, ?, ?, ?)',
                    (saldo, deposito, date, user_id)
                )
            elif saque is not None:
                self.cursor.execute(
                    'INSERT INTO Extrato (saldo, saque, date, user_id) VALUES (?, ?, ?, ?)',
                    (saldo, saque, date, user_id)
                )
            else:
                self.cursor.execute(
                    'INSERT INTO Extrato (saldo, date, user_id) VALUES (?, ?, ?)',
                    (saldo, date, user_id)
                )

            self.connection.commit()
        except sqlite3.Error as e:
            return e

        
    def db_update_user_age(self, user_id, new_age):
        try:
            self.cursor.execute(
                'UPDATE User SET age = ? WHERE id = ?', (new_age, user_id)
            )
            self.connection.commit()
            print("User updated successfully!")
        except sqlite3.Error as e:
            return e
    
    def db_mostra_user(self, name):
        try:
            self.cursor.execute(
                'SELECT * FROM User WHERE name = ?', (name,)
            )
            result = self.cursor.fetchall()
            return result
        except sqlite3.Error as e:
            return e
        
    def mostra_extrato(self, user_id):
        try:
            self.cursor.execute(
                'SELECT * FROM Extrato WHERE user_id = ?', (user_id,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return e
    
    def usuario_existe(self, name):
        try: 
            self.cursor.execute(
                'SELECT id FROM User WHERE name = ?', (name,)
            )
            
            return self.cursor.fetchone()
        
        except sqlite3.Error as e:
            return e
            
    def pegar_saldo_atual(self, user_id):
        try:
            self.cursor.execute(
                '''
                SELECT saldo 
                FROM Extrato 
                WHERE user_id = ? 
                ORDER BY id DESC 
                LIMIT 1
                ''', (user_id,)
            )
            resultado = self.cursor.fetchone()
            return resultado[0] if resultado else 0.0
        except sqlite3.Error as e:
            return e
db = DB()
db.db_create()