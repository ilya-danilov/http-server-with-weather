# Библиотека psycopg - это система управления базами данных.
# Позволяет подключаться к базе данных, выполнять SQL-запросы, обрабатывать результаты и другое.
import psycopg
# Библиотека dotenv позволяет управлять переменными окружения.
# Переменные окружения - это переменные,
# которые в целях безопасности не должны находится непосредственно в самом проекте.
# Эти переменные хранятся в файле .env, который в свою очередь не включается в систему контроля версий.
import dotenv
# Импортируем модуль os, с помощью которого будем считывать значения переменных окружения.
import os

# Функция connect() создает подключение к базе данных и возвращает кортеж,
# содержащий объект подключения и курсор для выполнения SQL-запросов.
def connect() -> tuple[psycopg.Connection, psycopg.Cursor]:
    # Загружаем переменные окружения из файла .env в текущий файл.
    dotenv.load_dotenv()
    # os.environ - это объект сопоставления, который представляет переменные окружения.
    # Возвращает словарь, содержащий названия переменных окружения в качестве ключей
    # и их значения в качестве значений ключей.
    # Метод get(key) возвращает значение ключа словаря по ключю.
    env_vars = os.environ
    # Записываем в словарь credentials данные для подключение к базе данных.
    # В качестве ключей - названия данных, в качестве значений ключей - значения данных.
    port = env_vars.get('PG_PORT')
    credentials = {
        'host': env_vars.get('PG_HOST', default='127.0.0.1'),
        # Предотвращаем ввод некоректных данных с помощью проверки значения порта на то,
        # является ли оно числом.
        'port': int(port) if port.isdigit() else 5555,
        'dbname': env_vars.get('PG_DBNAME', default='test'),
        'user': env_vars.get('PG_USER', default='test'),
        'password': env_vars.get('PG_PASSWORD'),
    }
    # Оператор "**" в **credentials распаковывает пары словаря credentials в значения ключей,
    # которые в качестве значений передаются в метод psycopg.connect(**credentials).
    # Метод psycopg.connect(**credentials) создаёт объект соединения с базой данных,
    # который предоставляет методы для взаимодействия с ней.
    connection = psycopg.connect(**credentials)
    # Метод connection.cursor() создаёт курсор.
    # Курсор - это объект, который используется для выполнения SQL-запросов к базе данных
    # и получения результатов этих запросов.
    # Курсор является адаптером между базой данных и клиентом.
    cursor = connection.cursor()
    # Возвращаем кортеж, содержащий объект подключения connection и курсор cursor.
    return connection, cursor

# Функция get_cities(cursor: psycopg.Cursor) выполняет SQL-запрос к базе данных,
# с помощью которого получает все записи (города) из таблицы city
# и возвращает эти записи в виде списка кортежей.
def get_cities(cursor: psycopg.Cursor) -> list[tuple]:
    # Метод cursor.execute('select * from city;') выполняет SQL-запрос,
    # с пмощью которого выбираются все записи (города) из таблицы city.
    # Этот метод сами записи не возвращает.
    cursor.execute('select * from city;')
    # Метод cursor.fetchall() извлекает все записи (города) из выборки по одному и помещает их в список
    # (при этом нужно учитывать, что данные в таблице неупорядочены).
    # Этот метод работает подобно методу pop().
    # При первом вызове извлекает все записи, при последующих - пустой список.
    #
    # Метод cursor.fetchmany(size) извлекает определённое количество записей, равное size.
    # Метод cursor.fetchone() извлекает первую запись.
    cities = cursor.fetchall()
    # Возвращаем полученные записи (города) в виде списка кортежей,
    # где каждый кортеж представляет собой одну запись (город) из таблицы city.
    return cities