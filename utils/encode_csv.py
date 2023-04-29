import codecs
import logging
import os

import pandas as pd
from pandas import DataFrame


def encode_csv(csv_file_path: str, encoding: str = "utf-8") -> tuple[str, DataFrame]:
    """
    Определяет кодировку CSV-файла и преобразует его в указанную кодировку. Возвращает путь к обработанному файлу и
    DataFrame с его содержимым.

    :param csv_file_path: путь к CSV-файлу.
    :param encoding: кодировка, в которую нужно преобразовать файл.
    :return: кортеж из пути к обработанному файлу и DataFrame с его содержимым.
    """
    logging.info(f"Определяем кодировку файла '{csv_file_path}'...")
    with codecs.open(csv_file_path, "r", "utf-8") as f:
        detected_encoding = f.encoding

    if not detected_encoding or detected_encoding.lower().startswith(encoding):
        df = pd.read_csv(csv_file_path, encoding=encoding)
    else:
        logging.info(f"Преобразуем файл '{detected_encoding}' в файл с кодировкой '{encoding}'...")
        df = pd.read_csv(csv_file_path, encoding=detected_encoding)
        obj_cols = df.select_dtypes(include=["object"]).columns
        df[obj_cols] = df[obj_cols].apply(lambda x: x.str.encode(encoding, "ignore").str.decode(encoding))
        os.remove(csv_file_path)
        csv_file_path = csv_file_path[:-4] + "_" + encoding + ".csv"
        df.to_csv(csv_file_path, encoding=encoding, index=False)

    return csv_file_path, df
