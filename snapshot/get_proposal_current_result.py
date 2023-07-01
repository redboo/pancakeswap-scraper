import requests

URL = "https://hub.snapshot.org/graphql"
QUERY = """
query getVotes($first: Int!, $skip: Int!, $where: VoteWhere) {
  votes(first: $first, skip: $skip, where: $where) {
    choice
    vp
  }
}
"""
HEADERS = {"Content-Type": "application/json"}


def get_proposal_current_result(proposal_id: int) -> list[dict]:
    variables = {"first": 1000, "skip": 0, "where": {"proposal": proposal_id}}
    with requests.Session() as session:
        response = session.post(URL, json={"query": QUERY, "variables": variables}, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("votes", [])
