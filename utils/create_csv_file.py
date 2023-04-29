import csv
import os
from datetime import datetime

DOWNLOADS_DIR = "downloads"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_csv_file(filename=None, headers=None, delimiter=",", encoding="utf-8", filename_prefix="data"):
    """
    Функция создает новый CSV-файл с заданными параметрами.

    Аргументы:
     - filename: str (default=None) - название файла. Если None, то имя файла генерируется автоматически.
     - headers: list (default=None) - список заголовков. Если None, то заголовок не записывается в файл.
     - delimiter: str (default=',') - разделитель, который будет использоваться в CSV-файле.
     - encoding: str (default='utf-8') - кодировка файла.
     - filename_prefix: str (default='data') - префикс для названия файла.

    Возвращает путь к созданному файлу.

    Исключения:
    - OSError: при ошибке создания директории или файла.
    """
    if filename is None:
        filename = f"{filename_prefix}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    file_pathname = os.path.join(BASE_DIR, DOWNLOADS_DIR, filename)

    try:
        with open(file_pathname, "w", newline="", encoding=encoding) as file:
            if headers:
                writer = csv.writer(file, delimiter=delimiter)
                writer.writerow(headers)
    except OSError as e:
        raise OSError(f"Ошибка при создании файла: {e}")

    return file_pathname
