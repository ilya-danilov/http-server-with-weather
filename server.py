from http.server import HTTPServer, BaseHTTPRequestHandler

# Импортируем файл db.py, с помощью которого будем получать записи (города) из таблицы city.
import db

HOST, PORT = ('127.0.0.1', 8000)
OK = 200
# Константа MAIN_PAGE определяет путь к файлу index.html.
MAIN_PAGE = 'index.html'

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(OK)
        # Заменяем заголовок Content-Type: text на Content-Type: text/html,
        # т.к. теперь в качестве ответа на GET-запрос данные в теле ответа передаются в html-формате.
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        # Контекстный менеджер with автоматически освобождает ресурсы
        # (закрывает файлы) после завершения их использования.
        # Функция open(file_path, mode) открывает файл по его пути file_path
        # в соответствии с режимом открытия.
        # Ключевое слово as присваивает открытый файл переменной file.
        with open(MAIN_PAGE, 'r') as file:
            # Метод read() считывает содержимое файла в переменную page.
            page = file.read()
        # Получаем список городов из базы данных с помощью метода db.get_cities(self.db_cursor),
        # преобразуем каждый город в строку и объединяем их в одну строку,
        # разделяя символом переноса строки в HTML.
        cities = '<br>'.join(str(city) for city in db.get_cities(self.db_cursor))
        # С помощью форматирования вставляем названия городов в содержимое html-файла.
        page_with_datetime = page.format(cities=cities)
        # В качестве тела ответа на GET-запрос отправляем закодированные данные в html-формате.
        self.wfile.write(page_with_datetime.encode())


if __name__ == '__main__':
    server = HTTPServer((HOST, PORT), MyRequestHandler)
    print(f'Server started at http://{HOST}:{PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Interrupted by user!')
    finally:
        server.server_close()