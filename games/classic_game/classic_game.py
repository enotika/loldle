import tkinter as tk
from PIL import Image, ImageTk
import json
from games.classic_game import first_terminal
from games.translate import champions_dict
from tkinter import ttk


class ClassicGame(tk.Frame):
    def __init__(self, parent):
        self.root = parent
        super().__init__(parent, background="#0B0C10")
        label = ttk.Label(self, text="Это игра Классика!")
        label.pack(pady=50)

        # back_button = tk.Button(self, text="Назад", command=parent.quit)
        # back_button.pack(pady=10)

        # Загружаем список чемпионов
        with open("data/info.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        self.all_answers = [item["answer"] for item in data["answers"]]

        # Подписи для полей
        self.labels = [
            "Чемпион",
            "Пол",
            "Позиция(и)",
            "Виды",
            "Ресурс",
            "Тип диапазона",
            "Регион(ы)",
            "Год выпуска",
        ]

        label_frame = ttk.Frame(self)
        label_frame.pack(pady=10)

        for label_text in self.labels:
            label = ttk.Label(label_frame, text=label_text)
            label.pack(side=tk.LEFT, padx=5)

        # Поле ввода для чемпиона
        self.entry = tk.Entry(
            self,
            background="#1F2833",
            foreground="#C5C6C7",
            highlightbackground="#66FCF1",  # Цвет обводки (к примеру, томатный)
            highlightcolor="#66FCF1",  # Цвет активной обводки
            highlightthickness=2,
        )  # Толщина активной обводки)
        self.entry.pack(pady=5)
        # Привязка клавиши Enter к кнопке проверки
        self.entry.bind("<Return>", self.check_answer_event)
        ##################################################################################################################
        # Список подсказок с прокруткой под полем ввода, но над кнопкой
        self.suggestion_frame = tk.Frame(self)
        self.suggestion_frame.pack(pady=5, fill=tk.X)

        self.suggestion_listbox = tk.Listbox(
            self.suggestion_frame,
            font=("Arial", 12),
            height=3,
            width=20,
            bg="#1F2833",
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
        self.entry.bind("<KeyRelease>", self.update_suggestions)

        # Привязка клавиш вверх и вниз для перемещения по списку
        self.suggestion_listbox.bind("<Up>", self.navigate_suggestions)
        self.suggestion_listbox.bind("<Down>", self.navigate_suggestions)

        ##################################################################################################################
        # Создаем объект Style для настройки стилей
        # style = ttk.Style()

        # # Создаем кастомный стиль для кнопок
        # style.configure("Custom.TButton",
        #                 font=("Arial", 14),              # Шрифт
        #                 padding=10,                      # Отступы внутри кнопки
        #                 relief="flat",                   # Рамка
        #                 background="#4CAF50",           # Цвет фона
        #                 foreground="white",             # Цвет текста
        #                 anchor="center",                # Выравнивание текста
        #                 width=20)                        # Ширина кнопки

        # # Добавляем стиль для кнопки при наведении
        # style.map("Custom.TButton",
        #           background=[('active', '#45a049')])  # Изменение фона при наведении

        # # Применяем кастомный стиль к кнопке
        # ########################################
        # # Кнопка для ввода
        # entry_button = ttk.Button(self, text="Ввод", style="Custom.TButton", command=self.get_text_from_button)
        # entry_button.pack(pady=10)
        # Кнопка для ввода
        self.entry_button = ttk.Button(
            self, text="Ввод", command=self.get_text_from_button
        )
        self.entry_button.pack(pady=10)
        # Создаем Canvas и Scrollbar для прокрутки результата
        self.canvas = tk.Canvas(
            self,
            bg="#1F2833",
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

        # Инициализация игры
        first_terminal.init_game()

    def add_row(self, guessed_properties, partly_guessed_properties, properties):
        if properties is None:
            return
        # Создание новой строки с метками
        row_frame = tk.Frame(self.row_frame, background="blue")
        row_frame.pack(pady=5, expand=True)  # Убираем fill=tk.X

        # Собираем все значения в один список для перебора
        guessed_data = {}
        for key, value in properties["properties"].items():
            guessed_data[key] = value

        # Загружаем изображение с помощью PIL
        imgAddress = "data/icons/" + champions_dict[properties["answer"]] + ".png"
        # print(imgAddress)
        image = Image.open(imgAddress)
        # Изменяем размер изображения
        image = image.resize((50, 50))  # Задайте нужные размеры (ширина, высота)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(
            row_frame,
            text=properties["answer"],
            image=photo,
            borderwidth=2,  # Ширина обводки
            relief="solid",  # Стиль обводки
            padx=5,  # Внутренний отступ по горизонтали
            pady=5,
        )  # Внутренний отступ по вертикали
        label.image = photo
        label.pack(side=tk.LEFT, padx=5, anchor="center", expand=True)

        # Создаем метки для каждого значения
        labels = []
        cnt_bad = 0
        for key, value in guessed_data.items():
            if key in guessed_properties:
                color = "green"  # Если текст в guessed_properties, цвет зеленый
            elif key in partly_guessed_properties:
                color = "yellow"  # Если текст в partly_guessed_properties, цвет желтый
                cnt_bad += 1
            else:
                color = "red"  # Остальные тексты красные
                cnt_bad += 1
            if key == "Год выпуска":
                txt = ", ".join(value)
                if int(value[0]) > int(
                    first_terminal.selected_answer["properties"]["Год выпуска"][0]
                ):
                    txt += "⬇️"
                elif int(value[0]) < int(
                    first_terminal.selected_answer["properties"]["Год выпуска"][0]
                ):
                    txt += "⬆️"
                label = tk.Label(
                    row_frame,
                    text=txt,
                    borderwidth=2,  # Ширина обводки
                    relief="solid",  # Стиль обводки
                    background=color,  # Цвет заливки в зависимости от статуса
                    padx=5,  # Внутренний отступ по горизонтали
                    pady=5,
                )  # Внутренний отступ по вертикали
            else:
                label = tk.Label(
                    row_frame,
                    text=", ".join(value),
                    borderwidth=2,  # Ширина обводки
                    relief="solid",  # Стиль обводки
                    background=color,  # Цвет заливки в зависимости от статуса
                    padx=5,  # Внутренний отступ по горизонтали
                    pady=5,
                )  # Внутренний отступ по вертикали
            labels.append(label)

        if cnt_bad == 0:
            self.entry.config(state="disabled")
        # Центрируем метки, добавляя их в Frame на основе pack
        for label in labels:
            label.pack(side=tk.LEFT, padx=5, anchor="center")
        #   ⬇️⬆️

    def check_answer_event(self, event):
        """Обработчик события для Enter, чтобы имитировать нажатие кнопки."""
        self.get_text_from_button()

    def get_text_from_button(self):
        user_input = (
            self.entry.get().lower()
        )  # Преобразуем ввод пользователя в нижний регистр
        self.entry.delete(0, tk.END)  # Очистить поле ввода

        if user_input in [
            answer.lower() for answer in self.all_answers
        ]:  # Преобразуем все ответы в нижний регистр для сравнения
            self.all_answers = [
                answer for answer in self.all_answers if answer.lower() != user_input
            ]  # Удаляем значение без учета регистра
        else:
            return

        (
            guessed_properties,
            partly_guessed_properties,
            guessed_data,
        ) = first_terminal.check(user_input)
        # print(guessed_properties)
        # print(partly_guessed_properties)
        self.add_row(guessed_properties, partly_guessed_properties, guessed_data)

    #############################################################################################################
    def update_suggestions(self, event):
        input_text = self.entry.get().lower()
        self.suggestion_listbox.delete(0, tk.END)
        if input_text:
            filtered_suggestions = [
                name for name in self.all_answers if name.lower().startswith(input_text)
            ]
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
