from pathlib import Path

FOLDER_FOR_FILE_TYPE = {
    "Texto": (".txt", ".md", ".csv", ".log", ".json", ".xml", ".yaml", ".yml", ".ini"),
    
    "Audio": (".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".aiff"),
    
    "Video": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg"),
    
    "Imagem": (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".ico"),
    
    "Documento": (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp"),
    
    "Compactado": (".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"),
    
    "Codigo": (".py", ".java", ".c", ".cpp", ".js", ".ts", ".html", ".css", ".php", ".rb", ".go", ".rs", ".swift"),
    
    "Executavel": (".exe", ".msi", ".bat", ".sh", ".app", ".jar", ".bin", ".cmd"),
    
    "Outros": (".dat", ".bak", ".tmp")
}

def get_unique_file_name(destination_folder, original_name):
    stem = original_name.stem
    suffix = original_name.suffix
    new_name = original_name.name
    counter = 1

    while (destination_folder / new_name).exists():
        new_name = f"{stem}({counter}){suffix}"
        counter += 1
    return new_name

path = Path(input("Digite o caminho do diretório: "))

files = [file for file in path.iterdir() if file.is_file()]

for file in files:
    file_extension = file.suffix
    file_type = None

    for folder, extensions in FOLDER_FOR_FILE_TYPE.items():
        if file_extension.lower() in extensions:
            file_type = folder
            break
    
    if file_type:
        destination_folder = path / file_type
        destination_folder.mkdir(exist_ok=True)

        new_path = destination_folder / file.name

        if new_path.exists():
            unique_name = get_unique_file_name(destination_folder, file)
            new_path = destination_folder / unique_name

        file.rename(new_path)