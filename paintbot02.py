import telebot
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = telebot.TeleBot("Enter your API token here...")

# Данные о картинах
paintings = {
    "easy": [
         {"title": "Звездная ночь", "artist": "Винсент Ван Гог", "year": 1889,
          "image": "https://storage.yandexcloud.net/roz-wiki/Van_Gogh_-_Starry_Night_-_Google_Art_Project-x1-y1.jpg"},
         {"title": "Мона Лиза", "artist": "Леонардо да Винчи", "year": 1503,
          "image": "https://commons.wikimedia.org/wiki/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF.jpg"},
         {"title": "Девятый вал", "artist": "Иван Айвазовский", "year": 1850,
          "image": "https://upload.wikimedia.org/wikipedia/commons/5/54/Aivazovsky%2C_Ivan_-_The_Ninth_Wave.jpg"},
         {"title": "Утро в сосновом лесу", "artist": "Иван Шишкин", "year": 1889,
          "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Shishkin%2C_Ivan_-_Morning_in_a_Pine_Forest.jpg/800px-Shishkin%2C_Ivan_-_Morning_in_a_Pine_Forest.jpg"},
         {"title": "Сирень", "artist": "Винсент Ван Гог", "year": 1889,
          "image": "https://upload.wikimedia.org/wikipedia/commons/3/33/Vincent_van_Gogh_-_Irises_-_Google_Art_Project.jpg"},
    ],
    "medium": [
        {"title": "Девочка с персиками", "artist": "Валентин Серов", "year": 1881,
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Valentin_Serov_-_Девочка_с_персиками._Портрет_В.С.Мамонтовой_-_Google_Art_Project.jpg/380px-Valentin_Serov_-_Девочка_с_персиками._Портрет_В.С.Мамонтовой_-_Google_Art_Project.jpg"},
        {"title": "Ночная стража", "artist": "Рембрандт", "year": 1642,
          "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/The_Night_Watch_-_HD.jpg/573px-The_Night_Watch_-_HD.jpg"},
        {"title": "Крик", "artist": "Эдвард Мунка", "year": 1893,
         "image": "https://upload.wikimedia.org/wikipedia/commons/f/f4/The_Scream.jpg"},
        {"title": "Творение Адама", "artist": "Микеланджело", "year": 1512,
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Michelangelo_-_Creation_of_Adam_%28cropped%29.jpg/270px-Michelangelo_-_Creation_of_Adam_%28cropped%29.jpg"},
        {"title": "Девушки на мосту", "artist": "Клод Моне", "year": 1869,
         "image": "https://upload.wikimedia.org/wikipedia/commons/2/2f/%27Le_Havre%2C_Bâteaux_de_Peche_Sortant_du_Port%27_by_Claude_Monet%2C_1874.JPG"},
    ],
    "hard": [
        {"title": "Тайная вечеря", "artist": "Леонардо да Винчи", "year": 1498,
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg/640px-The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg"},
        {"title": "Сон разума", "artist": "Франсиско Гойя", "year": 1799,
         "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Goya_-_Caprichos_%2843%29_-_Sleep_of_Reason.jpg/525px-Goya_-_Caprichos_%2843%29_-_Sleep_of_Reason.jpg"},
        {"title": "Автопортрет с пузырем", "artist": "Николя Пуссен", "year": 1640,
         "image": "https://upload.wikimedia.org/wikipedia/commons/1/14/Nicolas_Poussin_-_Self-Portrait_-_WGA18333.jpg"},
        {"title": "Свадебный праздник", "artist": "Диего Веласкес", "year": 1623,
         "image": "https://www.artble.com/imgs/b/6/e/322896/wedding_at_cana_300px.jpg"},
        {"title": "Женщина с веслом", "artist": "Пабло Пикассо", "year": 1936,
         "image": "https://media.mutualart.com/Images/2012_10/27/17/171137519/ec04a78b-bace-471a-930a-a9434623cf71_570.Jpeg"},
    ]

}

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Вы хотите сыграть в проверку знаний о картинах? Выберите уровень сложности: 'easy', 'medium' или 'hard'.")
    logging.info(f"User {message.chat.id} started the game.")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Проверь свои знания об искусстве. " 
                                       "Выбери уровень сложности: 'easy', 'medium' или 'hard'.")
    user_states[message.chat.id] = {}

@bot.message_handler(commands=['restart'])
def restart(message):
    if message.chat.id in user_states:
        del user_states[message.chat.id]
    start(message)

@bot.message_handler(func=lambda message: message.text.lower() in ["easy", "medium", "hard"])
def set_difficulty(message):
    difficulty = message.text.lower()
    user_states[message.chat.id] = {
        'difficulty': difficulty,
        'paintings': random.sample(paintings[difficulty], len(paintings[difficulty])),
        'score': 0
    }
    # logger.info(f"Выбрана сложность {difficulty}, картины {user_states[message.chat.id]['paintings']}.")
    show_painting(message.chat.id)

def show_painting(chat_id):
    state = user_states[chat_id]
    if state['paintings']:
        painting = state['paintings'].pop()

        logger.info(f"Показываем картину {painting}.")

        bot.send_photo(chat_id, painting['image'], caption="Как называется это произведение?")
        bot.send_message(chat_id, "Ваш ответ:")
        user_states[chat_id]['current_painting'] = painting
    else:
        bot.send_message(chat_id, "Игра окончена! Ваш итоговый счёт: " + str(state['score']))
        start_new_game(chat_id)

def start_new_game(chat_id):
    bot.send_message(chat_id, "Хотите сыграть снова? Введите /restart.")

    @bot.message_handler(func=lambda message: message.chat.id == chat_id and message.text.lower() in ['да', 'нет'])
    def handle_restart(message):
        if message.text.lower() == 'да':
            start(user_states[chat_id])
        else:
            bot.send_message(message.chat.id, "Спасибо за игру! До новых встреч!")
            del user_states[message.chat.id]

@bot.message_handler(func=lambda message: message.chat.id in user_states)
def handle_answer(message):
    state = user_states[message.chat.id]
    artist = state['current_painting']['artist']
    year = state['current_painting']['year']
    painting = state['current_painting']['title']
    if message.text.lower().replace('ё', 'е') == painting.lower():
        state['score'] += 1
        bot.send_message(message.chat.id, f"Правильно! Художник - {artist}, картина написана в {year} году. "
                                          f"Ваш текущий счёт: " + str(state['score']))
    else:
        bot.send_message(message.chat.id, f"Неправильно. На самом деле это картина {painting}, которую "
                                          f"написал {artist} в {year} году. Ваш счёт по-прежнему: " + str(state['score']))

    show_painting(message.chat.id)

bot.polling()