import tkinter as tk
from tkinter import PhotoImage
from games.classic_game.classic_game import ClassicGame
from games.image_game.game_images import ImageGame
from games.quote_game.quote_game import QuoteGame
from games.skill_game.game_skills import SkillGame
from PIL import Image, ImageTk, ImageDraw

class App:
    def __init__(self, root):
        
        self.color = "#800000"

        self.root = root
        # self.root.after(100, self.set_background)

        self.root.title("Меню игр")
        self.root.geometry("600x400")
        # self.set_background()

        self.create_custom_menu()
        self.main_frame = tk.Frame(self.root)

        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # self.main_frame.place(x=0, y =0)

        # self.main_frame.place(x=50, y =50)
        self.label = tk.Label(self.main_frame, text="Выберите игру из меню!", font=("Arial", 16))
        self.label.pack(pady=50)
        # self.root.wm_attributes("-transparentcolor", self.root["bg"])
        # Отложенный вызов для загрузки фона после отображения окна
    
    def set_background(self):
        # Загружаем изображение и изменяем его размер после отображения окна
        self.background_image = Image.open("unnamed.png")
        # Желаемый новый размер по ширине или высоте
        new_width = 2050  # например, новый размер по ширине
        aspect_ratio = self.background_image.height / self.background_image.width

        # Вычисляем новый размер с сохранением пропорций
        new_height = int(new_width * aspect_ratio)
        self.background_image = self.background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Преобразуем изображение в формат, который Tkinter может использовать
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Создаем Label, который будет использоваться как фон
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Растягиваем на весь размер окна
        # self.background_label = tk.Label(self.root, image=self.background_photo)
        # self.background_label.pack(side="top", fill="both", expand="no")

   

    def create_custom_menu(self):
        # Создаем Frame для меню
        
        menu_frame = tk.Frame(self.root, bg=self.color, bd=5)
        menu_frame.pack(fill=tk.X, pady=10)
        # Создаем контейнер для выравнивания кнопок по центру
        button_frame = tk.Frame(menu_frame, bg=self.color)
        button_frame.pack(side=tk.TOP, pady=20)

        # Кнопка для игры "Классика"
        classic_button = self.create_round_button(button_frame, "data/games/Classic.png", lambda: self.show_game(ClassicGame))
        classic_button.pack(side=tk.LEFT, padx=10)

        # Кнопка для игры "Цитата"
        quote_button = self.create_round_button(button_frame, "data/games/Quote.png", lambda: self.show_game(QuoteGame))
        quote_button.pack(side=tk.LEFT, padx=10)

        # Кнопка для игры "Умение"
        skill_button = self.create_round_button(button_frame, "data/games/Ability.png", lambda: self.show_game(SkillGame))
        skill_button.pack(side=tk.LEFT, padx=10)

        # Кнопка для игры "Сплеш-арт"
        image_button = self.create_round_button(button_frame, "data/games/Splash.png", lambda: self.show_game(ImageGame))
        image_button.pack(side=tk.LEFT, padx=10)

    def create_round_button(self, parent_frame, image_file, command):
        # Загружаем изображение
        image = Image.open(image_file)
        image = image.resize((80, 80))  # Размер изображения
        image = self.make_image_round(image)  # Делаем изображение круглым
        photo = ImageTk.PhotoImage(image)

        # Создаем кнопку с изображением
        button = tk.Button(parent_frame, image=photo, command=command, relief="flat", 
            borderwidth=1,  # Ширина границы
            highlightthickness=0,  # Убираем внутреннюю границу
            highlightbackground=self.color,  # Цвет внешней границы
            highlightcolor=self.color,  # Цвет активной границы
            bg=self.color,
            activebackground=self.color)  # Фон кнопки
        
        button.image = photo  # Сохраняем ссылку на изображение, чтобы не было потери

        return button

    def make_image_round(self, image):
        # Создаем круглое изображение
        width, height = image.size
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, width, height), fill=255)
        image.putalpha(mask)  # Применяем альфа-канал (прозрачность)

        return image

    def show_game(self, game_class):
        # Очистка текущего фрейма
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Создание нового окна игры
        game_instance = game_class(self.main_frame)
        self.root.geometry("800x800")
        game_instance.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
