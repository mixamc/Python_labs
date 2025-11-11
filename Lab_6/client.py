import socket
import configparser

'''
32mixa@gmail.com
Hello! Im from 6'th laborathory work for python
'''
def load_config(filename: str = "config.ini") -> tuple[str, int]:
    """Загружает настройки из config.ini"""
    config = configparser.ConfigParser()
    config.read(filename)

    try:
        host = config["SERVER"]["HOST"]
        port = int(config["SERVER"]["PORT"])
        return host, port
    except KeyError as e:
        raise ValueError(f"Ошибка в конфигурационном файле: отсутствует ключ {e}")


def send_message(host: str, port: int, email: str, text: str) -> str:
    """Отправляет сообщение на сервер и возвращает ответ"""
    message = f"{email};{text}"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(25)
        s.connect((host, port))
        s.sendall(message.encode("utf-8"))
        response = s.recv(1024).decode("utf-8")
        return response


def user_input() -> tuple[str, str]:
    """Запрашивает у пользователя email и текст сообщения"""
    try:
        email = input("Введите email получателя: ").strip()
        text = input("Введите текст сообщения: ").strip()
        return email, text
    except NameError as e:
        raise NameError(f'Ошибка ввода почты получателя: {e}')

def main():

    host, port = load_config()

    while True:
        email, text = user_input()

        try:
            response = send_message(host, port, email, text)
        except socket.timeout:
            print("Ошибка: Сервер не ответил вовремя (тайм-аут).")
            break
        except ConnectionRefusedError:
            print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что он запущен.")
            break
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            break

        if response == "OK":
            print("Сообщение успешно отправлено.")
            break
        else:
            print(f"Ошибка от сервера: {response}")
            retry = input("Повторим отправку? (да/нет): ").strip().lower()
            if retry != "да":
                break


if __name__ == "__main__":
    main()