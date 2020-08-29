from logging import basicConfig, error, info, ERROR, INFO


# Функция логгирования ошибок формата:
# "дата возникновения ошибки", "текст ошибки"
def log_error(err):
    basicConfig(filename='errors.log',
                filemode='a',
                format='%(asctime)s, %(message)s',
                datefmt='%H:%M:%S',
                level=ERROR)
    error(err)


# Функция логгирования результата опознавания формата:
# "дата распознавания", "текст презультата распознавания"
def log_data(data):
    basicConfig(filename='logs_result.log',
                filemode='a',
                format='%(asctime)s, %(message)s',
                datefmt='%H:%M:%S',
                level=INFO)
    data['datetime'] = data['datetime'].strftime("%Y-%m-%d %H:%M:%S")
    info(str(data).replace('{', '').replace('}', ''))
