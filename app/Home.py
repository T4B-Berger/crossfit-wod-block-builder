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

with st.sidebar:
    st.markdown("## Block Inputs")
    goal = st.selectbox("Goal", options=["engine", "strength", "gym", "general"])
    level = st.selectbox("Level", options=["beginner", "intermediate", "advanced"])
    sessions_per_week = st.selectbox("Sessions per week", options=[3, 4, 5], index=1)
    equipment = st.selectbox("Equipment", options=["full_gym", "home_gym", "no_machine"])
    max_duration = st.slider("Max duration (minutes)", min_value=8, max_value=60, value=20, step=1)
    generate = st.button("Generate block", type="primary", use_container_width=True)


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


def _render_wod_explorer(df: pd.DataFrame) -> None:
    st.subheader("WOD Explorer")
    with st.container(border=True):
        f1, f2, f3, f4, f5 = st.columns(5)
        with f1:
            format_filter = st.selectbox("Format", options=["all"] + sorted(df["format"].dropna().unique().tolist()))
        with f2:
            focus_filter = st.selectbox("Focus", options=["all"] + sorted(df["focus"].dropna().unique().tolist()))
        with f3:
            equipment_filter = st.selectbox(
                "Equipment",
                options=["all"] + sorted(df["equipment"].dropna().unique().tolist()),
            )
        with f4:
            duration_filter = st.slider("Max duration", min_value=8, max_value=60, value=30)
        with f5:
            benchmark_only = st.checkbox("Benchmark only")

    filtered = df.copy()
    if format_filter != "all":
        filtered = filtered[filtered["format"] == format_filter]
    if focus_filter != "all":
        filtered = filtered[filtered["focus"] == focus_filter]
    if equipment_filter != "all":
        filtered = filtered[filtered["equipment"] == equipment_filter]
    filtered = filtered[filtered["duration_estimate"] <= duration_filter]
    if benchmark_only:
        filtered = filtered[filtered["is_benchmark"] == True]

    if filtered.empty:
        st.info("No WODs match these explorer filters.")
        return

    for _, wod in filtered.sort_values("date", ascending=False).iterrows():
        with st.container(border=True):
            st.markdown(f"**{wod['name']}**")
            st.caption(
                f"{wod['format']} · {wod['focus']} · {wod['equipment']} · {int(wod['duration_estimate'])} min"
            )
            st.write(wod["description"])


if dataset.empty:
    st.warning("No dataset available. Add data/wod_dataset.csv to generate a block.")
elif generate:
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

    st.divider()
    _render_wod_explorer(dataset)
else:
    st.info("Select inputs and click **Generate block**.")
    st.divider()
    _render_wod_explorer(dataset)
