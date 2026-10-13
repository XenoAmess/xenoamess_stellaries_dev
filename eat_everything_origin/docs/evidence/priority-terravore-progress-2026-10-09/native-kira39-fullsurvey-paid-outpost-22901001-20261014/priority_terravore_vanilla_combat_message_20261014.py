"""Recognize the frozen native Kira 39 crystal battle report."""
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
MESSAGE_SHA256 = "91f16b30095bb3e7d34967680bd4c5e5a6149bfd46598a7571769a5b84a50852"
VALUES = {
    "type": "COMBAT_STATS",
    "receiver": 0,
    "end": "2290.06.24",
    "date": "2290.05.09",
    "notification": 322,
    "message_type": "combat_stats",
}


def is_one_crystal_battle(message):
    return (
        all(hashlib.sha256((GAME / path).read_bytes()).hexdigest() == expected
            for path, expected in OFFICIAL.items())
        and hashlib.sha256(message.encode("utf-8")).hexdigest() == MESSAGE_SHA256
        and q.scalars(message) == VALUES
        and [key for key, _, _ in q.fields(message)]
        == ["type", "receiver", "coordinate", "end", "date", "notification",
            "combat_stats", "message_type"]
        and q.scalars(q.block(message, "coordinate"))["origin"] == 39
        and all(("fleet=" + fleet) in q.block(message, "combat_stats")
                for fleet in ("50332250", "83886903", "917", "33555324"))
    )


def expected_pair(messages, survey):
    return (len(messages) == 2 and survey.is_one_surveyed(messages[:1])
            and is_one_crystal_battle(messages[1]))
