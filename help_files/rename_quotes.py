import os

def rename_files_in_directory(directory):
    # Получаем список всех файлов в указанной директории
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Перебираем все файлы
    for filename in files:
        # Выводим текущие имя файла
        print(f"Текущее имя файла: {filename}")
        
        # Запрашиваем новое имя у пользователя
        new_name = input("Введите новое имя для этого файла (или нажмите Enter для пропуска): ")
        
        # Если пользователь ввел новое имя, переименовываем файл
        if new_name:
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_name)
            
            # Проверяем, не существует ли уже файл с таким именем
            if os.path.exists(new_file_path):
                print(f"Файл с именем '{new_name}' уже существует. Переименование не выполнено.")
            else:
                # Переименовываем файл
                os.rename(old_file_path, new_file_path)
                print(f"Файл '{filename}' переименован в '{new_name}'.")
        else:
            print("Файл не был переименован.")

def add_txt_extension_to_files_in_folder(folder_path):
    # Проходим по всем файлам в папке
    for filename in os.listdir(folder_path):
        # Полный путь к файлу
        file_path = os.path.join(folder_path, filename)
        
        # Проверяем, что это файл (а не папка)
        if os.path.isfile(file_path):
            # Проверяем, что файл не заканчивается на .txt
            if not filename.endswith('.txt'):
                new_filename = filename + '.txt'
                new_file_path = os.path.join(folder_path, new_filename)
                
                # Переименовываем файл
                os.rename(file_path, new_file_path)
                print(f"Переименован файл: {filename} -> {new_filename}")


# Указываем директорию, где находятся файлы
directory = 'data/quotes'

# Запускаем функцию переименования файлов
# rename_files_in_directory(directory)
add_txt_extension_to_files_in_folder(directory)