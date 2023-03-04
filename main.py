import customtkinter as ctk
import tkinter as tk
from tkinter.filedialog import askopenfilename
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
        # self.geometry("380x430+700+260")
        self.geometry('900x700+380+50')
        # self.overrideredirect(True)
        self.title("Lost and Found")
        self.iconbitmap(True,'magnifyingglass_102622.ico')
        self.resizable(False,False)

        # add widgets to app

        self.loginFrame = LoginFrame(master=self, corner_radius=30)
        # self.loginFrame.pack(pady=30)
        self.mainFrame = MainFrame(self, fg_color='darkgray', corner_radius=0, Font=self.myFont)
        self.mainFrame.pack()
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
        self.choice = "Date Found"

        self.searchFrame = SearchBarFrame(self, corner_radius=0, width=400, Font=Font)
        self.searchFrame.grid(row=0,column=0,padx=5,pady=5,sticky='nsew')
        self.listFrame = ListFrame(self, width=430, height=580, corner_radius=0, Font=Font)
        self.listFrame.grid(row=1,column=0,padx=5,pady=(0,5),sticky='nsew')
        self.detailFrame = DetailFrame(self, width=440, height=690, corner_radius=0, Font=Font)
        self.detailFrame.grid(row=0,column=1,rowspan=2,padx=(0,5),pady=5,sticky='nsew')

    def comboboxCallback(self,choice):
        self.choice = choice
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

    def changeItemList(self,name):
        if name == "":
            self.listFrame.unpack()
            self.listFrame.buttonPack(self.listFrame.itemList)
        else:
            newItemList = searchItem(name)
            self.listFrame.unpack()
            self.listFrame.buttonPack(newItemList)


class SearchBarFrame(ctk.CTkFrame): # Width = 400px, Height = 350px
    def __init__(self, master, Font, **kwargs):
        super().__init__(master, **kwargs)
        self.searchBar = ctk.CTkEntry(self, corner_radius=7,width=275, placeholder_text='lost item name', font=Font)
        self.searchBar.grid(row=0,column=0,columnspan=2,padx=10,pady=(10,0))
        self.sortingCategory = ctk.CTkComboBox(self, values=['Date Found', 'Location Found', 'Category'], width=110, font=Font, command=master.comboboxCallback)
        self.sortingCategory.grid(row=0,column=2,padx=(0,10),pady=(10,0))
        self.searchButton = ctk.CTkButton(self,text='Search', font=Font, command=lambda : master.changeItemList(self.searchBar.get()))
        self.searchBar.bind("<Return>", lambda m :master.changeItemList(self.searchBar.get()))
        self.searchButton.grid(row=1,column=0,sticky="w",padx=10,pady=10)
        self.addButton = ctk.CTkButton(self, text="+ Add Lost Item", font=Font, command=master.addItem)
        self.addButton.grid(row=1,column=1,padx=5)
        self.sortOption = ctk.CTkLabel(self, text='^ Sort option', font=Font)
        self.sortOption.grid(row=1,column=2,padx=5)


class DetailFrame(ctk.CTkFrame): 
    def __init__(self, master, Font, **kwargs):
        super().__init__(master, **kwargs)
        self.Font = Font

        self.image = ctk.CTkLabel(self, width=380, text = "")
        self.image.pack(side='top', padx=0, pady=5)
        self.name = ctk.CTkLabel(self, width=440, font=self.Font, text="",anchor='w')
        self.name.pack(side='top',fill='x', padx=0, pady=5)
        self.category = ctk.CTkLabel(self, width=440, font=self.Font, text="",anchor='w')
        self.category.pack(side='top',fill='x', padx=0, pady=5)
        self.dateFound = ctk.CTkLabel(self, width=440, font=self.Font,text="",anchor='w')
        self.dateFound.pack(side='top',fill='x', padx=0, pady=5)
        self.locationFound = ctk.CTkLabel(self, width=440, font=self.Font, text="",anchor='w')
        self.locationFound.pack(side='top',fill='x', padx=0, pady=5)
        self.detail = ctk.CTkLabel(self, width=440, font=self.Font, text="",anchor='w')
        self.detail.pack(side='top',fill='x', padx=0, pady=5)

    def update(self,name,cat,date,loc,detail,image):
        self.name.configure(text=f"          Item name: {name}")
        self.category.configure(text=f"          Category: {cat}")
        self.dateFound.configure(text=f"          Date found: {date}")
        self.locationFound.configure(text=f"          Location found: {loc}")
        self.detail.configure(text=f"          Details: {detail}")
        if image != '':
            self.image.configure(text="")
            rawImg=Image.open(image)
            wpercent = (380/float(rawImg.size[0]))
            hsize = int((float(rawImg.size[1])*float(wpercent)))
            rawImg = rawImg.resize((380,hsize), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(rawImg)
            self.image.configure(image=img)
        else:
            self.image.configure(image="")
            self.image.configure(text="No image available")
            self.image.configure(fg_color='lightgray')


class ListFrame(ctk.CTkScrollableFrame): # scrollable, width 400px
    def __init__(self, master, Font, **kwargs):
        super().__init__(master, **kwargs)
        self.Font = Font
        self.itemList = listItemDate()
        self.master = master
        self.count = 0

        self.fieldName = ctk.CTkLabel(self,text="  ItemName    |    Category    |     Date     |    Location", font=self.Font, anchor='w')
        self.fieldName.pack(side='top', fill='x', padx=0)

        self.buttonArray = self.createButtonArray(master)
        self.buttonPack(self.itemList)

        
    def createButtonArray(self,master):
        buttonArray = []
        for i in self.itemList:
            buttonArray.append([ctk.CTkButton(self,text=self.format(i[1],i[2],i[3],i[4]), font=self.Font, border_width=2, fg_color='white', text_color='black', anchor='w', command=lambda m=self.count:master.itemClicked(m)), i[0]])
            self.count += 1
        return buttonArray
    
    # def addButton(self):
        # self.buttonArray.append([ctk.CTkButton(self,text=self.format(i[1],i[2],i[3],i[4]), font=self.Font, border_width=2, fg_color='white', text_color='black', anchor='w', command=lambda m=self.count:self.master.itemClicked(m)), i[0]])
    
    def unpack(self):
        for i in self.buttonArray:
            i[0].pack_forget()

    def buttonPack(self,newItemList):
        for i in newItemList:
            for j in self.buttonArray:
                if i[0] == j[1]:
                    j[0].pack(side='top', fill='x')

    def format(self,name,category,date,location):
        spaceNum = int((15-len(name) + ((15-len(name)) % 2))/2)
        nameString = " "*spaceNum + name + " "*spaceNum 
        spaceNum = int((18-len(category) + ((18-len(category)) % 2))/2)
        catString = " "*spaceNum + category + " "*spaceNum 
        spaceNum = int((12-len(date) + ((12-len(date)) % 2))/2)
        dateString = " "*spaceNum + date + " "*spaceNum 
        spaceNum = int((10-len(location) + ((10-len(location)) % 2))/2)
        locString = " "*spaceNum + location
        return nameString + catString + dateString + locString

class AddItemWindow(ctk.CTkToplevel):
    def __init__(self, master, Font, **kwargs):
        super().__init__(master, **kwargs)
        self.geometry("380x430+700+260")
        self.resizable(False,False)
        self.title("Add Lost Item")
        self.myFont = ctk.CTkFont(family="Consolas", size=15)
        self.imagepath = ''
        self.master =master

        self.nameLabel = ctk.CTkLabel(self,text="Name that best describe the item:", font=self.myFont)
        self.nameLabel.grid(row=0,column=0,sticky='w', padx=10)
        self.name = ctk.CTkEntry(self,placeholder_text="Name", width=360)
        self.name.grid(row=1,column=0,sticky='w', padx=10)
        self.catLabel = ctk.CTkLabel(self,text="Choose the category that best fit the item:", font=self.myFont)
        self.catLabel.grid(row=2,column=0,sticky='w',padx=10,pady=(10,0))
        self.category = ctk.CTkComboBox(self,values=['Clothing', 'Bag', 'Stationary', 'Sports Equipment', 'Electronics', 'Accessory', 'Shoes'], font=self.myFont)
        self.category.grid(row=3,column=0,sticky='w', padx=10)
        self.dateLabel = ctk.CTkLabel(self,text="Date that item was found (don't put 0 in front):", font=self.myFont)
        self.dateLabel.grid(row=4,column=0,sticky='w', padx=10, pady=(10,0))
        self.date = ctk.CTkEntry(self,placeholder_text="DD/MM/YYYY", width=360, font=self.myFont)
        self.date.grid(row=5,column=0,sticky='w', padx=10)
        self.locLabel = ctk.CTkLabel(self,text="Location that item was found:", font=self.myFont)
        self.locLabel.grid(row=6,column=0,sticky='w', padx=10, pady=(10,0))
        self.location = ctk.CTkComboBox(self,values=['SB', 'SC', 'PAC', 'WEC', 'CGA', 'Dining hall', 'Collingwood'], font=self.myFont)
        self.location.grid(row=7,column=0,sticky='w', padx=10)
        self.detailLabel = ctk.CTkLabel(self,text="Additional details on the item:", font=self.myFont)
        self.detailLabel.grid(row=8,column=0,sticky='w', padx=10, pady=(10,0))
        self.detail = ctk.CTkEntry(self, width=360, font=self.myFont)
        self.detail.grid(row=9,column=0,sticky='w', padx=10)
        self.addImageButton = ctk.CTkButton(self, text="Add image of item", font=self.myFont, command=self.storeImage)
        self.addImageButton.grid(row=10,column=0,sticky='w', padx=(10,0), pady=(10,0))
        self.addItemButton = ctk.CTkButton(self, text="Add item", font=self.myFont, command=self.addItemDatabase)
        self.addItemButton.grid(row=11,column=0, sticky = 'w', padx=10, pady=(10,0))

    def storeImage(self):
        root = tk.Tk()
        root.withdraw()
        fn = askopenfilename()
        root.destroy()
        img = cv2.imread(fn)
        print(fn)
        fileName = os.path.split(fn)[1]
        print(fileName)
        cv2.imwrite(r'D:/Users/Otsute/VScode/LostAndFound/LostAndFound/Images/' + fileName, img)
        self.imagepath = r'D:/Users/Otsute/VScode/LostAndFound/LostAndFound/Images/' + fileName

    def addItemDatabase(self):
        id = LastID()[0][0] +1
        addItem(id, self.name.get(), self.category.get(), self.date.get(), self.location.get(), self.detail.get(), self.imagepath)
        self.imagepath = ''
        self.destroy()

app = App()
app.mainloop()