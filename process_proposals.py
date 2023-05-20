import csv
import logging
from datetime import datetime

from snapshot import get_core_proposals, get_proposal_current_result, get_proposals_by_status

CATEGORIES = {
    "active": "Голосование",
    "pending": "Ожидает",
    "closed": "Закрыто",
}


def format_vote_results(vote, choice) -> dict[str, float]:
    return {k: round(sum(d["vp"] for d in vote if d["choice"] == i), 2) for i, k in enumerate(choice, start=1)}


def process_proposals(csv_file, limit: int = 0) -> None:
    headers = ["Категория", "Название", "Описание", "Дата старта", "Дата завершения"]
    max_num_choices, proposal_count, core_proposals_dict = 0, 0, {}

    for status, category in CATEGORIES.items():
        try:
            proposals = get_proposals_by_status(status)
        except Exception as e:
            raise Exception(f"Произошла ошибка при получении предложений со статусом '{status}': {e}")
        core_proposals = get_core_proposals(proposals)
        core_proposals_dict[status] = core_proposals
        if core_proposals:
            max_num_choices = max(max_num_choices, max(len(proposal["choices"]) for proposal in core_proposals))

    for i in range(max_num_choices):
        headers.append(f"Выбор {i+1}")
        headers.append(f"Сумма {i+1}")

    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for status, category in CATEGORIES.items():
            core_proposals = core_proposals_dict[status]

            rows = []
            for proposal in core_proposals:
                title = proposal["title"].replace("\n", " ")
                description = proposal["body"].replace("\n", " ")
                date_start = datetime.fromtimestamp(proposal["start"]).strftime("%Y-%m-%d %H:%M:%S")
                date_end = datetime.fromtimestamp(proposal["end"]).strftime("%Y-%m-%d %H:%M:%S")
                try:
                    current_results = get_proposal_current_result(proposal["id"])
                    votes = format_vote_results(current_results, proposal["choices"])
                except Exception as e:
                    logging.error(
                        f"Произошла ошибка при получении текущих результатов для пропозала {proposal['id']}: {e}",
                        exc_info=True,
                    )
                    continue

                row = [category, title, description, date_start, date_end]
                for choice, vp_sum in votes.items():
                    row.extend([choice, vp_sum])

                row.extend(["", ""] * (max_num_choices - len(votes)))
                rows.append(row)

                proposal_count += 1

                if limit and limit <= proposal_count:
                    break

            writer.writerows(rows)
