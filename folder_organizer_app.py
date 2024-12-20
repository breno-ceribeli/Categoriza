import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

BACKGROUND_COLOR = "#222831"
SECONDARY_COLOR = "#EEEEEE"
CONTRAST_COLOR = "#00ADB5"
TEXT_COLOR = "#393E46"
TITLE_HEX_COLOR = 0x00312822 # Win 11

APP_WIDTH = 500
APP_HEIGHT = 500

ICO_IMAGE = "images/empty.ico"
FOLDER_ICON = "images/folder_icon.png"
FOLDER_ICON_HOVER = "images/folder_icon_hover.png"


class App(ctk.CTk):

    def __init__(self):
        super().__init__(fg_color=BACKGROUND_COLOR)
        self.title("")
        self.iconbitmap(ICO_IMAGE)
        display_width = self.winfo_screenwidth()
        display_height = self.winfo_screenheight()

        left = int(display_width / 2 - 500 / 2)
        top = int(display_height / 2 - 500 / 2)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{left}+{top}")
        self.resizable(False, False)
        self.change_title_bar_color()

        self.entry_font = ctk.CTkFont(family="Dubai", size=14)
        self.buttons_font = "Tahoma"

        self.folder_path = ctk.StringVar()

        path_frame = PathFrame(self, self.entry_font, self.folder_path)
        path_frame.place(relx=0.5, rely=0.52, anchor="center")

        buttons_frame = ButtonsFrame(self, self.buttons_font, self.folder_path)
        buttons_frame.place(relx=0.5, rely=0.59, relheight=0.36, anchor="n")

        self.mainloop()
    
    def change_title_bar_color(self): # Win 11
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass


class PathFrame(ctk.CTkFrame):

    def __init__(self, parent, font, folder_path):
        super().__init__(
            master=parent,
            fg_color=SECONDARY_COLOR,
            corner_radius=15,
            width=360,
            height=35
        )

        self.folder_path = folder_path

        self.path_entry = ctk.CTkEntry(
            master=self,
            textvariable=self.folder_path,
            width=320,
            height=25,
            corner_radius=15,
            fg_color=SECONDARY_COLOR,
            bg_color=SECONDARY_COLOR,
            border_width=0,
            text_color=TEXT_COLOR,
            font=font
        )
        self.path_entry.place(relx=0.02, rely=0.5, anchor="w")

        self.normal_image = ctk.CTkImage(
            light_image=Image.open(FOLDER_ICON),
            dark_image=Image.open(FOLDER_ICON),
            size=(16, 16)
        )
        
        self.hover_image = ctk.CTkImage(
            light_image=Image.open(FOLDER_ICON_HOVER),
            dark_image=Image.open(FOLDER_ICON_HOVER),
            size=(16, 16)
        )

        self.folder_icon = ctk.CTkLabel(
            master=self,
            text="",
            image=self.normal_image,
            width=18,
            height=18,
            fg_color=SECONDARY_COLOR,
            cursor="hand2"
        )
        self.folder_icon.place(relx=0.95, rely=0.5, anchor="e")
        
        self.folder_icon.bind("<Button-1>", self.open_folder)
        self.folder_icon.bind("<Enter>", self.on_hover)
        self.folder_icon.bind("<Leave>", self.on_leave)

    def open_folder(self, event):
        folder_selected = filedialog.askdirectory(title="Selecione uma Pasta")
        if folder_selected:
            self.folder_path.set(folder_selected)
        
    def on_hover(self, event):
        self.folder_icon.configure(image=self.hover_image)
        
    def on_leave(self, event):
        self.folder_icon.configure(image=self.normal_image)


class ButtonsFrame(ctk.CTkFrame):

    def __init__(self, parent, font, folder_path):
        super().__init__(
            master=parent,
            fg_color=BACKGROUND_COLOR,
        )

        self.folder_path = folder_path
        
        self.organize_button = ctk.CTkButton(
            master=self,
            text="Organizar",
            font=(font, 25, "bold"),
            text_color=TEXT_COLOR,
            width=200,
            height=57,
            fg_color=SECONDARY_COLOR,
            hover_color=CONTRAST_COLOR,
            corner_radius=10,
            command=self.organize_folder
        )
        self.organize_button.pack(expand=True)

        self.config_button = ctk.CTkButton(
            master=self,
            text="Configurações",
            font=(font, 18, "bold"),
            text_color=TEXT_COLOR,
            width=170,
            height=48,
            fg_color=SECONDARY_COLOR,
            hover_color=CONTRAST_COLOR,
            corner_radius=10,
            command=self.app_config
        )
        self.config_button.pack(expand=True)

        self.buttons = (self.organize_button, self.config_button)

        for button in self.buttons:
            button.bind("<Enter>", lambda e, btn=button: self.on_hover(btn))
            button.bind("<Leave>", lambda e, btn=button: self.on_leave(btn))

    def organize_folder(self):
        print("Organizado")
    
    def app_config(self):
        print("Abrindo configurações")
    
    def on_hover(self, button):
        button.configure(text_color=SECONDARY_COLOR, fg_color=CONTRAST_COLOR)
    
    def on_leave(self, button):
        button.configure(text_color=TEXT_COLOR, fg_color=SECONDARY_COLOR)

App()