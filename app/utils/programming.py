from __future__ import annotations

from typing import Any

import pandas as pd

GOAL_PRIORITY = {
    "engine": {"engine", "mixed"},
    "strength": {"strength", "mixed"},
    "gym": {"gym", "mixed"},
    "general": {"engine", "strength", "gym", "mixed"},
}

LEVEL_BASE_DIFFICULTY = {
    "beginner": 4,
    "intermediate": 6,
    "advanced": 8,
}

WEEK_DIFFICULTY_OFFSET = {
    1: 0,
    2: 1,
    3: 2,
    4: -1,
}


def _goal_fit(focus: str, goal: str) -> float:
    focus = (focus or "").strip().lower()
    goal = goal.lower()

    if goal == "general":
        if focus in {"engine", "strength", "gym"}:
            return 2.0
        if focus == "mixed":
            return 1.0
        return 0.0

    if focus == goal:
        return 2.0
    if focus == "mixed":
        return 1.0
    return 0.0


def _duration_fit(duration_estimate: float, max_duration: int) -> float:
    if pd.isna(duration_estimate) or duration_estimate > max_duration:
        return 0.0
    closeness = 1 - abs(float(max_duration) - float(duration_estimate)) / max_duration
    return max(closeness, 0.0)


def _level_fit(row_level: str, requested_level: str) -> float:
    if not row_level:
        return 0.5
    return 1.0 if row_level.lower() == requested_level.lower() else 0.0


def _difficulty_fit(row_difficulty: float, target_difficulty: int) -> float:
    if pd.isna(row_difficulty):
        return 0.0
    return max(0.0, 1 - abs(float(row_difficulty) - float(target_difficulty)) / 10)


def _filter_candidates(
    df: pd.DataFrame,
    level: str,
    equipment: str,
    max_duration: int,
) -> pd.DataFrame:
    filtered = df.copy()
    filtered = filtered[filtered["equipment"].str.lower() == equipment.lower()]
    filtered = filtered[filtered["duration_estimate"] <= max_duration]

    level_filtered = filtered[filtered["level_hint"].str.lower() == level.lower()]
    if not level_filtered.empty:
        filtered = level_filtered

    return filtered


def _pick_week_sessions(
    candidates: pd.DataFrame,
    sessions_per_week: int,
) -> pd.DataFrame:
    if candidates.empty:
        return candidates

    selected_rows = []
    used_formats: set[str] = set()

    for _, row in candidates.iterrows():
        row_format = str(row["format"]).lower()
        if row_format not in used_formats or len(used_formats) >= sessions_per_week:
            selected_rows.append(row)
            used_formats.add(row_format)
        if len(selected_rows) == sessions_per_week:
            break

    if len(selected_rows) < sessions_per_week:
        for _, row in candidates.iterrows():
            if len(selected_rows) == sessions_per_week:
                break
            if any(r["wod_id"] == row["wod_id"] for r in selected_rows):
                continue
            selected_rows.append(row)

    return pd.DataFrame(selected_rows)


def generate_4_week_block(
    df: pd.DataFrame,
    goal: str,
    level: str,
    sessions_per_week: int,
    equipment: str,
    max_duration: int,
) -> dict[str, list[dict[str, Any]]]:
    """Generate a deterministic four-week training block from WOD history."""
    if df.empty:
        return {"weeks": []}

    filtered = _filter_candidates(df=df, level=level, equipment=equipment, max_duration=max_duration)
    if filtered.empty:
        return {"weeks": []}

    remaining = filtered.copy()
    weeks: list[dict[str, Any]] = []

    base_difficulty = LEVEL_BASE_DIFFICULTY.get(level.lower(), 6)

    for week in range(1, 5):
        target_difficulty = base_difficulty + WEEK_DIFFICULTY_OFFSET[week]

        scored = remaining.copy()
        scored["goal_fit"] = scored["focus"].apply(lambda x: _goal_fit(str(x), goal))
        scored["duration_fit"] = scored["duration_estimate"].apply(lambda x: _duration_fit(x, max_duration))
        scored["level_fit"] = scored["level_hint"].apply(lambda x: _level_fit(str(x), level))
        scored["difficulty_fit"] = scored["difficulty_score"].apply(
            lambda x: _difficulty_fit(x, target_difficulty)
        )
        scored["score"] = scored["goal_fit"] + scored["duration_fit"] + scored["level_fit"] + scored["difficulty_fit"]

        scored = scored.sort_values(by=["score", "difficulty_score", "wod_id"], ascending=[False, False, True])
        week_sessions = _pick_week_sessions(scored, sessions_per_week)

        weeks.append(
            {
                "week": week,
                "sessions": week_sessions.to_dict(orient="records"),
            }
        )

        if week_sessions.empty:
            continue

        remaining = remaining[~remaining["wod_id"].isin(week_sessions["wod_id"])]

        if remaining.empty:
            break

    return {"weeks": weeks}
