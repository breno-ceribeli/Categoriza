import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from pathlib import Path
from folder_organizer import FileOrganizer
from error_log_window import *
from app_config import SettingsFrame
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

BACKGROUND_COLOR = "#222831"
SECONDARY_COLOR = "#EEEEEE"
CONTRAST_COLOR = "#00ADB5"
TEXT_COLOR = "#393E46"
TITLE_HEX_COLOR = 0x00312822

APP_WIDTH = 500
APP_HEIGHT = 500

ROOT_IMAGE_PATH = Path(__file__).parent / "images"
ICO_IMAGE = ROOT_IMAGE_PATH / "empty.ico"
WELCOME_IMAGE = ROOT_IMAGE_PATH / "welcome.png"
FOLDER_ICON = ROOT_IMAGE_PATH / "folder_icon.png"
FOLDER_ICON_HOVER = ROOT_IMAGE_PATH / "folder_icon_hover.png"
ERROR_ICON = ROOT_IMAGE_PATH / "error_icon.png"
ERROR_ICON_HOVER = ROOT_IMAGE_PATH / "error_icon_hover.png"
RETURN_ICON = ROOT_IMAGE_PATH / "return_icon.png"
RETURN_ICON_HOVER = ROOT_IMAGE_PATH / "return_icon_hover.png"


class App(ctk.CTk):
    """
    Main application class for the folder organizer GUI.

    This class sets up the main window and initializes all the necessary components
    for the folder organizer application.

    Attributes:
        entry_font (ctk.CTkFont): Font used for entry fields.
        buttons_font (str): Font used for buttons.
        welcome_label (ctk.CTkLabel): Label to display the welcome (logo) image.
        folder_path (ctk.StringVar): StringVar to store the selected folder path.
        path_frame (PathFrame): Frame containing path entry.
        error_log (ErrorLog): Instance of ErrorLog to manage error logging.
        buttons_frame (ButtonsFrame): Frame containing the main buttons.
        return_button (ctk.CTkLabel): Icon to return to the main interface.
        settings_frame (SettingsFrame): Frame containing the settings interface.

    Methods:
        change_title_bar_color: Changes the title bar color for Windows 11.
        place_main_interface: Places the main interface and removes the settings interface components.
        place_settings_interface: Places the settings interface and removes the main interface components.
    """
    def __init__(self):
        """
        Initializes the main application window and sets up all components.
        """
        super().__init__(fg_color=BACKGROUND_COLOR)
        self.title("")
        self.iconbitmap(ICO_IMAGE)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - APP_WIDTH) // 2
        y = (screen_height - APP_HEIGHT) // 2
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")
        self.resizable(False, False)
        self.change_title_bar_color()

        self.entry_font = ctk.CTkFont(family="Dubai", size=14)
        self.buttons_font = "Tahoma"

        welcome_image = ctk.CTkImage(
            light_image=Image.open(WELCOME_IMAGE),
            dark_image=Image.open(WELCOME_IMAGE),
            size=(400, 220)
        )

        self.welcome_label = ctk.CTkLabel(master=self, text="", image=welcome_image)
        self.welcome_label.place(y=25, relx=0.5, anchor="n")

        self.folder_path = ctk.StringVar()

        self.path_frame = PathFrame(self, self.entry_font, self.folder_path)
        self.path_frame.place(relx=0.5, rely=0.52, anchor="center")

        self.error_log = ErrorLog()

        self.buttons_frame = ButtonsFrame(self, self.buttons_font, self.folder_path, self.error_log)
        self.buttons_frame.place(relx=0.5, rely=0.59, relheight=0.36, anchor="n")

        CornerButtons(self, self.error_log)

        self.return_image = ctk.CTkImage(
            light_image=Image.open(RETURN_ICON),
            dark_image=Image.open(RETURN_ICON),
            size=(16, 16)
        )
        
        self.hover_return_image = ctk.CTkImage(
            light_image=Image.open(RETURN_ICON_HOVER),
            dark_image=Image.open(RETURN_ICON_HOVER),
            size=(16, 16)
        )

        self.return_icon = ctk.CTkLabel(
            master=self,
            text="",
            image=self.return_image,
            cursor="hand2"
        )
        
        self.return_icon.bind("<Button-1>", lambda e: self.place_main_interface())
        self.return_icon.bind("<Enter>", lambda e: self.return_icon.configure(image=self.hover_return_image))
        self.return_icon.bind("<Leave>", lambda e: self.return_icon.configure(image=self.return_image))

        self.mainloop()
    
    def change_title_bar_color(self) -> None:
        """
        Changes the title bar color for Windows 11.

        This method attempts to change the color of the application's title bar
        using Windows-specific API calls. It's designed to work on Windows 11.
        """
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass
    
    def place_main_interface(self) -> None:
        """
        Places the Main Interface and removes the Settings Frame.
        """
        self.path_frame.place(relx=0.5, rely=0.52, anchor="center")
        self.buttons_frame.place(relx=0.5, rely=0.59, relheight=0.36, anchor="n")
        self.welcome_label.place(y=25, relx=0.5, anchor="n")
        self.return_icon.place_forget()
        self.settings_frame.place_forget()
        del self.settings_frame

    def place_settings_interface(self) -> None:
        """
        Places the Settings Frame (Interface) and removes all Main Interface components.
        """
        self.path_frame.place_forget()
        self.buttons_frame.place_forget()
        self.welcome_label.place_forget()
        self.return_icon.place(relx=0.02, rely=0.01, anchor="nw")
        self.settings_frame = SettingsFrame(self)
        self.settings_frame.place(relx=0.5, y=40, relwidth=0.99, relheight=0.91, anchor="n")


class PathFrame(ctk.CTkFrame):
    """
    A custom frame for displaying and selecting a folder path.

    This class creates a frame containing an entry field to display the selected
    folder path and an icon button to open a folder selection dialog.

    Attributes:
        folder_path (ctk.StringVar): StringVar to store the selected folder path.
        path_entry (ctk.CTkEntry): Entry widget to display the selected path.
        normal_image (ctk.CTkImage): Normal state image for the folder icon.
        hover_image (ctk.CTkImage): Hover state image for the folder icon.
        folder_icon (ctk.CTkLabel): Label widget used as a clickable folder icon.

    Methods:
        open_folder: Opens a folder selection dialog and updates the path.
        on_hover: Changes the folder icon to its hover state.
        on_leave: Changes the folder icon back to its normal state.
    """
    def __init__(self, parent: ctk.CTk, font: ctk.CTkFont, folder_path: ctk.StringVar):
        """
        Initializes the PathFrame with the given parent, font, and folder path.

        Args:
            parent (ctk.CTk): The parent window.
            font (ctk.CTkFont): The font to be used for the path entry.
            folder_path (ctk.StringVar): The StringVar to store the selected folder path.
        """
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

    def open_folder(self, event) -> None:
        """
        Opens a folder selection dialog and updates the path.

        This method is called when the folder icon is clicked. It opens a folder
        selection dialog and updates the folder_path StringVar with the selected path.
        """
        folder_selected = filedialog.askdirectory(title="Selecione uma Pasta")
        if folder_selected:
            self.folder_path.set(folder_selected)
        
    def on_hover(self, event) -> None:
        """
        Changes the folder icon to its hover state.

        This method is called when the mouse enters the folder icon area.
        """
        self.folder_icon.configure(image=self.hover_image)
        
    def on_leave(self, event) -> None:
        """
        Changes the folder icon back to its normal state.

        This method is called when the mouse leaves the folder icon area.
        """
        self.folder_icon.configure(image=self.normal_image)


class ButtonsFrame(ctk.CTkFrame):
    """
    A custom frame containing the main action buttons for the application.

    This class creates a frame with buttons for organizing folders and accessing
    application settings. It also manages notifications and error logging.

    Attributes:
        parent (ctk.CTk): The parent window.
        folder_path (ctk.StringVar): StringVar containing the selected folder path.
        notification_manager (NotificationManager): Instance to manage notifications.
        error_log (ErrorLog): Instance to manage error logging.
        organize_button (ctk.CTkButton): Button to trigger folder organization.
        config_button (ctk.CTkButton): Button to access application settings.
        buttons (tuple): Tuple containing all buttons in this frame.

    Methods:
        organize_folder: Handles the folder organization process and error management.
        app_config: 
        on_hover: Changes button appearance on mouse hover.
        on_leave: Reverts button appearance when mouse leaves.
    """
    def __init__(self, parent: ctk.CTk, font: str, folder_path: ctk.StringVar, error_log: ErrorLog):
        """
        Initializes the ButtonsFrame with the given parent, font, folder path, and error log.

        Args:
            parent (ctk.CTk): The parent window.
            font (str): The font to be used for the buttons.
            folder_path (ctk.StringVar): The StringVar containing the selected folder path.
            error_log (ErrorLog): The ErrorLog instance for managing error logs.
        """
        super().__init__(
            master=parent,
            fg_color=BACKGROUND_COLOR,
        )

        self.parent = parent
        self.folder_path = folder_path
        self.notification_manager = NotificationManager(self.master)
        self.error_log = error_log

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

    def organize_folder(self) -> None:
        """
        Handles the folder organization process and error management.

        This method is called when the organize button is clicked. It creates a
        FileOrganizer instance, checks for CSV errors, validates the selected
        directory, and manages the folder organization process. It also handles
        error logging and notifications for various scenarios.
        """
        organizer = FileOrganizer()

        try:
            if organizer.csv_error:
                short_message = "Erro ao carregar arquivo CSV"
                self.error_log.add_log(
                    "CSV Error",
                    short_message,
                    organizer.csv_error
                )
                self.notification_manager.show_notification(
                    short_message,
                    message_type="warning",
                    duration=5000
                )

            directory = self.folder_path.get()
            if not directory:
                self.notification_manager.show_notification(
                    "Selecione uma pasta para organizar!",
                    message_type="error"
                )
                return

            success, errors = organizer.organize_folder(directory)

            if success:
                if errors:
                    for error in errors:
                        short_message = "Erro ao mover arquivo"
                        self.error_log.add_log(
                            "File Error",
                            short_message,
                            error
                        )
                    
                    self.notification_manager.show_notification(
                        f"Organização concluída com {len(errors)} erros. Verifique os logs.",
                        message_type="warning",
                        duration=5000
                    )
                else:
                    self.notification_manager.show_notification(
                        "Pasta organizada com sucesso!",
                        message_type="success"
                    )
            else:
                short_message = "Falha na organização"
                
                self.error_log.add_log(
                    "Critical Error",
                    short_message,
                    errors
                )
                
                self.notification_manager.show_notification(
                    f"{short_message}. Verifique os logs.",
                    message_type="error",
                    duration=5000
                )
                
        except Exception as e:
            short_message = "Erro inesperado"
            self.error_log.add_log(
                "Unexpected Error",
                short_message,
                str(e)
            )
            self.notification_manager.show_notification(
                f"{short_message}. Verifique os logs.",
                message_type="error",
                duration=5000
            )
    
    def app_config(self) -> None:
        self.parent.place_settings_interface()
    
    def on_hover(self, button: ctk.CTkButton) -> None:
        """
        Changes button appearance on mouse hover.

        This method is called when the mouse enters a button's area.

        Args:
            button (ctk.CTkButton): The button being hovered over.
        """
        button.configure(text_color=SECONDARY_COLOR, fg_color=CONTRAST_COLOR)
    
    def on_leave(self, button: ctk.CTkButton) -> None:
        """
        Reverts button appearance when mouse leaves.

        This method is called when the mouse leaves a button's area.

        Args:
            button (ctk.CTkButton): The button the mouse is leaving.
        """
        button.configure(text_color=TEXT_COLOR, fg_color=SECONDARY_COLOR)


class Notification(ctk.CTkFrame):
    """
    A custom frame for displaying notifications.

    This class creates a notification widget with customizable message,
    type (success, warning, error, info), and duration.

    Attributes:
        manager (NotificationManager): The manager handling this notification.
        colors (dict[str, str]): Dictionary mapping message types to color codes.
        indicator (ctk.CTkFrame): Colored indicator showing the message type.
        message (ctk.CTkLabel): Label displaying the notification message.
        close_button (ctk.CTkLabel): Button to manually close the notification.

    Methods:
        destroy_notification: Destroys the notification and reorganizes others.
    """
    def __init__(self, parent: ctk.CTk, manager: 'NotificationManager', message: str, message_type: str = "success", duration: int = 3000):
        """
        Initializes a Notification.

        Args:
            parent (ctk.CTk): The parent widget.
            manager (NotificationManager): The manager handling this notification.
            message (str): The message to be displayed in the notification.
            message_type (str, optional): The type of notification. Defaults to "success".
            duration (int, optional): Duration in milliseconds for the notification to remain visible. Defaults to 3000.
        """
        super().__init__(
            master=parent, 
            fg_color=BACKGROUND_COLOR, 
            corner_radius=10, 
            height=50,
            border_width=1,
            border_color=SECONDARY_COLOR
        )

        self.manager = manager

        self.colors = {
            "success": "#4BB543",
            "warning": "#FFB302",
            "error": "#DC3545",
            "info": "#00ADB5"
        }

        color = self.colors.get(message_type, self.colors["info"])

        self.indicator = ctk.CTkFrame(
            master=self,
            fg_color=color,
            width=4,
            height=40
        )
        self.indicator.place(relx=0.02, rely=0.5, anchor="w")

        self.message = ctk.CTkLabel(
            master=self,
            text=message,
            font=("Dubai", 14),
            text_color=SECONDARY_COLOR
        )
        self.message.place(relx=0.07, rely=0.5, anchor="w")

        self.close_button = ctk.CTkLabel(
            master=self,
            text="X",
            font=("Dubai", 14, "bold"),
            text_color=SECONDARY_COLOR,
            cursor="hand2",
            width=20
        )
        self.close_button.place(relx=0.95, rely=0.5, anchor="e")
        self.close_button.bind("<Button-1>", self.destroy_notification)

        if duration:
            self.after(duration, self.destroy_notification)

    def destroy_notification(self, event=None) -> None:
        """
        Destroys the notification and reorganizes remaining notifications.

        This method is called when the close button is clicked or when the
        notification's duration expires.
        """
        self.destroy()
        self.manager.reorganize_notifications()


class NotificationManager:
    """
    Manages the display of multiple notifications.

    This class handles the creation, placement, and removal of notifications
    in the application window.

    Attributes:
        master (ctk.CTk): The master window where notifications are displayed.
        notifications (list): List of active Notification instances.

    Methods:
        show_notification: Creates and displays a new notification.
        reorganize_notifications: Adjusts the position of active notifications.
    """
    def __init__(self, parent: ctk.CTk):
        """
        Initializes the NotificationManager with the given parent.

        Args:
            parent (ctk.CTk): The parent widget where notifications will be displayed.
        """
        self.master = parent
        self.notifications = []
        
    def show_notification(self, message: str, message_type: str = "success", duration: int | None = 3000) -> None:
        """
        Creates and displays a new notification.

        This method creates a new Notification instance, adds it to the list of
        active notifications, and reorganizes their positions.

        Args:
            message (str): The message to display in the notification.
            message_type (str): The type of notification (success, warning, error, info).
            duration (int | None): Duration in milliseconds for the notification to remain visible.
        """
        while len(self.notifications) >= 3:
            old_notification = self.notifications.pop(0)
            old_notification.destroy()

        notification = Notification(
            parent=self.master,
            manager=self,
            message=message,
            message_type=message_type,
            duration=duration
        )

        self.notifications.append(notification)
        self.reorganize_notifications()

    def reorganize_notifications(self) -> None:
        """
        Adjusts the position of active notifications.

        This method updates the position of all active notifications to ensure
        they are displayed in the correct order and location.
        """
        self.notifications = [n for n in self.notifications if n.winfo_exists()]
        
        base_y = 0.95
        for i, notification in enumerate(self.notifications):
            offset = (len(self.notifications) - 1 - i) * 0.06
            notification.place(relx=0.5, rely=base_y-offset, anchor="s", relwidth=0.7)


class CornerButtons:
    """
    Manages the corner buttons in the application window.

    This class creates and handles the functionality of buttons placed in the
    corner of the main application window.

    Attributes:
        parent (ctk.CTk): The parent window where the buttons are placed.
        error_log (ErrorLog): The ErrorLog instance for managing error logs.
        normal_image (ctk.CTkImage): The default image for the log button.
        hover_image (ctk.CTkImage): The hover state image for the log button.
        log_label (ctk.CTkLabel): The label acting as the log button.

    Methods:
        show_logs: Opens the log window to display error logs.
    """
    def __init__(self, parent: ctk.CTk, error_log: ErrorLog):
        """
        Initializes the CornerButtons.

        Args:
            parent (ctk.CTk): The parent widget where the buttons will be placed.
            error_log (ErrorLog): The ErrorLog instance for managing error logs.
        """
        self.parent = parent
        self.error_log = error_log

        self.normal_image = ctk.CTkImage(
            light_image=Image.open(ERROR_ICON),
            dark_image=Image.open(ERROR_ICON),
            size=(16, 16)
        )
        
        self.hover_image = ctk.CTkImage(
            light_image=Image.open(ERROR_ICON_HOVER),
            dark_image=Image.open(ERROR_ICON_HOVER),
            size=(16, 16)
        )
        
        self.log_label = ctk.CTkLabel(
            master=self.parent,
            text="",
            image=self.normal_image,
            cursor="hand2"
        )
        self.log_label.place(relx=0.98, rely=0.01, anchor="ne")
        
        self.log_label.bind("<Button-1>", lambda e: self.show_logs())
        self.log_label.bind("<Enter>", lambda e: self.log_label.configure(image=self.hover_image))
        self.log_label.bind("<Leave>", lambda e: self.log_label.configure(image=self.normal_image))

    def show_logs(self) -> None:
        """
        Opens the log window to display error logs.

        This method is called when the log button is clicked. It creates a new
        LogWindow instance to display the current error logs.
        """
        LogWindow(self.parent, self.error_log)


if __name__ == "__main__":
    app = App()