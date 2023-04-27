import csv
import os

from snapshot import get_core_proposals, get_proposal_current_result, get_proposals_by_status

CATEGORIES = {
    "active": "Голосование",
    "pending": "Ожидает",
    "closed": "Закрыто",
}


def format_vote_results(current_results, choices):
    return {
        choice: f"{sum(vote['vp'] for vote, c in zip(current_results, choices) if c == choice):,.2f}"
        for choice in choices
    }


def process_proposals(csv_file, path="downloads"):
    os.makedirs(path, exist_ok=True)

    headers = ["Категория", "Название", "Описание"]
    max_num_choices = 0
    core_proposals_dict = {}

    for status, category in CATEGORIES.items():
        try:
            proposals = get_proposals_by_status(status)
        except Exception as e:
            raise Exception(f"Произошла ошибка при получении предложений со статусом '{status}': {e}")
        core_proposals = get_core_proposals(proposals)
        core_proposals_dict[status] = core_proposals
        if core_proposals:
            max_num_choices = max(max_num_choices, max([len(proposal["choices"]) for proposal in core_proposals]))

    for i in range(max_num_choices):
        headers.append(f"Выбор {i+1}")
        headers.append(f"Сумма {i+1}")

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for status, category in CATEGORIES.items():
            core_proposals = core_proposals_dict[status]

            rows = []
            for proposal in core_proposals:
                title = proposal["title"].replace("\n", " ")
                description = proposal["body"].replace("\n", " ")
                try:
                    current_results = get_proposal_current_result(proposal["id"])
                    votes = format_vote_results(current_results, proposal["choices"])
                except Exception as e:
                    raise Exception(
                        f"Произошла ошибка при получении текущих результатов для пропозала {proposal['id']}: {e}"
                    )

                row = [category, title, description]
                for choice, vp_sum in votes.items():
                    row.extend([choice, vp_sum])

                row.extend(["", ""] * (max_num_choices - len(votes)))
                rows.append(row)

            writer.writerows(rows)

    print(f"Данные сохранены в файле {csv_file}")
