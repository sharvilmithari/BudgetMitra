import streamlit as st

# ─────────────────────────────────────────────
#  LANDING PAGE CSS
# ─────────────────────────────────────────────

def inject_landing_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

    #MainMenu, footer, header { visibility: hidden; }

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        scroll-behavior: smooth;
    }

    .stApp {
        background: #05070f !important;
        color: #e2e8f0;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* ── NOISE OVERLAY ── */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
        opacity: 0.4;
    }

    /* ── HIDE STREAMLIT CHROME ── */
    [data-testid="stDecoration"] { display: none; }
    [data-testid="stToolbar"] { display: none; }
    section[data-testid="stSidebar"] { display: none; }

    /* ── BUTTONS ── */
    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        transition: all 0.22s ease !important;
        letter-spacing: 0.1px !important;
    }

    /* Primary CTA button */
    div[data-testid="column"]:nth-of-type(1) .stButton > button,
    .cta-primary-col .stButton > button {
        background: linear-gradient(135deg, #4f7cff 0%, #6a5cff 50%, #8b5cf6 100%) !important;
        color: #fff !important;
        border: none !important;
        height: 52px !important;
        font-size: 1rem !important;
        box-shadow: 0 8px 30px rgba(91,78,248,0.4) !important;
    }
    div[data-testid="column"]:nth-of-type(1) .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 40px rgba(91,78,248,0.55) !important;
    }

    /* Secondary button */
    div[data-testid="column"]:nth-of-type(2) .stButton > button {
        background: rgba(79,124,255,0.12) !important;
        color: #dbe4ff !important;
        border: 1px solid rgba(139,92,246,0.35) !important;
        height: 52px !important;
        font-size: 1rem !important;
        box-shadow: none !important;
    }
    div[data-testid="column"]:nth-of-type(2) .stButton > button:hover {
        background: rgba(255,255,255,0.08) !important;
        color: #e2e8f0 !important;
        border-color: rgba(255,255,255,0.2) !important;
        transform: translateY(-1px) !important;
    }

    /* ── SCROLL ANIMATIONS ── */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 40px rgba(91,78,248,0.3); }
        50% { box-shadow: 0 0 80px rgba(91,78,248,0.6), 0 0 120px rgba(139,92,246,0.3); }
    }
    @keyframes spin-slow {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    /* ── NAV ── */
    .sw-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 24px 60px;
        position: sticky;
        top: 0;
        z-index: 100;
        background: rgba(5,7,15,0.85);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .sw-nav-logo {
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    .sw-nav-logo-wrap {
        display: flex;
        align-items: center;
    }
    .sw-nav-logo-wrap img {
        height: 40px;
        max-width: 180px;
        object-fit: contain;
        display: block;
        filter: drop-shadow(0 0 10px rgba(129,140,248,0.25));
    }
    .sw-nav-links {
        display: flex;
        gap: 36px;
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
    }

    /* ── HERO ── */
    .sw-hero {
        position: relative;
        min-height: 92vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 80px 40px 60px;
        overflow: hidden;
        animation: fadeUp 0.8s ease both;
    }
    .sw-hero-orb-1 {
        position: absolute;
        width: 700px; height: 700px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(91,78,248,0.18) 0%, transparent 70%);
        top: -200px; left: 50%;
        transform: translateX(-50%);
        pointer-events: none;
        filter: blur(40px);
    }
    .sw-hero-orb-2 {
        position: absolute;
        width: 400px; height: 400px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%);
        bottom: 0; right: 10%;
        pointer-events: none;
        filter: blur(60px);
    }
    .sw-hero-orb-3 {
        position: absolute;
        width: 300px; height: 300px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(34,211,238,0.08) 0%, transparent 70%);
        bottom: 20%; left: 5%;
        pointer-events: none;
        filter: blur(50px);
    }
    .sw-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(91,78,248,0.1);
        border: 1px solid rgba(91,78,248,0.3);
        border-radius: 99px;
        padding: 6px 18px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #a5b4fc;
        margin-bottom: 32px;
        letter-spacing: 0.5px;
        animation: fadeUp 0.6s 0.1s ease both;
    }
    .sw-badge-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #818cf8;
        animation: pulse-glow 2s infinite;
        box-shadow: 0 0 8px rgba(129,140,248,0.8);
    }
    .sw-hero-title {
        font-family: 'Syne', sans-serif;
        font-size: clamp(3.2rem, 7vw, 6rem);
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #f1f5f9 20%, #94a3b8 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        animation: fadeUp 0.7s 0.2s ease both;
    }
    .sw-hero-title span {
        background: linear-gradient(135deg, #818cf8, #c084fc, #38bdf8);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 4s linear infinite;
    }
    .sw-hero-sub {
        font-size: clamp(1rem, 2vw, 1.3rem);
        color: #475569;
        max-width: 580px;
        margin: 0 auto 48px;
        line-height: 1.65;
        font-weight: 400;
        animation: fadeUp 0.7s 0.35s ease both;
    }
    .sw-hero-sub strong { color: #94a3b8; font-weight: 600; }

    .sw-hero-btns {
        display: flex;
        gap: 16px;
        justify-content: center;
        flex-wrap: wrap;
        animation: fadeUp 0.7s 0.5s ease both;
    }

    /* ── STATS BAR ── */
    .sw-stats {
        display: flex;
        justify-content: center;
        gap: 60px;
        padding: 32px 40px;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        background: rgba(255,255,255,0.01);
        animation: fadeUp 0.7s 0.7s ease both;
    }
    .sw-stat { text-align: center; }
    .sw-stat-val {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sw-stat-label { font-size: 0.78rem; color: #475569; font-weight: 500; margin-top: 4px; letter-spacing: 0.5px; }

    /* ── SECTION ── */
    .sw-section {
        padding: 100px 60px;
        max-width: 1200px;
        margin: 0 auto;
    }
    .sw-section-tag {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #818cf8;
        margin-bottom: 16px;
    }
    .sw-section-title {
        font-family: 'Syne', sans-serif;
        font-size: clamp(2rem, 4vw, 3rem);
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -1px;
        color: #f1f5f9;
        margin-bottom: 16px;
    }
    .sw-section-desc {
        font-size: 1rem;
        color: #475569;
        max-width: 520px;
        line-height: 1.7;
    }

    /* ── FEATURES GRID ── */
    .sw-features {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin-top: 60px;
    }
    .sw-feature-card {
        background: linear-gradient(145deg, #0c0f1a, #101523);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 36px 32px;
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .sw-feature-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at top left, rgba(91,78,248,0.05), transparent 60%);
        pointer-events: none;
    }
    .sw-feature-card:hover {
        transform: translateY(-6px);
        border-color: rgba(91,78,248,0.25);
        box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(91,78,248,0.1);
    }
    .sw-feature-icon {
        width: 52px; height: 52px;
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 24px;
    }
    .sw-feature-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 10px;
        letter-spacing: -0.3px;
    }
    .sw-feature-desc {
        font-size: 0.9rem;
        color: #475569;
        line-height: 1.65;
    }
    .sw-feature-arrow {
        position: absolute;
        bottom: 28px; right: 28px;
        font-size: 1.1rem;
        color: rgba(129,140,248,0.3);
        transition: color 0.2s, transform 0.2s;
    }
    .sw-feature-card:hover .sw-feature-arrow {
        color: rgba(129,140,248,0.8);
        transform: translate(3px, -3px);
    }

    /* ── APP PREVIEW ── */
    .sw-preview-section {
        padding: 60px 60px 100px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .sw-preview-section::before {
        content: '';
        position: absolute;
        width: 800px; height: 400px;
        background: radial-gradient(ellipse, rgba(91,78,248,0.1) 0%, transparent 70%);
        top: 0; left: 50%; transform: translateX(-50%);
        pointer-events: none;
        filter: blur(40px);
    }
    .sw-mockup {
        max-width: 880px;
        margin: 60px auto 0;
        background: linear-gradient(145deg, #0c0f1a, #0f1420);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 60px 120px rgba(0,0,0,0.7), 0 0 0 1px rgba(255,255,255,0.04), 0 0 60px rgba(91,78,248,0.15);
        animation: float 6s ease-in-out infinite, pulse-glow 4s ease-in-out infinite;
        position: relative;
    }
    .sw-mockup-topbar {
        background: rgba(255,255,255,0.03);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        padding: 14px 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sw-mockup-dot { width: 12px; height: 12px; border-radius: 50%; }
    .sw-mockup-url {
        flex: 1;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 6px;
        padding: 5px 14px;
        font-size: 0.75rem;
        color: #334155;
        text-align: center;
        font-family: 'DM Sans', monospace;
    }
    .sw-mockup-body {
        display: grid;
        grid-template-columns: 200px 1fr;
        min-height: 380px;
    }
    .sw-mockup-sidebar {
        background: rgba(255,255,255,0.015);
        border-right: 1px solid rgba(255,255,255,0.05);
        padding: 28px 16px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .sw-mockup-nav-item {
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.78rem;
        color: #334155;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sw-mockup-nav-item.active {
        background: linear-gradient(135deg, rgba(91,78,248,0.2), rgba(139,92,246,0.12));
        color: #a5b4fc;
        border: 1px solid rgba(91,78,248,0.2);
    }
    .sw-mockup-content {
        padding: 28px;
        display: flex;
        flex-direction: column;
        gap: 18px;
    }
    .sw-mockup-title-row {
        font-family: 'Syne', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #94a3b8;
    }
    .sw-mockup-cards {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }
    .sw-mockup-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 16px;
    }
    .sw-mockup-card-label { font-size: 0.62rem; color: #334155; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; }
    .sw-mockup-card-val { font-size: 1.1rem; font-weight: 700; font-family: monospace; }
    .sw-mockup-bar {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .sw-bar-row { display: flex; align-items: center; gap: 12px; }
    .sw-bar-label { font-size: 0.72rem; color: #475569; min-width: 60px; }
    .sw-bar-track { flex: 1; height: 6px; background: rgba(255,255,255,0.05); border-radius: 99px; overflow: hidden; }
    .sw-bar-fill { height: 100%; border-radius: 99px; }
    .sw-bar-amt { font-size: 0.72rem; color: #64748b; min-width: 50px; text-align: right; }

    /* ── WHY SECTION ── */
    .sw-why-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
        margin-top: 60px;
    }
    .sw-why-card {
        text-align: center;
        padding: 44px 28px;
        background: linear-gradient(160deg, #0c0f1a, #0f1420);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 20px;
        transition: transform 0.25s, border-color 0.25s;
    }
    .sw-why-card:hover {
        transform: translateY(-5px);
        border-color: rgba(129,140,248,0.2);
    }
    .sw-why-num {
        font-family: 'Syne', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        margin-bottom: 20px;
    }
    .sw-why-title { font-size: 1rem; font-weight: 700; color: #e2e8f0; margin-bottom: 10px; font-family: 'Syne', sans-serif; }
    .sw-why-desc { font-size: 0.87rem; color: #475569; line-height: 1.65; }

    /* ── FOOTER ── */
    .sw-footer {
        border-top: 1px solid rgba(255,255,255,0.05);
        padding: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .sw-footer-logo {
        font-family: 'Syne', sans-serif;
        font-size: 1.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sw-footer-links { display: flex; gap: 32px; font-size: 0.82rem; color: #334155; font-weight: 500; }
    .sw-footer-copy { font-size: 0.78rem; color: #1e293b; }
    .sw-footer-credit { font-size: 0.78rem; color: #334155; }
    .sw-footer-credit span { color: #4f46e5; font-weight: 600; }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(91,78,248,0.3); border-radius: 99px; }

    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  LANDING PAGE COMPONENTS
# ─────────────────────────────────────────────

def _hero_section():
    # ── CSS: style real Streamlit buttons to look premium ──
    st.markdown("""
    <style>
    @keyframes btn-shimmer {
        0%   { background-position: 200%% center; }
        100% { background-position: -200%% center; }
    }
    @keyframes btn-glow-pulse {
        0%, 100%% { box-shadow: 0 0 24px rgba(99,102,241,0.5), 0 0 60px rgba(139,92,246,0.2), inset 0 1px 0 rgba(255,255,255,0.15); }
        50%%      { box-shadow: 0 0 40px rgba(99,102,241,0.8), 0 0 90px rgba(139,92,246,0.4), inset 0 1px 0 rgba(255,255,255,0.2); }
    }

    /* ── Wrapper that centers the two columns ── */
    .sw-hero-btns-wrap {
        display: flex;
        justify-content: center;
        padding: 0 0 32px;
    }
    .sw-hero-btns-wrap > div[data-testid="stHorizontalBlock"] {
        max-width: 540px;
        width: 100%%;
        gap: 16px !important;
    }

    /* ── PRIMARY: Get Started button ── */
    div[data-testid="stButton"] button[data-testid="baseButton-secondary"][id="btn_getstarted"],
    .sw-hero-btns-wrap div[data-testid="column"]:nth-of-type(1) button {
        position: relative !important;
        height: 60px !important;
        width: 100%% !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: 0.3px !important;
        border-radius: 16px !important;
        border: none !important;
        cursor: pointer !important;
        background: linear-gradient(
            135deg,
            #6366f1 0%%, #8b5cf6 30%%,
            #a78bfa 50%%, #8b5cf6 70%%,
            #6366f1 100%%
        ) !important;
        background-size: 300%% auto !important;
        animation: btn-shimmer 4s linear infinite, btn-glow-pulse 3s ease-in-out infinite !important;
        transition: transform 0.2s ease, filter 0.2s ease !important;
        overflow: hidden !important;
    }
    .sw-hero-btns-wrap div[data-testid="column"]:nth-of-type(1) button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        filter: brightness(1.12) !important;
    }
    .sw-hero-btns-wrap div[data-testid="column"]:nth-of-type(1) button:active {
        transform: translateY(-1px) scale(0.99) !important;
    }
    /* Gloss sheen via pseudo - override with gradient overlay using outline trick */
    .sw-hero-btns-wrap div[data-testid="column"]:nth-of-type(1) button::after {
        content: '' !important;
        position: absolute !important;
        top: 0; left: 0; right: 0 !important;
        height: 50%% !important;
        background: linear-gradient(to bottom, rgba(255,255,255,0.18), transparent) !important;
        border-radius: 16px 16px 0 0 !important;
        pointer-events: none !important;
    }

    /* ── SECONDARY: Login button ── */
    .sw-hero-btns-wrap div[data-testid="column"]:nth-of-type(2) button {
        position: relative !important;
        height: 60px !important;
        width: 100%% !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #c4b5fd !important;
        letter-spacing: 0.2px !important;
        border-radius: 16px !important;
        cursor: pointer !important;
        background: rgba(99,102,241,0.08) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(139,92,246,0.45) !important;
        box-shadow:
            0 0 0 1px rgba(99,102,241,0.1),
            inset 0 1px 0 rgba(255,255,255,0.07),
            0 8px 32px rgba(0,0,0,0.3) !important;
        transition: all 0.25s ease !important;
    }
    .sw-hero-btns-wrap div[data-testid="column"]:nth-of-type(2) button:hover {
        color: #e2e8f0 !important;
        background: rgba(99,102,241,0.18) !important;
        border-color: rgba(139,92,246,0.75) !important;
        box-shadow:
            0 0 24px rgba(99,102,241,0.35),
            0 0 70px rgba(139,92,246,0.18),
            inset 0 1px 0 rgba(255,255,255,0.1),
            0 14px 40px rgba(0,0,0,0.4) !important;
        transform: translateY(-3px) !important;
    }
    .sw-hero-btns-wrap div[data-testid="column"]:nth-of-type(2) button:active {
        transform: translateY(-1px) !important;
    }

    /* Also style the bottom CTA button */
    .sw-cta-bottom-wrap div[data-testid="column"]:nth-of-type(1) button {
        position: relative !important;
        height: 60px !important;
        width: 100%% !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        border-radius: 16px !important;
        border: none !important;
        background: linear-gradient(135deg,#6366f1 0%%,#8b5cf6 35%%,#a78bfa 50%%,#8b5cf6 70%%,#6366f1 100%%) !important;
        background-size: 300%% auto !important;
        animation: btn-shimmer 4s linear infinite, btn-glow-pulse 3s ease-in-out infinite !important;
        transition: transform 0.2s ease, filter 0.2s ease !important;
    }
    .sw-cta-bottom-wrap div[data-testid="column"]:nth-of-type(1) button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        filter: brightness(1.12) !important;
    }
    </style>

    <div class="sw-hero">
        <div class="sw-hero-orb-1"></div>
        <div class="sw-hero-orb-2"></div>
        <div class="sw-hero-orb-3"></div>
        <div class="sw-hero-title">Spend<span>Wise</span></div>
        <div class="sw-hero-sub">
            Track smarter. Save better.<br>
            <strong>Control your finances</strong> with clarity, every rupee, every day.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Real Streamlit buttons inside a centered wrapper div
    st.markdown('<div class="sw-hero-btns-wrap">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✦  Get Started — It's Free", key="cta_get_started", use_container_width=True):
            st.session_state["page"] = "login"
            st.session_state["login_tab"] = "signup"
            st.rerun()
    with col2:
        if st.button("🔒︎  Login to Account", key="cta_login", use_container_width=True):
            st.session_state["page"] = "login"
            st.session_state["login_tab"] = "login"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def _stats_bar():
    st.markdown("""
    <div class="sw-stats">
        <div class="sw-stat">
            <div class="sw-stat-val">₹10L+</div>
            <div class="sw-stat-label">Tracked across users</div>
        </div>
        <div class="sw-stat">
            <div class="sw-stat-val">5K+</div>
            <div class="sw-stat-label">Transactions logged</div>
        </div>
        <div class="sw-stat">
            <div class="sw-stat-val">9+</div>
            <div class="sw-stat-label">Expense categories</div>
        </div>
        <div class="sw-stat">
            <div class="sw-stat-val">100%</div>
            <div class="sw-stat-label">Secure & private</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _features_section():
    st.markdown("""
    <div class="sw-section">
        <div class="sw-section-tag">✦ Features</div>
        <div class="sw-section-title">Everything you need to<br>own your money</div>
        <div class="sw-section-desc">
            A complete financial toolkit built for students and professionals in India —
            no spreadsheets, no confusion.
        </div>
        <div class="sw-features">
            <div class="sw-feature-card">
                <div class="sw-feature-icon" style="background:rgba(52,211,153,0.1);">⌕</div>
                <div class="sw-feature-title">Expense Tracking</div>
                <div class="sw-feature-desc">
                    Log every rupee in seconds. Categorise food, travel, rent, recharge —
                    with full history and instant search.
                </div>
                <div class="sw-feature-arrow">↗</div>
            </div>
            <div class="sw-feature-card">
                <div class="sw-feature-icon" style="background:rgba(91,78,248,0.1);">ⓘ</div>
                <div class="sw-feature-title">Smart Analytics</div>
                <div class="sw-feature-desc">
                    Visual charts that reveal where your money actually goes —
                    monthly trends, category breakdowns, and surplus tracking.
                </div>
                <div class="sw-feature-arrow">↗</div>
            </div>
            <div class="sw-feature-card">
                <div class="sw-feature-icon" style="background:rgba(192,132,252,0.1);">🗓</div>
                <div class="sw-feature-title">Budget Planning</div>
                <div class="sw-feature-desc">
                    Set monthly budgets and daily limits. Get warned before you overspend —
                    stay disciplined without thinking about it.
                </div>
                <div class="sw-feature-arrow">↗</div>
            </div>
            <div class="sw-feature-card">
                <div class="sw-feature-icon" style="background:rgba(56,189,248,0.1);">☁</div>
                <div class="sw-feature-title">Secure Cloud Storage</div>
                <div class="sw-feature-desc">
                    Your data lives in Supabase cloud — encrypted, backed up, and accessible
                    from any device, anywhere you go.
                </div>
                <div class="sw-feature-arrow">↗</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _app_preview_section():
    import base64, os
    # Load real dashboard screenshot — embed as base64 so Streamlit renders it
    _ss_b64 = "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"
    st.markdown(f"""
    <div class="sw-preview-section">
        <div class="sw-section-tag" style="text-align:center;">✦ App Preview</div>
        <div class="sw-section-title" style="text-align:center;">See it in action</div>
        <div class="sw-section-desc" style="text-align:center;margin:0 auto 48px;">
            A clean, dark interface designed to surface what matters — your money, your control.
        </div>
        <div class="sw-mockup">
            <div class="sw-mockup-topbar">
                <div class="sw-mockup-dot" style="background:#ff5f57;"></div>
                <div class="sw-mockup-dot" style="background:#ffbd2e;"></div>
                <div class="sw-mockup-dot" style="background:#28c840;"></div>
                <div class="sw-mockup-url">spendwise.streamlit.app · Dashboard</div>
            </div>
            <div style="padding:0;line-height:0;">
                <img
                    src="data:image/png;base64,{_ss_b64}"
                    style="width:100%;display:block;border-radius:0 0 22px 22px;object-fit:cover;"
                    alt="SpendWise Dashboard Preview"
                />
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _why_section():
    st.markdown("""
    <div class="sw-section" style="padding-top:40px;">
        <div class="sw-section-tag">✦ Why SpendWise</div>
        <div class="sw-section-title">Built different.<br>Because you deserve better.</div>
        <div class="sw-section-desc">
            Most finance apps are complicated or ugly. SpendWise is neither —
            it's minimal, fast, and actually enjoyable to use.
        </div>
        <div class="sw-why-grid">
            <div class="sw-why-card">
                <div class="sw-why-num">01</div>
                <div class="sw-why-title">Made for India</div>
                <div class="sw-why-desc">
                    Built with ₹ in mind. Indian categories, Indian context —
                    food, recharge, rent, stipend. Not a copy of a Western app.
                </div>
            </div>
            <div class="sw-why-card">
                <div class="sw-why-num">02</div>
                <div class="sw-why-title">Zero friction</div>
                <div class="sw-why-desc">
                    Log a transaction in 3 clicks. No bloated menus, no onboarding hell.
                    Open the app and start tracking — that's it.
                </div>
            </div>
            <div class="sw-why-card">
                <div class="sw-why-num">03</div>
                <div class="sw-why-title">Actually private</div>
                <div class="sw-why-desc">
                    Your data never gets sold. No ads, no tracking, no creepy recommendations.
                    Powered by Supabase with row-level security.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _cta_banner():
    st.markdown("""
    <div style="padding:20px 60px 80px;">
        <div style="
            background: linear-gradient(135deg, #0c0f1a, #101523);
            border: 1px solid rgba(91,78,248,0.2);
            border-radius: 24px;
            padding: 70px 60px 48px;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 30px 80px rgba(0,0,0,0.4), 0 0 60px rgba(91,78,248,0.08);
        ">
            <div style="position:absolute;inset:0;background:radial-gradient(ellipse at center top,rgba(91,78,248,0.12),transparent 60%);pointer-events:none;"></div>
            <div style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#f1f5f9;letter-spacing:-1px;margin-bottom:16px;line-height:1.1;">
                Ready to take control?
            </div>
            <div style="font-size:1rem;color:#475569;max-width:440px;margin:0 auto 36px;line-height:1.6;">
                Join thousands tracking their finances with SpendWise. Free, always.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Real Streamlit button centered and styled via .sw-cta-bottom-wrap CSS
    st.markdown('<div class="sw-cta-bottom-wrap">', unsafe_allow_html=True)
    _, col, _ = st.columns([2.5, 1.5, 2.5])
    with col:
        if st.button("✦  Get Started Free", key="cta_bottom", use_container_width=True):
            st.session_state["page"] = "login"
            st.session_state["login_tab"] = "signup"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def _footer():
    st.markdown("""
    <div class="sw-footer">
        <div>
            <div class="sw-footer-logo">SpendWise</div>
            <div class="sw-footer-credit" style="margin-top:8px;">
                Developed by <span>Sharvil Mithari</span> · India 2026
            </div>
        </div>
        <div class="sw-footer-links">
            <span>Features</span>
            <span>Analytics</span>
            <span>Security</span>
            <span>Contact</span>
        </div>
        <div class="sw-footer-copy">
            © 2026 SpendWise India · All rights reserved
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN LANDING PAGE FUNCTION
# ─────────────────────────────────────────────

def show_landing_page():
    import base64, os
    inject_landing_css()

    # ── Load logo as base64 (same approach as show_login) ──
    logo_b64 = ""
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()

    if logo_b64:
        nav_logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:40px;max-width:160px;object-fit:contain;display:block;" alt="SpendWise">'
    else:
        nav_logo_html = '<span class="sw-nav-logo">💰 SpendWise</span>'

    # Navbar
    st.markdown(f"""
    <div class="sw-nav">
        <div class="sw-nav-logo-wrap">{nav_logo_html}</div>
        <div class="sw-nav-links">
            <span>Features</span>
            <span>Analytics</span>
            <span>Security</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _hero_section()
    _stats_bar()
    _features_section()
    _app_preview_section()
    _why_section()
    _cta_banner()
    _footer()
