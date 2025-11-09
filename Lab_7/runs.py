import asyncio
import aiofiles
import random
import time
import aiohttp

# --- Задание 1 ---
async def read_file_async(filename):
    try:
        async with aiofiles.open(filename, mode='r', encoding='utf-8') as f:
            contents = await f.read()
            return contents
    except FileNotFoundError:
        return f"Ошибка: Файл '{filename}' не найден."

async def main_task1():
    async with aiofiles.open('test_file.txt', mode='w', encoding='utf-8') as f:
        await f.write('Это тестовый файл для демонстрации асинхронного чтения.')
    file_content = await read_file_async('test_file.txt')
    print("--- Задание 1: Асинхронное чтение файла ---")
    print(file_content)
    print("-" * 45)

# --- Задание 2 ---
async def process_data_async(data):
    print(f"Начало обработки данных: {data}")
    processing_time = random.uniform(0.5, 2.0)
    await asyncio.sleep(processing_time)
    processed_data = data.upper()
    print(f"Обработка данных '{data}' завершена за {processing_time:.2f} сек.")
    return processed_data

async def main_task2():
    print("\n--- Задание 2: Асинхронная обработка данных ---")
    result = await process_data_async("Пример данных для обработки")
    print(f"Результат: {result}")
    print("-" * 49)

# --- Задание 3 ---
async def greet_after_delay(name):
    await asyncio.sleep(2)
    print(f"Привет, {name}!")

async def main_task3():
    print("\n--- Задание 3: Асинхронное выполнение задач с asyncio.gather() ---")
    names = ["Анна", "Борис", "Виктор", "Диана"]
    tasks = [greet_after_delay(name) for name in names]
    start_time = time.time()
    await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Все приветствия выведены за {end_time - start_time:.2f} сек.")
    print("-" * 65)

# --- Задания 4 и 5 ---
async def fetch_status(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            print(f"Сайт: {url}, Статус: {response.status}")
    except aiohttp.ClientError:
        print(f"Сайт: {url}, Ошибка: Не удалось подключиться (Ошибка клиента).")
    except asyncio.TimeoutError:
        print(f"Сайт: {url}, Ошибка: Превышено время ожидания.")
    except Exception as e:
        print(f"Сайт: {url}, Ошибка: Произошла неизвестная ошибка - {e}.")

async def main_tasks4_5():
    print("\n--- Задания 4 и 5: Асинхронные HTTP-запросы с обработкой исключений ---")
    urls = [
        "https://www.google.com",
        "https://www.python.org",
        "https://github.com",
        "https://non-existent-url-12345.com",
        "https://httpbin.org/delay/5",
        "https://invalid-schema",
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_status(session, url) for url in urls]
        await asyncio.gather(*tasks)
    print("-" * 75)


if __name__ == "__main__":
    asyncio.run(main_task1())
    asyncio.run(main_task2())
    asyncio.run(main_task3())
    asyncio.run(main_tasks4_5())