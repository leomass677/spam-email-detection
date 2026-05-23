import streamlit as st
import pandas as pd
import tempfile
import os
import time
from src.pipeline.prediction_pipeline import PredictionPipeline

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="SpamGuard — Email Classifier",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Syne:wght@400;500;600;700;800&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }

/* ── Page background ── */
.stApp {
    background: #08080f;
    color: #ededf5;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 99px; }

/* ── Ambient glow canvas ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 55% 38% at 72% 8%, rgba(108,92,231,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 38% 28% at 12% 82%, rgba(29,158,117,0.07) 0%, transparent 52%);
    pointer-events: none;
    z-index: 0;
}

/* ── Block container width ── */
.block-container {
    max-width: 860px !important;
    padding: 2.5rem 1.5rem 5rem !important;
}

/* ══════════════════════════════════════════
   TOPBAR
══════════════════════════════════════════ */
.sg-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 3rem;
    padding-bottom: 1.25rem;
    border-bottom: 0.5px solid rgba(255,255,255,0.07);
}
.sg-brand {
    display: flex;
    align-items: center;
    gap: 11px;
}
.sg-brand-icon {
    width: 36px; height: 36px;
    background: rgba(108,92,231,0.15);
    border: 0.5px solid rgba(108,92,231,0.4);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
}
.sg-brand-name {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #ededf5;
}
.sg-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 12px;
    color: #1D9E75;
    background: rgba(29,158,117,0.1);
    border: 0.5px solid rgba(29,158,117,0.3);
    padding: 5px 13px;
    border-radius: 99px;
    font-family: 'DM Mono', monospace;
}
.sg-status-dot {
    width: 6px; height: 6px;
    background: #1D9E75;
    border-radius: 50%;
    animation: pulse 2s ease infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.25; }
}

/* ══════════════════════════════════════════
   HERO
══════════════════════════════════════════ */
.sg-hero {
    margin-bottom: 2.5rem;
}
.sg-hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6c5ce7;
    margin-bottom: 10px;
}
.sg-hero h1 {
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #ededf5;
    margin: 0 0 12px;
}
.sg-hero h1 em {
    font-style: normal;
    color: #a89dfc;
}
.sg-hero p {
    font-size: 15px;
    color: rgba(237,237,245,0.55);
    line-height: 1.6;
    max-width: 480px;
    font-weight: 400;
}

/* ══════════════════════════════════════════
   TABS
══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: #111120 !important;
    border: 0.5px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 3px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(237,237,245,0.45) !important;
    border-radius: 9px !important;
    border: none !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: all 0.18s !important;
    letter-spacing: 0.01em !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #ededf5 !important;
    background: rgba(255,255,255,0.05) !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #6c5ce7 !important;
    color: #fff !important;
    box-shadow: 0 0 22px rgba(108,92,231,0.28) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] {
    padding: 1.5rem 0 0 !important;
}

/* ══════════════════════════════════════════
   CARD
══════════════════════════════════════════ */
.sg-card {
    background: #111120;
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.75rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.sg-card:hover { border-color: rgba(255,255,255,0.13); }
.sg-card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: rgba(237,237,245,0.4);
    margin-bottom: 1.25rem;
}

/* ══════════════════════════════════════════
   TEXTAREA
══════════════════════════════════════════ */
.stTextArea label { display: none !important; }
.stTextArea textarea {
    background: #0d0d1a !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #d4d4e8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
    font-weight: 300 !important;
    line-height: 1.7 !important;
    padding: 14px 16px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    resize: vertical !important;
}
.stTextArea textarea::placeholder {
    color: rgba(237,237,245,0.2) !important;
}
.stTextArea textarea:focus {
    border-color: rgba(108,92,231,0.55) !important;
    box-shadow: 0 0 0 3px rgba(108,92,231,0.1) !important;
    background: #0f0f1e !important;
    outline: none !important;
}

/* ══════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════ */
.stButton > button {
    background: #6c5ce7 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: opacity 0.15s, transform 0.12s !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    opacity: 0.87 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 0 20px rgba(108,92,231,0.3) !important;
}
.stButton > button:active { transform: scale(0.97) !important; }
.stButton > button:focus { outline: none !important; box-shadow: none !important; }

/* Download button */
.stDownloadButton > button {
    background: rgba(29,158,117,0.15) !important;
    color: #2dca8a !important;
    border: 0.5px solid rgba(29,158,117,0.35) !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    transition: opacity 0.15s !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover { opacity: 0.82 !important; }

/* ══════════════════════════════════════════
   FILE UPLOADER
══════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: #0d0d1a !important;
    border: 1.5px dashed rgba(255,255,255,0.12) !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(108,92,231,0.45) !important;
    background: rgba(108,92,231,0.03) !important;
}
[data-testid="stFileUploader"] label {
    color: rgba(237,237,245,0.5) !important;
    font-size: 14px !important;
}
[data-testid="stFileUploader"] small {
    color: rgba(237,237,245,0.3) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
}

/* ══════════════════════════════════════════
   PROGRESS BAR
══════════════════════════════════════════ */
.stProgress > div > div {
    border-radius: 99px !important;
    background: rgba(255,255,255,0.06) !important;
}
.stProgress > div > div > div {
    background: #6c5ce7 !important;
    border-radius: 99px !important;
}

/* ══════════════════════════════════════════
   SPINNER
══════════════════════════════════════════ */
.stSpinner > div { border-color: #6c5ce7 transparent transparent transparent !important; }

/* ══════════════════════════════════════════
   RESULT BLOCKS
══════════════════════════════════════════ */
.sg-result {
    border-radius: 16px;
    overflow: hidden;
    margin-top: 1.25rem;
    animation: fadeUp 0.3s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.sg-result-accent { height: 3px; width: 100%; }
.sg-result-body {
    background: #111120;
    border: 0.5px solid rgba(255,255,255,0.08);
    border-top: none;
    padding: 1.5rem 1.75rem;
}
.sg-result-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 1.25rem;
}
.sg-result-icon {
    width: 46px; height: 46px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.sg-result-headline {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 3px;
}
.sg-result-sub {
    font-size: 13px;
    color: rgba(237,237,245,0.5);
}
.sg-conf-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 7px;
}
.sg-conf-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: rgba(237,237,245,0.35);
}
.sg-conf-pct {
    font-family: 'DM Mono', monospace;
    font-size: 18px;
    font-weight: 400;
}
.sg-track {
    height: 4px;
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    overflow: hidden;
    margin-bottom: 1.25rem;
}
.sg-fill {
    height: 100%;
    border-radius: 99px;
}
.sg-kw-section {
    margin-top: 0.75rem;
}
.sg-kw-label {
    font-size: 11px;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: rgba(237,237,245,0.25);
    margin-bottom: 8px;
}
.sg-kw-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}
.sg-kw-pill {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    padding: 3px 11px;
    border-radius: 99px;
}
.sg-kw-spam { background: rgba(226,75,74,0.12); color: #f09595; border: 0.5px solid rgba(226,75,74,0.3); }
.sg-kw-ham  { background: rgba(29,158,117,0.12); color: #5DCAA5; border: 0.5px solid rgba(29,158,117,0.3); }

/* spam accent colors */
.sg-accent-spam { background: #E24B4A; }
.sg-icon-spam   { background: rgba(226,75,74,0.12); color: #f09595; border: 0.5px solid rgba(226,75,74,0.25); }
.sg-text-spam   { color: #f09595; }

/* ham accent colors */
.sg-accent-ham  { background: #1D9E75; }
.sg-icon-ham    { background: rgba(29,158,117,0.12); color: #5DCAA5; border: 0.5px solid rgba(29,158,117,0.25); }
.sg-text-ham    { color: #5DCAA5; }

/* ══════════════════════════════════════════
   STAT CARDS
══════════════════════════════════════════ */
.sg-stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px;
    margin-bottom: 1.5rem;
}
.sg-stat {
    background: #111120;
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.1rem;
    text-align: center;
}
.sg-stat-val {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 5px;
}
.sg-stat-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: rgba(237,237,245,0.35);
}

/* ══════════════════════════════════════════
   TABLE
══════════════════════════════════════════ */
.sg-table-wrap {
    background: #111120;
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    overflow: hidden;
}
.sg-table-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px;
    border-bottom: 0.5px solid rgba(255,255,255,0.07);
}
.sg-table-title {
    font-size: 13px;
    font-weight: 600;
    color: rgba(237,237,245,0.6);
    letter-spacing: 0.02em;
}

/* Streamlit dataframe overrides */
[data-testid="stDataFrame"] {
    border-radius: 0 !important;
    border: none !important;
}
[data-testid="stDataFrame"] iframe {
    border-radius: 0 !important;
}

/* ══════════════════════════════════════════
   FILE SELECTED BADGE
══════════════════════════════════════════ */
.sg-file-badge {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 11px 16px;
    background: rgba(29,158,117,0.08);
    border: 0.5px solid rgba(29,158,117,0.28);
    border-radius: 10px;
    margin-top: 12px;
    font-size: 13px;
    color: rgba(237,237,245,0.75);
}
.sg-file-badge strong { color: #5DCAA5; font-weight: 500; }

/* ══════════════════════════════════════════
   ALERT / ERROR / WARNING
══════════════════════════════════════════ */
.sg-alert {
    padding: 12px 16px;
    border-radius: 10px;
    font-size: 13px;
    border-left: 3px solid;
    margin-top: 12px;
}
.sg-alert-warn {
    background: rgba(186,117,23,0.1);
    border-color: #BA7517;
    color: rgba(237,237,245,0.7);
}
.sg-alert-error {
    background: rgba(226,75,74,0.1);
    border-color: #E24B4A;
    color: rgba(237,237,245,0.75);
}

/* ══════════════════════════════════════════
   FOOTER
══════════════════════════════════════════ */
.sg-footer {
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 0.5px solid rgba(255,255,255,0.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.sg-footer-brand {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: rgba(237,237,245,0.25);
}
.sg-footer-pills {
    display: flex;
    gap: 1rem;
}
.sg-footer-pill {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: rgba(237,237,245,0.25);
}

</style>
""", unsafe_allow_html=True)


# ── Pipeline ─────────────────────────────────────────────────────────────────
@st.cache_resource
def get_pipeline():
    return PredictionPipeline(load_models=True)

try:
    pipeline = get_pipeline()
    model_loaded = True
except Exception as e:
    model_loaded = False
    load_error = str(e)


# ── Topbar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sg-topbar">
    <div class="sg-brand">
        <div class="sg-brand-icon">🛡</div>
        <span class="sg-brand-name">SpamGuard AI</span>
    </div>
    <div class="sg-status">
        <span class="sg-status-dot"></span>
        Model loaded
    </div>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.markdown(f'<div class="sg-alert sg-alert-error">Failed to load model: {load_error}</div>', unsafe_allow_html=True)
    st.stop()


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sg-hero">
    <div class="sg-hero-eyebrow">Email classifier</div>
    <h1>Identify spam with <em>confidence</em></h1>
    <p>Paste an email for instant analysis, or upload an MBOX file to classify in bulk.</p>
</div>
""", unsafe_allow_html=True)


# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["  📧  Single email  ", "  📁  Batch processing  "])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — Single email
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sg-card"><div class="sg-card-title">✉ Paste email content</div>', unsafe_allow_html=True)

    email_text = st.text_area(
        "email",
        height=190,
        placeholder="Dear friend, I have an exclusive business proposal worth $2,000,000 USD. Act now — guaranteed returns, no risk involved…",
        key="email_input",
        label_visibility="collapsed",
    )

    col_a, col_b, col_c = st.columns([2.2, 1, 1])
    with col_a:
        classify_btn = st.button("🔍  Analyze email", use_container_width=True, type="primary")

    st.markdown('</div>', unsafe_allow_html=True)  # close sg-card

    if classify_btn:
        if not email_text.strip():
            st.markdown("""
            <div class="sg-alert sg-alert-warn">
                Please paste some email content before analyzing.
            </div>""", unsafe_allow_html=True)
        else:
            with st.spinner("Analyzing…"):
                bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.008)
                    bar.progress(i + 1)
                bar.empty()

                try:
                    result     = pipeline.predict_single_email(email_text)
                    prediction = result["prediction"]
                    confidence = result.get("confidence", 0)
                    conf_pct   = f"{confidence:.1f}%" if confidence else "—"
                    conf_int   = int(round(confidence)) if confidence else 0
                    is_spam    = prediction == "Spam"
                    cls        = "spam" if is_spam else "ham"

                    headline = "This email looks like spam" if is_spam else "This email looks safe"
                    subline  = "Avoid clicking links or downloading attachments." if is_spam else "No suspicious signals detected."
                    icon     = "🚫" if is_spam else "✅"
                    kw_label = "Flagged signals" if is_spam else "Legitimate signals"

                    st.markdown(f"""
                    <div class="sg-result">
                        <div class="sg-result-accent sg-accent-{cls}"></div>
                        <div class="sg-result-body">
                            <div class="sg-result-row">
                                <div class="sg-result-icon sg-icon-{cls}">{icon}</div>
                                <div>
                                    <div class="sg-result-headline sg-text-{cls}">{headline}</div>
                                    <div class="sg-result-sub">{subline}</div>
                                </div>
                                <div style="margin-left:auto;text-align:right">
                                    <div style="font-size:11px;color:rgba(237,237,245,0.25);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px">model</div>
                                    <div style="font-family:'DM Mono',monospace;font-size:12px;color:rgba(237,237,245,0.4)">XGBoost v2.1</div>
                                </div>
                            </div>
                            <div class="sg-conf-row">
                                <span class="sg-conf-label">Confidence</span>
                                <span class="sg-conf-pct sg-text-{cls}">{conf_pct}</span>
                            </div>
                            <div class="sg-track">
                                <div class="sg-fill sg-accent-{cls}" style="width:{conf_int}%"></div>
                            </div>
                            <div class="sg-kw-section">
                                <div class="sg-kw-label">{kw_label}</div>
                                <div class="sg-kw-pills">
                                    <span class="sg-kw-pill sg-kw-{cls}">{"No strong signals" if conf_int < 60 else prediction}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.markdown(f'<div class="sg-alert sg-alert-error">Analysis error: {e}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — Batch processing
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sg-card"><div class="sg-card-title">📁 Upload email file</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload",
        type=["mbox", "txt"],
        help="Select an MBOX or TXT file exported from your email client",
        label_visibility="collapsed",
    )

    if uploaded_file:
        size_kb = uploaded_file.size / 1024
        st.markdown(f"""
        <div class="sg-file-badge">
            📄&nbsp; <strong>{uploaded_file.name}</strong>
            &nbsp;<span style="color:rgba(237,237,245,0.35);font-family:'DM Mono',monospace;font-size:11px">
                {size_kb:.1f} KB
            </span>
        </div>""", unsafe_allow_html=True)

        col_a2, col_b2, col_c2 = st.columns([2.2, 1, 1])
        with col_a2:
            process_btn = st.button("⚙️  Process emails", use_container_width=True, type="primary")

        st.markdown('</div>', unsafe_allow_html=True)  # close sg-card

        if process_btn:
            with st.spinner("Processing…"):
                bar2 = st.progress(0)
                for i in range(50):
                    time.sleep(0.015)
                    bar2.progress(i + 1)

                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mbox") as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name

                    try:
                        df = pipeline.predict_mbox_file(tmp_path)
                        bar2.progress(100)
                        bar2.empty()

                        spam_count  = len(df[df["Prediction"] == "Spam"])
                        ham_count   = len(df[df["Prediction"] == "Ham"])
                        total_count = len(df)

                        # ── Stats ─────────────────────────────────────────────
                        st.markdown(f"""
                        <div class="sg-stat-grid">
                            <div class="sg-stat">
                                <div class="sg-stat-val" style="color:#ededf5">{total_count}</div>
                                <div class="sg-stat-label">Total</div>
                            </div>
                            <div class="sg-stat">
                                <div class="sg-stat-val" style="color:#f09595">{spam_count}</div>
                                <div class="sg-stat-label">Spam</div>
                            </div>
                            <div class="sg-stat">
                                <div class="sg-stat-val" style="color:#5DCAA5">{ham_count}</div>
                                <div class="sg-stat-label">Legitimate</div>
                            </div>
                            <div class="sg-stat">
                                <div class="sg-stat-val" style="color:#a89dfc">
                                    {ham_count/total_count*100:.0f}%
                                </div>
                                <div class="sg-stat-label">Ham rate</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── Table ─────────────────────────────────────────────
                        st.markdown("""
                        <div class="sg-table-wrap">
                            <div class="sg-table-header">
                                <span class="sg-table-title">Email preview — first 10</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.dataframe(
                            df[["Time", "Subject", "Prediction"]].head(10),
                            use_container_width=True,
                            hide_index=True,
                        )

                        # ── Download ──────────────────────────────────────────
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            label="💾  Download full report (CSV)",
                            data=csv,
                            file_name=f"spamguard_{int(time.time())}.csv",
                            mime="text/csv",
                            use_container_width=False,
                        )

                    finally:
                        if os.path.exists(tmp_path):
                            try:
                                os.unlink(tmp_path)
                            except Exception:
                                pass

                except Exception as e:
                    bar2.empty()
                    st.markdown(f'<div class="sg-alert sg-alert-error">Processing error: {e}</div>', unsafe_allow_html=True)

    else:
        st.markdown('</div>', unsafe_allow_html=True)  # close sg-card when no file


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sg-footer">
    <span class="sg-footer-brand">SpamGuard AI</span>
    <div class="sg-footer-pills">
        <span class="sg-footer-pill">⚡ Real-time</span>
        <span class="sg-footer-pill">🛡 99% accuracy</span>
        <span class="sg-footer-pill">🔒 Private</span>
    </div>
</div>
""", unsafe_allow_html=True)