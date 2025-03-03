import os
import re
champions_dict = {
    "Аврора": "Aurora",
    "Азир": "Azir",
    "Акали": "Akali",
    "Акшан": "Akshan",
    "Алистар": "Alistar",
    "Амбесса": "Ambessa",
    "Амуму": "Amumu",
    "Анивия": "Anivia",
    "Ари": "Ahri",
    "Атрокс": "Aatrox",
    "АурелионСол": "AurelionSol",
    "Афелий": "Aphelios",
    "Бард": "Bard",
    "Бел'Вет": "BelVeth",
    "Блицкранк": "Blitzcrank",
    "Брайер": "Briar",
    "Браум": "Braum",
    "Брэнд": "Brand",
    "Вай": "Vi",
    "Варвик": "Warwick",
    "Варус": "Varus",
    "Вейгар": "Veigar",
    "Вейн": "Vayne",
    "Векс": "Vex",
    "Вел'Коз": "VelKoz",
    "Виего": "Viego",
    "Виктор": "Viktor",
    "Владимир": "Vladimir",
    "Волибир": "Volibear",
    "Вуконг": "Wukong",
    "Галио": "Galio",
    "Гангпланк": "Gangplank",
    "Гарен": "Garen",
    "Гвен": "Gwen",
    "Гекарим": "Hecarim",
    "Гнар": "Gnar",
    "Грагас": "Gragas",
    "Грейвз": "Graves",
    "Дариус": "Darius",
    "Джакс": "Jax",
    "ДжарванIV": "JarvanIV",
    "Джейс": "Jayce",
    "Джин": "Jhin",
    "Джинкс": "Jinx",
    "Диана": "Diana",
    "ДокторМундо": "DrMundo",
    "Дрейвен": "Draven",
    "Ёнэ": "Yone",
    "Жанна": "Janna",
    "Зайра": "Zyra",
    "Зак": "Zac",
    "Зед": "Zed",
    "Зерат": "Zerat",
    "Зери": "Zeri",
    "Зиггс": "Ziggs",
    "Зилеан": "Zilean",
    "Зои": "Zoe",
    "Иверн": "Ivern",
    "Иллаой": "Illaoi",
    "Ирелия": "Irelia",
    "Йорик": "Yorick",
    "К'Санте": "KSante",
    "Ка'Зикс": "KhaZix",
    "Каин": "Kayn",
    "Кай'Са": "KaiSa",
    "Калиста": "Kalista",
    "Камилла": "Camille",
    "Карма": "Karma",
    "Картус": "Karthus",
    "Кассадин": "Kassadin",
    "Кассиопея": "Cassiopeia",
    "Катарина": "Katarina",
    "Квинн": "Quinn",
    "Кейл": "Kayle",
    "Кейтлин": "Caitlyn",
    "Кеннен": "Kennen",
    "Киана": "Qiyana",
    "Киндред": "Kindred",
    "Клед": "Kled",
    "Ког'Мао": "KogMaw",
    "Корки": "Corki",
    "КсинЖао": "XinZhao",
    "ЛеБлан": "LeBlanc",
    "Леона": "Leona",
    "ЛиСин": "LeeSin",
    "Лиллия": "Lillia",
    "Лиссандра": "Lissandra",
    "Лулу": "Lulu",
    "Люкс": "Lux",
    "Люциан": "Lucian",
    "Мальзахар": "Malzahar",
    "Мальфит": "Malphite",
    "Маокай": "Maokai",
    "МастерЙи": "MasterYi",
    "Милио": "Milio",
    "МиссФортуна": "MissFortune",
    "Моргана": "Morgana",
    "Мордекайзер": "Mordekaiser",
    "Мэл": "Mel",
    "Наафири": "Naafiri",
    "Нами": "Nami",
    "Насус": "Nasus",
    "Наутилус": "Nautilus",
    "Нидали": "Nidalee",
    "Нико": "Niko",
    "Нила": "Nilah",
    "Ноктюрн": "Nocturne",
    "НунуиВиллумп": "Nunu",
    "Олаф": "Olaf",
    "Орианна": "Orianna",
    "Орн": "Ornn",
    "Пайк": "Pyke",
    "Пантеон": "Pantheon",
    "Поппи": "Poppy",
    "Райз": "Ryze",
    "Рамбл": "Rumble",
    "Раммус": "Rammus",
    "Рек'Сай": "RekSai",
    "Релл": "Rell",
    "РенатаГласк": "RenataGlasc",
    "Ренгар": "Rengar",
    "Ренектон": "Renekton",
    "Ривен": "Riven",
    "Рэйкан": "Rakan",
    "Сайлас": "Sylas",
    "Самира": "Samira",
    "Свейн": "Swain",
    "Седжуани": "Sejuani",
    "Сенна": "Senna",
    "Серафина": "Seraphine",
    "Сетт": "Sett",
    "Сивир": "Sivir",
    "Синджед": "Singed",
    "Синдра": "Syndra",
    "Сион": "Sion",
    "Скарнер": "Skarner",
    "Смолдер": "Smolder",
    "Сона": "Sona",
    "Сорака": "Soraka",
    "ТаамКенч": "TahmKench",
    "Талия": "Taliyah",
    "Талон": "Talon",
    "Тарик": "Taric",
    "ТвистедФэйт": "TwistedFate",
    "Твич": "Twitch",
    "Тимо": "Teemo",
    "Трандл": "Trundle",
    "Треш": "Thresh",
    "Триндамир": "Tryndamere",
    "Тристана": "Tristana",
    "Удир": "Udyr",
    "Ургот": "Urgot",
    "Фиддлстикс": "Fiddlesticks",
    "Физз": "Fizz",
    "Фиора": "Fiora",
    "Хвэй": "Hwei",
    "Хеймердингер": "Heimerdinger",
    "Чо'Гат": "ChoGath",
    "Шако": "Shaco",
    "Шая": "Xayah",
    "Шен": "Shen",
    "Шивана": "Shyvana",
    "Эвелинн": "Evelynn",
    "Эзреаль": "Ezreal",
    "Экко": "Ekko",
    "Элиза": "Elise",
    "Энни": "Annie",
    "Эш": "Ashe",
    "Юми": "Yuumi",
    "Ясуо": "Yasuo"
}

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
                    up_folder = os.path.basename(root)
                    if (not (up_folder[:-7] in champions_dict and
                        file_name_without_extension[:-1] == champions_dict[up_folder[:-7]]) or 
                        len(file_name_without_extension) > 15 or 
                        not file_name_without_extension.isalpha() or 
                        not file_name_without_extension.endswith(('Q', 'W', 'E', 'R', 'P'))
                    ):
                        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        # print(root[:-7])
                        # print(up_folder, up_folder[:-7] in champions_dict)
                        # print(file_name_without_extension[:-1])
                        # if up_folder[:-7] in champions_dict:
                        #     print(champions_dict[up_folder[:-7]])
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
