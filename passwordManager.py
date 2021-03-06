# Password Manager by Warren Lim
# Started on May 20, 2021

version = '2.1.0'

# GUI inports
import tkinter as tk
from tkinter import Frame, Label, Entry, Button, BOTH, END, NORMAL, StringVar
from tkinter.constants import DISABLED, GROOVE
from tkinter.ttk import Combobox, Separator 
from passmanFunctions import *
import ctypes

# encryption imports
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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
        self.parent.bind('<Return>', self.loginEnter) # makes enter key press the login button
        self.loginBut.grid(row=7,column=1,pady=10,padx=(0,20),sticky='w')

        # make database if not already made
        self.after(80,self.firstTime)

    def firstTime(self):
        if not DBexist():
            createDB()
            ctypes.windll.user32.MessageBoxW(0, 'First time run detected. Please create a new account', 'Create New Account', 0x0)
            self.newAccountUI()

    def loginEnter(self, event):
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
                self.masterPassword = password # store master password
                self.user = uname # store passman user
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

        self.parent.bind('<Return>', self.newAccEnter) # bind enter to button

    def newAccEnter(self, event):
        # make enter key press Go button
        self.create()

    def create(self):
        uname = self.uname.get()
        password = hashPassword(self.password.get())
        storeDB('MasterPassword',uname,password,uname)
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

        # Retrieve all services
        records = getServices(self.user)

        # Choose Service
        self.serviceLabel = Label(self, text='Choose a service:', font=('Calibri',12))
        self.serviceLabel.grid(row=2,sticky='w',padx=10,columnspan=2)
        self.service = StringVar(self)
        services = list(set(records[i][0] for i in range(len(records)))) # get all services and remove duplicates
        services.sort() # sort list
        self.serviceList = Combobox(self, state='readonly',textvariable=self.service, values=services, width=32)
        self.serviceList.grid(row=3,padx=(30,0),pady=(0,10),columnspan=2,sticky='w')
        self.serviceList.bind('<<ComboboxSelected>>', self.retrieve)

        # Show username
        self.unameLabel = Label(self, text='Username:', font=('Calibri',12))
        self.unameLabel.grid(row=4,sticky='w',padx=10,columnspan=2)
        self.username = StringVar(self)
        self.unameList = Combobox(self, state='readonly',textvariable=self.username, values=[], width=32)
        self.unameList.grid(row=5,padx=(30,0),pady=(0,10),columnspan=2,sticky='w')

        # Retrieved password
        self.pwLabel = Label(self, text='Password:', font=('Calibri',12))
        self.pwLabel.grid(row=6,sticky='w',padx=10,columnspan=2)
        self.showPass = Entry(self, width=28,show='\u2022') # show password as bullets
        self.showPass.grid(row=7,pady=(0,10),padx=(30,0),columnspan=2,sticky='w')
        # Show password
        self.showBut = Button(self,text='Show', command=lambda:self.show(self.showPass), width=5,bg='#ffff80',relief=GROOVE)
        self.showBut.grid(row=7,column=1,padx=(0,30),pady=10,sticky='e')

        # Seperator
        self.line = Separator(self,orient='horizontal')
        self.line.grid(row=8,sticky='we',columnspan=2)

        # Logout button
        self.createAccBut = Button(self,text='Logout', command=self.logout, width=15,bg='#ffff80',relief=GROOVE)
        self.createAccBut.grid(row=9,pady=(10,0),padx=(20,0),sticky='w',columnspan=2)

        # Copy button
        self.loginBut = Button(self,text='Copy', command=self.copy, width=15,bg='#ffff80',relief=GROOVE)
        self.loginBut.grid(row=9,column=1,pady=(10,0),padx=(0,20),sticky='w')

        # Edit Button
        self.editBut = Button(self,text='Edit', command=lambda: self.editUI(self.serviceList.get(),self.unameList.get()), width=15,bg='#ffff80',relief=GROOVE)
        self.editBut.grid(row=10,pady=10,padx=(20,0),sticky='w',columnspan=2)

        # Delete Button
        self.editBut = Button(self,text='Delete', command=self.deleteEntry, width=15,bg='#ffff80',relief=GROOVE)
        self.editBut.grid(row=10,column=1,pady=10,padx=(0,20),sticky='w')

        # Add new button
        self.addBut = Button(self,text='Add new', command=self.newEntryUI,bg='#ffff80',relief=GROOVE)
        self.addBut.grid(row=11,pady=(0,10),padx=20,sticky='we',columnspan=2)
    
    def show(self,widget):
        if widget.config()['show'][4] == '•': # returns ('show', 'show', 'Show', '', '•')
            widget.config(show='')
        else: widget.config(show='•')
        
    def copy(self):
        text = self.showPass.get()
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
    
    def encryptPassword(self,passwordTxt):
        key = self.createKey()
        f = Fernet(key)
        passwordEncrypted = f.encrypt(passwordTxt.encode())
        return passwordEncrypted

    def addNew(self):
        # get input
        service = self.serviceEntry.get().upper()
        username = self.uname.get()
        passwordTxt = self.passTxt.get()
        if service:
            self.serviceLabel.config(fg='black')
        if username:
            self.unameLabel.config(fg='black')
        if passwordTxt:
            self.pwLabel.config(fg='black')
        if service and username and passwordTxt:
            # encrypt and store
            passwordEncrypted = self.encryptPassword(passwordTxt)
            try:
                storeDB(service, username, passwordEncrypted, self.user)
                self.loggedInUI()
            except:
                self.unameLabel.config(text='An account with this username \nalready exists for this service',fg='red')
                print('Key error')
        else:
            if not service:
                self.serviceLabel.config(fg='red')
            if not username:
                self.unameLabel.config(fg='red')
            if not passwordTxt:
                self.pwLabel.config(fg='red')
        
    def deleteEntry(self):
        service = self.serviceList.get()
        username = self.unameList.get()
        account = self.user
        deleteEntry(account,service,username)

        # delete input in entry boxes/combobox
        self.serviceList.delete(0,END)
        self.unameList.delete(0,END)
        self.showPass.delete(0,END)

        self.loggedInUI()

    def newEntryUI(self):
        self.clearWidgets()
        
        # Title
        self.title = Label(self, text='New Entry', font=('Century Gothic', 20))
        self.title.grid(row=0,columnspan=2, padx=10)

        # Version
        self.version = Label(self, text='© Warren Lim 2021 | version %s'%version,font=('Calibri', 8))
        self.version.grid(row=1,pady=(0,10),sticky='n',columnspan=2)

        # Service/Website
        self.serviceLabel = Label(self, text='Service/Website:', font=('Calibri',12))
        self.serviceLabel.grid(row=2,sticky='w',padx=10,columnspan=2)
        self.serviceEntry = Entry(self, width=35)
        self.serviceEntry.grid(row=3,padx=(30,0),pady=(0,10),columnspan=2,sticky='w')

        # Username
        self.unameLabel = Label(self, text='Username:', font=('Calibri',12))
        self.unameLabel.grid(row=4,sticky='w',padx=10,columnspan=2)
        self.uname = Entry(self, width=35)
        self.uname.grid(row=5,padx=(30,0),pady=(0,10),columnspan=2,sticky='w')

        # Password
        self.pwLabel = Label(self, text='Password:', font=('Calibri',12))
        self.pwLabel.grid(row=6,sticky='w',padx=10,columnspan=2)
        self.passTxt = Entry(self, width=28,show='\u2022') # show password as bullets
        self.passTxt.grid(row=7,pady=(0,10),padx=(30,0),columnspan=2,sticky='w')
        # Show password
        self.copyBut = Button(self,text='Show', command=lambda:self.show(self.passTxt), width=5,bg='#ffff80',relief=GROOVE)
        self.copyBut.grid(row=7,column=1,padx=(0,30),sticky='e')

        # Seperator
        self.line = Separator(self,orient='horizontal')
        self.line.grid(row=8,sticky='we',columnspan=2)

        # Cancel button
        self.createAccBut = Button(self,text='Cancel', command=self.newEntryCancel, width=15,bg='#ffff80',relief=GROOVE)
        self.createAccBut.grid(row=9,pady=10,padx=(20,0),sticky='w',columnspan=2)

        # Enter button
        self.loginBut = Button(self,text='Enter', command=self.addNew, width=15,bg='#ffff80',relief=GROOVE)
        self.loginBut.grid(row=9,column=1,pady=10,padx=(0,20),sticky='w')

        self.parent.bind('<Return>', self.addNewEnter) # bind enter to button

    def addNewEnter(self, event):
        # make enter key press Go button
        self.addNew()

    def newEntryCancel(self):
        self.clearWidgets()
        self.loggedInUI()

    def retrieve(self,event): # populates username dropdown
        service = self.service.get()
        self.records = retrieveDB(service,self.user)
        print(self.records)
        self.unameList.config(values=[i[1] for i in self.records]) # gets all usernames
        self.unameList.current(0)
        self.unameList.bind('<<ComboboxSelected>>', self.showPassword)
        self.unameList.event_generate('<<ComboboxSelected>>') # force event for default combobox value
    
    def showPassword(self,event): # shows password when username is selected
        current = self.unameList.current()
        if current != -1:
            i = current
            encryptedPass = self.records[i][2]

            # decrypt password
            key = self.createKey()
            f = Fernet(key)
            decryptedPass = f.decrypt(encryptedPass)
            passwordTxt = decryptedPass.decode()

            self.showPass.delete(0, END) # delete entries from previous runs
            self.showPass.insert(0,passwordTxt) # insert password

    def createKey(self):
        # create key from masterpass
        password = self.masterPassword.encode() + self.user.encode()
        salt = b'w\tN\xd8\xf1[k\x97\xc3=\xc9\x90k\xde\xe8\xad'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256,
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def editUI(self, service, username):
        
        if not service and not username:
            self.serviceLabel.config(fg='red')
            return

        self.clearWidgets()

        # Title
        self.title = Label(self, text='Edit Entry', font=('Century Gothic', 20))
        self.title.grid(row=0,columnspan=2, padx=10)

        # Version
        self.version = Label(self, text='© Warren Lim 2021 | version %s'%version,font=('Calibri', 8))
        self.version.grid(row=1,pady=(0,10),sticky='n',columnspan=2)

        # Service/Website
        self.serviceLabel = Label(self, text='Service/Website:', font=('Calibri',12))
        self.serviceLabel.grid(row=2,sticky='w',padx=10,columnspan=2)
        self.serviceEntry = Entry(self, width=35)
        self.serviceEntry.grid(row=3,padx=(30,0),pady=(0,10),columnspan=2,sticky='w')
        self.serviceEntry.insert(0,service)
        self.serviceEntry.config(state=DISABLED)

        # Username
        self.unameLabel = Label(self, text='Username:', font=('Calibri',12))
        self.unameLabel.grid(row=4,sticky='w',padx=10,columnspan=2)
        self.uname = Entry(self, width=35)
        self.uname.grid(row=5,padx=(30,0),pady=(0,10),columnspan=2,sticky='w')
        self.uname.insert(0,username)
        self.uname.config(state=DISABLED)

        # Password
        self.pwLabel = Label(self, text='Password:', font=('Calibri',12))
        self.pwLabel.grid(row=6,sticky='w',padx=10,columnspan=2)
        self.passTxt = Entry(self, width=28,show='\u2022') # show password as bullets
        self.passTxt.grid(row=7,pady=(0,10),padx=(30,0),columnspan=2,sticky='w')
        # Show password
        self.copyBut = Button(self,text='Show', command=lambda:self.show(self.passTxt), width=5,bg='#ffff80',relief=GROOVE)
        self.copyBut.grid(row=7,column=1,padx=(0,30),sticky='e')

        # Seperator
        self.line = Separator(self,orient='horizontal')
        self.line.grid(row=8,sticky='we',columnspan=2)

        # Cancel button
        self.createAccBut = Button(self,text='Cancel', command=self.newEntryCancel, width=15,bg='#ffff80',relief=GROOVE)
        self.createAccBut.grid(row=9,pady=10,padx=(20,0),sticky='w',columnspan=2)

        # Enter button
        self.loginBut = Button(self,text='Enter', command=lambda:self.editEntry(service,username,self.passTxt.get()), width=15,bg='#ffff80',relief=GROOVE)
        self.loginBut.grid(row=9,column=1,pady=10,padx=(0,20),sticky='w')

        self.parent.bind('<Return>', self.editEntry) # bind enter to button

    def editEntry(self,service,username,password):
        account = self.user
        if service and username and password:
            encryptedPassword = self.encryptPassword(password)
            updateDB(account,service,username,encryptedPassword)
        else:
            if not password:
                self.serviceLabel.config(fg='red')
        self.loggedInUI()


def main():
    root = tk.Tk()
    root.iconbitmap('img/keyicon.ico')
    app = GUI(root)
    root.mainloop()  


if __name__ == '__main__':
    main()    