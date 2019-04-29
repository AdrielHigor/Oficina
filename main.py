from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from screens.servicos_screen import Servicos
from database.db import BancoDados

class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.db = BancoDados()

        self.imgGetter = Image.open("img/logo.jpg")
        self.imgResizer = self.imgGetter.resize((250, 120), Image.ANTIALIAS)
        self.logoImg = ImageTk.PhotoImage(self.imgResizer)
        self.logo = Button(image=self.logoImg, highlightthickness=0, bd=0)
        self.logo.place(width=250, height=120, x=0, y=0)

        self.servicos = Button(self, text="SERVIÇOS", font="Arial, 12", command=self.open_serv)
        self.servicos.place(bordermode=OUTSIDE, width=250, height=60, x=0, y=122)

        self.separadorHorizontal = ttk.Separator(orient=HORIZONTAL)
        self.separadorHorizontal.place(width=2000, height=None, x=0, y=120) 

        self.separadorVertical = ttk.Separator(orient=VERTICAL)
        self.separadorVertical.place(width=None, height=2000, x=251, y=0) 

    def open_serv(self):
        show_servicos = Servicos(self)
        show_servicos.place(x=0, y=0)



app = App()
app.geometry("1920x1080")
app.state('zoomed')
app.mainloop()