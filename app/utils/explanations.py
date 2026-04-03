from __future__ import annotations


def generate_block_explanation(goal: str, sessions_per_week: int) -> str:
    goal_label = goal.capitalize()
    return (
        f"This 4-week block targets **{goal_label}** with **{sessions_per_week} sessions per week**. "
        "Week 1 establishes a manageable base, week 2 increases training demand, "
        "week 3 is the highest loading week, and week 4 reduces stress to support recovery "
        "while maintaining movement quality and consistency."
    )


def generate_session_stimulus(
    wod_format: str,
    focus: str,
    time_domain: str,
    difficulty_score: int | float,
) -> str:
    format_map = {
        "for_time": "sustained but controlled output with smart transitions",
        "amrap": "steady pacing and repeatable rounds",
        "emom": "consistent work-rest rhythm and quality under the clock",
        "strength": "intentional loading with technical precision",
        "mixed": "balanced effort across mixed modalities",
    }

    focus_map = {
        "engine": "aerobic power and recovery between efforts",
        "strength": "force production and barbell/body tension",
        "gym": "body control, positional awareness, and skill efficiency",
        "mixed": "overall work capacity across domains",
    }

    effort = "moderate"
    if difficulty_score >= 8:
        effort = "high"
    elif difficulty_score <= 4:
        effort = "low-to-moderate"

    pacing = format_map.get(wod_format, "controlled effort with clean execution")
    quality = focus_map.get(focus, "general conditioning")

    return (
        f"Intended stimulus: {pacing}. "
        f"Target effort is **{effort}** for this {time_domain} session, training **{quality}**."
    )
