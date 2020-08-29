from random import getrandbits
from datetime import datetime
from re import search
from functions.logging import log_data
from database.add_to_db import add_to_db


# Функция анализа слов
def word_analysis(transcript, state_recognition):
    # Проверяем говорит человек или автоответчик
    if state_recognition == 1:
        words_machine = ['автоответчик', 'сигнала', 'сообщение']
        for word_machine in words_machine:
            if search(word_machine, transcript):
                return 'АО'
            else:
                return 'человек'
    # Узнаем этап распознования
    elif state_recognition == 2:
        words = ['нет', 'неудобно']
        for word in words:
            if search(word, transcript):
                return 'отрицательно'
            else:
                return 'положительно'


# Функция для создания уникального ID для записи в базе
def create_unique_id():
    id = getrandbits(16)
    while True:
        yield id
        id += 1


def processing_audio(response, phone_number, state_recognition, save_to_db):
    # вытаскиваем тест из аудио
    transcript = response[0]['alternatives'][0]['transcript']
    # расчитываем длину аудио дорожки
    time_start = response[0]['start_time'].replace('s', '')
    time_start = float(time_start)
    time_end = response[0]['end_time'].replace('s', '')
    time_end = float(time_end)
    audio_length = time_end - time_start
    # запаковываем полученные данные в словарь
    data = {
        "id": next(create_unique_id()),
        "datetime": datetime.now(),
        "result": word_analysis(transcript, state_recognition),
        "phone_number": phone_number,
        "audio_length": audio_length,
        "transcript": transcript,
    }

    if save_to_db == 1:
        try:
            # запись в базу данных
            add_to_db(data)
            # логгирование результата
            log_data(data)
        except Exception as error:
            print('An error occurred while adding a record to the database: {}'.format(error))
