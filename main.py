import customtkinter as ctk
import tkinter
import numpy
import cv2
import os
from Database import *
from PIL import ImageTk, Image

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('dark-blue')
button = 0


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.myFont = ctk.CTkFont(family="Consolas", size=13)
        self.geometry("380x430+700+260")
        # self.geometry('900x700+380+50')
        # self.overrideredirect(True)
        self.title("Lost and Found")
        self.iconbitmap(True,'magnifyingglass_102622.ico')
        self.resizable(False,False)

        # add widgets to app

        self.loginFrame = LoginFrame(master=self, corner_radius=30)
        self.loginFrame.pack(pady=30)
        self.mainFrame = MainFrame(self, fg_color='darkgray', corner_radius=0, Font=self.myFont)
        # self.mainFrame.pack()
        self.addWindow = None


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
        self.font = Font

        self.searchFrame = SearchBarFrame(self, corner_radius=0, width=400, Font=Font)
        self.searchFrame.grid(row=0,column=0,padx=5,pady=5,sticky='nsew')
        self.listFrame = ListFrame(self, width=430, height=580, corner_radius=0, Font=Font)
        self.listFrame.grid(row=1,column=0,padx=5,pady=(0,5),sticky='nsew')
        self.detailFrame = DetailFrame(self, width=440, height=690, corner_radius=0, Font=Font)
        self.detailFrame.grid(row=0,column=1,rowspan=2,padx=(0,5),pady=5,sticky='nsew')

    def comboboxCallback(self,choice):
        if choice == "Date Found":
            listItem = listItemDate()
            self.listFrame.unpack()
            self.listFrame.buttonPack(listItem)
        elif choice == "Location Found":
            listItem = listItemLocation()
            self.listFrame.unpack()
            self.listFrame.buttonPack(listItem)
        else:
            listItem = listItemCategory()
            self.listFrame.unpack()
            self.listFrame.buttonPack(listItem)

    def itemClicked(self, index):
        print(index)
        for i in self.listFrame.itemList:
            if i[0] == self.listFrame.buttonArray[index][1]:
                self.detailFrame.update(i[1], i[2], i[3], i[4], i[5], i[6])
    
    def addItem(self):
        if self.master.addWindow is None or not self.master.addWindow.winfo_exists():
            self.master.addWindow = AddItemWindow(self, self.font)  # create window if its None or destroyed
            self.master.addWindow.after(20, self.master.addWindow.lift)
        else:
            self.master.addWindow.focus()


        
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


class DetailFrame(ctk.CTkFrame): 
    def __init__(self, master, Font, **kwargs):
        super().__init__(master, **kwargs)
        self.Font = Font

        self.image = ctk.CTkLabel(self, width=440, text = "")
        self.image.pack(side='top',fill='x', padx=0, pady=5)
        self.name = ctk.CTkLabel(self, width=440, font=self.Font, text="")
        self.name.pack(side='top',fill='x', padx=0, pady=5)
        self.category = ctk.CTkLabel(self, width=440, font=self.Font, text="")
        self.category.pack(side='top',fill='x', padx=0, pady=5)
        self.dateFound = ctk.CTkLabel(self, width=440, font=self.Font,text="")
        self.dateFound.pack(side='top',fill='x', padx=0, pady=5)
        self.locationFound = ctk.CTkLabel(self, width=440, font=self.Font, text="")
        self.locationFound.pack(side='top',fill='x', padx=0, pady=5)
        self.detail = ctk.CTkLabel(self, width=440, font=self.Font, text="")
        self.detail.pack(side='top',fill='x', padx=0, pady=5)
        self.addButton = ctk.CTkButton(self, text="+ Add Lost Item", font=self.Font, height=50, command=master.addItem)
        self.addButton.pack(side='bottom', fill='x', pady=5, padx=5)

    def update(self,name,cat,date,loc,detail,image):
        self.name.configure(text=f"Item name: {name}")
        self.category.configure(text=f"Category: {cat}")
        self.dateFound.configure(text=f"Date found: {date}")
        self.locationFound.configure(text=f"Location found: {loc}")
        self.detail.configure(text=f"Details: {detail}")
        rawImg = Image.open(image)
        wpercent = (380/float(rawImg.size[0]))
        hsize = int((float(rawImg.size[1])*float(wpercent)))
        rawImg = rawImg.resize((380,hsize), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(rawImg)
        self.image.configure(image=img)


class ListFrame(ctk.CTkScrollableFrame): # scrollable, width 400px
    def __init__(self, master, Font, **kwargs):
        super().__init__(master, **kwargs)
        self.Font = Font
        self.itemList = listItemDate()

        self.fieldName = ctk.CTkLabel(self,text="  ItemName    |    Category    |     Date     |    Location", font=self.Font, anchor='w')
        self.fieldName.pack(side='top', fill='x', padx=0)

        self.buttonArray = self.createButtonArray(master)
        for i in self.buttonArray:
            i[0].pack(side='top',fill='x', pady=0)

        
    def createButtonArray(self,master):
        buttonArray = []
        count = 0
        for i in self.itemList:
            buttonArray.append([ctk.CTkButton(self,text=self.format(i[1],i[2],i[3],i[4]), font=self.Font, border_width=2, fg_color='white', text_color='black', anchor='w', command=lambda m=count:master.itemClicked(m)), i[0]])
            count += 1
        return buttonArray
    
    def unpack(self):
        for i in self.buttonArray:
            i[0].pack_forget()

    def buttonPack(self,newItemList):
        self.itemList = newItemList
        newButtonArray = self.buttonArray
        for i in self.itemList:
            for j in newButtonArray:
                if i[0] == j[1]:
                    j[0].pack(side='top', fill='x')

    def format(self,name,category,date,location):
        spaceNum = int((13-len(name) + ((13-len(name)) % 2))/2)
        nameString = " "*spaceNum + name + " "*spaceNum 
        spaceNum = int((15-len(category) + ((15-len(category)) % 2))/2)
        catString = " "*spaceNum + category + " "*spaceNum 
        spaceNum = int((12-len(date) + ((12-len(date)) % 2))/2)
        dateString = " "*spaceNum + date + " "*spaceNum 
        spaceNum = int((15-len(location) + ((15-len(location)) % 2))/2)
        locString = " "*spaceNum + location
        return nameString + catString + dateString + locString

class AddItemWindow(ctk.CTkToplevel):
    def __init__(self, master, Font, **kwargs):
        super().__init__(master, **kwargs)
        self.geometry("380x430+700+260")
        self.resizable(False,False)
        self.title("Add Lost Item")

        self.imageEntry = ctk.CTkEntry(self,placeholder_text="path to your image file", font=Font)
        self.imageEntry.bind('<Return>',lambda m:self.storeImage(self.imageEntry.get()))
        self.imageEntry.pack()

    def storeImage(self,filePath):
        fileName = os.path.split(filePath)[1]
        img = cv2.imread(filePath)
        print(fileName)
        cv2.imwrite(r'C:/Users/Tetsuo.Prac2023/Desktop/LostAndFound/Images/' + fileName, img)

app = App()
app.mainloop()