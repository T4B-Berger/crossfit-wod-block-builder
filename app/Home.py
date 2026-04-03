from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from utils.data_loader import load_wod_dataset
from utils.explanations import generate_block_explanation, generate_session_stimulus
from utils.programming import generate_4_week_block
from utils.theme import inject_theme
from utils.warmup import generate_session_warmup

st.set_page_config(
    page_title="WOD Block Builder",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()

st.title("WOD Block Builder")
st.caption("Deterministic MVP block generation from historical WOD data.")

dataset = load_wod_dataset()

if "mode" not in st.session_state:
    st.session_state.mode = None


def _flatten_sessions(block: dict) -> list[dict]:
    sessions: list[dict] = []
    for week_data in block.get("weeks", []):
        week_num = week_data["week"]
        for session in week_data.get("sessions", []):
            session_copy = dict(session)
            session_copy["week"] = week_num
            sessions.append(session_copy)
    return sessions


def _render_block_cards(block: dict) -> None:
    st.subheader("Generated 4-week block")
    cols = st.columns(4, gap="medium")

    for i, week_data in enumerate(block.get("weeks", [])):
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"### Week {week_data['week']}")
                for session in week_data.get("sessions", []):
                    with st.container(border=True):
                        st.markdown(f"**{session['name']}**")
                        st.caption(
                            f"{session['format']} · {session['focus']} · {session['duration_estimate']} min"
                        )


def _render_visualizations(flat_sessions: list[dict]) -> None:
    viz_cols = st.columns(2, gap="large")

    with viz_cols[0]:
        st.markdown("#### Focus distribution")
        focus_order = ["engine", "strength", "gym", "mixed"]
        focus_counter = Counter(str(s.get("focus", "")).lower() for s in flat_sessions)
        focus_values = [focus_counter.get(focus, 0) for focus in focus_order]

        fig, ax = plt.subplots(figsize=(6, 3.2))
        ax.bar(focus_order, focus_values)
        ax.set_xlabel("Focus")
        ax.set_ylabel("Session count")
        ax.set_ylim(bottom=0)
        st.pyplot(fig, clear_figure=True)

    with viz_cols[1]:
        st.markdown("#### Weekly load (avg difficulty)")
        if flat_sessions:
            df_sessions = pd.DataFrame(flat_sessions)
            weekly = (
                df_sessions.groupby("week", as_index=False)["difficulty_score"]
                .mean()
                .sort_values("week")
            )

            fig, ax = plt.subplots(figsize=(6, 3.2))
            ax.plot(weekly["week"], weekly["difficulty_score"], marker="o")
            ax.set_xlabel("Week")
            ax.set_ylabel("Avg difficulty score")
            ax.set_xticks([1, 2, 3, 4])
            ax.set_ylim(bottom=0)
            st.pyplot(fig, clear_figure=True)


def _render_session_detail(flat_sessions: list[dict]) -> None:
    st.markdown("#### Session details")
    if not flat_sessions:
        st.info("No sessions available for details.")
        return

    options = {
        f"Week {s['week']} · {s['name']} ({s['format']})": s
        for s in flat_sessions
    }
    selected_label = st.selectbox("Select a session", options=list(options.keys()))
    selected = options[selected_label]

    stimulus = generate_session_stimulus(
        wod_format=str(selected.get("format", "")),
        focus=str(selected.get("focus", "")),
        time_domain=str(selected.get("time_domain", "")),
        difficulty_score=float(selected.get("difficulty_score", 0)),
    )
    warmup = generate_session_warmup(
        movements=str(selected.get("movements", "")),
        focus=str(selected.get("focus", "")),
    )

    with st.container(border=True):
        st.markdown(f"**{selected['name']}**")
        st.caption(
            f"Week {selected['week']} · {selected['format']} · {selected['focus']} · {selected['duration_estimate']} min"
        )
        st.write(selected.get("description", "No description provided."))
        st.markdown(f"**Movements:** {selected.get('movements', 'N/A')}")

    with st.container(border=True):
        st.markdown("**Session stimulus**")
        st.write(stimulus)

    with st.container(border=True):
        st.markdown("**Warm-up proposal**")
        st.markdown("General warm-up")
        for item in warmup["general"]:
            st.markdown(f"- {item}")
        st.markdown("Specific prep")
        for item in warmup["specific"]:
            st.markdown(f"- {item}")




def _derive_explorer_fields(df: pd.DataFrame) -> pd.DataFrame:
    explorer = df.copy()

    explorer["workout_format"] = explorer["format"].fillna("unknown").str.lower()
    explorer.loc[~explorer["workout_format"].isin(["for_time", "amrap", "emom", "strength", "mixed"]), "workout_format"] = "unknown"
    explorer.loc[
        explorer["description"].fillna("").str.contains("chipper", case=False),
        "workout_format",
    ] = "chipper"
    explorer.loc[
        explorer["description"].fillna("").str.contains("interval", case=False),
        "workout_format",
    ] = "intervals"
    explorer.loc[explorer["workout_format"] == "mixed", "workout_format"] = "unknown"

    duration = explorer["duration_estimate"]
    explorer["time_domain_code"] = "unknown"
    explorer.loc[duration < 5, "time_domain_code"] = "<5"
    explorer.loc[(duration >= 5) & (duration < 10), "time_domain_code"] = "5–10"
    explorer.loc[(duration >= 10) & (duration < 20), "time_domain_code"] = "10–20"
    explorer.loc[(duration >= 20) & (duration < 40), "time_domain_code"] = "20–40"
    explorer.loc[duration >= 40, "time_domain_code"] = "40+"

    explorer["energy_system_primary"] = "indéterminée"
    explorer.loc[explorer["focus"].str.lower() == "engine", "energy_system_primary"] = "aérobie"
    explorer.loc[
        (explorer["duration_estimate"] < 10) & (explorer["difficulty_score"] >= 8),
        "energy_system_primary",
    ] = "anaérobie alactique"
    explorer.loc[
        (explorer["duration_estimate"] >= 5) & (explorer["duration_estimate"] <= 20) & (explorer["difficulty_score"] >= 7),
        "energy_system_primary",
    ] = "anaérobie lactique"
    explorer.loc[explorer["focus"].str.lower() == "mixed", "energy_system_primary"] = "mixte"

    explorer["rpe_inferred"] = (6 + (explorer["difficulty_score"].fillna(0) / 10) * 4).clip(6, 10).round(1)
    explorer["year"] = pd.to_datetime(explorer["date"], errors="coerce").dt.year.astype("Int64")

    return explorer


def _movement_list(movements: str) -> list[str]:
    if not movements:
        return []
    return [m.strip() for m in str(movements).split("|") if m.strip()]


def _render_wod_explorer(df: pd.DataFrame) -> None:
    st.subheader("WOD Explorer")
    explorer = _derive_explorer_fields(df)

    all_movements = sorted({m for raw in explorer["movements"].fillna("") for m in _movement_list(raw)})
    year_options = ["all"] + [str(y) for y in sorted(explorer["year"].dropna().unique().tolist())]

    with st.container(border=True):
        st.markdown("**Main filters**")
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            workout_format = st.radio(
                "workout_format",
                options=["all", "for_time", "amrap", "emom", "strength", "chipper", "intervals", "unknown"],
                horizontal=True,
            )
        with r1c2:
            time_domain_code = st.radio(
                "time_domain_code",
                options=["all", "<5", "5–10", "10–20", "20–40", "40+", "unknown"],
                horizontal=True,
            )

        r2c1, r2c2, r2c3 = st.columns([2, 1, 1])
        with r2c1:
            energy_system_primary = st.radio(
                "energy_system_primary",
                options=["all", "aérobie", "anaérobie lactique", "anaérobie alactique", "mixte", "indéterminée"],
                horizontal=True,
            )
        with r2c2:
            focus_filter = st.radio(
                "focus",
                options=["all"] + sorted(explorer["focus"].dropna().unique().tolist()),
                horizontal=True,
            )
        with r2c3:
            equipment_filter = st.radio(
                "equipment",
                options=["all"] + sorted(explorer["equipment"].dropna().unique().tolist()),
                horizontal=True,
            )

    with st.container(border=True):
        st.markdown("**Additional filters**")
        a1, a2 = st.columns([1, 2])
        with a1:
            rpe_range = st.slider("rpe_inferred", min_value=6.0, max_value=10.0, value=(6.0, 10.0), step=0.1)
        with a2:
            year_filter = st.radio("year", options=year_options, horizontal=True)

        movement_filters = st.multiselect("movements", options=all_movements)

    filtered = explorer.copy()
    if workout_format != "all":
        filtered = filtered[filtered["workout_format"] == workout_format]
    if time_domain_code != "all":
        filtered = filtered[filtered["time_domain_code"] == time_domain_code]
    if energy_system_primary != "all":
        filtered = filtered[filtered["energy_system_primary"] == energy_system_primary]

    filtered = filtered[
        filtered["rpe_inferred"].isna()
        | ((filtered["rpe_inferred"] >= rpe_range[0]) & (filtered["rpe_inferred"] <= rpe_range[1]))
    ]

    if movement_filters:
        filtered = filtered[
            filtered["movements"].fillna("").apply(
                lambda raw: any(m in _movement_list(raw) for m in movement_filters)
            )
        ]

    if year_filter != "all":
        filtered = filtered[filtered["year"] == int(year_filter)]
    if equipment_filter != "all":
        filtered = filtered[filtered["equipment"] == equipment_filter]
    if focus_filter != "all":
        filtered = filtered[filtered["focus"] == focus_filter]

    if filtered.empty:
        st.info("No WODs match these explorer filters.")
        return

    for _, wod in filtered.sort_values("date", ascending=False).iterrows():
        movements = ", ".join(_movement_list(wod.get("movements", ""))[:4])
        description = str(wod.get("description", ""))
        excerpt = description if len(description) <= 120 else f"{description[:120].rstrip()}..."
        with st.container(border=True):
            st.markdown(f"**{wod['name']}**")
            st.caption(
                f"{wod['date']} · {wod['workout_format']} · {wod['time_domain_code']} · {wod['energy_system_primary']} · RPE {wod['rpe_inferred']}"
            )
            st.markdown(f"**Main movements:** {movements if movements else 'N/A'}")
            st.write(excerpt)


def _render_landing() -> None:
    st.markdown("### Choose your mode")
    st.caption("Start by selecting one focused workflow.")

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown("#### Build a 4-week block")
            st.caption("Generate a deterministic block from your constraints.")
            if st.button("Build a 4-week block", use_container_width=True, type="primary"):
                st.session_state.mode = "builder"
                st.rerun()
    with right:
        with st.container(border=True):
            st.markdown("#### Explore the WOD library")
            st.caption("Browse and filter existing WODs quickly.")
            if st.button("Explore the WOD library", use_container_width=True, type="primary"):

                st.session_state.mode = "explorer"
                st.rerun()


if dataset.empty:
    st.warning("No dataset available. Add data/wod_dataset.csv to generate a block.")
elif st.session_state.mode is None:
    _render_landing()
elif st.session_state.mode == "builder":
    if st.button("Switch mode", key="switch_mode_builder"):
        st.session_state.mode = None
        st.rerun()

    with st.sidebar:
        st.markdown("## Block Inputs")
        goal = st.selectbox("Goal", options=["engine", "strength", "gym", "general"])
        level = st.selectbox("Level", options=["beginner", "intermediate", "advanced"])
        sessions_per_week = st.selectbox("Sessions per week", options=[3, 4, 5], index=1)
        equipment = st.selectbox("Equipment", options=["full_gym", "home_gym", "no_machine"])
        max_duration = st.slider("Max duration (minutes)", min_value=8, max_value=60, value=20, step=1)
        generate = st.button("Generate block", type="primary", use_container_width=True)

    if generate:
        block = generate_4_week_block(
            df=dataset,
            goal=goal,
            level=level,
            sessions_per_week=sessions_per_week,
            equipment=equipment,
            max_duration=max_duration,
        )

        if not block["weeks"]:
            st.info("No sessions found for this combination. Try a broader duration/equipment setting.")
        else:
            st.markdown(f"### 4-week block: {sessions_per_week} sessions/week, goal = {goal}")
            st.info(generate_block_explanation(goal=goal, sessions_per_week=sessions_per_week))

            _render_block_cards(block)
            flat_sessions = _flatten_sessions(block)
            _render_visualizations(flat_sessions)
            _render_session_detail(flat_sessions)
    else:
        st.info("Select inputs and click **Generate block**.")
else:
    if st.button("Switch mode", key="switch_mode_explorer"):
        st.session_state.mode = None
        st.rerun()
    _render_wod_explorer(dataset)
