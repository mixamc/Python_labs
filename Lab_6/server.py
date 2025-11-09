import socket
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
import logging
import random
import re

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - SERVER - %(levelname)s - %(message)s')


def validate_email(email):
    """Проверяет корректность email-адреса."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)


def send_email(receiver_email, subject, body, config):
    """Отправляет электронное письмо с тайм-аутом."""
    sender_email = config['EMAIL']['EMAIL_LOGIN']
    password = config['EMAIL']['EMAIL_PASSWORD']
    smtp_host = config['EMAIL']['SMTP_HOST']
    smtp_port = int(config['EMAIL']['SMTP_PORT'])

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    try:
        # Добавлен тайм-аут 20 секунд
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=20) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            logging.info(f"Письмо успешно отправлено на {receiver_email}")
            return True
    except socket.timeout:
        logging.error(f"Тайм-аут при отправке письма на {receiver_email}")
        return False
    except Exception as e:
        logging.error(f"Ошибка при отправке письма на {receiver_email}: {e}")
        return False


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    host = config['SERVER']['HOST']
    port = int(config['SERVER']['PORT'])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        logging.info(f"Сервер запущен и слушает на {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                logging.info(f"Подключено: {addr}")
                data = conn.recv(1024).decode('utf-8')
                logging.info(f"Получены данные от {addr}: {data}")

                if not data:
                    break

                try:
                    email, text = data.split(';', 1)
                except ValueError:
                    error_message = "Ошибка: Неверный формат данных. Ожидается 'email;text'."
                    logging.warning(error_message)
                    conn.sendall(error_message.encode('utf-8'))
                    continue

                if not validate_email(email):
                    error_message = f"Ошибка: Некорректный email-адрес '{email}'"
                    logging.warning(error_message)
                    conn.sendall(error_message.encode('utf-8'))
                    continue

                if not text.strip():
                    error_message = "Ошибка: Текст сообщения не может быть пустым."
                    logging.warning(error_message)
                    conn.sendall(error_message.encode('utf-8'))
                    continue

                ticket_id = random.randint(10000, 99999)
                subject = f"[Ticket #{ticket_id}] Mailer"

                admin_email = config['EMAIL']['EMAIL_LOGIN']
                success_user = send_email(email, subject, text, config)
                success_admin = send_email(admin_email, subject, text, config)

                if success_user and success_admin:
                    conn.sendall(b"OK")
                else:
                    error_message = "Ошибка: Не удалось отправить письмо. Проверьте лог сервера."
                    logging.error(error_message)
                    conn.sendall(error_message.encode('utf-8'))


if __name__ == "__main__":
    main()