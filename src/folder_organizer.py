from pathlib import Path
from sys import argv
import csv

DEFAULT_EXTENSION_TO_TYPE = {
    ".txt": "Texto", ".md": "Texto", ".csv": "Texto", ".log": "Texto",
    ".json": "Texto", ".xml": "Texto", ".yaml": "Texto", ".yml": "Texto", ".ini": "Texto",
    
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio", ".aac": "Audio",
    ".ogg": "Audio", ".wma": "Audio", ".m4a": "Audio", ".aiff": "Audio",
    
    ".mp4": "Video", ".mkv": "Video", ".avi": "Video", ".mov": "Video",
    ".wmv": "Video", ".flv": "Video", ".webm": "Video", ".mpeg": "Video", ".mpg": "Video",
    
    ".png": "Imagem", ".jpg": "Imagem", ".jpeg": "Imagem", ".gif": "Imagem",
    ".bmp": "Imagem", ".tiff": "Imagem", ".webp": "Imagem", ".svg": "Imagem", ".ico": "Imagem",
    
    ".pdf": "Documento", ".doc": "Documento", ".docx": "Documento",
    ".xls": "Documento", ".xlsx": "Documento", ".ppt": "Documento", ".pptx": "Documento",
    ".odt": "Documento", ".ods": "Documento", ".odp": "Documento",
    
    ".zip": "Compactado", ".rar": "Compactado", ".7z": "Compactado", ".tar": "Compactado",
    ".gz": "Compactado", ".bz2": "Compactado", ".xz": "Compactado", ".iso": "Compactado",
    
    ".py": "Codigo", ".java": "Codigo", ".c": "Codigo", ".cpp": "Codigo",
    ".js": "Codigo", ".ts": "Codigo", ".html": "Codigo", ".css": "Codigo",
    ".php": "Codigo", ".rb": "Codigo", ".go": "Codigo", ".rs": "Codigo", ".swift": "Codigo",
    
    ".exe": "Executavel", ".msi": "Executavel", ".bat": "Executavel",
    ".sh": "Executavel", ".app": "Executavel", ".jar": "Executavel",
    ".bin": "Executavel", ".cmd": "Executavel",

    "others": "Outros"
}

DATA_PATH = Path(__file__).parent.parent / "data.csv"
EXTENSION_FIELDNAME = "File extension"
FILE_TYPE_FIELDNAME = "File Type"

class FileOrganizer:
    """
    A class for organizing files in a directory based on their file extensions.

    This class provides functionality to:
    1. Read file extension mappings from a CSV file or use default mappings.
    2. Organize files in a specified directory into subdirectories based on their types.
    3. Handle file naming conflicts by creating unique file names.

    Attributes:
        file_type_dict (dict[str, str]): A dictionary mapping file extensions to file types.
        csv_error (str | None): An error message if there was an issue with the CSV file.

    Methods:
        get_unique_file_name: Generate a unique file name to avoid conflicts.
        dict_to_csv: Save the extension dictionary to the CSV file.
        csv_to_dict: Read the extension dictionary from the CSV file.
        organize_folder: Organize files in the specified directory.
    """

    def __init__(self):
        self.file_type_dict, self.csv_error = self.csv_to_dict()

    def get_unique_file_name(self, destination_folder: Path, original_name: Path) -> str:
        """
        Generate a unique file name to avoid conflicts in the destination folder.

        Args:
            destination_folder (Path): The folder where the file will be moved.
            original_name (Path): The original file name.

        Returns:
            str: A unique file name that doesn't exist in the destination folder.
        """
        stem = original_name.stem
        suffix = original_name.suffix
        new_name = original_name.name
        counter = 1

        while (destination_folder / new_name).exists():
            new_name = f"{stem}({counter}){suffix}"
            counter += 1
        return new_name

    def dict_to_csv(self) -> str | None:
        """
        Save the extension dictionary to the CSV file.
        
        Returns:
            str | None: Error message if there's an error, None otherwise
        """
        try:
            with open(DATA_PATH, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([EXTENSION_FIELDNAME, FILE_TYPE_FIELDNAME])
                writer.writerows(DEFAULT_EXTENSION_TO_TYPE.items())
            return None
        except PermissionError:
            return "Permissão negada para escrever no arquivo CSV. O arquivo padrão será utilizado."
        except Exception as e:
            return f"Ocorreu um erro ao tentar escrever no arquivo CSV: {e}\nO arquivo padrão será utilizado."

    def csv_to_dict(self) -> tuple[dict[str, str], str | None]:
        """
        Read the extension dictionary from the CSV file.
    
        Returns:
            tuple[dict[str, str], str | None]: A tuple containing:
                - dict[str, str]: Dictionary mapping file extensions to file types.
                - str | None: Error message if any, None otherwise.
        """
        file_type_dict = {}
        error_msg = None
        
        try:
            with open(DATA_PATH, "r", newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    extension = row[EXTENSION_FIELDNAME].strip().lower()
                    file_type = row[FILE_TYPE_FIELDNAME].strip()
                    if extension and file_type:
                        file_type_dict[extension] = file_type
        except FileNotFoundError:
            csv_error = self.dict_to_csv()
            return DEFAULT_EXTENSION_TO_TYPE, csv_error
        except:
            error_msg = "Erro com o arquivo CSV. O arquivo será sobreescrito com os dados padrões."
            csv_error = self.dict_to_csv()
            if csv_error:
                return DEFAULT_EXTENSION_TO_TYPE, csv_error
            return DEFAULT_EXTENSION_TO_TYPE, error_msg
                        
        return file_type_dict, error_msg

    def organize_folder(self, directory_path: str) -> tuple[bool, str | list[str]]:
        """
        Organize files in the specified directory.
        
        Args:
            directory_path (str): Path of the directory to be organized
        
        Returns:
        Tuple[bool, str | List[str]]: A tuple containing:
                - A boolean indicating the success of the operation.
                - A single error message or a list of error messages.
        """
        path = Path(directory_path)

        if not path.is_absolute():
            return False, "O Caminho fornecido não é absoluto."
        
        try:
            files = [file for file in path.iterdir() if file.is_file()]
        except FileNotFoundError:
            return False, "O Diretório fornecido não existe"
        except NotADirectoryError:
            return False, "O Caminho especificado não leva a um diretório"
        except Exception as e:
            return False, f"Ocorreu um erro: {e}"

        success = True
        errors = []
        for file in files:
            file_extension = file.suffix
            file_type = self.file_type_dict.get(file_extension.lower())
            
            if not file_type:
                file_type = self.file_type_dict.get("others", "Others")

            destination_folder = path / file_type
            destination_folder.mkdir(exist_ok=True)

            new_path = destination_folder / file.name

            try:
                file.rename(new_path)
            except FileExistsError:
                unique_name = self.get_unique_file_name(destination_folder, file)
                new_path = destination_folder / unique_name
                file.rename(new_path)
            except PermissionError:
                errors.append(f"Sem permissão para mover o arquivo {file}")
            except Exception as e:
                errors.append(f"Ocorreu um erro ao tentar mover o arquivo {file}: {e}")
        
        return success, errors

def main():
    """Main function for execution via command line"""
    organizer = FileOrganizer()
    
    if organizer.csv_error:
        print(organizer.csv_error)
    if len(argv) > 1:
        directory = argv[1]
    else:
        try:
            directory = input("Digite o caminho do diretório: ")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            exit(0)
    try:
        success, errors = organizer.organize_folder(directory)
        
        if success:
            if errors:
                print("\nOrganização concluída com alguns erros.\nErros encontrados:")
                for error in errors:
                    print(f"- {error}")
            else:
                print("\nOrganização concluída com sucesso!")

        else:
            print("\nA organização não pôde ser concluída.\nErro ocorrido:")
            print(f"- {errors}")
        
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        return
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()