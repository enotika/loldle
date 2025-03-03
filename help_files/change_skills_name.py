import os
import re

def rename_images_in_skills_folders(directory):
    """Рекурсивно ищет все изображения в папках, содержащих 'skills', и предлагает изменить их имена."""
    cnt = 0
    # Обходим все папки и подпапки в указанной директории
    for root, dirs, files in os.walk(directory):
        # Проверяем, содержит ли имя папки 'skills'
        if 'skills' in root.lower():
            for file in files:
                # Проверяем, что это изображение (можно добавить другие форматы, если нужно)
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                    # Извлекаем имя файла без расширения
                    file_name_without_extension = os.path.splitext(file)[0]
                    
                    # Проверяем, что длина имени больше 15 символов или в имени есть не-английские буквы
                    if len(file_name_without_extension) > 15 or not file_name_without_extension.isascii() or not file_name_without_extension.endswith(('Q', 'W', 'E', 'R', 'P')):
                        # Выводим путь папки и название изображения
                        print(f"Изображение найдено в папке: {root}")
                        print(f"Изображение: {file}")
                        cnt+=1
                        # Запрашиваем новое имя у пользователя
                        new_name = input(f"Введите новое название для изображения '{file}' (оставьте пустым, чтобы не изменять): ")

                        # Если новое имя не пустое, переименовываем файл
                        if new_name:
                            new_file_path = os.path.join(root, new_name + os.path.splitext(file)[1])  # Сохраняем расширение
                            old_file_path = os.path.join(root, file)

                            # Переименовываем файл
                            os.rename(old_file_path, new_file_path)
                            print(f"{cnt}/71 Файл '{file}' переименован в '{new_name + os.path.splitext(file)[1]}'")
                        else:
                            print(f"Имя файла '{file}' не изменено.")
                    else:
                        print(f"Файл '{file}' не соответствует условиям (длина меньше 15 символов и только английские буквы).")
    print(cnt)
# Пример использования
directory = "data/champ_images"  # Замените на путь к вашей папке
rename_images_in_skills_folders(directory)
