import socket
from threading import Thread
from _thread import start_new_thread
from random import randint


def threaded_first(conn):
    # Получение введенного пользователем идентификатора
    # И преобразование его из byte в str
    identifier = conn.recv(1024).decode('UTF-8')

    # Генерация ключа
    key = randint(0, 1000000)

    # Чтение users.txt и преобразование полученных данных в массив users_list
    file = open("users.txt", "r")
    users_list = [eval(line.strip()) for line in file]
    file.close()

    # Проверка является ли идентификатор уникальным
    for x in users_list:
        if x[0] == identifier:
            conn.send(str.encode(str("error")))     # Отправить сообщение об ошибке в сокет
            conn.close()
            break

    # Если соединение не закрылось после первой проверки продолжать
    if conn.fileno() != -1:

        # Проверка на уникальность сгенерированного ключа
        for x in users_list:
            if x[1] == key:
                while x == key:
                    key = randint(0, 1000000)

        # Отправить ключ в сокет
        conn.send(str.encode(str(key)))

        # Записать нового пользователя в users.txt и закрыть соединение
        file = open("users.txt", "a")
        file.write(str((identifier, str(key))) + "\n")
        file.close()
        conn.close()


def first_sock(sock):   # Функция для сокета с портом 8000
    print("Socket 8000 is running...")

    # Начало прослушивания (до 50 подключений)
    sock.listen(50)
    while True:

        # Ожидать подключение
        conn, addr = sock.accept()
        print('connected:', addr)

        # Создать для подключения отдельный поток (Функция threaded_first)
        start_new_thread(threaded_first, (conn,))


def threaded_second(conn):

    # Чтение users.txt и преобразование полученных данных в массив users_list
    file = open("users.txt", "r")
    users_list = [eval(line.strip()) for line in file]
    file.close()

    # Получение данных для входа и преобразование в str
    identifier = conn.recv(1024).decode('UTF-8')
    key = conn.recv(1024).decode('UTF-8')

    # Проверка на правильный идентификатор и ключ
    for x in users_list:
        if x == (identifier, key):

            # Отправка сообщения об успешном логине в сокет, закодированный в byte
            conn.send(str.encode("Valid"))

            # Получение введенного сообщения от пользователя
            string = conn.recv(1024).decode('UTF-8')

            # Открытие log.txt для записи сообщения
            log = open("log.txt", "a")
            log.write("User: " + identifier + "\nKey: " + key + "\nText: " + string + "\n\n")
            log.close()

    # Если идентификатор и ключ не подошли отправить сообщение о неверных данных
    conn.send(str.encode("Invalid"))

    # Закрыть соединение
    conn.close()


def second_sock(sock):  # Функция для сокета с портом 8000
    print("Socket 8001 is running...")

    # Начало прослушивания (до 50 подключений)
    sock.listen(50)
    while True:

        # Ожидать подключение
        conn, addr = sock.accept()
        print('connected:', addr)

        # Создать для подключения отдельный поток (Функция threaded_second)
        start_new_thread(threaded_second, (conn,))


def server_start():  # Функция создания сокетов и начала работы сервера

    # Создание сокетов
    sock_identifier = socket.socket()
    sock_message = socket.socket()

    # Привязка портов
    sock_identifier.bind(('', 8000))
    sock_message.bind(('', 8001))

    # Создание потоков
    thread_1 = Thread(target=first_sock, args=(sock_identifier,))
    thread_2 = Thread(target=second_sock, args=(sock_message,))

    # Начало потоков первого сокета (Функции first_sock и second_sock)
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()


if __name__ == "__main__":
    server_start()
