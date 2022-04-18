create_battle = {
    "type": "object",
    "properties": {
        "ntf_id": {"type": "number"},
        "player_id": {"type": "number"},
    },
}

accept_battle = {
    "type": "object",
    "properties": {
        "offer_id": {"type": "number"},
        "ntf_id": {"type": "number"},
        "player_id": {"type": "number"},
    },
}

start_battle = {
    "type": "object",
    "properties": {
        "offer_id": {"type": "number"},
        "accept_id": {"type": "number"},
    },
}

battle_move = {
    "type": "object",
    "properties": {
        "battle_id": {"type": "number"},
        "player_id": {"type": "number"},
        "choice_id": {"type": "number"},
        "round_id": {"type": "number"},
    },
}