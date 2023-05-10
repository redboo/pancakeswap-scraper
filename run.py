import logging
import os
import time
from datetime import datetime

import click

from process_proposals import process_proposals
from utils import convert_csv_to_excel, create_csv_file

DOWNLOAD_DIR = "downloads"


def setup_logging(level) -> None:
    """Настройка логирования.

    Args:
        level (str): Уровень логирования.
    """
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s: %(message)s")


@click.command()
@click.option(
    "--interval",
    default=None,
    type=int,
    help="Установите интервал в секундах для автоматического парсинга (по умолчанию не установлен)",
)
@click.option(
    "--log-level",
    "--logging",
    "--log",
    default="WARNING",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    help="Установите уровень логирования (по умолчанию: WARNING)",
)
@click.option(
    "--csv",
    is_flag=True,
    default=False,
    help="Укажите этот параметр, чтобы сохранить данные в CSV-файл (по умолчанию: сохранять)",
)
@click.option(
    "--excel",
    is_flag=True,
    default=False,
    help="Укажите этот параметр, чтобы сохранить данные в Excel-файл (по умолчанию: не сохранять)",
)
@click.option(
    "--encoding",
    default="utf-8",
    help="Укажите кодировку для сохранения в CSV и Excel (по умолчанию: utf-8)",
)
@click.option(
    "--limit",
    default=None,
    type=int,
    help="Укажите максимальное количество тем-топиков для парсинга (по умолчанию не ограничено)",
)
def run(log_level, interval=None, csv=False, excel=False, encoding="utf-8", limit=None):
    """Запускает скрипт для парсинга комментариев с сайта.

    Args:
        log_level (str): Уровень логирования.
        interval (int, optional): Интервал в секундах для автоматического парсинга. Defaults to None.
        csv (bool, optional): Сохранять данные в CSV-файл. Defaults to False.
        excel (bool, optional): Сохранять данные в Excel-файл. Defaults to False.
        limit (int, optional): Максимальное количество тем-топиков для парсинга. Defaults to None.
        encoding (str, optional): Кодировка для сохранения в CSV и Excel. Defaults to "utf-8".
    """
    setup_logging(log_level)
    excel_file = None
    while True:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        csv_file = create_csv_file(filename_suffix="core_proposals", download_dir=DOWNLOAD_DIR)
        start_time = time.monotonic()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Парсинг запущен...")

        try:
            process_proposals(csv_file, limit=limit)
            if excel or csv or encoding != "utf-8":
                excel_file = csv_file[:-3] + "xlsx"
                csv_file, excel_file = convert_csv_to_excel(
                    csv_file, encoding=encoding, output_csv=csv, output_excel=excel
                )
            print(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Парсинг завершен. "
                f"Данные cохранены в: {excel_file or csv_file}"
            )
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ошибка при парсинге. {e}")

        if interval:
            elapsed_time = time.monotonic() - start_time
            elapsed_time = elapsed_time if elapsed_time >= 0 else 0
            if (sleep_length := interval - elapsed_time) > 0:
                time.sleep(sleep_length)
        else:
            break


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
