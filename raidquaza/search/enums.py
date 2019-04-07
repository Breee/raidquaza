from enum import Enum

class SCORING_TYPE(Enum):
    LEVENSHTEIN = 1,
    NEEDLEMAN_WUNSCH = 2,
    AFFINE_GAPS = 3

class RECORD_TYPE(Enum):
    GYM = "Gym",
    POKESTOP = "Pokestop",
    QUEST = "Quest",
    PORTAL = "Portal",
    UNKNOWN = "Unknown"
