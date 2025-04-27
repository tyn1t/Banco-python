import sqlite3


class DB:
    
    def __init__(self):
        self.connection = sqlite3.connect('models/database.db')
        self.cursor = self.connection.cursor()

    def db_create(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER
            );

            CREATE TABLE IF NOT EXISTS Extrato (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                saldo FLOAT NOT NULL,
                date TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES User(id)
            );
                
        '''
    
        self.cursor.executescript(create_table_query)
        
        self.connection.commit()
    
        print("Database created and connected successfully!")
        
    
    def  db_insert_User(self, name, age):
        try: 
            self.cursor.execute(
                'INSERT INTO User (name, age) VALUES (?, ?)', (name, age))
            self.connection.commit() 
        except sqlite3.Error as e:
            return e
            
        
    def db_insert_Extrato(self, saldo, date, user_id):
        try:
            self.cursor.execute(
                'INSERT INTO Extrato (saldo, date, user_id) VALUES (?,  ?, ?)', (saldo, date, user_id)
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