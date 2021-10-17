import socket


def connection():
    # Cоздание сокета и таймаута подключения
    sock = socket.socket()
    sock.settimeout(10)

    # Ввод порта
    port = int(input('Input port (8000 or 8001)\n'))

    # Порт 8000 нужен для ввода идентификатора и получения ключа к нему
    if port == 8000:

        # Ввод идентификатора (логина)
        identifier = input("Input your identifier: ")

        # Подключение к порту и отправка идентификатора
        sock.connect(('localhost', port))
        sock.send(str.encode(identifier))

        # Получение ключа из сокета и преобразование из byte в str . При повторении идентификатора сервер выдаст error
        key = sock.recv(1024).decode('UTF-8')
        if key != "error":
            # Вывод данных клиенту
            print("\n-----------\nYour identifier and unique key for connect:\n" + identifier + "\n" + key)
        else:
            print("This identifier already exist")

        # Закрытие соединения
        sock.close()

    # Порт 8001 нужен для отправки сообщений серверу
    elif port == 8001:

        # Подключение к порту
        sock.connect(('localhost', port))

        # Ввод данных для входа и их отправка
        identifier = input("Input your identifier: ")
        sock.send(str.encode(identifier))
        key = input("Input your key: ")
        sock.send(str.encode(key))

        # Ожидание ответа от сервера
        data = sock.recv(1024).decode('UTF-8')

        # Если идентификатор и ключ подошли, сервер отправил Valid, начинаем отправку сообщения
        if data == 'Valid':
            string = input("LOGGED\nWrite message: ")
            sock.send(str.encode(string))
            sock.close()

        else:
            print("LOGIN is invalid")
            sock.close()

    # Если введен другой порт то raise
    else:
        print("Incorrect port")


if __name__ == "__main__":
    connection()
