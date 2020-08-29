from tinkoff_voicekit_client import ClientSTT
from functions.processing import processing_audio
from functions.validator import validator_number_phone, validator_save_db, \
    validator_path_audio, validator_state_recognition
from functions.logging import log_error
from os import remove

API_KEY = "****"
SECRET_KEY = "****"

client = ClientSTT(API_KEY, SECRET_KEY)

audio_config = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}

# Эти переменные нам нужны чтобы реализовать возможность повторного запроса ввода данных
# в случае ввода ошибочных данных.
# Они выполняют роль флагов и указывают куда нужно идти в бесконечном цикле
flag_audio = 0
flag_number_phone = 1
flag_save_db = 1
flag_state_recognition = 1

# Получаем данные от пользователя и так-же проверяем каждый полученный параметр.
# Именно тут используются флаги описанные выше.
while True:
    if flag_audio == 0:
        path_audio = input('Введите путь до аудио файла: ')
        flag_audio, flag_number_phone = validator_path_audio(path_audio)

    if flag_number_phone == 0:
        phone_number = input('Введите номер телефона: ')
        flag_number_phone, flag_save_db = validator_number_phone(phone_number)

    if flag_save_db == 0:
        save_to_db = int(input('Сохранить результат в базу данных?' '(1 - Да, 0 - Нет): '))
        flag_save_db, flag_state_recognition = validator_save_db(save_to_db)

    if flag_state_recognition == 0:
        state_recognition = int(input('Введите этап распознования (1 или 2) '))
        flag_state_recognition = validator_state_recognition(state_recognition)

    if flag_audio == 1 and flag_number_phone == 1\
            and flag_save_db == 1 and flag_state_recognition == 1:
        break


try:
    # Вызываем процесс распознавания аудио файла
    response = client.recognize(path_audio, audio_config)
except ValueError as error:
    print('Ошибка с распознованием аудио-файла: {}'.format(error))
    log_error(error)
else:
    processing_audio(response, phone_number, state_recognition, save_to_db)
    # Удаляем использованный аудио файл
    remove(path_audio)

