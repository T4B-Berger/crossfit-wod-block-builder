from __future__ import annotations

from typing import Final

DATASET_COLUMNS: Final[list[str]] = [
    "wod_id",
    "date",
    "name",
    "description",
    "format",
    "time_domain",
    "focus",
    "equipment",
    "level_hint",
    "movements",
    "duration_estimate",
    "difficulty_score",
    "score_type",
    "is_benchmark",
]

DATASET_DTYPES: Final[dict[str, str]] = {
    "wod_id": "string",
    "date": "string",
    "name": "string",
    "description": "string",
    "format": "string",
    "time_domain": "string",
    "focus": "string",
    "equipment": "string",
    "level_hint": "string",
    "movements": "string",
    "duration_estimate": "Int64",
    "difficulty_score": "Int64",
    "score_type": "string",
    "is_benchmark": "boolean",
}
