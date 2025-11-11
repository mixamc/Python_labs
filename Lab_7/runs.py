import asyncio
import aiofiles
import random
import time
import aiohttp


# ============================================================
# Вспомогательные асинхронные функции
# ============================================================

async def read_file_async(filename: str) -> str:
    """Асинхронное чтение файла."""
    try:
        async with aiofiles.open(filename, mode='r', encoding='utf-8') as f:
            return await f.read()
    except FileNotFoundError:
        return f"Ошибка: Файл '{filename}' не найден."


async def process_data_async(data: str) -> str:
    """Имитация асинхронной обработки данных."""
    print(f"Начало обработки данных: {data}")
    delay = random.uniform(0.5, 2.0)
    await asyncio.sleep(delay)
    result = data.upper()
    print(f"Обработка '{data}' завершена за {delay:.2f} сек.")
    return result


async def greet_after_delay(name: str, delay: float = 2.0):
    """Приветствие с задержкой."""
    await asyncio.sleep(delay)
    print(f"Привет, {name}!")


async def fetch_status(session: aiohttp.ClientSession, url: str):
    """Асинхронная проверка статуса сайта с обработкой ошибок."""
    try:
        async with session.get(url, timeout=10) as response:
            print(f"Сайт: {url}, Статус: {response.status}")
    except aiohttp.ClientError:
        print(f"Сайт: {url}, Ошибка: Не удалось подключиться.")
    except asyncio.TimeoutError:
        print(f"Сайт: {url}, Ошибка: Превышено время ожидания.")
    except Exception as e:
        print(f"Сайт: {url}, Неизвестная ошибка: {e}")


# ============================================================
# Основные задачи
# ============================================================

async def main_task1():
    """Задание 1 — асинхронное чтение файла."""
    print("\n=== Задание 1: Асинхронное чтение файла ===")
    filename = 'test_file.txt'
    async with aiofiles.open(filename, mode='w', encoding='utf-8') as f:
        await f.write('Это тестовый файл для демонстрации асинхронного чтения.')
    content = await read_file_async(filename)
    print(content)
    print("=" * 50)


async def main_task2():
    """Задание 2 — асинхронная обработка данных."""
    print("\n=== Задание 2: Асинхронная обработка данных ===")
    result = await process_data_async("Пример данных для обработки")
    print(f"Результат: {result}")
    print("=" * 50)


async def main_task3():
    """Задание 3 — выполнение задач через asyncio.gather()."""
    print("\n=== Задание 3: Асинхронное выполнение задач ===")
    names = ["Анна", "Борис", "Виктор", "Диана"]
    start = time.time()
    await asyncio.gather(*(greet_after_delay(name) for name in names))
    duration = time.time() - start
    print(f"Все приветствия завершены за {duration:.2f} сек.")
    print("=" * 50)


async def main_tasks4_5():
    """Задания 4 и 5 — асинхронные HTTP-запросы."""
    print("\n=== Задания 4 и 5: Асинхронные HTTP-запросы ===")
    urls = [
        "https://www.google.com",
        "https://www.python.org",
        "https://github.com",
        "https://non-existent-url-12345.com",
        "https://httpbin.org/delay/5",
        "https://invalid-schema",
    ]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(fetch_status(session, url) for url in urls))
    print("=" * 50)


# ============================================================
# Точка входа
# ============================================================

if __name__ == "__main__":
    asyncio.run(main_task1())
    asyncio.run(main_task2())
    asyncio.run(main_task3())
    asyncio.run(main_tasks4_5())