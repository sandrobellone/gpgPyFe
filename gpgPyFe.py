import sys
from Tkinter import *
import tkMessageBox
from os import system

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.a1=Label(frame,text="gpgPyFe",bg="yellow")
        self.a1.pack(side=TOP)
        self.testo=StringVar()
        self.t="\n"
        if (len(sys.argv)==1): self.t+="\n Non ci sono file da processare \n"
        else:
            for arg in sys.argv[1:]:
                self.t+=arg+'\n'            
        self.testo.set(self.t)
        self.area_testo=Label(frame, textvariable=self.testo, justify=LEFT)
        self.area_testo.pack(side=TOP)
        self.b1 = Button(frame, text="Cifra", command=self.cifra)
        self.b1.pack(side=LEFT)
        self.b2 = Button(frame, text="Cifra e firma", command=self.cifraFirma)
        self.b2.pack(side=LEFT)
        self.b3 = Button(frame, text="Decifra", command=self.decifra)
        self.b3.pack(side=LEFT)
        self.b4 = Button(frame, text="Firma", command=self.firma)
        self.b4.pack(side=LEFT)
        self.b5 = Button(frame, text="Verifica", command=self.verifica)
        self.b5.pack(side=LEFT)        
        self.bi = Button(frame, text="Info", command=self.info)
        self.bi.pack(side=LEFT)
        self.bq = Button(frame, text="Esci", bg="yellow", command=frame.quit)
        self.bq.pack(side=LEFT)
    def info(self):
        tkMessageBox.showinfo("gpgPyFe", "Un front end per gpg.\nSandro Bellone\nAprile 2017\n\n"
                              "Copyright 2017\nGNU General Public License vers.3")
    def eseguigpg(self,opt):
        self.t="\n"
        for arg in sys.argv[1:]:
            x=system("gpg "+opt+" "+arg)
            if x==0: self.t+="Ok - "
            else: self.t+="Exit status: "+str(x)+" "
            self.t+=arg+"\n"
            self.testo.set(self.t)
    def cifra(self):
        self.eseguigpg("-r 4B4EB747 -e")
    def cifraFirma(self):
        self.eseguigpg("-r 4B4EB747 -es")
    def decifra(self):
        self.eseguigpg("")
    def firma(self):
        self.eseguigpg("-sb")
    def verifica(self):
        self.eseguigpg("--verify")

root = Tk()
app = App(root)
root.mainloop()
root.destroy()