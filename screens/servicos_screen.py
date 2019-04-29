from tkinter import *
from tkinter import ttk
import time
import pyautogui
import sqlite3
from database.db import BancoDados

class Servicos(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.bd = BancoDados()
        self.connection = sqlite3.connect('Oficina.db')
        self.c = self.connection.cursor()

        self.txt = Label(parent, text="SERVIÇOS", font="Arial, 16")
        self.txt.place(width=None, height=None, x=720, y=50)

        self.servicoMenu = ttk.Notebook(parent)
        self.f1 = ttk.Frame(self.servicoMenu)
        self.f2 = ttk.Frame(self.servicoMenu)
        self.servicoMenu.add(self.f1, text="Cadastrar Serviço")
        self.servicoMenu.add(self.f2, text="Lista de Serviços")
        self.servicoMenu.place(width=2000, height=2000, x=252, y=95)

        self.cadastro_servico()
        self.lista_servico()
    
    def cadastro_servico(self):
        self.x = 0
        self.posEntryY = 230
        self.posEntryX = 50
        self.entry_dic = {}
        self.numero_dic = {}

        self.clientLbl = Label(self.f1, text="Cliente:")
        self.clientLbl.place(width=None, height=None, x=50, y=30)

        self.clientEnt = Entry(self.f1)
        self.clientEnt.place(width=400, height=25, x=50, y=50)

        self.motoLbl = Label(self.f1, text="Moto:")
        self.motoLbl.place(width=None, height=None, x=50, y=90)

        self.motoEnt = Entry(self.f1)
        self.motoEnt.place(width=200, height=25, x=50, y=110)

        self.placaLbl = Label(self.f1, text="Placa:")
        self.placaLbl.place(width=None, height=None, x=300, y=90)

        self.placaEnt = Entry(self.f1)
        self.placaEnt.place(width=150, height=25, x=300, y=110)

        self.mecanicoLbl = Label(self.f1, text="Mecânico:")
        self.mecanicoLbl.place(width=None, height=None, x=50, y=150 )

        self.mecanicosVar = StringVar()
        self.mecanicosVar.set('None')
        self.mecanico = ttk.Combobox(self.f1, textvariable=self.mecanicosVar, values=['None', 'teste', 'help'])
        self.mecanico.place(width=400, height=25, x=50, y=170)

        self.servicoLbl = Label(self.f1, text="Serviço:")
        self.servicoLbl.place(width=None, heigth=None, x=50, y=210)

        self.servicoEnt = Entry(self.f1)
        self.servicoEnt.place(width=400, height=25, x=50, y=230)
        self.servicoEnt.bind('<Return>', (lambda event: (self.add_serv())))
        self.servicoEnt.bind('<Delete>', (lambda event: (self.remove_serv())))
        
        self.numero_stb = Label(self.f1, text=("1-"))
        self.numero_stb.place(width=None, height=None, x=25, y=230)

        self.add_servico = Button(self.f1, text="Adicionar", command=self.add_serv)
        self.add_servico.place(width=100, height=25, x=460, y=230)

        self.rmv_servico = Button(self.f1, text="Remover", command=self.remove_serv)
        self.rmv_servico.place(width=100, height=25, x=460, y=255)

        self.finalizarBtn = Button(self.f1, text="finalizar", command=self.finalizar)
        self.finalizarBtn.place(width=100, height=25, x=460, y=400)


    def add_serv(self):
        
        self.posEntryY +=35
        self.x+=1

        self.numero_dic[self.x] = Label(self.f1, text=(self.x+1,"-"))
        self.numero_dic[self.x].place(width=None, height=None, x=25, y=(self.posEntryY+2))

        self.entry_dic[self.x] = Entry(self.f1)
        self.entry_dic[self.x].place(width=400, height=25, x=50, y=self.posEntryY)
        self.entry_dic[self.x].bind('<Return>', (lambda event: self.add_serv()))
        self.entry_dic[self.x].bind('<Delete>', (lambda event: (self.remove_serv())))

        print(
            self.entry_dic[self.x-1].get(),
            )
        
        self.entry_dic[self.x].selection_range(0,END)
    
    def remove_serv(self):
        self.entry_dic[self.x].place_forget()
        self.numero_dic[self.x].place_forget()
        del self.entry_dic[self.x]
        del self.numero_dic[self.x]
        
        self.x -=1
        self.posEntryY -= 35

    def posicao_counter(self):
        try:
            self.c.execute('INSERT INTO Servico VALUES(?, ?, ?, ?, ?, ?)',  (0, 'cliente', 'moto', 'placa', 'mecanico', 'servico'))
            self.connection.commit()
        except sqlite3.IntegrityError:
            pass

        pos = self.c.execute("SELECT posicao FROM Servico")
        posicoes = self.c.fetchall()
        
        for key in posicoes:
            print(key[0])
            aux = (key[0])
            return (aux)
    
    def finalizar(self):

        cliente = self.clientEnt.get()
        moto = self.motoEnt.get()
        placa = self.placaEnt.get()
        mecanico = self.mecanico.get()
        servico = self.servicoEnt.get()
            
        for key in self.entry_dic:
            print(self.entry_dic[key].get())
            self.entry_dic[key].place_forget()
            self.numero_dic[key].place_forget()
        
        pos = (self.posicao_counter() + 1)
        
        self.bd.add_servico(pos, cliente, moto, placa, mecanico, servico)

        self.cadastro_servico()
        self.show_servicos()
    
    def lista_servico(self):
        self.tabela = ttk.Treeview(self.f2, height=20,columns=("Pos", "Client", "Moto", "Placa", "Mecanico", "Servico"))
        self.tabela["show"] = 'headings'
        self.tabela.place(height=723, width=1326, x=0, y=0)
        self.tabela.heading("#1", text='Posição', anchor=W)
        self.tabela.heading("#2", text='Cliente', anchor=W)
        self.tabela.heading("#3", text='Moto', anchor=W)
        self.tabela.heading("#4", text='Placa', anchor=W)
        self.tabela.heading("#5", text='Mecânico', anchor=W)
        self.tabela.heading("#6", text='Serviço', anchor=W)

        self.verticalBar = Scrollbar(self.f2, orient='vertical', command=self.tabela.yview)
        self.verticalBar.place(height=723, width=20, x=1326, y=0)
        self.tabela.configure(yscroll=self.verticalBar.set)

        self.show_servicos()

    def show_servicos(self):
        pass
        pos = self.c.execute("SELECT posicao FROM Servico")
        posicoes = self.c.fetchall()
        print(posicoes)
        for key in posicoes:
            posicao = (key[0])
            posicao += 1 
            self.c.execute("SELECT * FROM Servico WHERE posicao == {}".format(posicao))
        self.listas = self.c.fetchall()

        for x in self.listas:
            self.tabela.insert("", END, values=x)
