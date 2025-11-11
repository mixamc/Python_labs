import socket
import smtplib
import ssl
import random
import re
import logging
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - SERVER - %(levelname)s - %(message)s"
)

# аннотация типов

def validate_email(email: str) -> bool:
    """Проверяет корректность email-адреса."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None



def load_config(filename: str = "config.ini") -> configparser.ConfigParser:
    """Загружает конфигурацию из config.ini."""
    config = configparser.ConfigParser()
    config.read(filename)
    return config


# ----------------------------
# ОТПРАВКА EMAIL
# ----------------------------
def send_email(receiver_email: str, subject: str, body: str, config: configparser.ConfigParser) -> bool:
    """Отправляет письмо с заданной темой и телом через SMTP."""
    sender_email = config["EMAIL"]["EMAIL_LOGIN"]
    password = config["EMAIL"]["EMAIL_PASSWORD"]
    smtp_host = config["EMAIL"]["SMTP_HOST"]
    smtp_port = int(config["EMAIL"]["SMTP_PORT"])

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    context = ssl._create_unverified_context()

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=20) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            logging.info(f"Письмо отправлено на {receiver_email}")
            return True
    except (socket.timeout, smtplib.SMTPException, Exception) as e:
        logging.error(f"Ошибка при отправке письма на {receiver_email}: {e}")
        return False


def handle_client(conn: socket.socket, addr, config: configparser.ConfigParser):
    """Обрабатывает подключение от клиента и отправляет письмо."""
    logging.info(f"Подключено: {addr}")

    try:
        data = conn.recv(1024).decode("utf-8")
        logging.info(f"Получены данные: {data}")

        if not data:
            return

        # --- Разделяем email и текст ---
        try:
            email, text = data.split(";", 1)
        except ValueError:
            error_msg = "Ошибка: неверный формат данных.\nОжидается: 'email;text'."
            conn.sendall(error_msg.encode("utf-8"))
            return

        # --- Проверка email ---
        if not validate_email(email):
            error_msg = f"Ошибка: некорректный email-адрес.\nПолучено: '{email}'."
            conn.sendall(error_msg.encode("utf-8"))
            return

        # --- Проверка текста сообщения ---
        if not text.strip():
            error_msg = "Ошибка: текст сообщения не может быть пустым."
            conn.sendall(error_msg.encode("utf-8"))
            return

        # --- Генерация темы письма ---
        ticket_id = random.randint(10000, 99999)
        subject = f"[Ticket #{ticket_id}] Mailer"

        admin_email = config["EMAIL"]["EMAIL_LOGIN"]

        # --- Отправка писем ---
        success_user = send_email(email, subject, text, config)
        success_admin = send_email(admin_email, subject, text, config)

        if success_user and success_admin:
            conn.sendall(b"OK")
            logging.info(f"Письма успешно отправлены ({ticket_id}) → {email}, {admin_email}")
        else:
            error_msg = "Ошибка: не удалось отправить письмо.\nПроверьте логи сервера."
            conn.sendall(error_msg.encode("utf-8"))
            logging.error(error_msg)

    except Exception as e:
        error_msg = f"Ошибка сервера при обработке запроса:\n{e}"
        conn.sendall(error_msg.encode("utf-8"))
        logging.error(error_msg)

    finally:
        conn.close()
        logging.info(f"Соединение с {addr} закрыто.")


def main():
    config = load_config()
    host = config["SERVER"]["HOST"]
    port = int(config["SERVER"]["PORT"])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        logging.info(f"Сервер запущен и слушает на {host}:{port}")

        while True:
            conn, addr = server.accept()
            handle_client(conn, addr, config)


if __name__ == "__main__":
    main()