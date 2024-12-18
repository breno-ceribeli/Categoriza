from pathlib import Path

EXTENSION_TO_TYPE = {
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
    file_type = EXTENSION_TO_TYPE.get(file_extension.lower(), "Outros")
    
    if file_type:
        destination_folder = path / file_type
        destination_folder.mkdir(exist_ok=True)

        new_path = destination_folder / file.name

        if new_path.exists():
            unique_name = get_unique_file_name(destination_folder, file)
            new_path = destination_folder / unique_name

        file.rename(new_path)