import streamlit as st

from app.utils.data_loader import load_wod_dataset
from app.utils.programming import generate_4_week_block
from app.utils.theme import inject_theme

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
        st.subheader("Generated 4-week block")
        for week_data in block["weeks"]:
            st.markdown(f"### Week {week_data['week']}")
            for i, session in enumerate(week_data["sessions"], start=1):
                st.markdown(
                    f"**Session {i}: {session['name']}**  \n"
                    f"Format: `{session['format']}` | Focus: `{session['focus']}` | "
                    f"Duration: `{session['duration_estimate']} min` | Difficulty: `{session['difficulty_score']}`"
                )
                st.caption(session["description"])
            st.divider()
else:
    st.info("Select inputs and click **Generate block**.")
