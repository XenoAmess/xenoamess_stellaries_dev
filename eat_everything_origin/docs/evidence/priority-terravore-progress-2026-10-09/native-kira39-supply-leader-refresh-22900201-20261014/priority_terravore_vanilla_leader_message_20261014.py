"""Recognize the one official 2290 recruitable-leader refresh message."""
import hashlib
from pathlib import Path

import audit_save as q

GAME = Path("C:/SteamLibrary/steamapps/common/Stellaris")
OFFICIAL = {
    "common/message_types/00_message_types.txt":
        "b9457c4434ef69ac407c0850a34b80a66ed93b70ec1140858045caba406a7904",
    "localisation/simp_chinese/messages_l_simp_chinese.yml":
        "7b3d8417034fe50d626cb90cc5f02d9500407338558d5c9304c718924199f8b5",
}
FIELDS = ["type", "localization", "receiver", "coordinate", "end", "date",
          "notification", "message_type"]
VALUES = {
    "type": "LEADER_POOL_REFRESHED_MESSAGE_TYPE",
    "localization": "LEADER_POOL_REFRESHED_TITLE",
    "receiver": 0,
    "end": "2290.04.01",
    "date": "2290.01.01",
    "notification": 320,
    "message_type": "leader_pool",
}


def official_sources_match():
    return all(hashlib.sha256((GAME / path).read_bytes()).hexdigest() == expected
               for path, expected in OFFICIAL.items())


def is_one_refresh(messages):
    if len(messages) != 1 or not official_sources_match():
        return False
    message = messages[0]
    return (q.scalars(message) == VALUES
            and q.scalars(q.block(message, "coordinate"))
            == {"x": 0, "y": 0, "origin": 4294967295}
            and [k for k, _, _ in q.fields(message)] == FIELDS)


def admissible(messages):
    return messages == [] or is_one_refresh(messages)


def transition(before, after, after_date):
    if not admissible(before) or not admissible(after):
        return False
    if before == []:
        return after == []
    return after == before or (after == [] and after_date >= "2290.04.01")
