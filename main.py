import customtkinter as ctk
from Database import *

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('dark-blue')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("380x440")
        self.title("Lost and Found")
        self.iconbitmap('magnifyingglass_102622.ico')


        # add widgets to app
        self.loginFrame = LoginFrame(master=self)
        self.loginFrame.pack(pady=30)
        self.mainFrame = MainFrame(self)

        # add methods to app
        def afterLogin(self):
            pass

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._border_width = 5
        self._border_color = '#E9A93B'
        self._fg_color = '#092851'

        # add widgets onto the frame...
        self.label = ctk.CTkLabel(master=self, width=300, bg_color='#092851', text='LOGIN', font=('Stone Sans', 40), text_color='#E9A93B')
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=(50, 50), sticky="nsew")
        self.usernameL = ctk.CTkLabel(master=self, bg_color='#092851', text='Username', font=('Stone Sans', 20), text_color='#E9A93B')
        self.usernameL.grid(row=1, column=0, padx=(20,0), pady=15, sticky="nsew")
        self.passwordL = ctk.CTkLabel(master=self, bg_color='#092851', text='Password', font=('Stone Sans', 20), text_color='#E9A93B')
        self.passwordL.grid(row=2, column=0, padx=(20,0), pady=15, sticky="nsew")
        self.username = ctk.CTkEntry(self, corner_radius=7, border_color='black', width=150)
        self.username.grid(row=1, column=1, padx=(0,20), pady=15, sticky="nsew")
        self.password = ctk.CTkEntry(self, corner_radius=7, border_color='black', width=150)
        self.password.grid(row=2, column=1, padx=(0,20), pady=15, sticky="nsew")
        self.button = ctk.CTkButton(self, width=100, corner_radius=7, border_color='black', text='Login', fg_color='#E9A93B', text_color='black', command=lambda : login_clicked([self.username.get(), self.password.get()]))
        self.button.grid(row=3, column=0, columnspan=2, padx=20, pady=(20,0), sticky="nsew")
        self.warning = ctk.CTkLabel(self, bg_color='#092851', text='',font=('Stone Sans', 15), text_color='red')
        self.warning.grid(row=4, column=0,columnspan=2, padx=20, pady=(20,80), sticky="nsew")

def login_clicked(userAndPassword):
    if '' not in userAndPassword:
        if searchUser(userAndPassword[0], userAndPassword[1]) != []:
            print('invoked!')
            app.loginFrame.pack_forget()
            app.mainFrame.pack(pady=30)
            app.geometry(f'{app.winfo_screenwidth}x{app.winfo_screenheight}')
        else:
            app.loginFrame.warning.configure(text='Wrong username or password')
    else:
        app.loginFrame.warning.configure(text='Empty field')

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._width = 200


app = App()
app.mainloop()