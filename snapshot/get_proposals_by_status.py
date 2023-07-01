import requests

URL = "https://hub.snapshot.org/graphql"
QUERY = """
query getProposals($first: Int!, $skip: Int!, $state: String!, $orderDirection: OrderDirection) {
  proposals(
    first: $first,
    skip: $skip,
    orderBy: "end",
    orderDirection: $orderDirection,
    where: { space_in: "cakevote.eth", state: $state }
  ) {
    id
    title
    body
    choices
    start
    end
    snapshot
    state
    author
  }
}
"""
HEADERS = {"Content-Type": "application/json"}


def get_proposals_by_status(status: str = "active", order: str = "asc") -> dict:
    if status not in ["active", "pending", "closed"]:
        raise ValueError("Недопустимое значение статуса, допустимые значения: 'active', 'pending', 'closed'")

    if status == "closed":
        order = "desc"

    variables = {"first": 1000, "skip": 0, "state": status, "orderDirection": order}

    with requests.Session() as session:
        response = session.post(URL, json={"query": QUERY, "variables": variables}, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
