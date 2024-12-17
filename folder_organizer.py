from pathlib import Path

FOLDER_FOR_FILE_TYPE = {
    "Texto": (".txt"),
    "Audio": (".mp3"),
    "Video": (".mp4"),
    "Imagem": (".png", ".jpg")
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