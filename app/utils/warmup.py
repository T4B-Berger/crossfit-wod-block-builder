from __future__ import annotations


def generate_session_warmup(movements: str, focus: str) -> dict[str, list[str]]:
    general = [
        "4 min easy cyclical work (bike, jog, or row)",
        "2 rounds: 10 air squats, 8 push-ups, 20 s hollow hold",
        "Dynamic mobility: ankles, hips, shoulders (2-3 min)",
    ]

    focus_specific = {
        "engine": [
            "2 rounds at easy pace: 200 m run + 10 light reps of session movements",
            "1 progressive build set to 70% target effort",
        ],
        "strength": [
            "3 technique sets with empty bar or light load",
            "2 build sets to working load with crisp tempo",
        ],
        "gym": [
            "2 rounds of movement pattern drills at low fatigue",
            "1-2 skill progressions for session-specific gymnastics movement",
        ],
        "mixed": [
            "1 round through each movement at low intensity",
            "1 round at moderate intensity with race pace transitions",
        ],
    }

    specific = focus_specific.get(
        focus,
        [
            "2 light prep rounds through session patterns",
            "1 moderate rehearsal set before start",
        ],
    )

    if movements:
        specific.insert(0, f"Movement prep emphasis: {movements}")

    return {"general": general, "specific": specific}
