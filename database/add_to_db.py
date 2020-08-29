from psycopg2 import connect

user = "***"
password = "***"
db = "***"


# Функция добавления записи в базу данных
def add_to_db(data):
    # Прописываем необходимые параметры для подключения к базе данных
    with connect(database=db,
                 user=user,
                 password=password,
                 host='127.0.0.1',
                 port='5432') as conn:
        with conn.cursor() as cur:
            # Проверяем наличии определенной таблицы в базе данных
            cur.execute("SELECT exists(SELECT * FROM information_schema.tables "
                        "WHERE table_name=%s)", ('date_voice',))
            check = cur.fetchone()[0]
            # если этой таблицы нету то создаём её
            if check == False:
                cur.execute('''
                            CREATE TABLE DATE_VOICE  
                                 (datetime DATE NOT NULL,
                                 id INTEGER PRIMARY KEY,
                                 result VARCHAR NOT NULL,
                                 phone_number VARCHAR NOT NULL,
                                 audio_length REAL NOT NULL,
                                 transcript VARCHAR NOT NULL,
                                 project_id VARCHAR,
                                 server_id VARCHAR
                                 );
                                 ''')

            # Подготавливаем данные для записи в базу данных
            columns = ', '.join(str(x).replace('/', '_') for x in data.keys())
            values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in data.values())
            cur.execute("INSERT INTO %s ( %s ) VALUES ( %s );"
                        % ('date_voice', columns, values))
            print('Запись успешна добавленна в базу данных')
