import random
import json

answers = []
answers_dict = {}
selected_answer = {}


def init_game():
    global answers, answers_dict, selected_answer  # Добавьте эту строку
    # Чтение данных из файла
    with open('data/info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Доступ к данным
    answers = data['answers']
    # Создаем словарь для быстрого поиска по имени ответа
    answers_dict = {answer['answer'].lower(): answer for answer in answers}

    # Выбираем случайный ответ
    selected_answer = random.choice(answers)

    print("answer is = ", selected_answer["answer"])
    # for i in answers:
    #     print(i["answer"])


def check(user):
    guessed_properties = {}  # Список для угаданных свойств
    partly_guessed_properties = {}
    
    user_guess = user.lower()

    guess_data = answers_dict.get(user_guess)
    if guess_data is None:
        print("Ответ не найден. Попробуйте снова.")
        return {"Ошибка": "ввода"},{}, None
    
    if(user_guess.lower() == selected_answer["answer"].lower()):
        print("UUUUUUUUUUUUUUUUUUUUUUUUUUU")
        return selected_answer["properties"],{"Победа": "ура"}, guess_data
    
    for prop in selected_answer["properties"]:
            # print(prop, " : ", selected_answer["properties"][prop], " = ", end=" ")
            # print(guess_data["properties"][prop])
        if(guess_data["properties"][prop] == selected_answer["properties"][prop]):
            guessed_properties[prop] = selected_answer['properties'][prop]
            continue
        found = False
        for i in guess_data["properties"][prop]:
            for j in selected_answer["properties"][prop]:
                if i == j:
                    found = True
                    break
            if found:
                break
        if found:
            partly_guessed_properties[prop] = guess_data['properties'][prop]
        # print(guessed_properties)
        # print(partly_guessed_properties)
    return guessed_properties, partly_guessed_properties, guess_data


def get_right(user, game):
    guessed_properties = {}  # Список для угаданных свойств
    partly_guessed_properties = {}
    for prop in game["properties"]:
            # print(prop, " : ", game["properties"][prop], " = ", end=" ")
            # print(user["properties"][prop])
        if(user["properties"][prop] == game["properties"][prop]):
            guessed_properties[prop] = game['properties'][prop]
            continue
        found = False
        for i in user["properties"][prop]:
            for j in game["properties"][prop]:
                if i == j:
                    found = True
                    break
            if found:
                break
        if found:
            partly_guessed_properties[prop] = user['properties'][prop]
        # print(guessed_properties)
        # print(partly_guessed_properties)
    return guessed_properties, partly_guessed_properties
    
def first_game_loldle():
    
    init_game()

    while True:
        guessed_properties = {}  # Список для угаданных свойств
        partly_guessed_properties = {}
        user_guess = input("Ваш ответ: ").lower()
        if(user_guess.lower() == selected_answer["answer"].lower()):
            print("UUUUUUUUUUUUUUUUUUUUUUUUUUU")
            break

        guess_data = answers_dict.get(user_guess)
        if guess_data is None:
            print("Ответ не найден. Попробуйте снова.")
            continue

        # print(selected_answer)
        # print(selected_answer["properties"]["Пол"])
        # print("ггггггггггггггггггггггггггггггггг")
        # print(guess_data["properties"]["Пол"])
        # for prop in guess_data["properties"]:
        #     print(prop, " : ", guess_data["properties"][prop])
        
        print("==============================================================================")
        guessed_properties, partly_guessed_properties = get_right(guess_data, selected_answer)
        print(guessed_properties)
        print(partly_guessed_properties)



# first_game_loldle()