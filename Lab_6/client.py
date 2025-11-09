import socket
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    host = config['SERVER']['HOST']
    port = int(config['SERVER']['PORT'])

    while True:
        email = input("Введите email получателя: ")
        text = input("Введите текст сообщения: ")

        # Используем timeout для сокета
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(25)  # Устанавливаем общий тайм-аут 25 секунд
            try:
                s.connect((host, port))
                message = f"{email};{text}"
                s.sendall(message.encode('utf-8'))

                response = s.recv(1024).decode('utf-8')

                if response == "OK":
                    print("Сообщение успешно отправлено.")
                    break
                else:
                    print(f"Получена ошибка от сервера: {response}")
                    retry = input("Хотите попробовать снова? (да/нет): ").lower()
                    if retry != 'да':
                        break
            except socket.timeout:
                print("Ошибка: Сервер не ответил вовремя. Проверьте, работает ли сервер и не завис ли он.")
                break
            except ConnectionRefusedError:
                print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
                break
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}")
                break


if __name__ == "__main__":
    main()