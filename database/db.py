import sqlite3

class BancoDados():
    def __init__(self):
        self.connection = sqlite3.connect('Oficina.db')
        self.c = self.connection.cursor()

        try:
            self.c.execute('CREATE TABLE Servico (posicao INTERGER NOT NULL, cliente VARCHAR, moto VARCHAR, placa VARCHAR, mecanico VARCHAR, servico VARCHAR, PRIMARY KEY(posicao))')
        except sqlite3.OperationalError:
            pass
    
    def add_servico (self, posicao, cliente, moto, placa, mecanico, servico):
        self.c.execute('INSERT INTO Servico VALUES(?, ?, ?, ?, ?, ?)',  (posicao, cliente, moto, placa, mecanico, servico))
        self.connection.commit()
    