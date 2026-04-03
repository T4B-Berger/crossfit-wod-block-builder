import streamlit as st


def render_sidebar() -> None:
    """Render MVP sidebar controls (placeholder state only)."""
    st.sidebar.markdown("## Plan Inputs")

    st.sidebar.selectbox(
        "Goal",
        options=[
            "Improve overall conditioning",
            "Build strength endurance",
            "Prepare for a competition cycle",
        ],
    )
    st.sidebar.selectbox("Level", options=["Beginner", "Intermediate", "Advanced"])
    st.sidebar.selectbox("Sessions per week", options=[2, 3, 4, 5, 6])
    st.sidebar.multiselect(
        "Equipment",
        options=[
            "Barbell",
            "Dumbbells",
            "Kettlebells",
            "Pull-up bar",
            "Box",
            "Rower",
            "Bike",
            "SkiErg",
            "Rings",
            "Wall ball",
        ],
        placeholder="Select available equipment",
    )
    st.sidebar.slider("Max session duration (minutes)", min_value=30, max_value=120, value=60, step=5)
    st.sidebar.text_input("Optional weakness", placeholder="e.g., Overhead squats")

    st.sidebar.markdown("---")
    st.sidebar.button("Generate 4-week block", type="primary", use_container_width=True)


def render_block_overview_placeholder() -> None:
    st.subheader("4-Week Block Preview")
    st.caption("Deterministic programming engine will power this section in the next iteration.")

    week_cols = st.columns(4)
    for i, col in enumerate(week_cols, start=1):
        with col:
            st.markdown(
                f"""
                <div class=\"week-card\">
                    <div class=\"week-label\">Week {i}</div>
                    <div class=\"week-phase\">Progression Placeholder</div>
                    <div class=\"week-detail\">Volume, intensity, and focus visualization coming next.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_charts_placeholder() -> None:
    st.subheader("Progression Signals")
    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.markdown(
            """
            <div class=\"panel\">
                <h4>Training Load Trend</h4>
                <p>Simple weekly progression chart placeholder.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with chart_cols[1]:
        st.markdown(
            """
            <div class=\"panel\">
                <h4>Focus Distribution</h4>
                <p>Strength / gymnastics / monostructural balance placeholder.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_explanation_placeholder() -> None:
    st.subheader("Block Explanation")
    st.markdown(
        """
        <div class="panel">
            <p>
                This area will contain a concise narrative explaining the block logic,
                intended adaptation over four weeks, and the rationale behind progression.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_wod_explorer_placeholder() -> None:
    st.subheader("WOD Explorer")
    st.caption("Browse historical WODs with filters. Data integration comes in the next step.")

    filter_cols = st.columns(4)
    with filter_cols[0]:
        st.selectbox("Format", options=["Any", "AMRAP", "For Time", "EMOM", "Intervals"], key="format")
    with filter_cols[1]:
        st.selectbox(
            "Focus",
            options=["Any", "Mixed", "Strength-biased", "Gymnastics-biased", "Monostructural-biased"],
            key="focus",
        )
    with filter_cols[2]:
        st.selectbox("Time domain", options=["Any", "<10 min", "10-20 min", "20+ min"], key="domain")
    with filter_cols[3]:
        st.selectbox(
            "Equipment",
            options=["Any", "Minimal", "Barbell", "Machine", "Bodyweight"],
            key="equipment",
        )

    st.markdown(
        """
        <div class="panel">
            <p>WOD table placeholder (name, format, focus, duration, equipment).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    render_sidebar()

    st.markdown(
        """
        <div class="hero">
            <p class="hero-kicker">WOD Block Builder</p>
            <h1>Generate a credible 4-week CrossFit training block in seconds.</h1>
            <p class="hero-sub">Modern MVP foundation with deterministic planning scaffolding and a clean explorer workflow.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_block_overview_placeholder()
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    render_charts_placeholder()
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    render_explanation_placeholder()
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    render_wod_explorer_placeholder()
