admins = [
    "0x842b508681ee336e74600974b4623b709477d29d",
    "0x977e0c1005dff8749f8cac22f4df0bd5f013d1a7",
    "0xa3d2124e4023ea5c74dc749012e0b46e42bdd648",
    "0x4634fc1462b7974db96b700e9abe915f0884e60a",
    "0xa7551abe0a066555cb5d859849426fb55543ca25",
]


def get_core_proposals(data):
    return [proposal for proposal in data["data"]["proposals"] if proposal["author"].lower() in admins]
