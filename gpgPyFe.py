#!/usr/bin/env python
##     gpgPyFe.py - versione 0.01
##	
##     Copyright 2017 Sandro Bellone
##	
##     This program is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.
##
##     This program is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.
##
##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from Tkinter import *
import tkMessageBox
import os
import ConfigParser

pw=""

class MyDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.myLabel = Label(top, text='Inserisci la password')
        self.myLabel.pack()

        self.myEntryBox = Entry(top, show = '*')
        self.myEntryBox.pack()
        self.myEntryBox.bind('<Return>', self.send_return)


        self.mySubmitButton = Button(top, text='Conferma', command=self.send_ok)
        self.mySubmitButton.pack()
        self.myEntryBox.focus_set()

    def send_ok(self):
        global pw
        pw = self.myEntryBox.get()
        self.top.destroy()
    def send_return(self, Event):
        self.send_ok()
def getpwd():
    inputDialog = MyDialog(root1)
    root1.wait_window(inputDialog.top)
    return pw
class App:
    def __init__(self, master):
        #Estrae cartella di lavoro
        pathname = os.path.dirname(sys.argv[0]) 
        #Lettura file di configurarazione gpgPyFe.ini
        cfg=ConfigParser.RawConfigParser()
        cfg.read(os.path.join(pathname,'gpgPyFe.ini'))
        if cfg.has_option('gpgPyFe','IDchiave'):
            self.IDchiave=cfg.get('gpgPyFe','IDchiave')
        else:
            self.IDchiave='xxxxxxxx'
        if cfg.has_option('gpgPyFe','gpgPath'):
            self.gpgPath=cfg.get('gpgPyFe','gpgPath')
        else:
            self.gpgPath=''
        #Verifica presenza gpg
        redir_to_dev_null=""
        if os.name=='posix':
            redir_to_dev_null=">/dev/null"
        #if (os.system(self.gpgPath+"gppg --version>/dev/null")!=0):
        if (os.system(self.gpgPath+"gpg --version"+redir_to_dev_null)!=0):
            tkMessageBox.showwarning("Errore","Programma gpg non presente nel sistema.")
        frame = Frame(master)
        frame.pack()

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
        self.b3 = Button(frame, text="Cifra simmetrica", command=self.cifraSimmetrica)
        self.b3.pack(side=LEFT)
        self.b4 = Button(frame, text="Decifra", command=self.decifra)
        self.b4.pack(side=LEFT)
        self.b5 = Button(frame, text="Decifra (asimmetrica)", command=self.decifraSimmetrica)
        self.b5.pack(side=LEFT)
        self.b6 = Button(frame, text="Firma", command=self.firma)
        self.b6.pack(side=LEFT)
        self.b7 = Button(frame, text="Verifica", command=self.verifica)
        self.b7.pack(side=LEFT)        
        self.bi = Button(frame, text="Info", command=self.info)
        self.bi.pack(side=LEFT)
        self.bq = Button(frame, text="Esci", bg="yellow", command=frame.quit)
        self.bq.pack(side=LEFT)
    def info(self):
        if os.name=="nt":
            nomeSistema="Microsoft Windows"
        elif os.name=="posix":
            nomeSistema="Gnu/Linux"
        else:
            nomeSistema="sconosciuto"
        tkMessageBox.showinfo("gpgPyFe", "Un front end per gpg.\nSandro Bellone\nAprile 2017\n\n"
                              "Copyright 2017\nGNU General Public License vers.3\n\n"
                              "Sistema: "+nomeSistema+"\n"
                              "Path: "+os.path.dirname(sys.argv[0])+"\n"
                              "ID Chiave: "+self.IDchiave+"\n"
                              "gpgPath: "+self.gpgPath)
    def eseguigpg(self,opt):
        self.t="\n"
        for arg in sys.argv[1:]:
            x=os.system(os.path.join(self.gpgPath,"gpg ")+opt+" "+arg)
            if x==0: self.t+="Ok - "
            else: self.t+="Exit status: "+str(x)+" "
            self.t+=arg+"\n"
            self.testo.set(self.t)
    def cifra(self):
        self.eseguigpg("-r "+self.IDchiave+" -e")
    def cifraFirma(self):
        self.eseguigpg("-r "+self.IDchiave+" -es")
    def cifraSimmetrica(self):
        pw=getpwd()
        self.eseguigpg("--passphrase "+pw+" -c --no-use-agent")
    def decifra(self):
        self.eseguigpg("")
    def decifraSimmetrica(self):
        pw=getpwd()
        self.eseguigpg("--passphrase "+pw+" --no-use-agent")
    def firma(self):
        self.eseguigpg("-sb")
    def verifica(self):
        self.eseguigpg("--verify")


root1 = Tk()
app = App(root1)
root1.title("gpgPyFe")
root1.mainloop()
root1.destroy()
