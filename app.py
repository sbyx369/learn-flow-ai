import streamlit as st
import google.generativeai as genai
import PyPDF2
from docx import Document
import datetime
import time
import re

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="LearnFlow AI — Study Smarter",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# THEME-AWARE STYLING
# ==========================================================

# Theme toggle must happen BEFORE rendering anything
dark = st.session_state.get("dark_mode", True)

# Color tokens
if dark:
    BG          = "#05080f"
    BG2         = "#080c16"
    BG3         = "#080e1c"
    BORDER      = "#0f1d35"
    BORDER2     = "#0f2040"
    TEXT        = "#dde3f0"
    TEXT2       = "#4a6080"
    TEXT3       = "#1e3a5f"
    ACCENT      = "#2563eb"
    ACCENT2     = "#4338ca"
    MUTED       = "#3a5a8a"
    CARD_BG     = "#080e1c"
    HERO_BG     = "linear-gradient(135deg,#070e1e 0%,#0a1428 50%,#060c1a 100%)"
    HERO_BORDER = "#0f2040"
    HERO_TITLE  = "linear-gradient(135deg,#e2e8f8 0%,#93c5fd 40%,#818cf8 70%,#c084fc 100%)"
    HERO_SUB    = "#4a6080"
    BTN_BG      = "#0d1829"
    BTN_BORDER  = "#0f2040"
    BTN_TEXT    = "#7a9cc4"
    INPUT_BG    = "#080e1c"
    PILL_BG     = "#080e1c"
    PILL_BORDER = "#0f1e38"
    PILL_TEXT   = "#3a5a8a"
    TAB_BG      = "#080e1c"
    FC_BG       = "linear-gradient(135deg,#080e1c,#0a1428)"
    FC_BORDER   = "#0f2040"
    FC_Q        = "#7aaad8"
    SB_BG       = "#080c16"
    SB_BORDER   = "#0f1d35"
    SCROLLBAR   = "#1a2a4a"
    SETUP_BG    = "linear-gradient(135deg,#070f20,#0a1428)"
    STAT_VAL    = "#60a5fa"
    EYEBROW     = "#1e4a8a"
    STAT_LBL    = "#2a3f5f"
    HR          = "#080e1c"
    PROG_BG     = "#0f1e38"
    POMO        = "#60a5fa"
    TOGGLE_BG   = "#0d1829"
    TOGGLE_ICON = "🌙"
    TOGGLE_TEXT = "Light Mode"
else:
    BG          = "#f0f4ff"
    BG2         = "#e8edf8"
    BG3         = "#ffffff"
    BORDER      = "#d0d8ee"
    BORDER2     = "#c0ccee"
    TEXT        = "#1a2240"
    TEXT2       = "#5a6888"
    TEXT3       = "#8898bb"
    ACCENT      = "#2563eb"
    ACCENT2     = "#4338ca"
    MUTED       = "#4a6aaa"
    CARD_BG     = "#ffffff"
    HERO_BG     = "linear-gradient(135deg,#dce8ff 0%,#eef3ff 50%,#f5f0ff 100%)"
    HERO_BORDER = "#c8d8ff"
    HERO_TITLE  = "linear-gradient(135deg,#1a3a8f 0%,#2563eb 40%,#4f46e5 70%,#7c3aed 100%)"
    HERO_SUB    = "#5a6888"
    BTN_BG      = "#eef2ff"
    BTN_BORDER  = "#c8d4f8"
    BTN_TEXT    = "#3b5bdb"
    INPUT_BG    = "#ffffff"
    PILL_BG     = "#eef2ff"
    PILL_BORDER = "#c8d4f8"
    PILL_TEXT   = "#4a6aaa"
    TAB_BG      = "#eef2ff"
    FC_BG       = "linear-gradient(135deg,#f5f8ff,#eef2ff)"
    FC_BORDER   = "#c8d4f8"
    FC_Q        = "#2a4a8a"
    SB_BG       = "#e8edf8"
    SB_BORDER   = "#c8d4f8"
    SCROLLBAR   = "#c0ccee"
    SETUP_BG    = "linear-gradient(135deg,#dce8ff,#eef3ff)"
    STAT_VAL    = "#2563eb"
    EYEBROW     = "#6a8acc"
    STAT_LBL    = "#7a90bb"
    HR          = "#dde8ff"
    PROG_BG     = "#d0d8ee"
    POMO        = "#2563eb"
    TOGGLE_BG   = "#eef2ff"
    TOGGLE_ICON = "☀️"
    TOGGLE_TEXT = "Dark Mode"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
    background: {BG} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: {TEXT} !important;
}}

#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] {{ display: none !important; }}

::-webkit-scrollbar {{ width: 3px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {SCROLLBAR}; border-radius: 10px; }}

.block-container {{ max-width: 1080px !important; margin: 0 auto !important; padding: 0 2rem 6rem !important; }}

[data-testid="stSidebar"] {{
    background: {SB_BG} !important;
    border-right: 1px solid {SB_BORDER} !important;
    min-width: 260px !important;
}}
[data-testid="stSidebar"] > div:first-child {{ padding: 1.5rem 1.2rem !important; }}

/* ── CURSOR FIXES ── */
button, [role="button"], select, option,
[data-baseweb="select"] *, [data-baseweb="radio"] *,
[data-baseweb="tab"] *, .stRadio label, .stSelectbox *,
.stTabs [data-baseweb="tab"], [data-testid="stFileUploader"] *,
label {{ cursor: pointer !important; }}
[data-baseweb="select"] input, [data-baseweb="combobox"] input,
div[data-baseweb="select"] input[type="text"], .stSelectbox input {{
    caret-color: transparent !important;
    cursor: pointer !important;
    user-select: none !important;
    pointer-events: none !important;
}}

/* ── HERO ── */
.hero {{
    background: {HERO_BG};
    border: 1px solid {HERO_BORDER};
    border-radius: 24px;
    padding: 3rem 3.5rem;
    margin: 2rem 0 1.5rem;
    position: relative;
    overflow: hidden;
}}
.hero::before {{
    content: '';
    position: absolute;
    width: 600px; height: 600px;
    top: -200px; right: -100px;
    background: radial-gradient(circle, rgba(56,189,248,0.06) 0%, transparent 65%);
    pointer-events: none;
}}
.hero-eyebrow {{
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {EYEBROW};
    margin-bottom: 1rem;
}}
.hero-title {{
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.1;
    background: {HERO_TITLE};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}
.hero-sub {{ font-size: 1.05rem; color: {HERO_SUB}; max-width: 540px; line-height: 1.6; }}
.hero-stats {{
    display: flex; gap: 2rem;
    margin-top: 2rem; padding-top: 2rem;
    border-top: 1px solid {BORDER2};
}}
.hero-stat-val {{ font-family: 'Space Mono', monospace; font-size: 1.4rem; font-weight: 700; color: {STAT_VAL}; }}
.hero-stat-lbl {{ font-size: 0.72rem; color: {STAT_LBL}; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.2rem; }}

/* ── FEATURES STRIP ── */
.features-strip {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0 2rem; }}
.fpill {{
    background: {PILL_BG};
    border: 1px solid {PILL_BORDER};
    border-radius: 100px;
    padding: 0.35rem 1rem;
    font-size: 0.75rem;
    color: {PILL_TEXT};
    font-weight: 500;
}}

/* ── SETUP CARD ── */
.setup-card {{
    background: {SETUP_BG};
    border: 1px solid {HERO_BORDER};
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
}}
.setup-title {{ font-size: 1.4rem; font-weight: 700; color: {TEXT}; margin-bottom: 0.5rem; }}
.setup-sub {{ font-size: 0.9rem; color: {TEXT2}; margin-bottom: 2rem; line-height: 1.6; }}
.setup-steps {{ display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2rem; }}
.setup-step {{
    background: {CARD_BG};
    border: 1px solid {BORDER2};
    border-radius: 12px;
    padding: 1rem 1.2rem;
    flex: 1; min-width: 120px; max-width: 160px;
}}
.setup-step-num {{ font-family: 'Space Mono', monospace; font-size: 1.2rem; font-weight: 700; color: {ACCENT}; margin-bottom: 0.4rem; }}
.setup-step-text {{ font-size: 0.78rem; color: {TEXT2}; line-height: 1.4; }}

/* ── SECTION HEADER ── */
.sec-header {{ display: flex; align-items: flex-start; gap: 1rem; margin: 2.5rem 0 1.2rem; }}
.sec-num {{
    width: 36px; height: 36px;
    background: linear-gradient(135deg, {ACCENT}, {ACCENT2});
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700; color: white;
    flex-shrink: 0; margin-top: 2px;
}}
.sec-title {{ font-size: 1.1rem; font-weight: 700; color: {TEXT}; }}
.sec-sub {{ font-size: 0.8rem; color: {TEXT3}; margin-top: 0.15rem; }}

/* ── BUTTONS ── */
.stButton > button {{
    background: {BTN_BG} !important;
    color: {BTN_TEXT} !important;
    border: 1px solid {BTN_BORDER} !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.18s ease !important;
    cursor: pointer !important;
}}
.stButton > button:hover {{
    border-color: {ACCENT} !important;
    color: {ACCENT} !important;
    transform: translateY(-1px) !important;
}}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT2}) !important;
    color: white !important;
    border: none !important;
}}
.stButton > button[kind="primary"]:hover {{
    box-shadow: 0 4px 24px rgba(37,99,235,0.35) !important;
    transform: translateY(-1px) !important;
}}

/* ── INPUTS ── */
.stTextArea textarea, .stTextInput > div > div > input {{
    background: {INPUT_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
.stTextArea textarea:focus, .stTextInput > div > div > input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
}}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {{
    background: {INPUT_BG} !important;
    border: 1.5px dashed {BORDER2} !important;
    border-radius: 14px !important;
    cursor: pointer !important;
}}
[data-testid="stFileUploader"]:hover {{ border-color: {ACCENT} !important; }}

/* ── SELECT & DROPDOWNS ── */
[data-baseweb="select"] > div {{
    background: {INPUT_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    color: {TEXT} !important;
}}
[data-baseweb="popover"] {{ background: {CARD_BG} !important; border: 1px solid {BORDER2} !important; border-radius: 12px !important; }}
[data-baseweb="option"] {{ background: {CARD_BG} !important; color: {TEXT2} !important; cursor: pointer !important; }}
[data-baseweb="option"]:hover {{ background: {BTN_BG} !important; color: {ACCENT} !important; }}

/* ── RADIO ── */
.stRadio > div {{ gap: 0.4rem !important; }}
.stRadio label {{
    background: {INPUT_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    padding: 0.45rem 0.9rem !important;
    color: {MUTED} !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}}
.stRadio label:hover {{ border-color: {ACCENT} !important; color: {ACCENT} !important; }}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {TAB_BG} !important;
    border-radius: 12px !important;
    padding: 0.3rem !important;
    border: 1px solid {BORDER} !important;
    gap: 0.2rem !important;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    color: {TEXT3} !important;
    border-radius: 8px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    border: none !important;
    cursor: pointer !important;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT2}) !important;
    color: white !important;
}}

/* ── EXPANDER ── */
details {{
    background: {CARD_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}
details summary {{ color: {TEXT2} !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 600 !important; cursor: pointer !important; }}

/* ── METRIC ── */
[data-testid="metric-container"] {{
    background: {CARD_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    padding: 0.8rem 1rem !important;
}}
[data-testid="metric-container"] label {{ color: {TEXT3} !important; font-size: 0.72rem !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{ color: {STAT_VAL} !important; font-family: 'Space Mono', monospace !important; }}

/* ── PROGRESS ── */
.stProgress > div {{ background: {PROG_BG} !important; border-radius: 100px !important; height: 6px !important; }}
.stProgress > div > div {{ background: linear-gradient(90deg, {ACCENT}, #7c3aed, #ec4899) !important; border-radius: 100px !important; }}

/* ── ALERTS ── */
[data-testid="stAlert"] {{ border-radius: 12px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.88rem !important; }}

/* ── SIDEBAR LABEL ── */
.sb-label {{
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: {TEXT3};
    margin: 1.4rem 0 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid {BORDER};
}}

/* ── FLASHCARD ── */
.fc-card {{
    background: {FC_BG};
    border: 1px solid {FC_BORDER};
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.8rem;
    border-left: 3px solid {ACCENT};
}}
.fc-num {{ font-family: 'Space Mono', monospace; font-size: 0.68rem; color: {TEXT3}; letter-spacing: 0.1em; margin-bottom: 0.6rem; }}
.fc-q {{ font-size: 0.95rem; color: {FC_Q}; font-weight: 500; line-height: 1.5; }}

/* ── TUTOR ── */
.tutor-q {{ background: {CARD_BG}; border: 1px solid {BORDER2}; border-radius: 14px 14px 14px 4px; padding: 1rem 1.2rem; margin: 0.6rem 0; color: {FC_Q}; font-size: 0.9rem; }}
.tutor-a {{ background: {CARD_BG}; border: 1px solid {BORDER2}; border-radius: 14px 14px 4px 14px; padding: 1rem 1.2rem; margin: 0.6rem 0; color: #10b981; font-size: 0.9rem; text-align: right; }}

/* ── POMODORO ── */
.pomo-time {{ font-family: 'Space Mono', monospace; font-size: 2.2rem; font-weight: 700; text-align: center; color: {POMO}; letter-spacing: 0.05em; }}

/* ── TOGGLE BUTTON ── */
.theme-toggle {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: {TOGGLE_BG};
    border: 1px solid {BORDER2};
    border-radius: 100px;
    padding: 0.3rem 0.8rem;
    font-size: 0.78rem;
    color: {TEXT2};
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}}

/* ── KEY STATUS ── */
.key-live {{ display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #10b981; margin-right: 5px; animation: blink 2s infinite; }}
@keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}

/* ── EMPTY STATE ── */
.empty-state {{ text-align: center; padding: 4rem 2rem; border: 1px dashed {BORDER2}; border-radius: 20px; margin: 1rem 0; }}
.empty-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
.empty-title {{ font-size: 0.95rem; font-weight: 600; color: {TEXT2}; }}
.empty-sub {{ font-size: 0.8rem; color: {TEXT3}; margin-top: 0.3rem; }}

hr {{ border: none !important; border-top: 1px solid {HR} !important; margin: 1.5rem 0 !important; }}
</style>
""", unsafe_allow_html=True)
# ==========================================================
# SESSION STATE
# ==========================================================

defaults = {
    "api_key": None,
    "api_key_valid": False,
    "history": [],
    "generated_output": None,
    "generated_heading": None,
    "quiz_score": None,
    "notes_content": None,
    "notes_heading": None,
    "tldr": None,
    "tutor_history": [],
    "feynman_feedback": None,
    "user_api_keys": [],
    "timer_start": None,
    "timer_duration": 0,
    "dark_mode": True,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==========================================================
# API KEY MANAGEMENT
# ==========================================================

# Built-in keys as silent fallback (used only AFTER user adds their key)
builtin_keys = []
try:
    if "GOOGLE_API_KEYS" in st.secrets:
        builtin_keys = list(st.secrets["GOOGLE_API_KEYS"])
except Exception:
    builtin_keys = []

def get_all_keys():
    """Returns all keys. User keys first, then builtin as fallback."""
    user = st.session_state.user_api_keys
    return user + builtin_keys

def user_has_setup():
    """True only if user has personally added at least one key."""
    return len(st.session_state.user_api_keys) > 0

def generate_with_rotation(prompt, creativity=0.4):
    keys = get_all_keys()
    if not keys:
        return "NO_KEYS"
    for key in keys:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            response = model.generate_content(
                prompt,
                generation_config={"temperature": creativity, "max_output_tokens": 2000}
            )
            if response and response.text:
                return response.text.strip()
        except Exception:
            time.sleep(0.8)
            continue
    return "QUOTA_EXCEEDED"

def validate_key(key):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        r = model.generate_content("Say OK", generation_config={"max_output_tokens": 5})
        return bool(r and r.text)
    except:
        return False

# ==========================================================
# FILE READERS
# ==========================================================

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])

def read_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def read_txt(file):
    return file.read().decode("utf-8")

# ==========================================================
# PROMPT BUILDER
# ==========================================================

def build_prompt(text, difficulty, persona, fmt):
    trimmed = len(text) > 3000
    text = text[:3000]
    base = f"Content:\n{text}\n\nDifficulty: {difficulty}\nPersona: {persona}\n\nRules:\n- Output ONLY the requested format\n- No introductions\n- Complete sentences\n"
    fmts = {
        "Notes":        "Generate structured academic notes with headings and bullet points. Max 400 words.\n",
        "Flashcards":   "Generate exactly 5 flashcards.\n\nFormat strictly:\nFlashcard 1\nQuestion:\nAnswer:\n\nFlashcard 2\nQuestion:\nAnswer:\n",
        "Quiz":         "Generate exactly 5 MCQ questions.\n\nFormat strictly:\nQuestion 1:\nA.\nB.\nC.\nD.\nCorrect Answer: X\n\nQuestion 2:\n",
        "Reflection":   "Generate exactly 5 deep reflection questions. Numbered list only.\n",
        "Study Plan":   "Generate a 5-step study plan with timelines and goals.\n",
        "Key Concepts": "Extract the 7 most important key concepts.\nFor each: bold name, one-line definition, why it matters.\n",
        "Exam Mode":    "Generate a realistic exam:\n- 3 MCQ (with Correct Answer)\n- 2 Fill in the blank (with Answer:)\n- 2 Short answer (with Model Answer:)\n",
        "TL;DR":        "Summarize in exactly 5 bullet points. Max 15 words each.\n",
        "Feynman":      "Evaluate the student's explanation:\n- What they understood\n- What is missing/wrong\n- Score out of 10\n- How to improve\n",
        "Socratic":     "Ask ONE probing Socratic question. Not factual recall. Short and deep.\n",
        "Mind Map":     "Generate a text mind map:\n- 1 central idea\n- 5 main branches\n- 2-3 sub-points each\nUse indentation and symbols.\n",
        "Mnemonics":    "Create 3 memorable mnemonics or acronyms for the key concepts.\n",
        "ELI5":         "Explain like I'm 10. Simple words, fun analogies. Max 200 words.\n",
    }
    return base + fmts.get(fmt, fmts["Notes"]), trimmed

def gen_heading(txt):
    r = generate_with_rotation(f"Convert to short heading. Max 7 words. No quotes.\nInput: {txt}", 0.2)
    return r.strip() if r not in ("QUOTA_EXCEEDED", "NO_KEYS") else "Learning Output"

def run_gen(fmt, save_as="output", content="", manual="", difficulty="Beginner", persona="University Professor", creativity=0.4):
    if not content:
        st.warning("⚠️ Enter a topic or upload a file first.")
        return False
    p, trimmed = build_prompt(content, difficulty, persona, fmt)
    if trimmed:
        st.caption("⚠️ Content trimmed to 3000 characters")
    with st.spinner(f"Generating {fmt}..."):
        r = generate_with_rotation(p, creativity)
    if r in ("QUOTA_EXCEEDED", "NO_KEYS"):
        show_quota_help()
        return False
    if save_as == "notes":
        st.session_state.notes_content = r
        st.session_state.notes_heading = gen_heading(manual if manual.strip() else "Document")
        st.session_state.generated_output = None
        st.session_state.quiz_score = None
    else:
        st.session_state.generated_output = r
        st.session_state.generated_heading = fmt
    st.session_state.history.append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "format": fmt,
        "preview": (manual if manual else "Document")[:50],
        "output": r
    })
    return True

# ==========================================================
# QUOTA / KEY HELP UI
# ==========================================================

def show_quota_help():
    st.error("⚠️ API quota exhausted or no keys available.")
    with st.expander("🔑 Get a Free API Key — takes 2 minutes", expanded=True):
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown("""
**Steps to get your free Gemini API key:**

**1.** Go to → [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

**2.** Sign in with your **Google account**

**3.** Click **"Create API Key"** → copy it

**4.** Paste below and click **Add Key** ✅

> It's 100% free — no credit card needed!
            """)
        with c2:
            st.markdown("""
**Free tier includes:**
- ✅ 15 requests / minute
- ✅ No credit card
- ✅ Ready in 2 minutes

**Your privacy:**
- 🔒 Stored in browser session only
- 🔒 Never sent to our servers
- 🔒 Auto-deleted on tab close
            """)
        nk = st.text_input("Paste API key:", type="password", placeholder="AIzaSy...", key=f"qh_key_{time.time()}")
        if st.button("➕ Add Key & Retry", type="primary", use_container_width=True):
            k = nk.strip()
            if k:
                if k not in st.session_state.user_api_keys:
                    st.session_state.user_api_keys.append(k)
                    st.success(f"✅ Key added! You now have {len(st.session_state.user_api_keys)} key(s). Try generating again.")
                    st.rerun()
                else:
                    st.warning("This key is already active.")
            else:
                st.warning("Please paste a valid API key.")

# ==========================================================
# SETUP SCREEN (shown when no API keys at all)
# ==========================================================

def show_setup_screen():
    # Full-page setup with theme-aware styling
    is_dark = st.session_state.get("dark_mode", True)

    page_bg   = "#05080f" if is_dark else "#f0f4ff"
    card_bg   = "#080e1c" if is_dark else "#ffffff"
    border_c  = "#0f2040" if is_dark else "#c8d8ff"
    text_main = "#dde3f0" if is_dark else "#1a2240"
    text_sub  = "#4a6080" if is_dark else "#5a6888"
    text_dim  = "#1e3a5f" if is_dark else "#8898bb"
    accent    = "#2563eb"
    step_bg   = "#070f20" if is_dark else "#eef3ff"
    badge_bg  = "rgba(37,99,235,0.1)" if is_dark else "rgba(37,99,235,0.08)"
    pill_text = "#60a5fa" if is_dark else "#2563eb"
    info_bg   = "rgba(37,99,235,0.06)" if is_dark else "rgba(37,99,235,0.05)"
    info_bdr  = "rgba(37,99,235,0.2)" if is_dark else "rgba(37,99,235,0.15)"
    warn_bg   = "rgba(245,158,11,0.08)" if is_dark else "rgba(245,158,11,0.06)"
    warn_bdr  = "#f59e0b"

    st.markdown(f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        background: {page_bg} !important;
    }}
    .onboard-wrap {{
        min-height: 90vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem 1rem;
    }}
    .onboard-logo {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.1rem;
        font-weight: 800;
        color: {text_main};
        text-align: center;
        margin-bottom: 2.5rem;
        letter-spacing: -0.01em;
    }}
    .onboard-card {{
        background: {card_bg};
        border: 1px solid {border_c};
        border-radius: 24px;
        padding: 3rem 3rem 2.5rem;
        max-width: 680px;
        width: 100%;
        margin: 0 auto;
        position: relative;
        overflow: hidden;
    }}
    .onboard-card::before {{
        content: '';
        position: absolute;
        top: -80px; right: -80px;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(37,99,235,0.07) 0%, transparent 70%);
        pointer-events: none;
    }}
    .onboard-badge {{
        display: inline-block;
        background: {badge_bg};
        border: 1px solid rgba(37,99,235,0.2);
        color: {pill_text};
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        padding: 0.3rem 0.9rem;
        border-radius: 100px;
        margin-bottom: 1.2rem;
    }}
    .onboard-title {{
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.7rem;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }}
    .onboard-sub {{
        font-size: 0.95rem;
        color: {text_sub};
        margin-bottom: 2rem;
        line-height: 1.65;
    }}
    .steps-row {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.75rem;
        margin-bottom: 2rem;
    }}
    .step-box {{
        background: {step_bg};
        border: 1px solid {border_c};
        border-radius: 12px;
        padding: 0.9rem 0.7rem;
        text-align: center;
    }}
    .step-n {{
        font-family: 'Space Mono', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        color: {accent};
        margin-bottom: 0.4rem;
    }}
    .step-t {{
        font-size: 0.75rem;
        color: {text_sub};
        line-height: 1.4;
    }}
    .divider-line {{
        border: none;
        border-top: 1px solid {border_c};
        margin: 1.5rem 0;
    }}
    .info-box {{
        background: {info_bg};
        border: 1px solid {info_bdr};
        border-radius: 10px;
        padding: 0.85rem 1.1rem;
        font-size: 0.82rem;
        color: {pill_text};
        line-height: 1.5;
        margin-top: 1rem;
    }}
    .warn-box {{
        background: {warn_bg};
        border-left: 3px solid {warn_bdr};
        border-radius: 0 10px 10px 0;
        padding: 0.75rem 1rem;
        font-size: 0.82rem;
        color: #fcd34d;
        margin-bottom: 1rem;
    }}
    .features-preview {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin: 1rem 0;
    }}
    .fp {{
        background: {step_bg};
        border: 1px solid {border_c};
        border-radius: 100px;
        padding: 0.25rem 0.75rem;
        font-size: 0.72rem;
        color: {text_dim};
    }}
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div style="text-align:center; padding: 2rem 0 1rem;">
        <div class="onboard-logo">🧠 LearnFlow <span style="color:{accent};">AI</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Centered card
    _, mid, _ = st.columns([1, 10, 1])
    with mid:
        st.markdown(f"""
        <div class="onboard-card">
            <div class="onboard-badge">✦ FREE SETUP — 2 MINUTES</div>
            <div class="onboard-title">Connect your free<br>Gemini API key to begin</div>
            <div class="onboard-sub">
                LearnFlow AI uses Google Gemini to power all features — notes, flashcards,
                quizzes, AI tutor and more. The API is <strong>100% free</strong>, no credit card needed.
            </div>
            <div class="steps-row">
                <div class="step-box"><div class="step-n">01</div><div class="step-t">Open Google AI Studio</div></div>
                <div class="step-box"><div class="step-n">02</div><div class="step-t">Sign in with Google</div></div>
                <div class="step-box"><div class="step-n">03</div><div class="step-t">Click Create API Key</div></div>
                <div class="step-box"><div class="step-n">04</div><div class="step-t">Paste below & start!</div></div>
            </div>
            <hr class="divider-line">
            <div class="warn-box">
                ⚡ Quick tip — keys look like: <strong>AIzaSyA...</strong> (39 characters long)
            </div>
        </div>
        """, unsafe_allow_html=True)

        # CTA link button
        st.markdown(f"""
        <div style="text-align:center; margin: 1.5rem 0 1rem;">
            <a href="https://aistudio.google.com/app/apikey" target="_blank" style="
                display: inline-block;
                background: linear-gradient(135deg, #1d4ed8, #4338ca);
                color: white;
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-weight: 700;
                font-size: 0.95rem;
                padding: 0.85rem 2.5rem;
                border-radius: 12px;
                text-decoration: none;
                letter-spacing: 0.01em;
                box-shadow: 0 4px 20px rgba(37,99,235,0.3);
            ">🔑 Get My Free API Key →</a>
        </div>
        <div style="text-align:center; font-size:0.78rem; color:{text_dim}; margin-bottom:1.5rem;">
            Opens Google AI Studio in a new tab
        </div>
        """, unsafe_allow_html=True)

        # Key input
        key_input = st.text_input(
            "Paste your API key here:",
            type="password",
            placeholder="AIzaSy...",
            key="setup_key_input",
        )

        if st.button("🚀 Validate & Start Learning", type="primary", use_container_width=True):
            k = key_input.strip()
            if not k:
                st.warning("⚠️ Paste your API key above first.")
            elif not k.startswith("AIza"):
                st.warning("⚠️ That doesn't look right — Gemini keys always start with **AIza**")
            elif len(k) < 30:
                st.warning("⚠️ Key seems too short — copy the full key from Google AI Studio")
            else:
                with st.spinner("🔍 Validating your key with Google..."):
                    valid = validate_key(k)
                if valid:
                    st.session_state.user_api_keys = [k]
                    st.balloons()
                    st.success("✅ Key validated! Welcome to LearnFlow AI 🎉 Loading your workspace...")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("❌ Key rejected by Google. Double-check you copied the full key correctly.")

        st.markdown(f"""
        <div class="info-box">
            🔒 <strong>Your privacy:</strong> This key is stored only in your browser session memory.
            It is never sent to our servers, never logged, and is automatically cleared when you close this tab.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Features preview
        st.markdown(f'<div style="font-size:0.8rem; color:{text_dim}; margin-bottom:0.5rem; font-weight:600;">🎓 What you\'ll unlock:</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="features-preview">
            <span class="fp">📝 Smart Notes</span>
            <span class="fp">🎴 Flashcards</span>
            <span class="fp">❓ AI Quiz</span>
            <span class="fp">🧪 Feynman Check</span>
            <span class="fp">🤖 Socratic Tutor</span>
            <span class="fp">📅 Study Plan</span>
            <span class="fp">🎓 Exam Mode</span>
            <span class="fp">🧠 Mind Map</span>
            <span class="fp">💡 Mnemonics</span>
            <span class="fp">⚡ TL;DR</span>
            <span class="fp">⏱ Pomodoro Timer</span>
            <span class="fp">🌙 Dark / Light Mode</span>
        </div>
        """, unsafe_allow_html=True)

        # Theme toggle even on setup screen
        st.markdown("<br>", unsafe_allow_html=True)
        toggle_col1, toggle_col2, toggle_col3 = st.columns([2,1,2])
        with toggle_col2:
            if st.button("🌙 Dark" if not is_dark else "☀️ Light", use_container_width=True):
                st.session_state.dark_mode = not is_dark
                st.rerun()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    # Logo
    # Theme toggle row
    tc1, tc2 = st.columns([3, 1])
    with tc1:
        st.markdown(f"""
        <div style='padding: 0.5rem 0 1rem;'>
            <div style='font-size:1.05rem; font-weight:800; color:{TEXT}; letter-spacing:-0.01em;'>🧠 LearnFlow <span style="color:{ACCENT};">AI</span></div>
            <div style='font-family:"Space Mono",monospace; font-size:0.6rem; color:{TEXT3}; letter-spacing:0.15em; margin-top:0.3rem;'>STUDY COMPANION</div>
        </div>
        """, unsafe_allow_html=True)
    with tc2:
        if st.button("🌙" if dark else "☀️", help="Toggle Light/Dark Mode", use_container_width=True):
            st.session_state.dark_mode = not dark
            st.rerun()
    st.markdown(f'<hr style="border-top:1px solid {BORDER}; margin: 0 0 0.5rem;">', unsafe_allow_html=True)

    keys_exist = user_has_setup()

    if keys_exist:
        st.markdown('<div class="sb-label">⚙ Learning Settings</div>', unsafe_allow_html=True)

        difficulty = st.selectbox(
            "Difficulty",
            ["Beginner", "Intermediate", "Advanced"],
            index=0,
            label_visibility="collapsed"
        )

        persona = st.selectbox(
            "Persona",
            ["🎓 University Professor", "👩‍🏫 School Teacher",
             "🧒 Child-Friendly", "🔬 Scientist",
             "📊 Analytical", "📝 Exam-Oriented", "💪 Motivational"],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown('<div style="font-size:0.75rem;color:#1e3a5f;margin:0.6rem 0 0.2rem;">Creativity</div>', unsafe_allow_html=True)
        creativity = st.slider("", 0.1, 1.0, 0.4, label_visibility="collapsed")

        st.markdown('<div class="sb-label">⏱ Pomodoro</div>', unsafe_allow_html=True)
        pc1, pc2 = st.columns([3, 1])
        with pc1:
            pmin = st.selectbox("", [25, 10, 15, 30, 45, 60], index=0, label_visibility="collapsed")
        with pc2:
            if st.button("▶", use_container_width=True):
                st.session_state.timer_start = time.time()
                st.session_state.timer_duration = pmin * 60

        if st.session_state.timer_start:
            elapsed = time.time() - st.session_state.timer_start
            rem = st.session_state.timer_duration - elapsed
            if rem > 0:
                m, s = int(rem // 60), int(rem % 60)
                st.markdown(f'<div class="pomo-time">{m:02d}:{s:02d}</div>', unsafe_allow_html=True)
                st.progress(1 - (rem / st.session_state.timer_duration))
            else:
                st.markdown('<div class="pomo-time pomo-break">Break!</div>', unsafe_allow_html=True)
                if st.button("Reset", use_container_width=True):
                    st.session_state.timer_start = None
                    st.rerun()

        st.markdown('<div class="sb-label">🔑 API Keys</div>', unsafe_allow_html=True)
        nk = len(get_all_keys())
        uk = len(st.session_state.user_api_keys)

        if uk > 0:
            st.markdown(f'<span class="key-live"></span><span style="font-size:0.8rem;color:#10b981;">{uk} personal key(s) active</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="key-live"></span><span style="font-size:0.8rem;color:#10b981;">{nk} shared key(s) active</span>', unsafe_allow_html=True)

        with st.expander("➕ Add My Own Key"):
            st.caption("👉 [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)")
            sk = st.text_input("", type="password", placeholder="AIzaSy...", key="sb_key_input", label_visibility="collapsed")
            if st.button("Add Key", use_container_width=True, key="sb_add_btn"):
                if sk.strip() and sk.strip() not in st.session_state.user_api_keys:
                    st.session_state.user_api_keys.append(sk.strip())
                    st.success("✅ Added!")
                    st.rerun()
            if st.session_state.user_api_keys:
                if st.button("Remove My Keys", use_container_width=True, key="sb_rm_btn"):
                    st.session_state.user_api_keys = []
                    st.rerun()

        st.markdown('<div class="sb-label">📊 Session Stats</div>', unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Generated", len(st.session_state.history))
        with m2:
            st.metric("Notes", 1 if st.session_state.notes_content else 0)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑 Reset Session", use_container_width=True):
            preserved_keys = st.session_state.user_api_keys
            for k, v in defaults.items():
                st.session_state[k] = v
            st.session_state.user_api_keys = preserved_keys
            st.rerun()

    else:
        difficulty, persona, creativity = "Beginner", "University Professor", 0.4
        st.info("Add your API key to unlock all features!")

# ==========================================================
# MAIN
# ==========================================================

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ Powered by Google Gemini 2.5 Flash</div>
    <h1 class="hero-title">Learn Smarter.<br>Not Harder.</h1>
    <p class="hero-sub">Transform any topic or document into notes, flashcards, quizzes, and more — in seconds.</p>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-val">10+</div>
            <div class="hero-stat-lbl">AI Features</div>
        </div>
        <div>
            <div class="hero-stat-val">∞</div>
            <div class="hero-stat-lbl">Topics Supported</div>
        </div>
        <div>
            <div class="hero-stat-val">Free</div>
            <div class="hero-stat-lbl">Forever</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="features-strip">
    <span class="fpill">📝 Smart Notes</span>
    <span class="fpill">🎴 Flashcards</span>
    <span class="fpill">❓ AI Quiz</span>
    <span class="fpill">🧪 Feynman Check</span>
    <span class="fpill">🤖 Socratic Tutor</span>
    <span class="fpill">📅 Study Plan</span>
    <span class="fpill">🎓 Exam Mode</span>
    <span class="fpill">🧠 Mind Map</span>
    <span class="fpill">💡 Mnemonics</span>
    <span class="fpill">⚡ TL;DR</span>
    <span class="fpill">👶 ELI5</span>
    <span class="fpill">⏱ Pomodoro</span>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# GATE: Show setup screen if user hasn't added their personal key yet
# ==========================================================

if not user_has_setup():
    show_setup_screen()
    st.stop()

# ==========================================================
# STEP 1 — INPUT
# ==========================================================

st.markdown("""
<div class="sec-header">
    <div class="sec-num">1</div>
    <div>
        <div class="sec-title">Enter Topic or Upload File</div>
        <div class="sec-sub">Type any subject, paste your notes, or upload PDF / DOCX / TXT</div>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("", type=["pdf", "docx", "txt"], label_visibility="collapsed")
file_text = ""

if uploaded:
    with st.spinner("Reading file..."):
        try:
            ft = uploaded.type
            if ft == "application/pdf":
                file_text = read_pdf(uploaded)
            elif "document" in ft:
                file_text = read_docx(uploaded)
            else:
                file_text = read_txt(uploaded)
            st.success(f"✅ **{uploaded.name}** — {len(file_text):,} characters loaded")
        except Exception as e:
            st.error(f"❌ Failed to read: {e}")

manual = st.text_area(
    "", height=110, label_visibility="collapsed",
    placeholder="Type any topic → Photosynthesis · Newton's Laws · French Revolution · Machine Learning · Thermodynamics..."
)

if file_text and manual.strip():
    content = f"User Instruction:\n{manual.strip()}\n\nDocument:\n{file_text}"
elif file_text:
    content = file_text
else:
    content = manual.strip()

# ==========================================================
# STEP 2 — READ & LEARN
# ==========================================================

st.markdown("""
<div class="sec-header">
    <div class="sec-num">2</div>
    <div>
        <div class="sec-title">Read & Learn</div>
        <div class="sec-sub">Start with Notes — then explore summaries, concepts and memory aids</div>
    </div>
</div>
""", unsafe_allow_html=True)

g = dict(content=content, manual=manual, difficulty=difficulty, persona=persona, creativity=creativity)

r1c1, r1c2, r1c3, r1c4 = st.columns(4)
with r1c1:
    if st.button("📝 Notes", use_container_width=True, type="primary"):
        if run_gen("Notes", save_as="notes", **g):
            st.success("✅ Notes ready!")
with r1c2:
    if st.button("⚡ TL;DR", use_container_width=True):
        if content:
            p, _ = build_prompt(content, difficulty, persona, "TL;DR")
            with st.spinner("Summarizing..."):
                r = generate_with_rotation(p, 0.3)
            if r not in ("QUOTA_EXCEEDED","NO_KEYS"):
                st.session_state.tldr = r
                st.success("✅ Done!")
            else:
                show_quota_help()
        else:
            st.warning("Enter a topic first.")
with r1c3:
    if st.button("🔑 Key Concepts", use_container_width=True):
        if run_gen("Key Concepts", **g):
            st.success("✅ Done!")
with r1c4:
    if st.button("💡 Mnemonics", use_container_width=True):
        if run_gen("Mnemonics", **g):
            st.success("✅ Done!")

r2c1, r2c2, r2c3 = st.columns(3)
with r2c1:
    if st.button("🧠 Mind Map", use_container_width=True):
        if run_gen("Mind Map", **g):
            st.success("✅ Done!")
with r2c2:
    if st.button("👶 ELI5 (Explain Simply)", use_container_width=True):
        if run_gen("ELI5", **g):
            st.success("✅ Done!")
with r2c3:
    if st.button("📅 Study Plan", use_container_width=True):
        if run_gen("Study Plan", **g):
            st.success("✅ Done!")

# Display TL;DR
if st.session_state.tldr:
    st.info(f"⚡ **TL;DR**\n\n{st.session_state.tldr}")

# Display Notes
if st.session_state.notes_content:
    with st.expander(f"📘 {st.session_state.notes_heading}", expanded=True):
        st.markdown(st.session_state.notes_content)
        st.download_button("📥 Download Notes", data=st.session_state.notes_content,
            file_name=f"Notes_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", mime="text/plain")

# Display other Step 2 outputs
step2_types = ["Key Concepts", "Mnemonics", "Mind Map", "ELI5", "Study Plan"]
if st.session_state.generated_output and st.session_state.generated_heading in step2_types:
    with st.expander(f"📄 {st.session_state.generated_heading}", expanded=True):
        st.markdown(st.session_state.generated_output)
        st.download_button("📥 Download", data=st.session_state.generated_output,
            file_name=f"{st.session_state.generated_heading}.txt", mime="text/plain",
            key="dl_step2")

# ==========================================================
# STEP 3 — TEST (unlocks after notes)
# ==========================================================

if st.session_state.notes_content:
    st.markdown("""
    <div class="sec-header">
        <div class="sec-num">3</div>
        <div>
            <div class="sec-title">Test Your Knowledge</div>
            <div class="sec-sub">Flashcards, Quiz, Reflection, Feynman Check & your personal AI Tutor</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🎴  Flashcards", "❓  Quiz", "🤔  Reflect & Feynman", "🤖  Socratic Tutor"])

    # ── FLASHCARDS ──
    with tab1:
        st.caption("Generate cards and reveal answers to test your recall.")
        if st.button("Generate Flashcards", use_container_width=True, type="primary", key="fc_gen"):
            run_gen("Flashcards", **g)

        if st.session_state.generated_heading == "Flashcards" and st.session_state.generated_output:
            blocks = st.session_state.generated_output.split("Flashcard")
            idx = 1
            for block in blocks:
                if not block.strip():
                    continue
                parts = block.split("Answer:")
                if len(parts) == 2:
                    q = parts[0].replace("Question:", "").strip().lstrip("0123456789. \n")
                    a = parts[1].strip()
                    rk = f"fc_reveal_{idx}"
                    if rk not in st.session_state:
                        st.session_state[rk] = False
                    st.markdown(f'<div class="fc-card"><div class="fc-num">CARD {idx} OF 5</div><div class="fc-q">{q}</div></div>', unsafe_allow_html=True)
                    if st.button("👁️ Reveal Answer" if not st.session_state[rk] else "🙈 Hide Answer", key=f"fc_btn_{idx}"):
                        st.session_state[rk] = not st.session_state[rk]
                    if st.session_state[rk]:
                        st.success(f"**Answer:** {a}")
                    st.markdown("<br>", unsafe_allow_html=True)
                    idx += 1

    # ── QUIZ ──
    with tab2:
        st.caption("Answer all 5 questions and submit to get your score and exam readiness rating.")
        if st.button("Generate Quiz", use_container_width=True, type="primary", key="qz_gen"):
            run_gen("Quiz", **g)
            st.session_state.quiz_score = None

        if st.session_state.generated_heading == "Quiz" and st.session_state.generated_output:
            out = st.session_state.generated_output
            blocks = re.split(r'\*?\*?Question\s*\d+[\.\:]?\*?\*?', out, flags=re.IGNORECASE)
            blocks = [b.strip() for b in blocks if b.strip()]
            u_ans, c_ans, qi = [], [], 1

            for blk in blocks:
                lines = [l.strip() for l in blk.split("\n") if l.strip()]
                if not lines:
                    continue
                qtxt = lines[0].lstrip("0123456789:.*) ")
                opts = [l for l in lines if re.match(r'^[A-Da-d][\.\)]\s+.+', l)]
                cline = [l for l in lines if re.search(r'correct\s*answer', l, re.IGNORECASE)]
                if opts and qtxt and len(opts) >= 2:
                    st.markdown(f"**Q{qi}.** {qtxt}")
                    sel = st.radio("", opts, key=f"qans_{qi}", index=None, label_visibility="collapsed")
                    u_ans.append(sel)
                    if cline:
                        m = re.search(r':\s*([A-Da-d])', cline[0])
                        if m:
                            c_ans.append(m.group(1).upper())
                    st.markdown("---")
                    qi += 1

            if u_ans:
                if st.button("📝 Submit Quiz", use_container_width=True, type="primary"):
                    if None in u_ans:
                        st.warning("⚠️ Answer all questions first!")
                    else:
                        score = sum(
                            1 for i in range(len(c_ans))
                            if u_ans[i] and re.match(r'^' + c_ans[i], u_ans[i].strip(), re.IGNORECASE)
                        )
                        st.session_state.quiz_score = score

                if st.session_state.quiz_score is not None:
                    sc = st.session_state.quiz_score
                    tot = len(c_ans)
                    pct = int((sc / tot) * 100) if tot > 0 else 0
                    readiness = min(100, pct + 10)
                    st.markdown("---")
                    mc1, mc2, mc3 = st.columns(3)
                    with mc1: st.metric("Score", f"{sc}/{tot}")
                    with mc2: st.metric("Percentage", f"{pct}%")
                    with mc3: st.metric("Exam Ready", f"{readiness}%")
                    st.progress(readiness / 100)
                    if pct >= 80:
                        st.success("🎉 Excellent! You're ready for the exam.")
                    elif pct >= 50:
                        st.warning("👍 Good effort! Review weak areas and try again.")
                    else:
                        st.error("📚 Keep going — re-read notes and retake the quiz.")

    # ── REFLECT + FEYNMAN ──
    with tab3:
        rfc1, rfc2 = st.columns(2)
        with rfc1:
            if st.button("Generate Reflection Questions", use_container_width=True, key="ref_gen"):
                run_gen("Reflection", **g)
        with rfc2:
            if st.button("Generate Exam Paper", use_container_width=True, key="exam_gen"):
                run_gen("Exam Mode", **g)

        if st.session_state.generated_heading in ["Reflection", "Exam Mode"] and st.session_state.generated_output:
            st.markdown(st.session_state.generated_output)
            st.download_button("📥 Download", data=st.session_state.generated_output,
                file_name=f"{st.session_state.generated_heading}.txt", mime="text/plain", key="dl_ref")

        st.markdown("---")
        st.markdown("#### 🧪 Feynman Technique Checker")
        st.caption("Write your explanation of the topic. AI will score it and tell you what's missing — like a real teacher.")
        fi = st.text_area("Explain the topic in your own words (as if teaching a friend):", height=130, key="feynman_ta", placeholder="In my own words, this topic is about...")
        if st.button("✅ Analyse My Understanding", use_container_width=True, type="primary"):
            if not fi.strip():
                st.warning("⚠️ Write your explanation first!")
            else:
                cp = f"Topic: {manual if manual.strip() else 'uploaded content'}\n\nStudent explanation:\n{fi}\n\n"
                fp, _ = build_prompt(cp, difficulty, persona, "Feynman")
                with st.spinner("Analysing your understanding..."):
                    fr = generate_with_rotation(fp, 0.3)
                if fr in ("QUOTA_EXCEEDED", "NO_KEYS"):
                    show_quota_help()
                else:
                    st.session_state.feynman_feedback = fr

        if st.session_state.feynman_feedback:
            st.markdown(st.session_state.feynman_feedback)

    # ── SOCRATIC TUTOR ──
    with tab4:
        st.caption("Your AI study buddy asks deep questions to challenge your real understanding — not just memorisation.")

        if st.button("🤔 Ask Me a Question", use_container_width=True, type="primary"):
            sp, _ = build_prompt(content, difficulty, "Analytical", "Socratic")
            with st.spinner("Thinking of a deep question..."):
                sr = generate_with_rotation(sp, 0.6)
            if sr in ("QUOTA_EXCEEDED", "NO_KEYS"):
                show_quota_help()
            else:
                st.session_state.tutor_history.append({"role": "tutor", "message": sr})

        for msg in st.session_state.tutor_history:
            if msg["role"] == "tutor":
                st.markdown(f'<div class="tutor-q">🤖 <strong>Tutor:</strong> {msg["message"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="tutor-a">👤 <strong>You:</strong> {msg["message"]}</div>', unsafe_allow_html=True)

        if st.session_state.tutor_history:
            reply = st.text_input("Your answer:", key="tutor_reply", placeholder="Type your answer...")
            tc1, tc2 = st.columns([3, 1])
            with tc1:
                if st.button("Send ➡️", use_container_width=True):
                    if reply.strip():
                        st.session_state.tutor_history.append({"role": "student", "message": reply})
                        fup = f"Topic: {manual if manual.strip() else 'the content'}\nStudent answered: {reply}\nAsk a deeper Socratic follow-up. Short and thought-provoking."
                        with st.spinner("Thinking..."):
                            fur = generate_with_rotation(fup, 0.6)
                        if fur not in ("QUOTA_EXCEEDED", "NO_KEYS"):
                            st.session_state.tutor_history.append({"role": "tutor", "message": fur})
                        st.rerun()
            with tc2:
                if st.button("Reset", use_container_width=True):
                    st.session_state.tutor_history = []
                    st.rerun()

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📖</div>
        <div class="empty-title">Generate Notes first to unlock all testing features</div>
        <div class="empty-sub">Enter a topic above and click "📝 Notes" to get started</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# SESSION HISTORY
# ==========================================================

if st.session_state.history:
    st.markdown("""
    <div class="sec-header">
        <div class="sec-num" style="background:linear-gradient(135deg,#0f766e,#0891b2);">📜</div>
        <div>
            <div class="sec-title">Session History</div>
            <div class="sec-sub">Everything generated this session — download any output</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"**{item['format']}** — {item['preview']}..."):
            st.markdown(f'<span class="history-time">{item["timestamp"]}</span>', unsafe_allow_html=True)
            st.markdown(item.get("output", ""))
            st.download_button("📥 Download", data=item.get("output", ""),
                file_name=f"{item['format']}_{i}.txt", mime="text/plain", key=f"hist_dl_{i}")