from itertools import count

import streamlit as st
import pandas as pd
import json
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded")

# 🔐 LOGIN FUNCTIONS
if not os.path.exists("data"):
    os.makedirs("data", exist_ok=True)

def get_user_file(username):
    return f"data/{username}.json"

def load_user_data(username):
    file_path = get_user_file(username)
    empty_df = pd.DataFrame(columns=["id", "type", "amount", "category", "date", "notes"])

    if not os.path.exists(file_path):
        return empty_df

    with open(file_path, "r") as f:
        raw = json.load(f)

    # Handle dict format {"password": ..., "data": [...]}
    if isinstance(raw, dict):
        records = raw.get("data", [])
    elif isinstance(raw, list):
        records = raw
    else:
        return empty_df

    if not records:
        return empty_df

    df = pd.DataFrame(records)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
    if "amount" in df.columns:
        df["amount"] = df["amount"].astype(float)
    return df

def save_user_data(username, data):
    file_path = get_user_file(username)
    # Preserve password if file already has dict format
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            raw = json.load(f)
    else:
        raw = {}

    if isinstance(raw, dict) and "password" in raw:
        # data can be a DataFrame or a list
        if isinstance(data, pd.DataFrame):
            records = data.copy()
            records["date"] = records["date"].astype(str)
            records = records.to_dict(orient="records")
        else:
            records = data
        raw["data"] = records
        with open(file_path, "w") as f:
            json.dump(raw, f)
    else:
        # Legacy list format
        if isinstance(data, pd.DataFrame):
            records = data.copy()
            records["date"] = records["date"].astype(str)
            records = records.to_dict(orient="records")
        else:
            records = data
        with open(file_path, "w") as f:
            json.dump(records, f)

#  CONFIGURATION & CONSTANTS

DATA_FILE = "expense_data.json"          # Local storage file
SETTINGS_FILE = "settings.json"          # Budget & limit settings

EXPENSE_CATEGORIES = [
    "🍱 Food",
    "🚌 Travel",
    "📱 Recharge",
    "🏠 Rent",
    "🛍️ Shopping",
    "📚 Education",
    "💊 Healthcare",
    "🎮 Entertainment",
    "🔧 Other",
]

INCOME_CATEGORIES = [
    "💰 Stipend",
    "🏦 Allowance",
    "💼 Part-time Job",
    "🎁 Gift",
    "📈 Other Income",
]

# Color palette for charts
CHART_COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
    "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE"
]


#  PAGE CONFIG — must be first Streamlit call


st.set_page_config(
    page_title="SpendWise India",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

#  CUSTOM CSS — Professional Dark Theme


def inject_css():
    """Inject premium UI CSS."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ── GLOBAL ── */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }

    /* ── APP BACKGROUND — deep obsidian with subtle noise texture ── */
    .stApp {
        background: #080b11;
        color: #e2e8f0;
    }

    /* ── MAIN CONTENT AREA ── */
    .block-container {
        padding: 2.5rem 2.5rem 4rem !important;
        max-width: 1200px !important;
    }

    /* ══════════════════════════════════════
       SIDEBAR — glass morphism panel
    ══════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d111a 0%, #090d15 100%) !important;
        border-right: 1px solid rgba(99,102,241,0.12) !important;
        box-shadow: 4px 0 40px rgba(0,0,0,0.5) !important;
    }
    [data-testid="stSidebar"] > div { padding-top: 0 !important; }
    [data-testid="stSidebar"] div[role="radiogroup"] label {
       display: block !important;
       width: 100% !important;
       margin: 6px 0;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label div {
       white-space: normal !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) > div {
        background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(139,92,246,0.12)) !important;
        color: #a5b4fc !important;
        font-weight: 600 !important;
        border: 1px solid rgba(99,102,241,0.25) !important;
        box-shadow: 0 0 20px rgba(99,102,241,0.08);
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover > div {
        background: rgba(255,255,255,0.04) !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
    display: none !important;
    }   
    /* Sidebar divider */
    .sidebar-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin: 14px 0;
    }

    /* ── LOGOUT BUTTON ── */
    [data-testid="stSidebar"] .stButton:last-child > button {
        background: rgba(239,68,68,0.08) !important;
        border: 1px solid rgba(239,68,68,0.2) !important;
        color: #f87171 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        letter-spacing: 0.2px !important;
        transition: all 0.18s !important;
        font-size: 0.875rem !important;
    }
    [data-testid="stSidebar"] .stButton:last-child > button:hover {
        background: rgba(99,102,241,0.12) !important;
        border-color: rgba(239,68,68,0.5) !important;
        transform: none !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25) !important;
    }

    /* ══════════════════════════════════════
       METRIC CARDS
    ══════════════════════════════════════ */
    .metric-card {
        background: linear-gradient(145deg, #0f1420, #111827);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 26px 24px 22px;
        text-align: left;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 20px;
        background: radial-gradient(ellipse at top left, rgba(255,255,255,0.03), transparent 60%);
        pointer-events: none;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255,255,255,0.12);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    .metric-card-icon {
        font-size: 1.6rem;
        margin-bottom: 14px;
        display: block;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #64748b;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.75rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .metric-value.income  { color: #34d399; }
    .metric-value.expense { color: #f87171; }
    .metric-value.balance { color: #818cf8; }
    .metric-value.budget  { color: #c084fc; }
    .metric-sub {
        font-size: 0.72rem;
        color: #475569;
        margin-top: 8px;
        font-weight: 500;
    }
    /* Glowing left accent stripe */
    .card-income  { border-left: 3px solid #34d399 !important; box-shadow: -4px 0 20px rgba(52,211,153,0.15); }
    .card-expense { border-left: 3px solid #f87171 !important; box-shadow: -4px 0 20px rgba(248,113,113,0.15); }
    .card-balance { border-left: 3px solid #818cf8 !important; box-shadow: -4px 0 20px rgba(129,140,248,0.15); }
    .card-budget  { border-left: 3px solid #c084fc !important; box-shadow: -4px 0 20px rgba(192,132,252,0.15); }

    /* ══════════════════════════════════════
       SECTION HEADERS
    ══════════════════════════════════════ */
    .section-header {
        font-size: 1rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 32px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-header::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(99,102,241,0.3), transparent);
    }

    /* ══════════════════════════════════════
       PAGE TITLE
    ══════════════════════════════════════ */
    .page-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #e2e8f0 30%, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 4px;
        letter-spacing: -0.8px;
        line-height: 1.1;
    }
    .page-subtitle {
        font-size: 0.85rem;
        color: #475569;
        margin-bottom: 32px;
        font-weight: 400;
    }

    /* ══════════════════════════════════════
       BANNERS
    ══════════════════════════════════════ */
    .banner {
        border-radius: 12px;
        padding: 14px 18px;
        margin: 10px 0;
        font-size: 0.875rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 10px;
        backdrop-filter: blur(8px);
    }
    .banner-danger  { background: rgba(239,68,68,0.1);  border: 1px solid rgba(239,68,68,0.25);  color: #fca5a5; }
    .banner-warn    { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.25); color: #fcd34d; }
    .banner-success { background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.25); color: #6ee7b7; }

    /* ══════════════════════════════════════
       FORM INPUTS — glassmorphism
    ══════════════════════════════════════ */
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input {
        background: #0f1520 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        transition: border-color 0.18s, box-shadow 0.18s !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: rgba(99,102,241,0.5) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
        outline: none !important;
    }
    .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: rgba(99,102,241,0.5) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
    }
    div[data-baseweb="input"] { height: 50px !important; }
    div[data-baseweb="popover"] { background: #0f1520 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; }

    /* Input labels */
    label[data-testid="stWidgetLabel"] p,
    .stSelectbox label, .stTextInput label,
    .stNumberInput label, .stTextArea label, .stDateInput label {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        color: #475569 !important;
        margin-bottom: 6px !important;
    }

    /* ══════════════════════════════════════
       GLOBAL BUTTONS
    ══════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.2px !important;
        padding: 0 20px !important;
        height: 46px !important;
        transition: all 0.18s ease !important;
        box-shadow: 0 4px 15px rgba(79,70,229,0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #4338ca, #6d28d9) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79,70,229,0.45) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* Form submit */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        height: 52px !important;
        width: 100% !important;
        letter-spacing: 0.3px !important;
        transition: all 0.18s ease !important;
        box-shadow: 0 4px 20px rgba(79,70,229,0.35) !important;
    }
    .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #4338ca, #6d28d9) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(79,70,229,0.5) !important;
    }

    /* ── Download button ── */
    .stDownloadButton > button {
        background: rgba(99,102,241,0.1) !important;
        border: 1px solid rgba(99,102,241,0.3) !important;
        color: #a5b4fc !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover {
        background: rgba(99,102,241,0.2) !important;
        box-shadow: none !important;
    }

    /* ══════════════════════════════════════
       DATAFRAME TABLE
    ══════════════════════════════════════ */
    .stDataFrame {
        border-radius: 14px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: #0f1520 !important;
    }

    /* ══════════════════════════════════════
       TABS
    ══════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        background: #0d111a !important;
        border-radius: 12px !important;
        gap: 4px !important;
        padding: 5px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9px !important;
        color: #64748b !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.3px !important;
        padding: 8px 18px !important;
        transition: all 0.18s !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #fff !important;
        box-shadow: 0 4px 15px rgba(79,70,229,0.35) !important;
    }

    /* ══════════════════════════════════════
       PILLS
    ══════════════════════════════════════ */
    .pill {
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .pill-income  { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.2); }
    .pill-expense { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }

    /* ══════════════════════════════════════
       MISC
    ══════════════════════════════════════ */
    hr { border-color: rgba(255,255,255,0.06) !important; }
    .stRadio > div { gap: 8px; }
    .stProgress > div > div > div { background: linear-gradient(90deg, #4f46e5, #7c3aed) !important; border-radius: 99px !important; }
    .stProgress > div > div { background: rgba(255,255,255,0.06) !important; border-radius: 99px !important; }

    /* Streamlit metric widget */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #0f1420, #111827) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }
    [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-family: 'JetBrains Mono', monospace !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 1.5px; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.5); }

    /* Info / success / warning streamlit boxes */
    .stAlert { border-radius: 12px !important; border: none !important; }

    </style>
    """, unsafe_allow_html=True)



#  DATA LAYER — Load / Save / CRUD


def load_data() -> pd.DataFrame:
    """Load transactions from JSON file. Returns empty DataFrame if file missing."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r",encoding="utf-8") as f:
            records = json.load(f)
        if records:
            df = pd.DataFrame(records)
            df["date"] = pd.to_datetime(df["date"],errors ="coerce")
            df = df.dropna(subset=["date"])

            df["amount"] = df["amount"].astype(float)
            return df
        
    # Return empty DataFrame with correct columns

    return pd.DataFrame(columns=["id", "type", "amount", "category", "date", "notes"])


def save_data(df: pd.DataFrame):
    """Persist DataFrame to JSON file."""
    records = df.copy()
    records["date"] = records["date"].astype(str)   # Serialize datetime
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records.to_dict(orient="records"), f, indent=2,ensure_ascii=False)


def load_settings() -> dict:
    """Load budget & daily limit settings."""
    defaults = {"monthly_budget": 0.0, "daily_limit": 0.0}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r" , encoding="utf-8") as f:
            return {**defaults, **json.load(f)}
    return defaults


def save_settings(settings: dict):
    """Persist settings to JSON."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def add_transaction(df: pd.DataFrame, t_type: str, amount: float,
                    category: str, date, notes: str) -> pd.DataFrame:
    """Append a new transaction row and return updated DataFrame."""
    new_id = int(df["id"].max() + 1) if not df.empty else 1
    new_row = {
        "id": new_id,
        "type": t_type,
        "amount": amount,
        "category": category,
        "date": pd.to_datetime(date),
        "notes": notes,
    }
    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)


def delete_transaction(df: pd.DataFrame, row_id: int) -> pd.DataFrame:
    """Remove a transaction by ID."""
    return df[df["id"] != row_id].reset_index(drop=True)



#  CALCULATIONS


def get_summary(df: pd.DataFrame) -> dict:
    """Calculate total income, expenses, and balance."""
    total_income  = df[df["type"] == "Income"]["amount"].sum()
    total_expense = df[df["type"] == "Expense"]["amount"].sum()
    balance       = total_income - total_expense
    return {
        "income":  total_income,
        "expense": total_expense,
        "balance": balance,
    }


def get_today_expense(df):
    df = df.copy()

    # ✅ Fix date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    today = pd.Timestamp.now().normalize()

    mask = (df["type"] == "Expense") & \
           (df["date"].dt.normalize() == today)

    return df[mask]["amount"].sum()


def get_this_month_expense(df: pd.DataFrame) -> float:
    df = df.copy()  # ✅ important

    # ✅ fix date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    now = pd.Timestamp.now()

    mask = (df["type"] == "Expense") & \
           (df["date"].dt.year == now.year) & \
           (df["date"].dt.month == now.month)

    return df[mask]["amount"].sum()


def fmt(amount: float) -> str:
    """Format number as Indian Rupee string with commas."""
    return f"₹{amount:,.2f}"


#  UI COMPONENTS


CARD_ICONS = {
    "card-income":  "💵",
    "card-expense": "💸",
    "card-balance": "⚖️",
    "card-budget":  "🎯",
}

def render_metric_card(label: str, value: str, card_class: str,
                       value_class: str, sub: str = ""):
    icon = CARD_ICONS.get(card_class, "📊")
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div class="metric-card {card_class}">
        <span class="metric-card-icon">{icon}</span>
        <div class="metric-label">{label}</div>
        <div class="metric-value {value_class}">{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_banner(message: str, level: str = "warn"):
    """Render a colored alert banner (danger / warn / success)."""
    st.markdown(f'<div class="banner banner-{level}">{message}</div>',
                unsafe_allow_html=True)


def render_section_header(title: str):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)



#  PAGE: DASHBOARD


def page_dashboard(df: pd.DataFrame, settings: dict):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Your complete financial overview</div>', unsafe_allow_html=True)

    summary = get_summary(df)
    month_expense = get_this_month_expense(df)
    today_expense = get_today_expense(df)

    # ── Summary Cards ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Total Income", fmt(summary["income"]),
                           "card-income", "income", "All time")
    with c2:
        render_metric_card("Total Expenses", fmt(summary["expense"]),
                           "card-expense", "expense", "All time")
    with c3:
        render_metric_card("Net Balance", fmt(summary["balance"]),
                           "card-balance", "balance",
                           "✅ Surplus" if summary["balance"] >= 0 else "⚠️ Deficit")
    with c4:
        budget = settings["monthly_budget"]
        remaining = budget - month_expense if budget > 0 else 0
        sub = fmt(remaining) + " left" if budget > 0 else "No budget set"
        render_metric_card("Monthly Budget", fmt(budget),
                           "card-budget", "budget", sub)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Budget Alerts ──
    budget = settings["monthly_budget"]
    if budget > 0:
        pct = (month_expense / budget) * 100
        if month_expense > budget:
            render_banner(
                f"🚨 Budget exceeded! You've spent {fmt(month_expense)} of your "
                f"{fmt(budget)} budget this month ({pct:.0f}%).", "danger"
            )
        elif pct >= 80:
            render_banner(
                f"⚠️ Heads up! You've used {pct:.0f}% of your monthly budget. "
                f"Only {fmt(budget - month_expense)} remaining.", "warn"
            )
        else:
            render_banner(
                f"✅ Budget on track! {fmt(budget - month_expense)} remaining "
                f"({100 - pct:.0f}% left).", "success"
            )

    # ── Daily Limit Alert ──
    daily_limit = settings.get("daily_limit", 0)
    if daily_limit > 0 and today_expense > daily_limit:
        render_banner(
            f"🔴 Daily limit breached! Today's spending: {fmt(today_expense)} "
            f"(limit: {fmt(daily_limit)}).", "danger"
        )

    # ── This Month's Mini Stats ──
    render_section_header("📅 This Month at a Glance")
    m1, m2, m3 = st.columns(3)
    tx_count = len(df[
        (df["date"].dt.year == pd.Timestamp.now().year) &
        (df["date"].dt.month == pd.Timestamp.now().month)
    ])
    with m1:
        st.metric("Month Expenses", fmt(month_expense))
    with m2:
        st.metric("Today's Spending", fmt(today_expense))
    with m3:
        st.metric("Transactions This Month", tx_count)

    # ── Recent Transactions ──
    render_section_header("🕐 Recent Transactions")
    if df.empty:
        st.info("No transactions yet. Add your first transaction from the sidebar!")
    else:
        recent = df.sort_values("date", ascending=False).head(10).copy()
        recent["date"] = recent["date"].dt.strftime("%d %b %Y")
        recent["amount"] = recent["amount"].apply(fmt)
        recent = recent[["date", "type", "category", "amount", "notes"]].rename(
            columns={"date": "Date", "type": "Type", "category": "Category",
                     "amount": "Amount", "notes": "Notes"}
        )
        st.dataframe(recent, use_container_width=True, hide_index=True)



#  PAGE: ADD TRANSACTION


def page_add_transaction(df: pd.DataFrame, settings: dict):
    """Form to add a new income or expense entry."""
    st.markdown('<div class="page-title">Add Transaction</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Record a new income or expense entry</div>', unsafe_allow_html=True)

    # ── Type selector OUTSIDE the form so category list updates immediately ──
    if "txn_type_radio" not in st.session_state:
        st.session_state["txn_type_radio"] = "Expense"
    t_type = st.session_state["txn_type_radio"]

    # ── Style the Streamlit buttons themselves to look like beautiful cards ──
    st.markdown(f"""
    <style>
    [data-testid="stButton-_exp_btn"] > button,
    [data-testid="stButton-_inc_btn"] > button {{
        height: 82px !important;
        border-radius: 18px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.1px !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="stButton-_exp_btn"] > button {{
        background: {"linear-gradient(135deg, #2d0a0a 0%, #450f0f 100%)" if t_type == "Expense" else "rgba(239,68,68,0.04)"} !important;
        border: 2px solid {"#ef4444" if t_type == "Expense" else "rgba(239,68,68,0.15)"} !important;
        color: {"#fca5a5" if t_type == "Expense" else "#4a2525"} !important;
        box-shadow: {"0 0 0 4px rgba(239,68,68,0.1), 0 12px 35px rgba(239,68,68,0.25)" if t_type == "Expense" else "none"} !important;
    }}
    [data-testid="stButton-_exp_btn"] > button:hover {{
        background: linear-gradient(135deg, #3d0e0e 0%, #561313 100%) !important;
        border-color: #ef4444 !important;
        color: #fca5a5 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 0 0 4px rgba(239,68,68,0.15), 0 16px 40px rgba(239,68,68,0.3) !important;
    }}
    [data-testid="stButton-_inc_btn"] > button {{
        background: {"linear-gradient(135deg, #052010 0%, #083018 100%)" if t_type == "Income" else "rgba(52,211,153,0.04)"} !important;
        border: 2px solid {"#34d399" if t_type == "Income" else "rgba(52,211,153,0.15)"} !important;
        color: {"#6ee7b7" if t_type == "Income" else "#1a3d2a"} !important;
        box-shadow: {"0 0 0 4px rgba(52,211,153,0.1), 0 12px 35px rgba(52,211,153,0.25)" if t_type == "Income" else "none"} !important;
    }}
    [data-testid="stButton-_inc_btn"] > button:hover {{
        background: linear-gradient(135deg, #072a15 0%, #0a3c1e 100%) !important;
        border-color: #34d399 !important;
        color: #6ee7b7 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 0 0 4px rgba(52,211,153,0.15), 0 16px 40px rgba(52,211,153,0.3) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    _c1, _c2 = st.columns(2)
    with _c1:
        if st.button("💸   Expense\n Money going out", key="_exp_btn", use_container_width=True):
            st.session_state["txn_type_radio"] = "Expense"
            st.rerun()
    with _c2:
        if st.button("💰   Income\n Money coming in", key="_inc_btn", use_container_width=True):
            st.session_state["txn_type_radio"] = "Income"
            st.rerun()

    # Re-read after possible rerun
    t_type = st.session_state["txn_type_radio"]

    # Reset category key when type changes so the correct list is shown
    if "prev_type" not in st.session_state:
        st.session_state.prev_type = t_type
    if st.session_state.prev_type != t_type:
        st.session_state.pop("exp_cat", None)
        st.session_state.pop("inc_cat", None)
        st.session_state.prev_type = t_type

    with st.form("add_txn_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            # Category dropdown — shows only the relevant sub-options for the chosen type
            if t_type == "Expense":
                category = st.selectbox("Category", EXPENSE_CATEGORIES, key="exp_cat")
            else:
                category = st.selectbox("Category", INCOME_CATEGORIES, key="inc_cat")

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                step=10.0,
                format="%.2f",
            )

        with col2:
            date = st.date_input("Date", value=datetime.date.today())
            notes = st.text_area(
                "Notes (optional)",
                placeholder="e.g. Lunch at canteen...",
                height=120,
            )

        submitted = st.form_submit_button("💾 Save Transaction", use_container_width=True)

        if submitted:
            # Validate amount
            if amount <= 0:
                st.error("Please enter a valid amount greater than ₹0.")
            else:
                # Check daily limit
                daily_limit = settings.get("daily_limit", 0)
                if t_type == "Expense" and daily_limit > 0:
                    today_total = get_today_expense(df) + amount
                    if today_total > daily_limit:
                        st.warning(
                            f"⚠️ Adding this will exceed your daily limit! "
                            f"(Today total: {fmt(today_total)}, Limit: {fmt(daily_limit)})"
                        )

                # Add & save
                updated = add_transaction(df, t_type, amount, category, date, notes)

                # get logged-in user and save to user-specific file
                user = st.session_state["user"]
                save_user_data(user, updated)

                st.success(f"✅ {t_type} of {fmt(amount)} added successfully!")
                st.balloons()
                st.rerun()

    # ── Quick budget status reminder ──
    if settings["monthly_budget"] > 0:
        month_expense = get_this_month_expense(df)
        remaining     = settings["monthly_budget"] - month_expense
        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("💡 Budget Reminder")
        pct = (month_expense / settings["monthly_budget"]) * 100
        st.progress(min(pct / 100, 1.0))
        st.caption(
            f"Spent {fmt(month_expense)} of {fmt(settings['monthly_budget'])} "
            f"({pct:.1f}%) — {fmt(max(remaining, 0))} remaining this month"
        )



#  PAGE: TRANSACTION HISTORY


def page_history(df: pd.DataFrame):
    """Display filterable transaction history with delete & CSV export."""
    st.markdown('<div class="page-title">Transaction History</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Browse, filter, and export all your records</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("No transactions recorded yet. Start by adding one!")
        return

    # ── Filters ──
    render_section_header("🔍 Filters")
    f1, f2, f3 = st.columns(3)

    with f1:
        type_filter = st.selectbox("Type", ["All", "Income", "Expense"])
    with f2:
        all_cats = ["All"] + sorted(df["category"].unique().tolist())
        cat_filter = st.selectbox("Category", all_cats)
    with f3:
        months = ["All"] + sorted(
            df["date"].dt.strftime("%b %Y").unique().tolist(), reverse=True
        )
        month_filter = st.selectbox("Month", months)

    # Apply filters
    filtered = df.copy()
    if type_filter != "All":
        filtered = filtered[filtered["type"] == type_filter]
    if cat_filter != "All":
        filtered = filtered[filtered["category"] == cat_filter]
    if month_filter != "All":
        filtered = filtered[filtered["date"].dt.strftime("%b %Y") == month_filter]

    # ── Export ──
    col_exp, col_del = st.columns([3, 1])
    with col_exp:
        csv = filtered.copy()
        csv["date"] = csv["date"].dt.strftime("%Y-%m-%d")
        st.download_button(
            label="⬇️ Export CSV",
            data=csv.to_csv(index=False).encode("utf-8"),
            file_name="expense_export.csv",
            mime="text/csv",
        )
    with col_del:
        st.caption(f"{len(filtered)} record(s) found")

    # ── Display table ──
    display = filtered.sort_values("date", ascending=False).copy()
    display["date"]   = display["date"].dt.strftime("%d %b %Y")
    display["amount"] = display["amount"].apply(fmt)
    display = display[["id", "date", "type", "category", "amount", "notes"]].rename(
        columns={"id": "ID", "date": "Date", "type": "Type",
                 "category": "Category", "amount": "Amount", "notes": "Notes"}
    )
    st.dataframe(display, use_container_width=True, hide_index=True)

    # ── Delete transaction ──
    render_section_header("🗑️ Delete Transaction")
    del_id = st.number_input("Enter Transaction ID to delete", min_value=1, step=1)
    if st.button("Delete"):
        if del_id in df["id"].values:
            updated = delete_transaction(df, int(del_id))
            user = st.session_state["user"]
            save_user_data(user, updated)
            st.success(f"Transaction #{int(del_id)} deleted.")
            st.rerun()
        else:
            st.error(f"No transaction found with ID {int(del_id)}.")



#  PAGE: ANALYTICS


def page_analytics(df: pd.DataFrame):
    """Charts: pie by category + bar by month."""
    st.markdown('<div class="page-title">Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Visual breakdown of your spending patterns</div>', unsafe_allow_html=True)

    if df.empty or df[df["type"] == "Expense"].empty:
        st.info("Add some expense transactions to see analytics.")
        return

    expenses = df[df["type"] == "Expense"].copy()

    # ── Tabs ──
    tab1, tab2, tab3 = st.tabs(["🥧 Category Breakdown", "📊 Monthly Trend", "📋 Summary Table"])

    # ── Pie Chart ──────────────────────────────
    with tab1:
        cat_totals = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#0f1520")
        ax.set_facecolor("#0f1520")

        wedges, texts, autotexts = ax.pie(
            cat_totals,
            labels=None,
            autopct="%1.1f%%",
            colors=CHART_COLORS[:len(cat_totals)],
            startangle=140,
            pctdistance=0.75,
            wedgeprops=dict(width=0.45, edgecolor="#1C2128", linewidth=2),
        )

        for at in autotexts:
            at.set_color("white")
            at.set_fontsize(10)
            at.set_fontweight("bold")

        # Legend
        legend_patches = [
            mpatches.Patch(color=CHART_COLORS[i], label=f"{cat}  {fmt(val)}")
            for i, (cat, val) in enumerate(cat_totals.items())
        ]
        ax.legend(handles=legend_patches, loc="center left", bbox_to_anchor=(1, 0.5),
                  fontsize=9, frameon=False, labelcolor="white")

        ax.set_title("Expense by Category", color="#E6EDF3", fontsize=14,
                     fontweight="bold", pad=18)

        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Bar Chart ──────────────────────────────
    with tab2:
        expenses["month"] = expenses["date"].dt.to_period("M")
        monthly = expenses.groupby("month")["amount"].sum().reset_index()
        monthly["month_str"] = monthly["month"].astype(str)
        monthly = monthly.sort_values("month")

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#0f1520")
        ax.set_facecolor("#0f1520")

        bars = ax.bar(
            monthly["month_str"],
            monthly["amount"],
            color="#4f46e5",
            edgecolor="#0f1520",
            linewidth=0.5,
            width=0.5,
        )

        # Color highest bar differently
        if len(bars) > 0:
            max_idx = monthly["amount"].idxmax()
            bars[monthly.index.get_loc(max_idx)].set_color("#7c3aed")

        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + (monthly["amount"].max() * 0.01),
                    fmt(h), ha="center", va="bottom", color="#94a3b8", fontsize=8)

        ax.set_facecolor("#0f1520")
        ax.tick_params(colors="#475569", labelsize=9)
        ax.spines["bottom"].set_color("#1e293b")
        ax.spines["left"].set_color("#1e293b")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlabel("Month", color="#475569", fontsize=10)
        ax.set_ylabel("Total Expense (₹)", color="#475569", fontsize=10)
        ax.set_title("Monthly Spending Trend", color="#e2e8f0", fontsize=14,
                     fontweight="bold", pad=14)
        ax.yaxis.label.set_color("#475569")

        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Summary Table ──────────────────────────
    with tab3:
        render_section_header("💰 Category-wise Summary")
        summary = expenses.groupby("category")["amount"].agg(["sum", "count", "mean"])
        summary.columns = ["Total Spent", "Transactions", "Avg per Transaction"]
        summary["Total Spent"] = summary["Total Spent"].apply(fmt)
        summary["Avg per Transaction"] = summary["Avg per Transaction"].apply(fmt)
        summary = summary.sort_values("Transactions", ascending=False)
        st.dataframe(summary, use_container_width=True)

    # insights Bar#

    st.markdown("### 💡 Insights")
    st.write(df)
    raw_summary = df.groupby("category")["amount"].sum()

    if not raw_summary.empty:
        top_category = raw_summary.idxmax()
        max_amount = raw_summary.max()
        total_expense = raw_summary.sum()

        percentage = (max_amount / total_expense) * 100

        st.success(
            f"🧠 You spent most on **{top_category}** "
            f"(₹{max_amount:.2f}, {percentage:.1f}% of total expenses)"
        )

# ─────────────────────────────────────────────
#  PAGE: SETTINGS
# ─────────────────────────────────────────────

def page_settings(settings: dict) -> dict:
    """Budget & daily limit configuration page."""
    st.markdown('<div class="page-title">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Configure your budget and spending limits</div>', unsafe_allow_html=True)

    render_section_header("💼 Monthly Budget")
    budget = st.number_input(
        "Set your monthly budget (₹)",
        min_value=0.0,
        value=float(settings.get("monthly_budget", 0)),
        step=500.0,
        format="%.2f",
        help="Set ₹0 to disable budget tracking",
    )

    render_section_header("🔔 Daily Expense Limit")
    daily = st.number_input(
        "Set daily expense limit (₹)",
        min_value=0.0,
        value=float(settings.get("daily_limit", 0)),
        step=50.0,
        format="%.2f",
        help="You'll be warned when you exceed this each day. Set ₹0 to disable.",
    )

    if st.button("💾 Save Settings"):
        new_settings = {"monthly_budget": budget, "daily_limit": daily}
        save_settings(new_settings)
        st.success("✅ Settings saved!")
        return new_settings

    return settings


#  SIDEBAR

def render_sidebar() -> str:
    with st.sidebar:
        st.image("logo.png", width=200)
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        user = st.session_state.get("user", "")
        initial = user[0].upper() if user else "?"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;padding:10px 4px 16px;">
            <div style="width:38px;height:38px;border-radius:12px;
                        background:linear-gradient(135deg,#4f46e5,#7c3aed);
                        display:flex;align-items:center;justify-content:center;
                        font-size:0.95rem;font-weight:700;color:#fff;
                        box-shadow:0 4px 15px rgba(79,70,229,0.4);flex-shrink:0;">
                {initial}
            </div>
            <div>
                <div style="font-size:0.85rem;font-weight:600;color:#e2e8f0;letter-spacing:-0.2px;">{user}</div>
                <div style="font-size:0.68rem;color:#34d399;font-weight:500;margin-top:1px;">● Active session</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        page = st.radio(
            "Navigate",
            ["🏠  Dashboard", "➕  Add Transaction", "📋  History",
             "📈  Analytics", "⚙️  Settings"],
            label_visibility="collapsed",
        )

        st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        if st.button("🚪  Sign Out", use_container_width=True, key="logout_btn"):
            st.session_state["user"] = None
            st.rerun()

        st.markdown("""
        <div style="font-size:0.65rem;color:#334155;text-align:center;padding:14px 0 4px;letter-spacing:0.3px;">
            Developed by Sharvil Mithari<br>
            <span style="color:#4f46e5;font-weight:600;">SpendWise · India 2026</span>
        </div>
        """, unsafe_allow_html=True)

    # Map back to original page names used in main()
    page_map = {
        "🏠  Dashboard": "🏠 Dashboard",
        "➕  Add Transaction": "💲 Add Transaction",
        "📋  History": "📋 History",
        "📈  Analytics": "📈 Analytics",
        "⚙️  Settings": "⚙️ Settings",
    }
    return page_map.get(page, page)



#  MAIN ENTRY POINT

def signup(username, password):
    file_path = f"data/{username}.json"

    if os.path.exists(file_path):
        return False  # user exists

    with open(file_path, "w") as f:
        json.dump({
            "password": password,
            "data": []
        }, f)

    return True

def login(username, password):
    file_path = f"data/{username}.json"

    if not os.path.exists(file_path):
        return False

    with open(file_path, "r") as f:
        user_data = json.load(f)

    return user_data["password"] == password

def main():
    inject_css()

    # ✅ initialize
    if "user" not in st.session_state:
        st.session_state["user"] = None

    # ✅ ONLY show login
    if st.session_state["user"] is None:
        show_login()
        return   # 🚨 USE RETURN HERE (NOTHING BELOW RUNS)

    # ✅ AFTER LOGIN ONLY
    user = st.session_state["user"]
    df = load_user_data(user)

    page = render_sidebar()

    settings = load_settings()

    if page == "🏠 Dashboard":
        page_dashboard(df, settings)

    elif page == "💲 Add Transaction":
        updated = page_add_transaction(df, settings)
        if updated is not None:
            save_user_data(user, updated)

    elif page == "📋 History":
        page_history(df)

    elif page == "📈 Analytics":
        page_analytics(df)

    elif page == "⚙️ Settings":
        page_settings(settings)

def reset_password(username, new_password):
    """Reset password for an existing user. Returns True on success, False if user not found."""
    file_path = f"data/{username}.json"
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r") as f:
        user_data = json.load(f)
    if isinstance(user_data, dict):
        user_data["password"] = new_password
    else:
        user_data = {"password": new_password, "data": user_data}
    with open(file_path, "w") as f:
        json.dump(user_data, f)
    return True


def show_login():
    import base64, os

    if "login_tab" not in st.session_state:
        st.session_state["login_tab"] = "login"
    tab = st.session_state["login_tab"]

    # Encode logo as base64
    logo_b64 = ""
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()

    # ── All CSS up front, using reliable key-based selectors ──
    # Tab buttons are targeted by their data-testid key attribute which Streamlit
    # renders as:  button[kind="secondary"][data-testid="baseButton-secondary"]
    # We use the *parent* column position via :has() on the stButton key selector.
    # The safest cross-version approach: target by button text content won't work,
    # so we use nth-child on the columns inside the tab row container.

    login_active   = "background:linear-gradient(135deg,#4f46e5,#7c3aed)!important;color:#fff!important;border:none!important;box-shadow:0 6px 20px rgba(79,70,229,0.4)!important;"
    login_inactive = "background:rgba(255,255,255,0.04)!important;color:#475569!important;border:1px solid rgba(255,255,255,0.07)!important;box-shadow:none!important;"

    if tab == "login":
        col1_style, col2_style, col3_style = login_active, login_inactive, login_inactive
    elif tab == "signup":
        col1_style, col2_style, col3_style = login_inactive, login_active, login_inactive
    else:  # forgot
        col1_style, col2_style, col3_style = login_inactive, login_inactive, login_active

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    #MainMenu, footer, header {{ visibility: hidden; }}
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

    .stApp {{ background: #060810 !important; }}

    .block-container {{
        padding-top: 6vh !important;
        padding-bottom: 0 !important;
        max-width: 440px !important;
        margin: 0 auto !important;
    }}

    div[data-testid="stVerticalBlock"] > div:has(> div > .lcard) {{
        background: rgba(10, 14, 24, 0.98) !important;
        border: 1px solid rgba(99,102,241,0.15) !important;
        border-radius: 24px !important;
        padding: 40px 36px 32px !important;
        box-shadow: 0 40px 100px rgba(0,0,0,0.7), 0 0 0 1px rgba(99,102,241,0.05) !important;
        backdrop-filter: blur(20px) !important;
    }}

    .stTextInput label {{
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        color: #334155 !important;
    }}
    .stTextInput > div > div > input {{
        background: #080c17 !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
        height: 50px !important;
        padding: 0 16px !important;
        transition: border-color 0.18s, box-shadow 0.18s !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: rgba(99,102,241,0.5) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
    }}

    .stButton > button {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.18s !important;
        white-space: nowrap !important;
        line-height: 1 !important;
    }}

    div[data-testid="column"]:nth-of-type(1) .stButton > button {{
        {col1_style}
        height: 42px !important;
        font-size: 0.82rem !important;
    }}
    div[data-testid="column"]:nth-of-type(2) .stButton > button {{
        {col2_style}
        height: 42px !important;
        font-size: 0.82rem !important;
    }}
    div[data-testid="column"]:nth-of-type(3) .stButton > button {{
        {col3_style}
        height: 42px !important;
        font-size: 0.82rem !important;
    }}

    [data-testid="stButton-login_btn"] > button,
    [data-testid="stButton-signup_btn"] > button,
    [data-testid="stButton-forgot_btn"] > button {{
        background: linear-gradient(135deg,#4f46e5,#7c3aed) !important;
        color: #fff !important;
        border: none !important;
        height: 52px !important;
        border-radius: 14px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 8px 28px rgba(79,70,229,0.45) !important;
        margin-top: 8px !important;
    }}
    [data-testid="stButton-login_btn"] > button:hover,
    [data-testid="stButton-signup_btn"] > button:hover,
    [data-testid="stButton-forgot_btn"] > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 40px rgba(79,70,229,0.6) !important;
    }}
    div[data-baseweb="input"] {{ height: 50px !important; }}
    </style>
    """, unsafe_allow_html=True)

    # ── Card ──
    with st.container():
        # Marker div for :has() card selector
        st.markdown('<div class="lcard" style="display:none"></div>', unsafe_allow_html=True)

        # ── Logo: rendered fully in HTML so it sits inside the card ──
        if logo_b64:
            logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="max-width:180px;max-height:64px;object-fit:contain;display:block;margin:0 auto 6px;">'
        else:
            logo_html = '<div style="font-size:2.4rem;text-align:center;margin-bottom:6px;">💰</div>'

        st.markdown(
            logo_html +
            '<p style="font-size:0.72rem;color:#334155;text-align:center;'
            'margin:4px 0 28px;letter-spacing:1px;text-transform:uppercase;font-weight:600;">Track smarter · Save better</p>',
            unsafe_allow_html=True,
        )

        # ── Tab toggle row ──
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔐  Login", key="tab_login", use_container_width=True):
                st.session_state["login_tab"] = "login"
                st.rerun()
        with c2:
            if st.button("✨  Sign Up", key="tab_signup", use_container_width=True):
                st.session_state["login_tab"] = "signup"
                st.rerun()
        with c3:
            if st.button("🔑  Forgot", key="tab_forgot", use_container_width=True):
                st.session_state["login_tab"] = "forgot"
                st.rerun()

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # ── Fields ──
        if tab in ("login", "signup"):
            username = st.text_input("Username", placeholder="Enter your username", key="auth_username")
            password = st.text_input("Password", placeholder="Enter your password", type="password", key="auth_password")
        elif tab == "forgot":
            st.markdown(
                '<p style="font-size:0.82rem;color:#8B949E;text-align:center;margin-bottom:16px;">'
                'Enter your username and a new password to reset your account.</p>',
                unsafe_allow_html=True,
            )
            username = st.text_input("Username", placeholder="Enter your username", key="fp_username")
            new_pass = st.text_input("New Password", placeholder="Enter new password", type="password", key="fp_newpass")
            confirm_pass = st.text_input("Confirm Password", placeholder="Confirm new password", type="password", key="fp_confirm")

        # ── Submit ──
        if tab == "login":
            if st.button("Login →", key="login_btn", use_container_width=True):
                if not username or not password:
                    st.error("Please enter both fields.")
                elif login(username, password):
                    st.session_state["user"] = username
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")
        elif tab == "signup":
            if st.button("Create Account →", key="signup_btn", use_container_width=True):
                if not username or not password:
                    st.error("Please fill in all fields.")
                elif len(password) < 4:
                    st.warning("Password must be at least 4 characters.")
                elif signup(username, password):
                    st.success("✅ Account created! Please log in.")
                    st.session_state["login_tab"] = "login"
                    st.rerun()
                else:
                    st.error("⚠️ Username already exists.")
        elif tab == "forgot":
            if st.button("Reset Password →", key="forgot_btn", use_container_width=True):
                if not username or not new_pass or not confirm_pass:
                    st.error("Please fill in all fields.")
                elif len(new_pass) < 4:
                    st.warning("New password must be at least 4 characters.")
                elif new_pass != confirm_pass:
                    st.error("❌ Passwords do not match.")
                elif reset_password(username, new_pass):
                    st.success("✅ Password reset successfully! You can now log in.")
                    st.session_state["login_tab"] = "login"
                    st.rerun()
                else:
                    st.error("⚠️ Username not found.")

        # ── Footer ──
        st.markdown(
            '<p style="font-size:0.65rem;color:#1e293b;text-align:center;margin-top:24px;margin-bottom:0;letter-spacing:0.5px;">'
            'Developed by Sharvil Mithari · <span style="color:#4f46e5;">SpendWise India 2026</span>'
            '</p>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
