import csv
import os
from datetime import datetime


def create_csv_file(
    filename=None,
    headers=None,
    delimiter=",",
    encoding="utf-8",
    filename_suffix="data",
    download_dir: str = "downloads",
):
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
        filename = f"{download_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename_suffix}.csv"

    with open(filename, "w", newline="", encoding=encoding) as file:
        if headers:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow(headers)

    return os.path.abspath(filename)
