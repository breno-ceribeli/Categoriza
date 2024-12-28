import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
from folder_organizer import FileOrganizer, DEFAULT_EXTENSION_TO_TYPE
import csv

BACKGROUND_COLOR = "#222831"
SECONDARY_COLOR = "#2E333C"
SCROLL_HOVER_COLOR = "#292E37"
ROW_COLOR = "#1A1E25"
SELECTED_ROW_COLOR = "#262A31"
TEXT_COLOR = "#FFFFFF"
BUTTONS_COLOR = "#1A1E25"

DATA_PATH = Path(__file__).parent / "data.csv"
EXTENSION_FIELDNAME = "Extensão do arquivo"
FILE_TYPE_FIELDNAME = "Tipo de arquivo"

class ScrollableTable(ctk.CTkFrame):
    """
    A custom scrollable table widget that extends CTkFrame.
    Creates a table with headers and scrollable content that can have selectable rows.

    Attributes:
        headers (list[str]): List of column headers for the table.
        data (list[tuple[str, str]]): List of tuples containing row data.
        row_height (int): Height of each table row in pixels.
        column_width (list[int]): List of widths for each column.
        selected_rows (set): Set containing indices of currently selected rows.
        canvas (ctk.CTkCanvas): Canvas widget for scrollable content.
        scrollbar (ctk.CTkScrollbar): Vertical scrollbar for table navigation.
        scrollable_frame (ctk.CTkFrame): Frame containing the table content.

    Methods:
        refresh_table: Rebuilds the table content with current data.
        toggle_selection: Toggles selection state of a specific row.
        get_selected_rows: Returns list of currently selected row indices.
        bind_mousewheel: Sets up mouse wheel scrolling functionality.
    """
    def __init__(self, parent: ctk.CTk, headers: list[str], data: list[tuple[str, str]], row_height: int = 30, column_width: list[int] = [200, 200]):
        """
        Initializes the ScrollableTable with specified dimensions and data.

        Args:
            parent (ctk.CTk): Parent window containing this widget
            headers (list[str]): List of column headers for the table
            data (list[tuple[str, str]]): List of tuples containing row data
            row_height (int, optional): Height of each table row. Defaults to 30.
            column_width (list[int], optional): List of column widths. Defaults to [200, 200].
        """
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)

        self.headers = headers
        self.data = data
        self.row_height = row_height
        self.column_width = column_width
        self.selected_rows = set()
        
        self.canvas = ctk.CTkCanvas(
            master=self,
            borderwidth=0,
            background=BACKGROUND_COLOR,
            highlightthickness=0
        )
        self.scrollbar = ctk.CTkScrollbar(
            master=self,
            orientation="vertical",
            command=self.canvas.yview,
            fg_color=BACKGROUND_COLOR,
            button_color=SECONDARY_COLOR,
            button_hover_color=SCROLL_HOVER_COLOR
        )
        self.scrollable_frame = ctk.CTkFrame(
            master=self.canvas,
            fg_color=BACKGROUND_COLOR
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        for col, header in enumerate(self.headers):
            header_label = ctk.CTkLabel(
                master=self.scrollable_frame,
                text=header,
                width=self.column_width[col],
                height=self.row_height,
                fg_color=SECONDARY_COLOR,
                text_color=TEXT_COLOR
            )
            header_label.grid(row=0, column=col, sticky="nsew")

        self.refresh_table()

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.bind_mousewheel()

    def refresh_table(self) -> None:
        """
        Rebuilds the table content with current data.
        Clears existing rows and recreates them with current data.
        Sets up row selection bindings and styling for each row.
        """
        for widget in self.scrollable_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        for row, (col1, col2) in enumerate(self.data, start=1):
            if col1 != "others":
                row_frame = ctk.CTkFrame(
                    self.scrollable_frame,
                    fg_color=ROW_COLOR
                )
                row_frame.grid(row=row, column=0, columnspan=2, sticky="nsew")
                
                ctk.CTkLabel(
                    row_frame,
                    text=col1,
                    width=self.column_width[0],
                    height=self.row_height,
                    text_color=TEXT_COLOR
                ).grid(row=0, column=0)
                
                ctk.CTkLabel(
                    row_frame,
                    text=col2,
                    width=self.column_width[1],
                    height=self.row_height,
                    text_color=TEXT_COLOR
                ).grid(row=0, column=1)

                row_frame.bind("<Button-1>", lambda e, r=row: self.toggle_selection(r))
                for widget in row_frame.winfo_children():
                    widget.bind("<Button-1>", lambda e, r=row: self.toggle_selection(r))

    def toggle_selection(self, row_index: int) -> None:
        """
        Toggles selection state of a specific row.
        Changes row background color and updates selected_rows set.

        Args:
            row_index (int): Index of the row to toggle selection
        """
        row_frame = self.scrollable_frame.grid_slaves(row=row_index)[0]
        
        if row_index in self.selected_rows:
            self.selected_rows.remove(row_index)
            row_frame.configure(fg_color=ROW_COLOR)
        else:
            self.selected_rows.add(row_index)
            row_frame.configure(fg_color=SELECTED_ROW_COLOR)

    def get_selected_rows(self) -> list[int]:
        """
        Returns list of currently selected row indices.

        Returns:
            list[int]: Sorted list of selected row indices.
        """
        return sorted(list(self.selected_rows))

    def bind_mousewheel(self) -> None:
        """
        Sets up mouse wheel scrolling functionality.
        Binds mouse wheel events to scroll the table content when mouse is over the table area.
        """
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        self.canvas.bind("<Enter>", bind_to_mousewheel)
        self.canvas.bind("<Leave>", unbind_from_mousewheel)


class DataManager:
    """
    A class to manage data persistence and operations for file extension mappings.

    Attributes:
        filename (Path): Path to the CSV file storing extension mappings.
        headers (list[str]): Column headers for the CSV file.
        data (list[tuple[str, str]]): List of tuples containing extension mappings.

    Methods:
        load_data: Loads extension mappings from CSV file or defaults.
        save_data: Saves current extension mappings to CSV file.
        extension_exists: Checks if an extension already exists in mappings.
        update_others_value: Updates the default value for unmapped extensions.
        add_item: Adds a new extension mapping.
        edit_item: Modifies an existing extension mapping.
        delete_items: Removes selected extension mappings.
    """
    def __init__(self):
        """
        Initializes DataManager and loads initial data.
        Sets up file path and headers, then loads data from file or defaults.
        """
        self.filename = DATA_PATH
        self.headers = [EXTENSION_FIELDNAME, FILE_TYPE_FIELDNAME]
        self.load_data()

    def load_data(self) -> None:
        """
        Loads extension mappings from CSV file or defaults.
        Creates new data with defaults if file doesn't exist, otherwise reads mappings from CSV file.
        """
        if not self.filename.exists():
            file_organizer = FileOrganizer()
            self.data = list(DEFAULT_EXTENSION_TO_TYPE.items())
            del file_organizer
        else:
            self.data = []
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    self.data.append(tuple(row))
        

    def save_data(self) -> None:
        """
        Saves current extension mappings to CSV file.
        Writes current headers and data to the CSV file.
        """
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)
            writer.writerows(self.data)

    def extension_exists(self, extension: str) -> bool:
        """
        Checks if an extension already exists in mappings.
        Case-insensitive comparison of extensions.

        Args:
            extension (str): File extension to check

        Returns:
            bool: True if extension exists, False otherwise
        """
        return any(ext.lower() == extension.lower() for ext, _ in self.data)

    def update_others_value(self, new_value: str) -> None:
        """
        Updates the default value for unmapped extensions.
        Updates the 'others' type mapping and saves changes.

        Args:
            new_value (str): New default type for unmapped extensions.
        """
        for i, (ext, type_) in enumerate(self.data):
            if ext == "others":
                self.data[i] = ("others", new_value)
                break
        self.save_data()

    def add_item(self, item: str, value: str) -> None:
        """
        Adds a new extension mapping.
        Validates extension doesn't exist before adding.

        Args:
            item (str): File extension to add.
            value (str): File type for the extension.

        Raises:
            ValueError: If extension already exists.
        """
        if self.extension_exists(item):
            raise ValueError("Esta extensão já existe!")
        self.data.append((item, value))
        self.save_data()

    def edit_item(self, index: int, value: str) -> None:
        """
        Modifies an existing extension mapping.
        Updates type for specified extension and saves changes.

        Args:
            index (int): Index of mapping to modify.
            value (str): New file type value.
        """
        self.data[index - 1] = (self.data[index - 1][0], value)
        self.save_data()

    def delete_items(self, indices: list[int]) -> None:
        """
        Removes selected extension mappings.
        Deletes mappings at specified indices and saves changes.

        Args:
            indices (list[int]): List of indices to remove.
        """
        indices = sorted(indices, reverse=True)
        for index in indices:
            del self.data[index - 1]
        self.save_data()


class SettingsFrame(ctk.CTkFrame):
    """
    A settings interface frame for managing file extension type mappings.
    Creates a window with a table and controls for viewing and editing mappings.

    Attributes:
        parent (ctk.CTk): Parent window containing this frame.
        control_frame (ctk.CTkFrame): Frame containing control buttons and inputs.
        default_entry_var (ctk.StringVar): Variable for default type input.
        default_entry (ctk.CTkEntry): Entry widget for default type.
        table (ScrollableTable): Table displaying extension mappings.
        data_manager (DataManager): Instance managing data operations.

    Methods:
        update_default_value: Updates the default type for unmapped extensions.
        restore_default: Resets all mappings to system defaults.
        show_add_dialog: Shows dialog for adding new extension mapping.
        show_edit_dialog: Shows dialog for editing selected mapping.
        delete_selected: Removes selected mappings after confirmation.
    """
    def __init__(self, parent: ctk.CTk):
        """
        Initializes the SettingsFrame with all controls and table.
        Sets up UI elements and loads initial data.

        Args:
            parent (ctk.CTk): Parent window containing this frame.
        """
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)
        
        self.parent = parent

        self.control_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.control_frame.place(relx=0.5, y=10, relwidth=0.98, anchor="n")

        self.default_label = ctk.CTkLabel(self.control_frame, text="Valor padrão:", text_color=TEXT_COLOR)
        self.default_label.pack(side="left", padx=(4, 2))

        self.default_entry_var = ctk.StringVar()
        self.default_entry = ctk.CTkEntry(self.control_frame, textvariable=self.default_entry_var, width=70, fg_color=BUTTONS_COLOR, text_color=TEXT_COLOR, border_width=1)
        self.default_entry.pack(side="left", padx=2)

        self.update_button = ctk.CTkButton(self.control_frame, text="Atualizar", command=self.update_default_value, fg_color=BUTTONS_COLOR, hover_color=SECONDARY_COLOR, text_color=TEXT_COLOR, width=54)
        self.update_button.pack(side="left", padx=5)

        self.action_buttons = [
            ("Restaurar", self.restore_default),
            ("Adicionar", self.show_add_dialog),
            ("Editar", self.show_edit_dialog),
            ("Excluir", self.delete_selected)
        ]
        
        for text, command in self.action_buttons:
            ctk.CTkButton(
                self.control_frame,
                text=text,
                command=command,
                fg_color=BUTTONS_COLOR,
                hover_color=SECONDARY_COLOR,
                text_color=TEXT_COLOR,
                width=54
            ).pack(side="left", padx=2)
        
        self.data_manager = DataManager()
        
        for ext, type in self.data_manager.data:
            if ext == "others":
                self.default_entry_var.set(type)
                break
        
        frame_padding = 10
        scrollbar_width = 20
        available_width = 500 - frame_padding - scrollbar_width
        column_width = available_width // 2

        self.table = ScrollableTable(self, headers=self.data_manager.headers, data=self.data_manager.data, row_height=30, column_width=[column_width, column_width])
        self.table.place(relx=0.5, y=60, relwidth=0.98, relheight=0.85, anchor="n")

    def update_default_value(self) -> None:
        """
        Updates the default file type for unmapped extensions.
        Validates input value is not empty before updating.
        Shows success message if update succeeds, warning if no value provided.
        """
        new_value = self.default_entry_var.get()
        if new_value:
            self.data_manager.update_others_value(new_value)
            messagebox.showinfo("Sucesso", "Valor padrão atualizado!")
        else:
            messagebox.showwarning("Aviso", "Digite um valor padrão!")

    def restore_default(self) -> None:
        """
        Restores all extension mappings to system defaults.
        Shows confirmation dialog before resetting.
        Updates table display after restore.
        """
        if messagebox.askyesno("Confirmar", "Deseja realmente restauras os dados padrão?"):
            DATA_PATH.unlink(missing_ok=True)
            file_organizer = FileOrganizer()
            self.data_manager.data = list(DEFAULT_EXTENSION_TO_TYPE.items())
            del file_organizer
            self.table.data = self.data_manager.data
            self.table.refresh_table()

    def show_add_dialog(self) -> None:
        """
        Displays dialog for adding new extension mapping.
        Creates a modal window with inputs for extension and type.
        Validates inputs and shows appropriate warnings.
        Updates table display after successful addition.
        """
        dialog = ctk.CTkToplevel(self.parent, fg_color=BACKGROUND_COLOR)
        dialog.title("Adicionar Item")
        APP_WIDTH = 250
        APP_HEIGHT = 220
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - APP_WIDTH) // 2
        y = (screen_height - APP_HEIGHT) // 2
        dialog.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Extensão:",
            text_color=TEXT_COLOR
        ).pack(pady=5)
        
        ext_entry = ctk.CTkEntry(
            dialog,
            fg_color=BUTTONS_COLOR,
            text_color=TEXT_COLOR,
            border_width=1
        )
        ext_entry.pack(pady=5)

        ctk.CTkLabel(
            dialog,
            text="Tipo:",
            text_color=TEXT_COLOR
        ).pack(pady=5)
        
        type_entry = ctk.CTkEntry(
            dialog,
            fg_color=BUTTONS_COLOR,
            text_color=TEXT_COLOR,
            border_width=1
        )
        type_entry.pack(pady=5)

        def add():
            ext = ext_entry.get()
            type = type_entry.get()
            if ext and type:
                try:
                    self.data_manager.add_item(ext, type)
                    self.table.data = self.data_manager.data
                    self.table.refresh_table()
                    dialog.destroy()
                except ValueError as e:
                    messagebox.showwarning("Aviso", str(e))
            else:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")

        ctk.CTkButton(
            dialog,
            text="Adicionar",
            command=add,
            fg_color=BUTTONS_COLOR,
            hover_color=SECONDARY_COLOR,
            text_color=TEXT_COLOR
        ).pack(pady=15)

    def show_edit_dialog(self) -> None:
        """
        Displays dialog for editing selected extension mapping.
        Validates exactly one row is selected before showing dialog.
        Shows current values and allows type modification.
        Updates table display after successful edit.
        """
        selected = self.table.get_selected_rows()
        if len(selected) != 1:
            messagebox.showwarning("Aviso", "Selecione exatamente um item para editar!")
            return

        row_index = selected[0]
        current_item = self.data_manager.data[row_index - 1]

        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Editar Item")
        APP_WIDTH = 250
        APP_HEIGHT = 170
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - APP_WIDTH) // 2
        y = (screen_height - APP_HEIGHT) // 2
        dialog.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(fg_color=BACKGROUND_COLOR)

        ctk.CTkLabel(
            dialog,
            text=f"Extensão: {current_item[0]}",
            text_color=TEXT_COLOR
        ).pack(pady=5)

        ctk.CTkLabel(
            dialog,
            text="Tipo:",
            text_color=TEXT_COLOR
        ).pack(pady=5)
        
        type_entry = ctk.CTkEntry(
            dialog,
            fg_color=BUTTONS_COLOR,
            text_color=TEXT_COLOR,
            border_width=1
        )
        type_entry.insert(0, current_item[1])
        type_entry.pack(pady=5)

        def edit():
            type = type_entry.get()
            if type:
                self.data_manager.edit_item(row_index, type)
                self.table.data = self.data_manager.data
                self.table.refresh_table()
                dialog.destroy()
            else:
                messagebox.showwarning("Aviso", "Preencha o campo de tipo!")

        ctk.CTkButton(
            dialog,
            text="Salvar",
            command=edit,
            fg_color=BUTTONS_COLOR,
            hover_color=SECONDARY_COLOR,
            text_color=TEXT_COLOR
        ).pack(pady=10)

    def delete_selected(self) -> None:
        """
        Removes selected extension mappings.
        Validates at least one row is selected.
        Shows confirmation dialog before deletion.
        Updates table display after successful removal.
        """
        selected = self.table.get_selected_rows()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione pelo menos um item para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir os itens selecionados?"):
            self.data_manager.delete_items(selected)
            self.table.data = self.data_manager.data
            self.table.selected_rows.clear()
            self.table.refresh_table()