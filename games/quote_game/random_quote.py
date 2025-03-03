import random
import json
answer = ""
quote = ""

def get_random_line_from_file(file_path):
    # Открываем файл и читаем все строки
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Проверяем, что файл не пуст
    if lines:
        # Возвращаем случайную строку
        return random.choice(lines).strip()  # .strip() удаляет лишние символы новой строки
    else:
        return None  # Если файл пуст, возвращаем None
    
def init_random_quote_game():
    global answer, quote
    with open('data/info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Доступ к данным
    answers = data['answers']

    # Выбираем случайный ответ
    selected_answer = random.choice(answers)

    print("answer is = ", selected_answer["answer"])
    quote_address = "data/quotes/"+selected_answer["answer"]+".txt"

    print(quote_address)
    quote = get_random_line_from_file(quote_address)
    answer = selected_answer["answer"]
    
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
        
    #     # Перемещаем курсор в начало файла и записываем оставшиеся строки
    #     file.seek(0)
    #     file.writelines(lines)
    #     file.truncate()  # Обрезаем лишнее
    #     answer = first_line[:-1]
    #     quote_address = "data/quotes/"+answer+".txt"
    #     quote = get_random_line_from_file(quote_address)

    # ############################################################

    print(quote)
    print(answer)
    return