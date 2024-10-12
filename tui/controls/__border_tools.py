from enum import StrEnum


class SingleBorders(StrEnum):
    UPPER_LEFT   = "┌",
    UPPER_LOWER  = "─",
    UPPER_MIDDLE = "┬",
    UPPER_RIGHT  = "┐",
    LEFT_RIGHT   = "│",
    MIDDLE       = "┼",
    LOWER_LEFT   = "└",
    LOWER_MIDDLE = "┴",
    LOWER_RIGHT  = "┘"


class DoubleBorders(StrEnum):
    UPPER_LEFT   = "╔",
    UPPER_LOWER  = "═",
    UPPER_MIDDLE = "╦",
    UPPER_RIGHT  = "╗",
    LEFT_RIGHT   = "║",
    MIDDLE       = "╬",
    LOWER_LEFT   = "╚",
    LOWER_MIDDLE = "╩",
    LOWER_RIGHT  = "╝"