import argparse
import time
from datetime import datetime

from process_proposals import process_proposals


def main():
    parser = argparse.ArgumentParser(description="Запустить скрипт для парсинга PancakeSwap.")
    parser.add_argument(
        "--interval",
        type=int,
        default=86400,
        help="Интервал в секундах, через который запускать скрипт (по умолчанию: 1 день)",
    )
    args = parser.parse_args()

    path = "downloads"

    try:
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

            elapsed_time = time.monotonic() - start_time
            elapsed_time = elapsed_time if elapsed_time >= 0 else 0
            time.sleep(args.interval - elapsed_time)
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")


if __name__ == "__main__":
    main()
