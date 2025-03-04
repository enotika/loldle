import os
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Папки для поиска и переноса картинок
source_folder = "data/champ_images"
target_folder = "data/bad_skins"

# Собираем все изображения из папок, содержащих "_skins" в имени
image_files = []

# Ищем все подпапки с "_skins" в пути
for root, dirs, files in os.walk(source_folder):
    if "_skins" in root:  # Проверяем, содержит ли папка "_skins" в имени
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_files.append(os.path.join(root, file))

# Если нет картинок для обработки, показываем сообщение и выходим
if not image_files:
    messagebox.showinfo("Ошибка", "Не найдено изображений для обработки.")
    exit()

# Класс для приложения
class ImageMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Перенос изображений")
        
        # Инициализируем переменные
        self.current_image_index = 0
        self.image_label = tk.Label(root)
        self.image_label.pack()
        
        self.move_button = tk.Button(root, text="Перенести", command=self.move_image)
        self.move_button.pack()

        # Загружаем первое изображение
        self.show_image()

        # Обработчик события для клавиши Enter
        self.root.bind("<Return>", self.next_image)

    def show_image(self):
        if self.current_image_index < len(image_files):
            image_path = image_files[self.current_image_index]
            image_name = os.path.basename(image_path)  # Получаем имя файла без пути
            print(f"Показываем изображение: {image_name}")  # Выводим имя картинки в консоль

            img = Image.open(image_path)
            img.thumbnail((400, 400))  # Уменьшаем изображение для показа
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img
        else:
            messagebox.showinfo("Конец", "Все картинки просмотрены.")
            self.root.quit()

    def move_image(self):
        if self.current_image_index < len(image_files):
            image_path = image_files[self.current_image_index]
            # Перемещаем изображение в папку target_folder
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            shutil.move(image_path, os.path.join(target_folder, os.path.basename(image_path)))
            # Переходим к следующему изображению
            self.current_image_index += 1
            self.show_image()

    def next_image(self, event=None):
        if self.current_image_index < len(image_files):
            self.current_image_index += 1
            self.show_image()

# Создание и запуск приложения
root = tk.Tk()
app = ImageMoverApp(root)
root.mainloop()
