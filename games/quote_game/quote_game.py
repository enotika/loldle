import tkinter as tk
from PIL import Image, ImageTk
import json
from games.quote_game import random_quote
from tkinter import messagebox
from games.translate import champions_dict
class QuoteGame(tk.Frame):
    def __init__(self, parent):
        self.root = parent
        super().__init__(parent)

        # Заголовок
        label = tk.Label(self, text="Это игра Цитата!")
        label.pack(pady=50)

        # Поле для вывода цитаты
        self.quote_label = tk.Label(self, text="", font=("Arial", 14), wraplength=400, width=40, height=4, relief="solid", anchor="w", justify="left", padx=10, pady=10)
        self.quote_label.pack(pady=10)

        # Кнопка "Назад"
        # back_button = tk.Button(self, text="Назад", command=parent.quit)
        # back_button.pack(pady=10)
        
        # Загружаем список чемпионов
        with open('data/info.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.all_answers = [item['answer'] for item in data['answers']]

        # Поле ввода для чемпиона
        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.check_answer_event)

        # Список подсказок с прокруткой под полем ввода, но над кнопкой
        self.suggestion_frame = tk.Frame(self)
        self.suggestion_frame.pack(pady=5, fill=tk.X)

        self.suggestion_listbox = tk.Listbox(self.suggestion_frame, font=("Arial", 12), height=3, width=20)
        self.suggestion_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.suggestion_frame, orient="vertical", command=self.suggestion_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.suggestion_listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.suggestion_listbox.bind("<Double-1>", self.on_suggestion_click)  # Для выбора подсказки

        # Обновляем подсказки при вводе
        self.entry.bind("<KeyRelease>", self.update_suggestions)

        # Привязка клавиш вверх и вниз для перемещения по списку
        self.suggestion_listbox.bind("<Up>", self.navigate_suggestions)
        self.suggestion_listbox.bind("<Down>", self.navigate_suggestions)

        # Кнопка для ввода
        self.entry_button = tk.Button(self, text="Ввод", command=self.get_text_from_button)
        self.entry_button.pack(pady=10)
        
        # Создаем Canvas и Scrollbar для прокрутки результата
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, background='orange')
        self.scrollable_frame.grid(sticky='ew')

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

        self.row_frame = self.scrollable_frame  # Используем scrollable_frame для добавления строк
        random_quote.init_random_quote_game()
        self.quote_label.config(text=random_quote.quote)

    def update_quote(self, quote):
        # Обновляем текст в поле для цитаты
        self.quote_label.config(text=quote)
    
    def add_row(self, name):
        print(name)
        print(self.all_answers)
        # Создание новой строки с метками
        row_frame = tk.Frame(self.row_frame, background='blue')
        row_frame.pack(pady=5, expand=True)  # Убираем fill=tk.X
        img_address = ""
        name_save = ""
        labels = []
        for i in self.all_answers:
            if i.lower() == name:
                print(champions_dict[i])
                name_save = i
                img_address = "data/icons/" + champions_dict[i] +".png"
        print(img_address)
        # print(imgAddress)
        image = Image.open(img_address)
        # Изменяем размер изображения
        image = image.resize((50, 50))  # Задайте нужные размеры (ширина, высота)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(row_frame, text=img_address,
                         image=photo,
                         borderwidth=2,  # Ширина обводки
                         relief="solid",  # Стиль обводки
                         padx=5,  # Внутренний отступ по горизонтали
                         pady=5)  # Внутренний отступ по вертикали
        label.image = photo
        labels.append(label)
        # label.pack(side=tk.LEFT, pady=5, anchor='center', expand=True)
        label = tk.Label(row_frame, text=name_save,
                        #  image=photo,
                         borderwidth=2,  # Ширина обводки
                         relief="solid",  # Стиль обводки
                         padx=5,  # Внутренний отступ по горизонтали
                         pady=5)  # Внутренний отступ по вертикали
        labels.append(label)
        # Центрируем метки, добавляя их в Frame на основе pack
        for label in labels:
            label.pack(side=tk.LEFT, padx=5, anchor='center')
    def check_answer_event(self, event):
        """Обработчик события для Enter, чтобы имитировать нажатие кнопки."""
        self.get_text_from_button()
    def get_text_from_button(self):
        user_input = self.entry.get().lower()  # Преобразуем ввод пользователя в нижний регистр
        if user_input in [answer.lower() for answer in self.all_answers]:
            self.add_row(user_input)
        self.entry.delete(0, tk.END)  # Очистить поле ввода
        print("USER")
        print(repr(user_input))
        print(repr(random_quote.answer.lower()))
        print(user_input == random_quote.answer.lower())
        if user_input in [answer.lower() for answer in self.all_answers]:  # Преобразуем все ответы в нижний регистр для сравнения
            self.all_answers = [answer for answer in self.all_answers if answer.lower() != user_input]  # Удаляем значение без учета регистра
        else:
            return
        print(user_input == random_quote.answer.lower())
        if user_input == random_quote.answer.lower():
            print("YEEE")
            messagebox.showinfo("Правильный ответ", "Поздравляем, вы угадали цитату!")
            self.entry.config(state="disabled")  # Блокирует ввод в поле
            self.entry_button.config(state="disabled")



    def update_suggestions(self, event):
        input_text = self.entry.get().lower()
        self.suggestion_listbox.delete(0, tk.END)
        
        self.icon = tk.PhotoImage(file="data/icons/Ahri.png")

        if input_text:
            filtered_suggestions = [name for name in self.all_answers if name.lower().startswith(input_text)]
            for suggestion in filtered_suggestions:
                self.suggestion_listbox.insert(tk.END, suggestion)

    def on_suggestion_click(self, event):
        selected_suggestion = self.suggestion_listbox.get(tk.ACTIVE)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected_suggestion)
        self.suggestion_listbox.delete(0, tk.END)  # Очищаем подсказки

    def navigate_suggestions(self, event):
        current_selection = self.suggestion_listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
        else:
            current_index = -1

        if event.keysym == "Up":
            new_index = max(0, current_index - 1)
        elif event.keysym == "Down":
            new_index = min(self.suggestion_listbox.size() - 1, current_index + 1)

        if new_index != current_index:
            self.suggestion_listbox.select_clear(current_index)
            self.suggestion_listbox.select_set(new_index)

            selected_suggestion = self.suggestion_listbox.get(new_index)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_suggestion)
