import customtkinter as ctk
from datetime import datetime

class ErrorLog:
    """
    A class to manage and store error logs.

    Attributes:
        logs (list[dict]): List of dictionaries containing error information.
            Each dictionary has the following keys:
            - timestamp (str): Time when the error occurred
            - type (str): Type of the error
            - short_message (str): Brief error description
            - detailed_message (str): Detailed error information

    Methods:
        add_log: Adds a new error entry to the log with timestamp and provided information.
        get_logs: Returns all logged errors as a list of dictionaries.
        clear_logs: Removes all errors from the log, resetting it to empty state.
    """

    def __init__(self):
        self.logs: list[dict] = []
        
    def add_log(self, error_type: str, short_message: str, detailed_message: str) -> None:
        """
        Adds a new error entry to the log with the current timestamp.
        Creates a dictionary with error information and appends it to the logs list.

        Args:
            error_type (str): Type of the error (e.g., 'CSV Error', 'File Error', etc)
            short_message (str): Brief message for notification display
            detailed_message (str): Complete error message for the log
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.logs.append({
            "timestamp": timestamp,
            "type": error_type,
            "short_message": short_message,
            "detailed_message": detailed_message
        })
    
    def get_logs(self) -> list[dict]:
        """
        Retrieves all recorded error logs from the error tracking system.
        Provides access to the complete history of errors that have been logged.

        Returns:
            list[dict]: A list of dictionaries containing error logs
        """
        return self.logs
    
    def clear_logs(self) -> None:
        """
        Removes all recorded error logs from the system.
        Resets the log history to an empty state.
        """
        self.logs.clear()


class LogWindow(ctk.CTkToplevel):
    """
    A window to display error logs.
    Creates a top-level window with a text display for errors and a clear button.

    Attributes:
        error_log (ErrorLog): Instance containing the error logs to display
        log_text (ctk.CTkTextbox): Text widget to display the logs
        clear_button (ctk.CTkButton): Button to clear all logs

    Methods:
        update_log_display: Updates the text widget content with current logs from error_log instance.
        clear_logs: Clears all logs from error_log instance and updates the display.
    """

    def __init__(self, parent: ctk.CTk, error_log: ErrorLog) -> None:
        """
        Initializes the LogWindow with a parent window and an ErrorLog instance.

        Args:
            parent (ctk.CTk): The parent window
            error_log (ErrorLog): The ErrorLog instance to display and manage
        """
        super().__init__(parent, fg_color="#222831")
        self.title("Log de Erros")
        
        window_width = 600
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        
        self.lift()
        self.grab_set()
        
        self.error_log: ErrorLog = error_log
            
        self.log_text: ctk.CTkTextbox = ctk.CTkTextbox(
            self,
            width=580,
            height=350,
            font=("Consolas", 12)
        )
        self.log_text.pack(padx=10, pady=10)
        
        self.clear_button: ctk.CTkButton = ctk.CTkButton(
            self,
            text="Limpar Logs",
            font=("Tahoma", 14, "bold"),
            command=self.clear_logs,
            width=100,
            fg_color="#00ADB5",
            text_color="#EEEEEE",
            hover=False
        )
        self.clear_button.pack(pady=(0, 5))

        self.bind("<Escape>", lambda e: self.destroy())
        
        self.update_log_display()
    
    def update_log_display(self) -> None:
        """
        Updates the text display with the current error logs.
        Clears the existing display and shows either the logs or a message if no logs exist.
        Each log entry shows timestamp, type, message and details.
        """
        self.log_text.delete("1.0", "end")
        logs = self.error_log.get_logs()
        
        if not logs:
            self.log_text.insert("1.0", "Nenhum erro registrado.")
            return
        
        for log in logs:
            log_entry = (
                f"[{log['timestamp']}] {log['type']}\n"
                f"Mensagem: {log['short_message']}\n"
                f"Detalhes: {log['detailed_message']}\n"
                f"{'-' * 60}\n\n"
            )
            self.log_text.insert("end", log_entry)
    
    def clear_logs(self) -> None:
        """
        Clears all error logs from the system and updates the display.
        Removes all logs from the ErrorLog instance and refreshes the window to show empty state.
        """
        self.error_log.clear_logs()
        self.update_log_display()