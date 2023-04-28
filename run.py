import argparse
import time
from datetime import datetime

from process_proposals import process_proposals


def run(log_level, interval=None):
    path = "downloads"

    while True:
        start_time = time.monotonic()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_file = f"{path}/core_proposals_{timestamp}.csv"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Начинаю парсинг...")
        try:
            process_proposals(csv_file, path)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Парсинг завершён.")
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ошибка при парсинге. {e}")

        if interval:
            elapsed_time = time.monotonic() - start_time
            elapsed_time = elapsed_time if elapsed_time >= 0 else 0
            if sleep_length := args.interval - elapsed_time > 0:
                time.sleep(sleep_length)
        else:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.add_argument(
        "--interval",
        type=int,
        help="Установите интервал в секундах для автоматического парсинга",
    )
    args = parser.parse_args()

    try:
        run(log_level=args.level, interval=args.interval)
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
