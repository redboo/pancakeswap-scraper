import logging
import os

from .encode_csv import encode_csv


def convert_csv_to_excel(
    csv_file_path: str, encoding: str = "utf-8", output_csv: bool = False, output_excel: bool = True
) -> tuple[str, str]:
    """
    Преобразует CSV-файл в Excel-файл, используя указанную кодировку.

    :param csv_file_path: путь к CSV-файлу.
    :param encoding: кодировка CSV-файла (по умолчанию "utf-8").
    :param output_csv: если True, то сохраняет преобразованный CSV-файл (по умолчанию False).
    :param output_excel: если True, то сохраняет преобразованный Excel-файл (по умолчанию True).
    :return: кортеж из пути к обработанному CSV-файлу и Excel-файлу.
    """
    allowed_encodings = ["utf-8", "cp1251"]
    encoding = encoding.lower()

    if encoding not in allowed_encodings:
        raise ValueError(f"Кодировка должна быть одной из следующих: {', '.join(allowed_encodings)}")

    csv_file_path, df = encode_csv(csv_file_path, encoding)

    excel_file_path = ""
    if output_excel:
        logging.info(f"Преобразуем файл '{csv_file_path}' в Excel-файл...")
        excel_file_path = f"{os.path.splitext(csv_file_path)[0]}.xlsx"
        df.to_excel(excel_file_path, index=False)

        if not output_csv:
            os.remove(csv_file_path)
            csv_file_path = ""

    return csv_file_path, excel_file_path
