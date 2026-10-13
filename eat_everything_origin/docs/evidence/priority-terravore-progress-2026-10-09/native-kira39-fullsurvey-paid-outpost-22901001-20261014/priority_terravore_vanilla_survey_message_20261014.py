"""Recognize the frozen vanilla Iolam system-survey notification."""
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
MESSAGE_SHA256 = "fa7b25391a05f2b48c77140ca8a2b5eb393559c62f9ef6cec893039ab102fdcd"
FIELDS = ["type", "localization", "variables", "receiver", "target_system",
          "coordinate", "end", "date", "notification", "message_type"]
VALUES = {
    "type": "SYSTEM_SURVEYED",
    "localization": "MESSAGE_FLEET_SYSTEM_FULLY_SURVEYED",
    "receiver": 0,
    "target_system": 191,
    "end": "2290.07.02",
    "date": "2290.04.02",
    "notification": 321,
    "message_type": "none",
}


def official_sources_match():
    return all(hashlib.sha256((GAME / path).read_bytes()).hexdigest() == expected
               for path, expected in OFFICIAL.items())


def is_one_surveyed(messages):
    if len(messages) != 1 or not official_sources_match():
        return False
    message = messages[0]
    return (hashlib.sha256(message.encode("utf-8")).hexdigest() == MESSAGE_SHA256
            and q.scalars(message) == VALUES
            and [key for key, _, _ in q.fields(message)] == FIELDS
            and q.scalars(q.block(message, "coordinate"))
            == {"x": 0, "y": 0, "origin": 4294967295}
            and 'key="SYSTEM"' in q.block(message, "variables")
            and 'value="\u4f0a\u6b27\u62c9\u59c6"' in q.block(message, "variables"))


def admissible(messages):
    return messages == [] or is_one_surveyed(messages)


def transition(before, after, after_date):
    if not admissible(before) or not admissible(after):
        return False
    if before == []:
        return after == []
    return after == before or (after == [] and after_date >= "2290.07.02")
