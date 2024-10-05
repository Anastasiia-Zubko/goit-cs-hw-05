import asyncio
import aiofiles
import shutil
from pathlib import Path
import argparse
import logging

# логування
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Асинхронна функція для копіювання файлу
async def copy_file(source: Path, destination: Path):
    try:
        # Створюємо цільову директорію, якщо вона не існує
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Асинхронне копіювання файлу
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, shutil.copy2, source, destination)
        print(f"Copied: {source} -> {destination}")
    except Exception as e:
        logging.error(f"Error copying file {source} to {destination}: {e}")

# Асинхронна функція для читання директорії та копіювання файлів за розширенням
async def read_folder(source_folder: Path, output_folder: Path):
    try:
        # Перебір всіх файлів і папок у вказаній директорії
        for item in source_folder.rglob('*'):
            if item.is_file():
                # Отримуємо розширення файлу
                file_extension = item.suffix.lstrip('.').lower() or 'unknown'
                # Формуємо шлях до відповідної підпапки в директорії призначення
                dest_folder = output_folder / file_extension
                dest_file = dest_folder / item.name
                # Копіюємо файл у відповідну підпапку
                await copy_file(item, dest_file)
    except Exception as e:
        logging.error(f"Error reading folder {source_folder}: {e}")

# Головна асинхронна функція для запуску програми
async def main():
    # Ініціалізуємо парсер аргументів командного рядка
    parser = argparse.ArgumentParser(description="Asynchronous file sorter")
    parser.add_argument("source", type=str, help="Source folder path")
    parser.add_argument("destination", type=str, help="Destination folder path")
    args = parser.parse_args()

    # Перетворюємо шляхи на об'єкти Path
    source_folder = Path(args.source)
    output_folder = Path(args.destination)

    # Перевіряємо, чи існує вихідна папка
    if not source_folder.is_dir():
        logging.error(f"Source folder does not exist: {source_folder}")
        return

    # Створюємо директорію призначення, якщо вона не існує
    output_folder.mkdir(parents=True, exist_ok=True)

    # Виконуємо асинхронне сортування файлів
    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
