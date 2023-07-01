import csv
import logging
from datetime import datetime

from snapshot import get_core_proposals, get_proposal_current_result, get_proposals_by_status

STATUS = ("active", "pending", "closed")


def format_vote_results(vote: list[dict], choice: list[str]) -> dict[str, float]:
    return {k: round(sum(d["vp"] for d in vote if d["choice"] == i), 2) for i, k in enumerate(choice, start=1)}


def process_proposals(csv_file: str, limit: int = 0) -> None:
    headers = ["status", "title", "description", "start_date", "end_date"]
    max_num_choices, proposal_count, core_proposals_dict = 0, 0, {}

    for status in STATUS:
        try:
            proposals = get_proposals_by_status(status)
        except Exception as e:
            raise Exception(f"Произошла ошибка при получении предложений со статусом '{status}': {e}") from e
        core_proposals = get_core_proposals(proposals)
        core_proposals_dict[status] = core_proposals
        if core_proposals:
            max_num_choices = max(max_num_choices, max(len(proposal["choices"]) for proposal in core_proposals))

    for i in range(max_num_choices):
        headers.extend((f"choice_{i + 1}", f"amount_{i + 1}"))

    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for status in STATUS:
            core_proposals = core_proposals_dict[status]

            rows = []
            for proposal in core_proposals:
                try:
                    votes = format_vote_results(get_proposal_current_result(proposal["id"]), proposal["choices"])
                except Exception as e:
                    logging.error(
                        f"Произошла ошибка при получении текущих результатов для пропозала {proposal['id']}: {e}",
                        exc_info=True,
                    )
                    continue

                row = [
                    status,
                    proposal["title"].replace("\n", " "),
                    proposal["body"].replace("\n", " "),
                    datetime.fromtimestamp(proposal["start"]).strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.fromtimestamp(proposal["end"]).strftime("%Y-%m-%d %H:%M:%S"),
                ]
                total_sum = sum(votes.values())
                for choice, value in votes.items():
                    try:
                        row.extend([choice, f"{(value / total_sum) * 100:.2f}%"])
                    except ZeroDivisionError:
                        row.extend([choice, 0])

                row.extend(["", ""] * (max_num_choices - len(votes)))
                rows.append(row)

                proposal_count += 1

                if limit and limit <= proposal_count:
                    break

            writer.writerows(rows)
