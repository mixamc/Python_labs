import imaplib
import email
import email.message
import time
import logging
import configparser
from email.header import decode_header
from datetime import datetime, timedelta
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - COLLECTOR - %(levelname)s - %(message)s"
)


# === Вспомогательные функции ===

def decode_subject(header: str) -> str:
    """Декодирует MIME-заголовок темы письма."""
    if not header:
        return ""
    decoded_parts = decode_header(header)
    subject = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            subject += part.decode(encoding or "utf-8", errors="ignore")
        else:
            subject += part
    return subject.strip()


def extract_body(msg: email.message.Message) -> str:
    """Извлекает тело письма (предпочтительно text/plain)."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                charset = part.get_content_charset() or "utf-8"
                try:
                    body = part.get_payload(decode=True).decode(charset, errors="ignore")
                    break
                except Exception:
                    pass
    else:
        try:
            charset = msg.get_content_charset() or "utf-8"
            body = msg.get_payload(decode=True).decode(charset, errors="ignore")
        except Exception:
            body = "[Не удалось прочитать тело письма]"
    return body.strip()


def log_to_file(filename: str, content: str) -> None:
    """Добавляет строку в лог-файл."""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content + "\n")


# === Память обработанных писем ===

PROCESSED_FILE = "processed_ids.txt"


def load_processed_ids() -> set:
    """Загружает уже обработанные UID писем из файла."""
    if not os.path.exists(PROCESSED_FILE):
        return set()
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def save_processed_id(uid: str) -> None:
    """Добавляет UID письма в файл обработанных."""
    with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
        f.write(uid + "\n")


# === Основная логика ===

def check_mail(config: configparser.ConfigParser) -> None:
    """Проверяет новые письма и сохраняет только нужные тикеты."""
    login = config["EMAIL"]["EMAIL_LOGIN"]
    password = config["EMAIL"]["EMAIL_PASSWORD"]
    imap_host = config["EMAIL"]["IMAP_HOST"]

    processed_ids = load_processed_ids()

    try:
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(login, password)
        mail.select("INBOX")

        # --- фильтруем письма за последние сутки ---
        date_since = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        status, messages = mail.uid("search", None, f'(SINCE "{date_since}")')

        if status != "OK":
            logging.error("Ошибка при поиске писем.")
            return

        email_uids = messages[0].split()
        if not email_uids:
            logging.info("Нет новых писем за последние сутки.")
            return

        processed_count = 0

        for uid in email_uids:
            uid_str = uid.decode()

            # Пропускаем, если уже обработан
            if uid_str in processed_ids:
                continue

            status, msg_data = mail.uid("fetch", uid, "(RFC822)")
            if status != "OK":
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            subject = decode_subject(msg.get("Subject", ""))
            body = extract_body(msg)

            if "[Ticket #" in subject and "] Mailer" in subject:
                try:
                    ticket_id = subject.split("#")[1].split("]")[0]
                    log_entry = f"ID: {ticket_id}, Сообщение: {body}"
                    log_to_file("success_request.log", log_entry)
                    processed_count += 1
                    save_processed_id(uid_str)
                    logging.info(f"Обработано письмо Ticket #{ticket_id}")
                except Exception as e:
                    logging.warning(f"Ошибка обработки письма '{subject}': {e}")

        if processed_count == 0:
            logging.info("Новых тикетов не найдено.")
        else:
            logging.info(f"Обработано {processed_count} новых тикет(ов).")

        mail.logout()

    except Exception as e:
        logging.error(f"Ошибка при проверке почты: {e}")


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    period = int(config["EMAIL"]["PERIOD_CHECK"])

    while True:
        logging.info("Проверка входящих писем...")
        check_mail(config)
        logging.info(f"⏱ Следующая проверка через {period} секунд.\n")
        time.sleep(period)


if __name__ == "__main__":
    main()