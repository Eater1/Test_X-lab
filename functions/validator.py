from os import path
from functions.logging import log_error
from phonenumbers import parse, is_valid_number


# Функция для проверки наличия файла по указанному пути
def validator_path_audio(path_audio):
    if path.exists(path_audio):
        flag_audio = 1
        flag_number_phone = 0
        return flag_audio, flag_number_phone
    else:
        print('Файл не найден\nПопробуйте ещё раз')
        log_error('Invalid path audio')
        flag_audio = 0
        flag_number_phone = 1
        return flag_audio, flag_number_phone


# Функция для проверки корректности вводимого номера телефона
def validator_number_phone(phone_number):
    try:
        valid_number = parse(phone_number, 'RU')
        if not is_valid_number(valid_number):
            print('Некоректный номер\nПопробуйте ещё раз')
            log_error('Invalid phone number')
            flag_number_phone = 0
            flag_save_db = 1
            return flag_number_phone, flag_save_db
        else:
            flag_number_phone = 1
            flag_save_db = 0
            return flag_number_phone, flag_save_db
    except Exception as error:
        print('Error phone_number: {}'.format(error))
        log_error(error)
        flag_number_phone = 0
        flag_save_db = 1
        return flag_number_phone, flag_save_db


# Последнии две функции нужны для проверки вводимых значений
# на запрос о добавлении записи в базу данных (1 или 0) и
# на запрос этапе распознования (1 или 2)
def validator_save_db(save_to_db):
    try:
        if save_to_db == 1 or save_to_db == 0:
            flag_save_db = 1
            flag_state_recognition = 0
            return flag_save_db, flag_state_recognition
        else:
            print('Введите только 1 или 0\nПопробуйте ещё раз')
            log_error('Invalid value save_db')
            flag_save_db = 0
            flag_state_recognition = 1
            return flag_save_db, flag_state_recognition
    except ValueError:
        print('Введите только число\nПопробуйте ещё раз')
        log_error('Invalid value save_db')
        flag_save_db = 0
        flag_state_recognition = 1
        return flag_save_db, flag_state_recognition


def validator_state_recognition(state_recognition):
    try:
        if state_recognition == 1 or state_recognition == 2:
            flag_state_recognition = 1
            return flag_state_recognition
        else:
            print('Введите только 1 или 2\nПопробуйте ещё раз')
            log_error('Invalid value state_recognition')
            flag_state_recognition = 0
            return flag_state_recognition
    except ValueError:
        print('Введите только число\nПопробуйте ещё раз')
        log_error('Invalid value state_recognition')
        flag_state_recognition = 0
        return flag_state_recognition
