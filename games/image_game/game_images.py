import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
from games.image_game import random_image_part
from games.translate import champions_dict
import json
from tkinter import ttk


class ImageGame(tk.Frame):
    def __init__(self, parent):
        self.root = parent

        super().__init__(parent, background="#0B0C10")
        self.count_expand = 0
        # self.parent.title("Игра картинки")
        self.expand_sz = 0
        self.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        self.title_label = ttk.Label(self, text="Игра картинки", font=("Arial", 24))
        self.title_label.pack(pady=10)

        # Инициализация случайной картинки
        self.load_random_image()

        # Отображение картинки
        self.image_label = tk.Label(
            self,
            image=self.image_tk,
            highlightbackground="#66FCF1",  # Цвет обводки (к примеру, томатный)
            highlightcolor="#66FCF1",  # Цвет активной обводки
            highlightthickness=2,
        )  # Толщина активной обводки)
        self.image_label.pack(pady=10)

        # Поле для ввода
        self.input_label = ttk.Label(self, text="Введите название картинки:")
        self.input_label.pack(pady=5)

        self.input_field = tk.Entry(
            self,
            font=("Arial", 14),
            background="#1F2833",
            foreground="#C5C6C7",
            highlightbackground="#66FCF1",  # Цвет обводки (к примеру, томатный)
            highlightcolor="#66FCF1",  # Цвет активной обводки
            highlightthickness=2,
        )  # Толщина активной обводки)
        self.input_field.pack(pady=5)

        # Список подсказок с прокруткой
        self.suggestion_frame = tk.Frame(self)
        self.suggestion_frame.pack(pady=5)

        self.suggestion_listbox = tk.Listbox(
            self.suggestion_frame,
            font=("Arial", 12),
            height=3,
            width=20,
            background="#1F2833",
            fg="#C5C6C7",
            highlightbackground="#66FCF1",  # Цвет обводки (к примеру, томатный)
            highlightcolor="#66FCF1",  # Цвет активной обводки
            highlightthickness=2,
        )  # Толщина активной обводки)
        self.suggestion_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(
            self.suggestion_frame,
            orient="vertical",
            command=self.suggestion_listbox.yview,
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.suggestion_listbox.config(yscrollcommand=self.scrollbar.set)

        self.suggestion_listbox.bind(
            "<Double-1>", self.on_suggestion_click
        )  # Для выбора подсказки

        # Обновляем подсказки при вводе
        self.input_field.bind("<KeyRelease>", self.update_suggestions)

        # Привязка клавиши Enter к кнопке проверки
        self.input_field.bind("<Return>", self.check_answer_event)

        # Привязка клавиш вверх и вниз для перемещения по списку
        self.suggestion_listbox.bind("<Up>", self.navigate_suggestions)
        self.suggestion_listbox.bind("<Down>", self.navigate_suggestions)

        # Кнопка проверки
        self.check_button = ttk.Button(
            self, text="Проверить", command=self.check_answer
        )
        self.check_button.pack(pady=20)

        with open("data/info.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        self.all_answers = [item["answer"] for item in data["answers"]]
        # Создаем Canvas и Scrollbar для прокрутки результата
        self.canvas = tk.Canvas(
            self,
            background="#1F2833",
            highlightbackground="#66FCF1",  # Цвет обводки (к примеру, томатный)
            highlightcolor="#66FCF1",  # Цвет активной обводки
            highlightthickness=2,
        )  # Толщина активной обводки)
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, background="orange")
        self.scrollable_frame.grid(sticky="ew")

        # Настройка прокрутки
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Упаковываем Canvas и Scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.row_frame = (
            self.scrollable_frame
        )  # Используем scrollable_frame для добавления строк

    def add_row(self, name):
        print(name)
        print(self.all_answers)
        # Создание новой строки с метками
        row_frame = tk.Frame(self.row_frame, background="blue")
        row_frame.pack(pady=5, expand=True)  # Убираем fill=tk.X
        img_address = ""
        name_save = ""
        labels = []
        for i in self.all_answers:
            if i.strip().lower().replace(" ", "") == name:
                print(champions_dict[i])
                name_save = i
                img_address = "data/icons/" + champions_dict[i] + ".png"
        print(img_address)
        # print(imgAddress)
        image = Image.open(img_address)
        # Изменяем размер изображения
        image = image.resize((50, 50))  # Задайте нужные размеры (ширина, высота)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(
            row_frame,
            text=img_address,
            image=photo,
            borderwidth=2,  # Ширина обводки
            relief="solid",  # Стиль обводки
            padx=5,  # Внутренний отступ по горизонтали
            pady=5,
        )  # Внутренний отступ по вертикали
        label.image = photo
        labels.append(label)
        # label.pack(side=tk.LEFT, pady=5, anchor='center', expand=True)
        label = tk.Label(
            row_frame,
            text=name_save,
            #  image=photo,
            borderwidth=2,  # Ширина обводки
            relief="solid",  # Стиль обводки
            padx=5,  # Внутренний отступ по горизонтали
            pady=5,
        )  # Внутренний отступ по вертикали
        labels.append(label)
        # Центрируем метки, добавляя их в Frame на основе pack
        for label in labels:
            label.pack(side=tk.LEFT, padx=5, anchor="center")

    def load_random_image(self):
        base_path = "data/champ_images"
        all_folders = [
            f
            for f in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, f))
        ]
        self.all_folders = all_folders  # Сохраняем все папки как список
        self.random_folder = random.choice(all_folders)
        print(self.random_folder)
        image_folder_addres = (
            "data/champ_images/"
            + self.random_folder
            + "/"
            + self.random_folder
            + "_skins"
        )
        print(image_folder_addres)

        all_named_images = [f for f in os.listdir(image_folder_addres)]
        self.image_address = random.choice([f for f in os.listdir(image_folder_addres)])
        self.image_address = image_folder_addres + "/" + self.image_address
        # ##################################################################################################
        # file_path = "data/persons.txt"
        # # Читаем все строки, удаляем первую и записываем оставшиеся
        # # Открываем файл для чтения и записи
        # with open(file_path, 'r+') as file:
        #     lines = file.readlines()

        #     # Сохраняем первую строку
        #     first_line = lines[0] if lines else None

        #     # Удаляем первую строку
        #     lines = lines[1:]
        #     first_line = first_line[:-1]
        #     # Перемещаем курсор в начало файла и записываем оставшиеся строки
        #     file.seek(0)
        #     file.writelines(lines)
        #     file.truncate()  # Обрезаем лишнее
        #     image_folder_addres = "data/champ_images/" + first_line + "/" + first_line + "_skins"
        #     print(image_folder_addres)
        #     self.image_address = random.choice([f for f in os.listdir(image_folder_addres)])
        #     self.image_address = image_folder_addres + "/" + self.image_address
        # ############################################################

        print(self.image_address)

        img_to_show = random_image_part.crop_random_patch(self.image_address, 200, 200)
        img_to_show.save("show_image.jpg")  # Сохраняем вырезанный фрагмент

        # Загружаем картинку
        self.image = Image.open("show_image.jpg")  # Укажите путь к изображению
        self.image = self.image.resize((300, 300))
        self.image_tk = ImageTk.PhotoImage(self.image)
        os.remove("show_image.jpg")

    def check_answer(self, event=None):
        answer = self.input_field.get().strip().lower().replace(" ", "")
        self.add_row(answer)

        self.input_field.delete(0, tk.END)  # Очищаем поле ввода

        if answer in [
            i.strip().lower().replace(" ", "") for i in self.all_answers
        ]:  # Преобразуем все ответы в нижний регистр для сравнения
            self.all_answers = [
                i
                for i in self.all_answers
                if i.strip().lower().replace(" ", "") != answer
            ]  # Удаляем значение без учета регистра
        else:
            return

        if answer == self.random_folder.lower():
            messagebox.showinfo("Правильный ответ", "Поздравляем, вы угадали картинку!")
            self.image = Image.open(self.image_address)  # Загружаем картинку
            max_size = 300
            self.image.thumbnail(
                (max_size, max_size)
            )  # Пропорциональное уменьшение изображения
            self.image_tk = ImageTk.PhotoImage(self.image)

            # Обновляем изображение
            self.image_label.config(image=self.image_tk)
            self.image_label.image = self.image_tk  # Сохраняем ссылку на изображение
            self.input_field.config(state="disabled")  # Блокирует ввод в поле
        else:
            # messagebox.showerror("Неправильный ответ", "Попробуйте снова!")
            if self.count_expand < 20:
                self.expand_sz += 10

            self.count_expand += 1
            expanded_image = random_image_part.expand_img(
                self.image_address, 200, 200, self.expand_sz
            )
            expanded_image.save("show_image.jpg")
            self.image = Image.open("show_image.jpg")  # Загружаем картинку
            self.image = self.image.resize((300, 300))
            self.image_tk = ImageTk.PhotoImage(self.image)
            os.remove("show_image.jpg")
            self.image_label.config(image=self.image_tk)
            self.image_label.image = self.image_tk

    def check_answer_event(self, event):
        """Обработчик события для Enter, чтобы имитировать нажатие кнопки."""
        self.check_answer()

    def update_suggestions(self, event):
        input_text = self.input_field.get().lower()
        self.suggestion_listbox.delete(0, tk.END)
        if input_text:
            filtered_suggestions = [
                name for name in self.all_answers if name.lower().startswith(input_text)
            ]
            for suggestion in filtered_suggestions:
                self.suggestion_listbox.insert(tk.END, suggestion)

    def on_suggestion_click(self, event):
        selected_suggestion = self.suggestion_listbox.get(tk.ACTIVE)
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, selected_suggestion)
        self.suggestion_listbox.delete(0, tk.END)  # Очищаем подсказки

    def navigate_suggestions(self, event):
        current_selection = self.suggestion_listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
        else:
            current_index = -1

        if event.keysym == "Up":
            new_index = max(0, current_index - 1)
            # new_index = current_index + 1
            # if new_index > self.suggestion_listbox.size():
            #     new_index = 0
            print("UP")
        elif event.keysym == "Down":
            print("DOWN")
            new_index = min(self.suggestion_listbox.size() - 1, current_index + 1)
            print(current_index, new_index)

        if new_index != current_index:
            self.suggestion_listbox.select_clear(current_index)
            self.suggestion_listbox.select_set(new_index)
            # self.suggestion_listbox.activate(new_index)
            selected_suggestion = self.suggestion_listbox.get(new_index)
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, selected_suggestion)
        print(self.suggestion_listbox.curselection())


# if __name__ == "__main__":
#     root = tk.Tk()
#     game = ImageGame(root)
#     root.mainloop()
