import streamlit as st


APP_THEME = """
<style>
:root {
  --bg: #0b1020;
  --surface: #121a2f;
  --surface-2: #192445;
  --control: #1b2850;
  --control-hover: #243666;
  --control-active: #2f457a;
  --text: #f2f6ff;
  --muted: #c0cdf0;
  --accent: #79a8ff;
  --accent-2: #a3ffd6;
  --cta-red: #e14b5a;
  --cta-red-hover: #f05b6b;
  --cta-red-active: #c83f4f;
  --border: #3c548a;
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

/* Control labels and helper text */
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label,
[data-testid="stCheckbox"] label,
[data-testid="stTextInput"] label,
[data-testid="stMultiSelect"] label {
  color: var(--text) !important;
  font-weight: 600;
}

[data-testid="stCaptionContainer"],
[data-testid="stMarkdownContainer"] p small,
[data-testid="stHelpIcon"],
small {
  color: var(--muted) !important;
}

/* Closed select field readability */
[data-baseweb="select"] > div {
  background: var(--control) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
}

[data-baseweb="select"] > div:hover {
  background: var(--control-hover) !important;
  border-color: var(--accent) !important;
}

[data-baseweb="select"] > div:focus-within,
[data-baseweb="select"] > div:active {
  background: var(--control-active) !important;
  border-color: var(--accent) !important;
  outline: 2px solid rgba(121, 168, 255, 0.6) !important;
  outline-offset: 1px;
}

[data-baseweb="select"] input,
[data-baseweb="select"] span,
[data-baseweb="select"] div,
[data-baseweb="select"] [aria-live="polite"] {
  color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important;
}

[data-baseweb="select"] input::placeholder {
  color: var(--muted) !important;
  opacity: 1 !important;
}

[data-baseweb="tag"],
[data-baseweb="tag"] * {
  background: var(--control-active) !important;
  color: #ffffff !important;
  border-color: rgba(255, 255, 255, 0.22) !important;
}

[data-baseweb="select"] [data-baseweb="tag"] {
  border-radius: 999px !important;
}

/* Open dropdown panel readability */
[data-baseweb="popover"],
[data-baseweb="menu"] {
  background: var(--surface-2) !important;
}

[data-baseweb="popover"] [role="listbox"],
[data-baseweb="menu"] ul,
[data-baseweb="menu"] {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}

[data-baseweb="popover"] [role="option"],
[data-baseweb="menu"] li,
[data-baseweb="menu"] div[role="option"] {
  color: var(--text) !important;
  background: transparent !important;
}

[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [role="option"][aria-selected="true"],
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] li[aria-selected="true"],
[data-baseweb="menu"] div[role="option"]:hover,
[data-baseweb="menu"] div[role="option"][aria-selected="true"] {
  color: #ffffff !important;
  background: var(--control-hover) !important;
}

[data-baseweb="popover"] [role="option"]:focus,
[data-baseweb="menu"] li:focus,
[data-baseweb="menu"] div[role="option"]:focus {
  background: var(--control-active) !important;
  outline: 1px solid var(--accent) !important;
}

/* Slider and checkbox readability */
[data-testid="stSlider"] [data-testid="stTickBar"],
[data-testid="stSlider"] div[data-baseweb="slider"] span {
  color: var(--muted) !important;
}

[data-testid="stSlider"] div[data-baseweb="slider"] [role="slider"] {
  background: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(121, 168, 255, 0.25);
}

[data-testid="stCheckbox"] input + div {
  border-color: var(--border) !important;
  background: var(--surface-2) !important;
}

[data-testid="stCheckbox"] input:focus + div {
  outline: 2px solid rgba(121, 168, 255, 0.6) !important;
  outline-offset: 1px;
}

/* Buttons, including mode switch, remain readable in dark theme */
[data-testid="stButton"] button {
  background: var(--cta-red) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #ffffff !important;
  font-weight: 600 !important;
}

[data-testid="stButton"] button:hover {
  background: var(--cta-red-hover) !important;
  border-color: rgba(255, 255, 255, 0.35) !important;
}

[data-testid="stButton"] button:focus,
[data-testid="stButton"] button:focus-visible,
[data-testid="stButton"] button:active {
  background: var(--cta-red-active) !important;
  outline: 2px solid rgba(240, 91, 107, 0.55) !important;
  outline-offset: 2px !important;
}

.movement-pill {
  display: inline-block;
  margin: 0.12rem 0.2rem 0.12rem 0;
  padding: 0.28rem 0.62rem;
  border-radius: 999px;
  background: var(--cta-red-active);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 0.82rem;
}

</style>
"""


def inject_theme() -> None:
    st.markdown(APP_THEME, unsafe_allow_html=True)
