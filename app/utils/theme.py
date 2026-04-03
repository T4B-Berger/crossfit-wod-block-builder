import streamlit as st


APP_THEME = """
<style>
:root {
  --bg: #0b1020;
  --surface: #121a2f;
  --surface-2: #192445;
  --text: #e8eeff;
  --muted: #9eb0db;
  --accent: #79a8ff;
  --accent-2: #a3ffd6;
  --border: #273459;
}

.stApp {
  background:
    radial-gradient(circle at 15% 10%, rgba(121, 168, 255, 0.18), transparent 35%),
    radial-gradient(circle at 85% 0%, rgba(163, 255, 214, 0.12), transparent 25%),
    var(--bg);
  color: var(--text);
}

h1, h2, h3, h4, p, label, div { color: var(--text); }

.hero {
  padding: 1.25rem 1.4rem;
  margin-bottom: 0.75rem;
  border: 1px solid var(--border);
  border-radius: 16px;
  background: linear-gradient(130deg, rgba(25, 36, 69, 0.95), rgba(18, 26, 47, 0.9));
}

.hero-kicker {
  font-size: 0.84rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent-2);
  margin-bottom: 0.35rem;
}

.hero-sub {
  color: var(--muted);
  max-width: 56rem;
}

.week-card,
.panel {
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 0.9rem;
  background: linear-gradient(180deg, rgba(25, 36, 69, 0.75), rgba(18, 26, 47, 0.75));
  min-height: 130px;
}

.week-label {
  color: var(--accent-2);
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.week-phase {
  font-size: 1.02rem;
  margin-top: 0.35rem;
  margin-bottom: 0.3rem;
  font-weight: 600;
}

.week-detail,
.panel p { color: var(--muted); }

.spacer { margin: 0.7rem 0; }

section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(18, 26, 47, 0.96), rgba(11, 16, 32, 0.98));
  border-right: 1px solid var(--border);
}
</style>
"""


def inject_theme() -> None:
    st.markdown(APP_THEME, unsafe_allow_html=True)
