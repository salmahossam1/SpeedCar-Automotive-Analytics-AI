import base64
from pathlib import Path
import streamlit as st
from utils import setup_page, sidebar

# ============================================================
# PAGE SETUP
# ============================================================

setup_page("Speed Car", "🏎️")
sidebar()

BASE = Path(__file__).resolve().parent

# ============================================================
# LOAD CAR IMAGE
# ============================================================

img = next(
    (
        p
        for p in [BASE / "car.avif", BASE / "car.jpg", BASE / "car.png"]
        if p.exists()
    ),
    None,
)

if img:
    b64 = base64.b64encode(img.read_bytes()).decode()
    mime = {
        "avif": "image/avif",
        "jpg": "image/jpeg",
        "png": "image/png",
    }[img.suffix.lower().lstrip(".")]
    bg = f"data:{mime};base64,{b64}"
else:
    bg = "linear-gradient(135deg,#020817,#06345a,#020817)"


# ============================================================
# CSS STYLING & HERO FIXES
# ============================================================

st.markdown(
    f"""<style>
.hero {{
    position: relative !important;
    width: 100vw !important;
    height: 75vh !important;
    margin-left: calc(50% - 50vw) !important;
    margin-right: calc(50% - 50vw) !important;
    margin-top: -3.5rem !important;
    background-image: url('{bg}') !important;
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    overflow: hidden !important;
}}

.hero::after {{
    content: "" !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(1,9,18,0.85) 100%) !important;
    z-index: 1 !important;
}}

.hero-content {{
    position: relative !important;
    z-index: 3 !important;
    text-align: center !important;
}}

.hero-title {{
    font-size: clamp(4rem, 10vw, 9rem) !important;
    font-weight: 1000 !important;
    letter-spacing: 8px !important;
    line-height: 0.85 !important;
    margin: 0 !important;
    text-transform: uppercase !important;
    color: rgba(255, 255, 255, 0.05) !important;
    -webkit-text-stroke: 3px rgba(125, 211, 252, 0.95) !important;
    text-shadow: 0 0 15px rgba(56, 189, 248, 0.9), 0 0 50px rgba(0, 140, 255, 0.6) !important;
    mix-blend-mode: screen !important;
}}

.hero-sub {{
    font-size: 1.15rem !important;
    color: #e8f7ff !important;
    margin-top: 25px !important;
    letter-spacing: 5px !important;
    font-weight: 800 !important;
    text-shadow: 0 4px 20px #000 !important;
}}

.home-navigation {{
    margin-top: -90px !important;
    position: relative !important;
    z-index: 10 !important;
    padding: 0 2% !important;
}}

div[data-testid="stPageLink"] a {{
    background: rgba(0, 8, 16, 0.38) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 16px !important;
    min-height: 80px !important;
    box-shadow: 0 10px 35px rgba(0,0,0,0.5) !important;
    transition: all .25s ease-in-out !important;
}}

div[data-testid="stPageLink"] a:hover {{
    background: rgba(0, 20, 40, 0.65) !important;
    border-color: rgba(125, 211, 252, 0.8) !important;
    transform: translateY(-5px) !important;
    box-shadow: 0 15px 40px rgba(56, 189, 248, 0.3) !important;
}}

div[data-testid="stPageLink"] a span {{
    color: #eaf6ff !important;
    font-weight: 800 !important;
}}
</style>""",
    unsafe_allow_html=True,
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """<div class="hero"><div class="hero-content"><div class="hero-title">SPEED CAR</div><div class="hero-sub">AUTOMOTIVE PERFORMANCE • DATA • AI</div></div></div>""",
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION CARDS
# ============================================================

st.markdown('<div class="home-navigation">', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="small")

with c1:
    st.page_link(
        "pages/1_Dashboard.py",
        label="Dashboard",
        icon="📊",
        use_container_width=True,
    )

with c2:
    st.page_link(
        "pages/2_Data_Description.py",
        label="Data Description",
        icon="🧹",
        use_container_width=True,
    )

with c3:
    st.page_link(
        "pages/3_Best_Model_Prediction.py",
        label="Prediction",
        icon="🤖",
        use_container_width=True,
    )

st.markdown("</div>", unsafe_allow_html=True)