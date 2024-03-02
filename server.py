# Библиотека http.server содержит базовые классы HTTP-серверов.
# Класс HTTPServer создает и прослушивает HTTP-сокет, отправляя запросы обработчику.
# Класс BaseHTTPRequestHandler используется для обработки HTTP-запросов, поступающих на сервер.
from http.server import HTTPServer, BaseHTTPRequestHandler

# Константы HOST и PORT определяют IP-адрес и порт, на котором будет работать HTTP-сервер.
# IP-адрес localhost (127.0.0.1) позволяет взаимодействовать программам -сервер и -клиент, работающим на одном компьютере.
# Порт 8000 является портом по умолчанию (наряду с 80, 8080 и другими), который используется для предоставления веб-сервисов.
HOST, PORT = ('127.0.0.1', 8000)
# Константа OK определяет код состояния 200 (OK), который указывает на успешное выполнение запроса.
OK = 200

# Сам по себе класс BaseHTTPRequestHandler не может отвечать ни на какие фактические HTTP-запросы.
# Он должен быть подклассом для обработки каждого метода запроса.
# Таким образом, объявляем класс CustomHandler, который наследуется от класса BaseHTTPRequestHandler.
class MyRequestHandler(BaseHTTPRequestHandler):
    # Обработчик анализирует запрос и заголовки, а затем вызывает метод, соответствующий типу запроса.
    # Таким образом, метод do_GET() будет вызываться для GET-запроса (имя запроса чувствительно к регистру).
    def do_GET(self) -> None:
        # Метод send_response(code, message=None) отправляет заголовок ответа и записывает принятый запрос.
        # Таким образом, отправляем клиенту код ответа 200 (OK), который информирует об успешном соединении с сервером.
        self.send_response(OK)
        # Метод send_header(keyword, value) добавляет HTTP-заголовок во внутренний буфер,
        # который состоит из коючевого слова (заголовока) keyword и значения value.
        # Таким образом, добавляем заголовок Content-Type: text,
        # который определяет в каком формате (text) будут передаваться данные в теле запроса или ответа.
        self.send_header('Content-Type', 'text')
        # Метод end_headers() завершает запись заголовков в буфер заголовков и вызывает метод flush_headers(),
        # который отправляет заголовки в выходной поток и очищает внутренний буфер заголовков.
        self.end_headers()
        # Объект wfile cодержит поток вывода для обратной записи ответа клиенту.
        # Вывод сообщения message в браузер осуществляется методом wfile.write(message).
        # Метод string.write(encoding='utf-8') кодирует строку string с использованием кодировки encoding.
        # Таким образом, выводим клиенту ответ в виде сообщения Hello, World!.
        self.wfile.write('Hello, World!'.encode())


# Если исполняемый файл является основной программой,
# то интерпретатор присваивает специальной переменной __name__ значение '__main__'.
# Таким образом, условная конструкция if __name__ == '__main__' позволяет избежать случайного вызова модулей,
# которые были импортирован в основную программу.
if __name__ == '__main__':
    # Создаём экземпляр объекта HTTPServer, который будет слушать входящие HTTP-запросы на указанном адресе и порту,
    # используя указанный обработчик запросов.
    # Класс HTTPServer (базовый HTTP-сервер) создаёт сервер, который может обрабатывать HTTP-запросы.
    # HTTP-сервер будет работать на IP-адресе HOST и порте PORT.
    # Класс MyRequestHandler определяет, как сервер будет обрабатывать различные типы HTTP-запросов.
    # Таким образом, экземпляр server будет использоваться для управления сервером, включая его запуск и остановку.
    server = HTTPServer((HOST, PORT), MyRequestHandler)
    # Сообщаем о запуске HTTP-сервера.
    print(f'Server started at http://{HOST}:{PORT}')
    # Метод serve_forever() имеет у себя под капотом бесконечный цикл,
    # поэтому блок кода в теле конструкции try будет выполняься до тех пор, пока цикл не завершит свою работу.
    try:
        # Метод serve_forever() запускает работу сервера, т.е. постоянно ожидает,
        # принимает и обрабатывает запросы до тех пор, пока его работа не будет прервана.
        server.serve_forever()
    # Если пользователь досрочно прерывает работу сервера с помощью сочетания клавиш Ctrl + C,
    # то коректно завершаем работу сервера.
    except KeyboardInterrupt:
        # Уведомляем пользователя о завершении работы сервера.
        print('Interrupted by user!')
    # Блок кода в теле конструкции finally выполниться при прерывании работы сервера.
    finally:
        # Метод server_close() завершает работу сервера,
        # т.е. останавливает прослушку запросов, закрывает соединение и освобождает ресурсы.
        server.server_close()