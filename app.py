import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* =========================================================
   RESEARCHMIND - READABLE DARK THEME
   ========================================================= */

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');


/* =========================================================
   GLOBAL
   ========================================================= */

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #F5F7FA !important;
}

.stApp {
    background: #111827;

    background-image:
        radial-gradient(
            ellipse 80% 50% at 20% -10%,
            rgba(59, 130, 246, 0.14) 0%,
            transparent 60%
        ),
        radial-gradient(
            ellipse 60% 40% at 80% 110%,
            rgba(139, 92, 246, 0.12) 0%,
            transparent 55%
        );
}


/* =========================================================
   STREAMLIT UI
   ========================================================= */

#MainMenu,
footer,
header {
    visibility: hidden;
}

.block-container {
    padding: 2rem 3rem 4rem;
    max-width: 1200px;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}

.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;

    color: #60A5FA !important;

    margin-bottom: 1rem;
}

.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.03em;

    color: #FFFFFF !important;

    margin: 0 0 1rem;
}

.hero h1 span {
    color: #60A5FA !important;
}

.hero-sub {
    font-size: 1.05rem;
    font-weight: 400;

    color: #CBD5E1 !important;

    max-width: 600px;
    margin: 0 auto;
    line-height: 1.7;
}


/* =========================================================
   DIVIDER
   ========================================================= */

.divider {
    height: 1px;

    background: linear-gradient(
        90deg,
        transparent,
        rgba(96, 165, 250, 0.5),
        transparent
    );

    margin: 2rem 0;
}


/* =========================================================
   INPUT CARD
   ========================================================= */

.input-card {
    background: #1E293B;

    border: 1px solid #334155;

    border-radius: 16px;

    padding: 2rem;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.25);
}


/* =========================================================
   TEXT INPUT
   ========================================================= */

.stTextInput > div > div > input {

    background: #0F172A !important;

    border: 1px solid #475569 !important;

    border-radius: 10px !important;

    color: #FFFFFF !important;

    font-family: 'DM Sans', sans-serif !important;

    font-size: 1rem !important;

    padding: 0.75rem 1rem !important;

    transition:
        border-color 0.2s,
        box-shadow 0.2s !important;
}


/* Placeholder */

.stTextInput > div > div > input::placeholder {
    color: #94A3B8 !important;
    opacity: 1 !important;
}


/* Input focus */

.stTextInput > div > div > input:focus {

    border-color: #60A5FA !important;

    box-shadow:
        0 0 0 3px rgba(96, 165, 250, 0.15) !important;
}


/* Input label */

.stTextInput > label {

    font-family: 'DM Mono', monospace !important;

    font-size: 0.75rem !important;

    letter-spacing: 0.15em !important;

    text-transform: uppercase !important;

    color: #93C5FD !important;

    font-weight: 500 !important;
}


/* =========================================================
   RUN BUTTON
   ========================================================= */

.stButton > button {

    background: linear-gradient(
        135deg,
        #3B82F6 0%,
        #2563EB 100%
    ) !important;

    color: #FFFFFF !important;

    font-family: 'Syne', sans-serif !important;

    font-weight: 700 !important;

    font-size: 0.95rem !important;

    letter-spacing: 0.04em !important;

    border: none !important;

    border-radius: 10px !important;

    padding: 0.7rem 2.2rem !important;

    cursor: pointer !important;

    transition:
        transform 0.15s,
        box-shadow 0.15s,
        opacity 0.15s !important;

    box-shadow:
        0 4px 20px rgba(59, 130, 246, 0.35) !important;

    width: 100%;
}


.stButton > button:hover {

    transform: translateY(-2px) !important;

    box-shadow:
        0 8px 28px rgba(59, 130, 246, 0.45) !important;

    opacity: 0.95 !important;
}


.stButton > button:active {
    transform: translateY(0) !important;
}


/* =========================================================
   EXAMPLE TOPICS
   ========================================================= */

.example-chip {

    background: #1E293B;

    border: 1px solid #475569;

    border-radius: 6px;

    padding: 0.25rem 0.7rem;

    font-size: 0.75rem;

    color: #CBD5E1 !important;

    font-family: 'DM Sans', sans-serif;

}


/* =========================================================
   PIPELINE STEP CARDS
   ========================================================= */

.step-card {

    background: #1E293B;

    border: 1px solid #334155;

    border-radius: 14px;

    padding: 1.5rem 1.8rem;

    margin-bottom: 1.2rem;

    position: relative;

    overflow: hidden;

    transition: border-color 0.3s;

}


.step-card.active {

    border-color: #60A5FA;

    background: #1E3A5F;
}


.step-card.done {

    border-color: #4ADE80;

    background: #16351F;
}


.step-card::before {

    content: '';

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 3px;

    border-radius: 14px 0 0 14px;

    background: #475569;

    transition: background 0.3s;
}


.step-card.active::before {
    background: #60A5FA;
}


.step-card.done::before {
    background: #4ADE80;
}


/* =========================================================
   STEP HEADER
   ========================================================= */

.step-header {

    display: flex;

    align-items: center;

    gap: 0.8rem;

    margin-bottom: 0.3rem;
}


.step-num {

    font-family: 'DM Mono', monospace;

    font-size: 0.7rem;

    font-weight: 500;

    letter-spacing: 0.15em;

    color: #93C5FD !important;
}


.step-title {

    font-family: 'Syne', sans-serif;

    font-size: 0.95rem;

    font-weight: 700;

    color: #FFFFFF !important;
}


.step-status {

    margin-left: auto;

    font-family: 'DM Mono', monospace;

    font-size: 0.68rem;

    letter-spacing: 0.1em;
}


.status-waiting {

    color: #CBD5E1 !important;
}


.status-running {

    color: #60A5FA !important;

    font-weight: 600;
}


.status-done {

    color: #4ADE80 !important;

    font-weight: 600;
}


/* =========================================================
   STEP DESCRIPTION
   ========================================================= */

.step-card div[style*="font-size"] {

    color: #CBD5E1 !important;

    font-size: 0.85rem !important;

    line-height: 1.5 !important;
}


/* =========================================================
   RESULT PANELS
   ========================================================= */

.result-panel {

    background: #1E293B;

    border: 1px solid #334155;

    border-radius: 14px;

    padding: 1.8rem 2rem;

    margin-top: 1rem;

    margin-bottom: 1.5rem;
}


.result-panel-title {

    font-family: 'DM Mono', monospace;

    font-size: 0.72rem;

    font-weight: 500;

    letter-spacing: 0.2em;

    text-transform: uppercase;

    color: #93C5FD !important;

    margin-bottom: 1rem;

    padding-bottom: 0.7rem;

    border-bottom: 1px solid #475569;
}


.result-content {

    font-size: 0.95rem;

    line-height: 1.8;

    color: #E2E8F0 !important;

    white-space: pre-wrap;

    font-family: 'DM Sans', sans-serif;
}


/* =========================================================
   REPORT PANEL
   ========================================================= */

.report-panel {

    background: #1E293B;

    border: 1px solid #3B82F6;

    border-radius: 16px;

    padding: 2rem 2.5rem;

    margin-top: 1rem;
}


/* =========================================================
   FEEDBACK PANEL
   ========================================================= */

.feedback-panel {

    background: #172B1D;

    border: 1px solid #4ADE80;

    border-radius: 16px;

    padding: 2rem 2.5rem;

    margin-top: 1rem;
}


/* =========================================================
   PANEL LABELS
   ========================================================= */

.panel-label {

    font-family: 'DM Mono', monospace;

    font-size: 0.72rem;

    letter-spacing: 0.2em;

    text-transform: uppercase;

    margin-bottom: 1.2rem;

    padding-bottom: 0.7rem;
}


.panel-label.orange {

    color: #60A5FA !important;

    border-bottom: 1px solid #475569;
}


.panel-label.green {

    color: #4ADE80 !important;

    border-bottom: 1px solid #475569;
}


/* =========================================================
   SPINNER
   ========================================================= */

.stSpinner > div {

    color: #60A5FA !important;
}


/* =========================================================
   EXPANDER
   ========================================================= */

details summary {

    font-family: 'DM Mono', monospace !important;

    font-size: 0.75rem !important;

    color: #CBD5E1 !important;

    letter-spacing: 0.1em !important;

    cursor: pointer;
}


/* =========================================================
   SECTION HEADINGS
   ========================================================= */

.section-heading {

    font-family: 'Syne', sans-serif;

    font-size: 1.3rem;

    font-weight: 700;

    color: #FFFFFF !important;

    margin: 2rem 0 1rem;
}


/* =========================================================
   FOOTER / NOTICE
   ========================================================= */

.notice {

    font-family: 'DM Mono', monospace;

    font-size: 0.72rem;

    color: #94A3B8 !important;

    text-align: center;

    margin-top: 3rem;

    letter-spacing: 0.08em;
}


/* =========================================================
   STREAMLIT MARKDOWN
   ========================================================= */

.stMarkdown,
.stMarkdown p,
.stMarkdown li {

    color: #E2E8F0 !important;

}


/* Headings */

.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4 {

    color: #FFFFFF !important;

}


/* =========================================================
   WARNING / ERROR / SUCCESS
   ========================================================= */

.stAlert {

    color: #F8FAFC !important;

}


/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0F172A;
}

::-webkit-scrollbar-thumb {

    background: #475569;

    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #64748B;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done": ("✓ DONE", "status-done"),
    }

    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")

    st.markdown(
        f"""
        <div class="step-card {card_cls}">
            <div class="step-header">
                <span class="step-num">{num}</span>
                <span class="step-title">{title}</span>
                <span class="step-status {cls}">{label}</span>
            </div>
            {
                "<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>"
                + desc +
                "</div>"
                if desc else ""
            }
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">Multi-Agent AI System</div>
        <h1>Research<span>Mind</span></h1>
        <p class="hero-sub">
            Four specialized AI agents collaborate — searching, scraping, writing,
            and critiquing — to deliver a polished research report on any topic.
        </p>
    </div>

    <div class="divider"></div>
    """,
    unsafe_allow_html=True,
)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown(
        '<div class="input-card">',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )

    run_btn = st.button(
        "Run Research Pipeline",
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # Example topics
    st.markdown(
        """
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
            <span style="
                font-family:'DM Mono',monospace;
                font-size:0.68rem;
                color:#605850;
                letter-spacing:0.1em;
            ">TRY →</span>
        """,
        unsafe_allow_html=True,
    )

    examples = [
        "LLM agents 2025",
        "CRISPR gene editing",
        "Fusion energy progress",
    ]

    for ex in examples:
        st.markdown(
            f"""
            <span style="
                background:rgba(255,255,255,0.04);
                border:1px solid rgba(255,255,255,0.08);
                border-radius:6px;
                padding:0.25rem 0.7rem;
                font-size:0.75rem;
                color:#a09890;
                font-family:'DM Sans',sans-serif;
                cursor:default;
            ">{ex}</span>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


with col_pipeline:
    st.markdown(
        '<div class="section-heading">Pipeline</div>',
        unsafe_allow_html=True
    )

    r = st.session_state.results

    def s(step):
        if not r:
            return "waiting"

        steps = ["search", "reader", "writer", "critic"]

        if step in r:
            return "done"

        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"

        return "waiting"

    step_card(
        "01",
        "Search Agent",
        s("search"),
        "Gathers recent web information"
    )

    step_card(
        "02",
        "Reader Agent",
        s("reader"),
        "Scrapes & extracts deep content"
    )

    step_card(
        "03",
        "Writer Chain",
        s("writer"),
        "Drafts the full research report"
    )

    step_card(
        "04",
        "Critic Chain",
        s("critic"),
        "Reviews & scores the report"
    )


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:

    if not topic.strip():
        st.warning("Please enter a research topic first.")

    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False

        st.rerun()


if st.session_state.running and not st.session_state.done:

    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ─────────────────────────────────────────────────────────
    with st.spinner("🔍  Search Agent is working…"):

        search_agent = build_search_agent()

        sr = search_agent.invoke({
            "messages": [
                (
                    "user",
                    f"Find recent, reliable and detailed information about: "
                    f"{topic_val}"
                )
            ]
        })

        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)


    # ── Step 2: Reader ─────────────────────────────────────────────────────────
    with st.spinner("📄  Reader Agent is scraping top resources…"):

        reader_agent = build_reader_agent()

        rr = reader_agent.invoke({
            "messages": [
                (
                    "user",
                    f"Based on the following search results about '{topic_val}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{results['search'][:800]}"
                )
            ]
        })

        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)


    # ── Step 3: Writer ─────────────────────────────────────────────────────────
    with st.spinner("✍️  Writer is drafting the report…"):

        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )

        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined,
        })

        st.session_state.results = dict(results)


    # ── Step 4: Critic ─────────────────────────────────────────────────────────
    with st.spinner("🧐  Critic is reviewing the report…"):

        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })

        st.session_state.results = dict(results)


    st.session_state.running = False
    st.session_state.done = True

    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">Results</div>',
        unsafe_allow_html=True
    )

    # Raw search output
    if "search" in r:

        with st.expander(
            "🔍 Search Results (raw)",
            expanded=False
        ):

            st.markdown(
                f"""
                <div class="result-panel">
                    <div class="result-panel-title">
                        Search Agent Output
                    </div>
                    <div class="result-content">
                        {r["search"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


    # Raw scraped content
    if "reader" in r:

        with st.expander(
            "📄 Scraped Content (raw)",
            expanded=False
        ):

            st.markdown(
                f"""
                <div class="result-panel">
                    <div class="result-panel-title">
                        Reader Agent Output
                    </div>
                    <div class="result-content">
                        {r["reader"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


    # Final report
    if "writer" in r:

        st.markdown(
            """
            <div class="report-panel">
                <div class="panel-label orange">
                    📝 Final Research Report
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(r["writer"])

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )


    # Critic feedback
    if "critic" in r:

        st.markdown(
            """
            <div class="feedback-panel">
                <div class="panel-label green">
                    🧐 Critic Feedback
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(r["critic"])

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="notice">
        ResearchMind · Multi-Agent AI Research & Report Generation · Built by Keyura Motegaonkar
    </div>
    """,
    unsafe_allow_html=True,
)
