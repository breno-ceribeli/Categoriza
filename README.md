# Categoriza

## 🇺🇸 In English

**Categoriza** is a Python desktop application that automatically organizes files into folders based on their types. It offers both command-line (CLI) and graphical user interfaces (GUI) for flexibility and ease of use.

With the GUI, users can:
- Organize files into folders.
- Edit format maps in the CSV file by adding, removing, or modifying extensions.
- View and manage error logs with ease.

The CLI is perfect for users who prefer direct commands for quick tasks and automation.

## 🇧🇷 Em Português

**Categoriza** é uma aplicação desktop desenvolvida em Python que organiza automaticamente arquivos em pastas, com base em seus tipos. A aplicação oferece duas interfaces: linha de comando (CLI) e gráfica (GUI), permitindo flexibilidade e facilidade de uso.

Com a GUI, o usuário pode:
- Organizar arquivos em pastas.
- Editar mapas de formatos no arquivo CSV, adicionando, removendo ou modificando extensões.
- Visualizar e gerenciar logs de erros de forma simples.

A CLI é ideal para usuários que preferem comandos diretos para tarefas rápidas e automação.

---

## Table of Contents / Índice

- [🇺🇸 English Documentation](#🇺🇸-english-documentation)
  - [Installation](#installation)
  - [Usage](#usage)
  - [CSV Configuration](#csv-configuration)
  - [Future Features](#future-features)
  - [Contributing](#contributing)
  - [License and Dependencies](#license-and-dependencies)
- [🇧🇷 Documentação em Português](#🇧🇷-documentação-em-português)
  - [Instalação](#instalação)
  - [Como Usar](#como-usar)
  - [Configuração do CSV](configuração-do-csv)
  - [Funcionalidades Futuras](#funcionalidades-futuras)
  - [Contribuição](#contribuição)
  - [Licença e Dependências](#licença-e-dependências)

---

## 🇺🇸 English Documentation

### Installation

1. Ensure Python is installed (version 3.9 or higher).

2. Clone this repository:
   ```bash
   git clone https://github.com/breno-ceribeli/Categoriza
   ```

3. Navigate to the project directory:
   ```bash
   cd Categoriza
   ```

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### GUI

1. Open the program by running the following command:
    ```bash
    python folder_organizer_app.py
    ```

2. Select the folder you wish to organize using the graphical interface.

3. Click the "Organize" button to start sorting the files into folders based on their types.

4. Use the "Settings" option to edit the format map (CSV file) by adding, modifying, or removing file extensions.

5. Check and manage error logs if any issues arise during the process.

#### CLI

You can use the command-line version of the application in two ways:

1. **Interactive mode:**
   - Run the script without any arguments:
    ```bash
    python folder_organizer.py
    ```
   - The program will prompt you to enter the directory path to be organized. Enter the path and press Enter.

2. **Direct mode:**
   - Provide the directory path as an argument when running the script:
    ```bash
    python folder_organizer.py absolute-path-directory
    ```
In both cases, the program will organize the files in the specified folder, sorting them into subfolders based on their types.

### CSV Configuration

The `data.csv` file is the core configuration file for defining how files are categorized. It consists of two columns:

1. **File Extension:** Specifies the extension of the file (e.g., `.txt`, `.jpg`).

2. **File Type (Folder Name):** Defines the folder where files of the corresponding extension will be placed. 

Additionally, there is a special entry:
- `others`: Defines the name of the folder where files with extensions not explicitly listed will be placed.

#### Editing the CSV

- **GUI**: Use the graphical interface to easily add, modify, or remove entries in the `data.csv` file. This option is user-friendly and does not require direct interaction with the file.

- **CLI**: You can manually edit the `data.csv` file in a text editor or spreadsheet application. Ensure that each row follows the format:
  ```bash
  .extension,FolderName
  ```

**Example:**
  ```bash
  .txt,Documents
  .jpg,Images
  .png,Images
  .mp3,Audio
  others,Miscellaneous
  ```

In this example:
- `.txt` files will go into the `Documents` folder.

- `.jpg` and `.png` files will go into the `Images` folder.

- `.mp3` files will go into the `Audio` folder.

- Any file extension not listed will go into the `Miscellaneous` folder.

### Future Features

- Option to select the GUI language (Portuguese or English)

### Contributing

Contributions are welcome! Follow these steps:
1. Fork this repository.

2. Create a branch for your feature:
   `git checkout -b my-feature`

3. Make your changes.

4. Push your branch: 
   `git push origin my-feature`.

5. Submit a pull request detailing your changes.

### License and Dependencies

This project is licensed under the [MIT License](LICENSE).

This project uses the following external libraries:

- **CustomTkinter**  
  License: [MIT License](https://github.com/TomSchimansky/CustomTkinter/blob/master/LICENSE).  
  Copyright © 2023 Tom Schimansky.

- **Pillow**  
  License: [MIT-CMU License](https://github.com/python-pillow/Pillow/blob/main/LICENSE).  
  Copyright © 1995-2011 Fredrik Lundh and contributors,  
  Copyright © 1997-2011 Secret Labs AB,  
  Copyright © 2010 Jeffrey A. Clark and contributors.

Make sure to respect the licenses of the dependencies when redistributing this software.

---

## 🇧🇷 Documentação em Português

### Instalação

1. Certifique-se de ter o Python instalado (versão 3.9 ou superior).

2. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/categoriza.git
   ```
3. Navegue até o diretório do projeto:
   ```bash
   cd Categoriza
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Como Usar

#### GUI

1. Abra o programa executando o seguinte comando:
    ```bash
    python folder_organizer_app.py
    ```

2. Selecione a pasta que deseja organizar utilizando a interface gráfica.

3. Clique no botão "Organizar" para iniciar a separação dos arquivos em pastas, com base nos seus tipos.

4. Utilize a opção "Configurações" para editar o mapa de formatos (arquivo CSV), adicionando, modificando ou removendo extensões.

5. Verifique e gerencie logs de erros caso ocorram problemas durante o processo.

#### CLI

Você pode usar a versão em linha de comando da aplicação de duas maneiras:

1. **Modo interativo:**
   - Execute o script sem nenhum argumento:
    ```bash
    python folder_organizer.py
    ```
   - O programa solicitará que você insira o caminho do diretório a ser organizado. Insira o caminho e pressione Enter.

2. **Modo direto:**
   - Informe o caminho do diretório como argumento ao executar o script:
    ```bash
    python folder_organizer.py caminho-absoluto
    ```
Em ambos os casos, o programa organizará os arquivos na pasta especificada, separando-os em subpastas de acordo com seus tipos.

### Configuração do CSV

O arquivo `data.csv` é o principal arquivo de configuração para definir como os arquivos são categorizados. Ele consiste em duas colunas:

1. **File extension:** Especifica a extensão do arquivo (por exemplo, `.txt`, `.jpg`).

2. **File Type (Nome da Pasta):** Define a pasta onde os arquivos da extensão correspondente serão colocados.

Além disso, há uma entrada especial:
- `others`: Define o nome da pasta onde os arquivos com extensões não explicitamente listadas serão colocados.

#### Editando o CSV

- **GUI**: Use a interface gráfica para adicionar, modificar ou remover entradas no arquivo `data.csv`. Esta opção é intuitiva e não requer interação direta com o arquivo.

- **CLI**: Você pode editar manualmente o arquivo `data.csv` em um editor de texto ou aplicação de planilhas. Certifique-se de que cada linha segue o formato:
  ```bash
  .extensao,NomeDaPasta
  ```

**Exemplo:**
  ```bash
  .txt,Documentos
  .jpg,Imagens
  .png,Imagens
  .mp3,Áudio
  others,Miscelânea
  ```

Nesse exemplo:
- Arquivos `.txt` irão para a pasta `Documentos`.

- Arquivos `.jpg` e `.png` irão para a pasta `Imagens`.

- Arquivos `.mp3` irão para a pasta `Áudio`.

- Qualquer extensão não listada irá para a pasta `Miscelânea`.

### Funcionalidades Futuras

- Opção para selecionar a linguagem da GUI (português ou inglês).

### Contribuição

Contribuições são bem-vindas! Siga os passos:
1. Faça um fork deste repositório.

2. Crie uma branch para sua feature:
   `git checkout -b minha-feature`

3. Faça suas alterações.

4. Suba sua branch: 
    `git push origin minha-feature`.

5. Submeta um pull request detalhando suas alterações.

### Licença e Dependências

Este projeto está licenciado sob a [Licença MIT](LICENSE).

Este projeto utiliza as seguintes bibliotecas externas:

- **CustomTkinter**  
  Licença: [MIT License](https://github.com/TomSchimansky/CustomTkinter/blob/master/LICENSE).  
  Copyright © 2023 Tom Schimansky.

- **Pillow**  
  Licença: [MIT-CMU License](https://github.com/python-pillow/Pillow/blob/main/LICENSE).  
  Copyright © 1995-2011 Fredrik Lundh e contribuidores,  
  Copyright © 1997-2011 Secret Labs AB,  
  Copyright © 2010 Jeffrey A. Clark e contribuidores.

Certifique-se de respeitar as licenças das dependências ao redistribuir este software.
