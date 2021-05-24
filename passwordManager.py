#
# Password Manager by Warren Lim
version = '0.0.2-test'

import tkinter as tk
from tkinter import Frame, Label, Entry, Button, BOTH, END, NORMAL, StringVar
from tkinter.constants import GROOVE
from tkinter.ttk import Combobox, Separator 
from passmanFunctions import *
import ctypes

class GUI(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
                 
        self.parent = parent
        self.loginUI()
                
        
    def loginUI(self):

        self.parent.title('Password Manager')
        self.pack(fill=BOTH, expand=True)
        
        self.grid_columnconfigure(0,weight=1,minsize=150)
        self.grid_rowconfigure(0,weight=1,minsize=50)
        
        # Title
        self.title = Label(self, text='Password Manager', font=('Century Gothic', 20))
        self.title.grid(row=0,columnspan=2, padx=10)

        # Version
        self.version = Label(self, text='© Warren Lim 2021 | version %s'%version,font=('Calibri', 8))
        self.version.grid(row=1,pady=(0,10),sticky='n',columnspan=2)
        
        # Username
        self.unameLabel = Label(self, text='Username:', font=('Calibri',12))
        self.unameLabel.grid(row=2,sticky='w',padx=10,columnspan=2)
        self.uname = Entry(self, width=35)
        self.uname.grid(row=3,pady=(0,10),columnspan=2)

        # Password
        self.pwLabel = Label(self, text='Master password:', font=('Calibri',12))
        self.pwLabel.grid(row=4,sticky='w',padx=10,columnspan=2)
        self.password = Entry(self, width=35,show='\u2022') # show password as bullets
        self.password.grid(row=5,pady=(0,10),columnspan=2)

        # Seperator
        self.line = Separator(self,orient='horizontal')
        self.line.grid(row=6,sticky='we',columnspan=2)

        # Create Account Button
        self.createAccBut = Button(self,text='Create Account', command=self.newAccountUI, width=15,bg='#ffff80',relief=GROOVE)
        self.createAccBut.grid(row=7,pady=10,padx=(20,0),sticky='w',columnspan=2)

        # Login Button
        self.loginBut = Button(self,text='Login', command=self.loginButton, width=15,bg='#ffff80',relief=GROOVE)
        self.parent.bind('<Return>', self.enter) # makes enter key press the login button
        self.loginBut.grid(row=7,column=1,pady=10,padx=(0,20),sticky='w')

    def enter(self, event):
        # make enter key press Go button
        self.loginButton()

    def loginButton(self):
        # get input
        uname = self.uname.get()
        password = self.password.get()

        # reset font colours
        if uname != '':
            self.unameLabel.config(fg='black')
        if password != '':
            self.pwLabel.config(fg='black')

        if uname and password: # run code if both entries are filled in
            # clear entries
            self.uname.delete(0, END) 
            self.password.delete(0, END) 
            # make database if not already made
            createDB()
            # store/check master password
            status = checkMaster(uname,password)
            if status == -1: # record DNE
                ans = ctypes.windll.user32.MessageBoxW(0, 'Unrecognized account. Do you want to create a new account?', 'Confirmation', 0x10004) #yes no dialog pop up that always stays on top
                if ans == 7: # if answer is no
                    return -1
                if ans == 6: # answer is yes
                    self.newAccountUI() # go to new account screen
            if status == 0: # login successful
                print('login successful')
                self.loggedInUI()
            if status == -2: # login unsuccessful
                print('invalid password')
                self.pwLabel.config(text='Invalid password. Please try again:',fg='red')

        # make font colour red for missing fields
        if uname == '':
            self.unameLabel.config(fg='red')
        if password == '':
            self.pwLabel.config(fg='red')
    
    def newAccountUI(self):
        self.title.config(text='New account')
        self.unameLabel.config(text='Create a username:', fg='black')
        self.pwLabel.config(text='Create a strong master password:', fg='black')

        self.createAccBut.grid_forget()
        self.loginBut.grid_forget()

        self.version.config(text='Master password will be used to retrieve your \nstored passwords.Please keep it in a safe place \nand make sure it is strong.')

        # Cancel Button
        self.cancelBut = Button(self,text='Cancel', command=self.cancel, width=15,bg='#ffff80',relief=GROOVE)
        self.cancelBut.grid(row=7,pady=10,padx=(20,0),sticky='w',columnspan=2)

        # Create Button
        self.createBut = Button(self,text='Create', command=self.create, width=15,bg='#ffff80',relief=GROOVE)
        self.createBut.grid(row=7,column=1,pady=10,padx=(0,20),sticky='w')

    def create(self):
        uname = self.uname.get()
        password = hashPassword(self.password.get())
        storeDB('MasterPassword',uname,password)
        self.clearWidgets()
        self.loginUI()

    def cancel(self):
        self.clearWidgets()
        self.loginUI()
    
    def loggedInUI(self):
        self.clearWidgets()
        
        # Title
        self.title = Label(self, text='Password Manager', font=('Century Gothic', 20))
        self.title.grid(row=0,columnspan=2, padx=10)

        # Version
        self.version = Label(self, text='© Warren Lim 2021 | version %s'%version,font=('Calibri', 8))
        self.version.grid(row=1,pady=(0,10),sticky='n',columnspan=2)

        # Choose Service
        self.serviceLabel = Label(self, text='Choose a service:', font=('Calibri',12))
        self.serviceLabel.grid(row=2,sticky='w',padx=10,columnspan=2)
        self.service = StringVar(self)
        self.serviceList = Combobox(self, state='readonly',textvariable=self.service, values=[], width=32)
        self.serviceList.grid(row=3,padx=(30,0),pady=(0,10),columnspan=2,sticky='w')

        # Show username
        self.unameLabel = Label(self, text='Username:', font=('Calibri',12))
        self.unameLabel.grid(row=4,sticky='w',padx=10,columnspan=2)
        self.uname = Entry(self, width=35)
        self.uname.grid(row=5,padx=(30,0),pady=(0,10),columnspan=2,sticky='w')

        # Show password
        self.pwLabel = Label(self, text='Password:', font=('Calibri',12))
        self.pwLabel.grid(row=6,sticky='w',padx=10,columnspan=2)
        self.showPass = Entry(self, width=28,show='\u2022') # show password as bullets
        self.showPass.grid(row=7,pady=(0,10),padx=(30,0),columnspan=2,sticky='w')
        # Copy password
        self.copyBut = Button(self,text='Show', command=self.show, width=5,bg='#ffff80',relief=GROOVE)
        self.copyBut.grid(row=7,column=1,padx=(0,30),sticky='e')

        # Seperator
        self.line = Separator(self,orient='horizontal')
        self.line.grid(row=8,sticky='we',columnspan=2)

        # Logout button
        self.createAccBut = Button(self,text='Logout', command=self.logout, width=15,bg='#ffff80',relief=GROOVE)
        self.createAccBut.grid(row=9,pady=10,padx=(20,0),sticky='w',columnspan=2)

        # Copy button
        self.loginBut = Button(self,text='Copy', command=self.copy, width=15,bg='#ffff80',relief=GROOVE)
        self.parent.bind('<Return>', self.enter) # makes enter key press the login button
        self.loginBut.grid(row=9,column=1,pady=10,padx=(0,20),sticky='w')

        # Add new button
        self.addBut = Button(self,text='Add new', command=self.addNew,bg='#ffff80',relief=GROOVE)
        self.addBut.grid(row=10,pady=(0,10),padx=20,sticky='we',columnspan=2)
    
    def show(self):
        if self.showPass.config()['show'][4] == '•': # returns ('show', 'show', 'Show', '', '•')
            self.showPass.config(show='')
        else: self.showPass.config(show='•')
        
    def copy(self):
        text = self.showPass.get()
        print(text)
        # copy to clipboard
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

    def logout(self):
        self.clearWidgets()
        self.loginUI()
        # forget master password

    def clearWidgets(self):
        for widget in self.winfo_children(): # remove all widgets and remake them
            widget.destroy()
    
    def addNew(self):
        pass


def main():
    root = tk.Tk()
    root.iconbitmap('img/keyicon.ico')
    app = GUI(root)
    root.mainloop()  


if __name__ == '__main__':
    main()    