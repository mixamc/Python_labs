import imaplib
import email
from email.header import decode_header
import configparser
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - COLLECTOR - %(levelname)s - %(message)s')


def decode_subject(header):
    """Декодирует тему письма."""
    decoded_parts = decode_header(header)
    subject = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            subject += part.decode(encoding or "utf-8", 'ignore')
        else:
            subject += part
    return subject


def log_to_file(filename, content):
    """Записывает информацию в лог-файл."""
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(content + '\n')


def check_mail(config):
    """Проверяет почтовый ящик и обрабатывает письма."""
    login = config['EMAIL']['EMAIL_LOGIN']
    password = config['EMAIL']['EMAIL_PASSWORD']
    imap_host = config['EMAIL']['IMAP_HOST']

    try:
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(login, password)
        mail.select("inbox")
        status, messages = mail.search(None, "UNSEEN")

        if status != "OK":
            logging.error("Не удалось выполнить поиск сообщений.")
            return

        email_ids = messages[0].split()
        if not email_ids:
            logging.info("Новых писем нет.")
            return

        logging.info(f"Найдено {len(email_ids)} новых писем.")

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            subject = decode_subject(msg["Subject"])

            body = ""
            # Ищем текстовую часть в письме, игнорируя HTML
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        try:
                            charset = part.get_content_charset() or 'utf-8'
                            payload = part.get_payload(decode=True)
                            if payload:
                                body = payload.decode(charset, 'ignore')
                                break
                        except Exception as e:
                            logging.warning(f"Не удалось декодировать часть письма: {e}")
            else:
                try:
                    charset = msg.get_content_charset() or 'utf-8'
                    payload = msg.get_payload(decode=True)
                    if payload:
                        body = payload.decode(charset, 'ignore')
                except Exception as e:
                    logging.warning(f"Не удалось декодировать тело письма: {e}")
                    body = "[Не удалось прочитать тело письма]"

            if "[Ticket #" in subject and "] Mailer" in subject:
                try:
                    ticket_id = subject.split('#')[1].split(']')[0]
                    log_entry = f"ID: {ticket_id}, Сообщение: {body.strip()}"
                    log_to_file("success_request.log", log_entry)
                    logging.info(f"Запись в success_request.log: ID {ticket_id}")
                except IndexError:
                    log_entry = f"Тема: {subject}, Сообщение: {body.strip()}"
                    log_to_file("../error_request.log", log_entry)
            else:
                log_entry = f"Тема: {subject}, Сообщение: {body.strip()}"
                log_to_file("../error_request.log", log_entry)
                logging.info(f"Запись в error_request.log: Тема '{subject}'")

            mail.store(email_id, '+FLAGS', '\\Seen')

        mail.logout()
    except Exception as e:
        logging.error(f"Ошибка при проверке почты: {e}")


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    period = int(config['EMAIL']['PERIOD_CHECK'])

    while True:
        logging.info("Проверка почты...")
        check_mail(config)
        logging.info(f"Следующая проверка через {period} секунд.")
        time.sleep(period)


if __name__ == "__main__":
    main()