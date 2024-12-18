from pathlib import Path
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
}

DATA_PATH = Path("data.csv")
EXTENSION_FIELDNAME = "Extensão do arquivo"
FILE_TYPE_FIELDNAME = "Tipo de arquivo"

def get_unique_file_name(destination_folder, original_name):
    stem = original_name.stem
    suffix = original_name.suffix
    new_name = original_name.name
    counter = 1

    while (destination_folder / new_name).exists():
        new_name = f"{stem}({counter}){suffix}"
        counter += 1
    return new_name

def dict_to_csv():
    try:
        with open("data.csv", "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([EXTENSION_FIELDNAME, FILE_TYPE_FIELDNAME])
            writer.writerows(DEFAULT_EXTENSION_TO_TYPE.items())
    except PermissionError:
        print("Permissão negada para escrever no arquivo CSV.")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar escrever no arquivo CSV: {e}")

def csv_to_dict():
    file_type_dict = {}
    try:
        with open(DATA_PATH, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                extension = row[EXTENSION_FIELDNAME].strip().lower()
                file_type = row[FILE_TYPE_FIELDNAME].strip()
                if extension and file_type:
                    file_type_dict[extension] = file_type
    except:
        print("Erro com o arquivo CSV. O arquivo será sobreescrito com os dados padrões.")
        dict_to_csv()
        with open(DATA_PATH, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                extension = row[EXTENSION_FIELDNAME].strip().lower()
                file_type = row[FILE_TYPE_FIELDNAME].strip()
                if extension and file_type:
                    file_type_dict[extension] = file_type
    return file_type_dict

def organize_folder():
    path = Path(input("Digite o caminho do diretório: "))

    file_type_dict = csv_to_dict()

    try:
        files = [file for file in path.iterdir() if file.is_file()]
    except FileNotFoundError:
        print("O Diretório fornecido não existe.")
    except NotADirectoryError:
        print("O Caminho especificado não leva a um diretório.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    else:
        for file in files:
            file_extension = file.suffix

            file_type = file_type_dict.get(file_extension.lower(), "Outros")
            
            if file_type:
                destination_folder = path / file_type
                destination_folder.mkdir(exist_ok=True)

                new_path = destination_folder / file.name

                try:
                    file.rename(new_path)
                except FileExistsError:
                    unique_name = get_unique_file_name(destination_folder, file)
                    new_path = destination_folder / unique_name
                    file.rename(new_path)
                except PermissionError:
                    print(f"Sem permissão para mover o arquivo {file}.")
                except Exception as e:
                    print(f"Ocorreu um erro ao tentar mover o arquivo {file}: {e}")

organize_folder()