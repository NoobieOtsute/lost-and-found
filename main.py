import customtkinter as ctk
import tkinter
from Database import *

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('dark-blue')



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.myFont = ctk.CTkFont(family="Consolas", size=12)
        # self.geometry("380x430+700+260")
        self.geometry('900x700+380+50')
        # self.overrideredirect(True)
        self.title("Lost and Found")
        self.iconbitmap('magnifyingglass_102622.ico')
        self.resizable(False,False)

        # add widgets to app

        self.loginFrame = LoginFrame(master=self, corner_radius=30)
        # self.loginFrame.pack(pady=30)
        self.mainFrame = MainFrame(self, fg_color='darkgray', corner_radius=0, Font=self.myFont)
        self.mainFrame.pack()


        # add methods to app

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._border_width = 5
        self._border_color = '#E9A93B'
        self._fg_color = '#092851'

        # add widgets onto the frame...
        self.label = ctk.CTkLabel(master=self, width=300, bg_color='#092851', text='SIGN IN', font=('Trebuchet MS bold', 40), text_color='#E9A93B')
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=(40, 40), sticky="nsew")
        self.usernameL = ctk.CTkLabel(master=self, bg_color='#092851', text='Username', font=('Trebuchet MS', 17), text_color='#E9A93B')
        self.usernameL.grid(row=1, column=0, padx=(20,0), pady=15, sticky="nsew")
        self.passwordL = ctk.CTkLabel(master=self, bg_color='#092851', text='Password', font=('Trebuchet MS', 17), text_color='#E9A93B')
        self.passwordL.grid(row=2, column=0, padx=(20,0), pady=15, sticky="nsew")
        self.username = ctk.CTkEntry(self, corner_radius=7, border_color='black', width=150)
        self.username.grid(row=1, column=1, padx=(0,20), pady=15, sticky="nsew")
        self.username.focus_set()
        self.username.bind('<Return>',self.changeFocus)
        self.username.bind('<Down>',self.changeFocus)
        self.password = ctk.CTkEntry(self, corner_radius=7, border_color='black', width=150)
        self.password.grid(row=2, column=1, padx=(0,20), pady=15, sticky="nsew")
        self.password.bind('<Return>',lambda x: login_clicked([self.username.get(), self.password.get()]))
        self.password.bind('<Up>',self.focusUsername)
        self.button = ctk.CTkButton(self, width=100, corner_radius=7, border_color='black', text='Login', fg_color='#E9A93B', text_color='black', command=lambda : login_clicked([self.username.get(), self.password.get()]))
        self.button.grid(row=3, column=0, columnspan=2, padx=20, pady=(20,0), sticky="nsew")
        self.exitbutton = ctk.CTkButton(self, width=75, corner_radius=7, border_color='black', text='exit', fg_color='#E9A93B', text_color='black', command=close)
        self.exitbutton.grid(row=4,column=0,padx=(20,10),pady=(20,40), sticky='w')
        self.warning = ctk.CTkLabel(self, bg_color='#092851', text='',font=('Trebuchet MS', 15), text_color='red')
        self.warning.grid(row=4, column=1, padx=(0,20), pady=(20,40), sticky="nw")
        
    def changeFocus(self,name):
        self.password.focus_set()

    def focusUsername(self,name):
        self.username.focus_set()
def login_clicked(userAndPassword):
    if '' not in userAndPassword:
        if searchUser(userAndPassword[0], userAndPassword[1]) != []:
            print('invoked!')
            app.loginFrame.pack_forget()
            app.mainFrame.pack()
            app.geometry('900x700+380+50') # Main window size
            
        else:
            app.loginFrame.warning.configure(text='Wrong username or password')
    else:
        app.loginFrame.warning.configure(text='Empty field')

def close():
    app.destroy()

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, Font, **kwargs):
        super().__init__(master, **kwargs)
        
        self.searchFrame = SearchBarFrame(self, corner_radius=0, width=400, Font=Font)
        self.searchFrame.grid(row=0,column=0,padx=5,pady=5,sticky='nsew')
        self.listFrame = ListFrame(self, width=400, height=580, corner_radius=0, Font=Font)
        self.listFrame.grid(row=1,column=0,padx=5,pady=(0,5),sticky='nsew')
        self.detailFrame = DetailFrame(self, width=470, height=690, corner_radius=0, Font=Font)
        self.detailFrame.grid(row=0,column=1,rowspan=2,padx=(0,5),pady=5,sticky='nsew')

    def comboboxCallback(self,choice):
        # if choice == "Date Found":
        pass


        
class SearchBarFrame(ctk.CTkFrame): # Width = 400px, Height = 350px
    def __init__(self, master, Font, **kwargs):
        super().__init__(master, **kwargs)
        self.searchBar = ctk.CTkEntry(self, corner_radius=7,width=250, placeholder_text='lost item name', font=Font)
        self.searchBar.grid(row=0,column=0,padx=10,pady=(10,0))
        self.sortingCategory = ctk.CTkComboBox(self, values=['Date Found', 'Location Found', 'Category'], width=110, font=Font, command=master.comboboxCallback)
        self.sortingCategory.grid(row=0,column=1,padx=(0,10),pady=(10,0))
        self.list = ctk.CTkButton(self,text='Search', font=Font)
        self.list.grid(row=1,column=0,sticky="w",padx=10,pady=10)
        self.sortOption = ctk.CTkLabel(self, text='^ Sort option', font=Font)
        self.sortOption.grid(row=1,column=1,padx=5)


class DetailFrame(ctk.CTkFrame): # Width = 450px, Height = 500px
    def __init__(self, master, Font, **kwargs):
        super().__init__(master, **kwargs)
        self.Font = Font




class ListFrame(ctk.CTkScrollableFrame): # scrollable, width 400px
    def __init__(self, master, Font, itemList=[], **kwargs):
        super().__init__(master, **kwargs)
        self.Font = Font
        self.itemList = itemList


        self.fieldName = ctk.CTkLabel(self,text="  Item Name    |    Category    |     Date     |    Location", font=self.Font, anchor='w')
        self.fieldName.pack(side='top', fill='x', padx=0)

        self.buttonArray = self.createButtonArray(listItemCategory())
        for i in self.buttonArray:
            i[0].pack(side='top',fill='x', pady=0)

        
    def createButtonArray(self,itemList):
        buttonArray = []
        for i in itemList:
            buttonArray.append([ctk.CTkButton(self,text=self.format(i[0],i[1],i[2],i[3]), font=self.Font, border_width=2, fg_color='white', text_color='black', anchor='w'), i[0]])
        return buttonArray
    
    def unpack(self,buttonArray):
        for i in buttonArray:
            i[0].pack_forget()

    def buttonPack(self,buttonArray,newItemList):
        newButtonArray = buttonArray
        for i in newItemList:
            for j in newButtonArray:
                if i[0] == j[1]:
                    j[0].pack(side='top', fill='x')
                    newButtonArray.remove(j)

    def format(self,name,category,date,location):
        spaceNum = int((15-len(name) + ((15-len(name)) % 2))/2)
        print(spaceNum, 13-len(name), 13-len(name)%2)
        nameString = " "*spaceNum + name + " "*spaceNum 
        spaceNum = int((15-len(category) + ((15-len(category)) % 2))/2)
        catString = " "*spaceNum + category + " "*spaceNum 
        spaceNum = int((12-len(date) + ((12-len(date)) % 2))/2)
        dateString = " "*spaceNum + date + " "*spaceNum 
        spaceNum = int((15-len(location) + ((15-len(location)) % 2))/2)
        locString = " "*spaceNum + location
        return nameString + catString + dateString + locString

        
        

app = App()
app.mainloop()