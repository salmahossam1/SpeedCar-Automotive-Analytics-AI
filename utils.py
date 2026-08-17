import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import re, joblib

BASE=Path(__file__).resolve().parent
CSV_PATH=BASE/"DriveArabia_All_uae_updated.csv"
MODELS=BASE/"models"

def midpoint_num(x):
    if pd.isna(x): return np.nan
    nums=re.findall(r'-?\d+(?:\.\d+)?',str(x).replace(',',''))
    if not nums: return np.nan
    return float(np.mean([float(v) for v in nums]))

@st.cache_data
def load_data():
    df=pd.read_csv(CSV_PATH)
    for c in ["Approx Cost","Weight","Torque (Nm)","Fuel Econ (L/100km)","Fuel Econ (km/L)","Performance 0-100 kph (sec)","Top speed (kph)","Power (hp)"]:
        df[c]=df[c].apply(midpoint_num)
    df["gear_count"]=df["Gear box"].astype(str).str.extract(r"(\d+)")[0].astype(float)
    df["gear_type"]=df["Gear box"].astype(str).str.extract(r"(\d+)(.*)")[1].str.replace("/","_",regex=False).str.strip().replace("",np.nan)
    df["Brand_Manufacturer"]=df["Manufacturer"].astype(str)+" | "+df["Brand"].astype(str)
    return df

def load_joblib(name):
    p=MODELS/name
    return joblib.load(p) if p.exists() else None

CHART_COLORS=["#38BDF8","#22D3EE","#818CF8","#A78BFA","#F472B6","#FB7185","#FBBF24","#34D399"]

def setup_page(title,icon):
    st.set_page_config(page_title=title,page_icon=icon,layout="wide")
    st.markdown("""
    <style>
    .stApp{background:radial-gradient(circle at 12% 5%,rgba(0,80,150,.10),transparent 27%),linear-gradient(135deg,#01040a 0%,#03101d 52%,#00070d 100%);color:#dcecff}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,#03101f,#051d35)}
    .block-container{padding-top:1.2rem;padding-bottom:2rem}
    h1,h2,h3,h4,p,label,span{color:#eaf6ff}
    .hero {
        position:relative; width:calc(100% + 2.4rem); height:calc(100vh - 0.5rem);
        min-height:700px; margin:-1.2rem -1.2rem 0 -1.2rem;
        border-radius:0; overflow:hidden; background-size:cover;
        background-position:center center; box-shadow:none;
        display:flex; align-items:center; justify-content:center;
    }
    .hero:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.70),rgba(0,5,12,.10),rgba(0,0,0,.72))}
    .hero-content{position:relative;z-index:2;text-align:center}
    .hero-title {
        font-size:clamp(5rem,12vw,12rem); font-weight:1000;
        letter-spacing:12px; line-height:.78; margin:0;
        text-transform:uppercase;
        color:rgba(255,255,255,.06)!important;
        -webkit-text-stroke:3px rgba(120,220,255,.9);
        text-shadow:0 0 12px rgba(56,189,248,.95),0 0 55px rgba(0,140,255,.65),0 15px 55px rgba(0,0,0,1);
        mix-blend-mode:screen; transform:translateY(15px) scale(1.03);
    }
    .hero-sub {
        font-size:1.15rem; color:#e8f7ff!important; margin:35px 0 25px;
        letter-spacing:5px; font-weight:800; text-shadow:0 4px 20px #000;
    }
    .card,.page-card{background:linear-gradient(145deg,rgba(4,35,64,.92),rgba(2,16,32,.96));border:1px solid rgba(56,189,248,.14);border-radius:18px;padding:22px;box-shadow:0 8px 28px rgba(0,0,0,.25)}
    .page-card{min-height:145px}.page-icon{font-size:2.2rem}.page-name{font-size:1.3rem;font-weight:800;margin-top:8px}.small-muted{color:#9cc0dd!important}
    .kpi{background:linear-gradient(145deg,rgba(2,19,35,.97),rgba(1,9,18,.97));border:1px solid rgba(56,189,248,.25);border-radius:16px;padding:18px 12px;text-align:center}
    .kpi-value{font-size:2rem;font-weight:900;color:#7dd3fc!important}.kpi-label{color:#a9c8e3!important;font-size:.9rem}
    .best-model{background:linear-gradient(135deg,rgba(8,64,103,.8),rgba(2,25,46,.9));border:1px solid #38bdf8;border-radius:20px;padding:28px;text-align:center}
    .best-model-name{font-size:2.7rem;font-weight:900;color:#67e8f9!important}.info-box{background:rgba(2,15,28,.88);border-left:4px solid #38bdf8;padding:14px 18px;border-radius:10px;margin:8px 0}
    
    .hero-nav{position:absolute;z-index:4;bottom:42px;left:50%;transform:translateX(-50%);display:flex;gap:14px;justify-content:center;width:min(850px,90%);}
    .hero-link{display:block;text-decoration:none!important;color:#eefaff!important;background:rgba(1,10,18,.28);backdrop-filter:blur(8px);border:1px solid rgba(150,220,255,.28);border-radius:16px;padding:12px 22px;min-width:175px;text-align:center;box-shadow:0 8px 28px rgba(0,0,0,.35);transition:.2s;}
    .hero-link:hover{background:rgba(8,35,55,.48);border-color:rgba(125,211,252,.75);transform:translateY(-4px);}
    .hero-link-icon{font-size:1.65rem;display:block}.hero-link-name{font-weight:800;font-size:.92rem;letter-spacing:.4px}.hero-link-sub{font-size:.68rem;color:#9fc0d8!important;margin-top:2px;}
    .prediction-icon-card {background:linear-gradient(145deg,rgba(4,35,64,.92),rgba(2,16,32,.96));border:1px solid rgba(56,189,248,.14);border-radius:16px;padding:14px 8px;text-align:center;box-shadow:0 6px 20px rgba(0,0,0,.22);transition:.2s;}
    .prediction-icon {font-size:1.8rem;line-height:1.1;}
    .prediction-icon-title {font-size:.82rem;font-weight:800;color:#dff6ff!important;margin-top:6px;}
    .prediction-icon-card:hover {transform:translateY(-2px);border-color:#38bdf8;box-shadow:0 8px 24px rgba(56,189,248,.18);}
    </style>
    """,unsafe_allow_html=True)

def sidebar():

    st.sidebar.title("🏎️ SPEED CAR")
    st.sidebar.caption("Automotive Performance Analytics")

    st.sidebar.divider()

    st.sidebar.page_link(
        "app.py",
        label="🏠 Home"
    )

    st.sidebar.page_link(
        "pages/1_Dashboard.py",
        label="📊 Dashboard"
    )

    st.sidebar.page_link(
        "pages/2_Data_Description.py",
        label="🧹 Data Description"
    )

    st.sidebar.page_link(
        "pages/3_Best_Model_Prediction.py",
        label="🤖 Best Model Prediction"
    )

    st.sidebar.divider()

    st.sidebar.caption(
        "Python • Pandas • Plotly • Scikit-learn • Streamlit"
    )

def chart_layout(fig,height=420,legend=True):
    fig.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(2,12,25,.35)",font=dict(color="#EAF6FF"),height=height,margin=dict(l=20,r=20,t=60,b=20),showlegend=legend)
    return fig



st.markdown(r'''<style>
/* FINAL HOME HERO OVERRIDES */
.hero {
    position:relative !important;
    width:100vw !important;
    min-height:100vh !important;
    height:100vh !important;
    margin-left:calc(50% - 50vw) !important;
    margin-right:calc(50% - 50vw) !important;
    border-radius:0 !important;
    overflow:hidden !important;
    background-size:cover !important;
    background-position:center center !important;
    box-shadow:none !important;
}
.hero::after {
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(90deg,rgba(0,0,0,.78),rgba(0,8,18,.18),rgba(0,0,0,.72));
    z-index:1;
    pointer-events:none;
}
.hero-content {
    position:relative !important;
    z-index:3 !important;
}
.hero-title {
    font-size:clamp(5rem,13vw,12rem) !important;
    font-weight:1000 !important;
    letter-spacing:8px !important;
    line-height:.78 !important;
    color:rgba(255,255,255,.08) !important;
    -webkit-text-stroke:3px rgba(125,211,252,.9) !important;
    text-shadow:0 0 12px rgba(56,189,248,.95),0 0 55px rgba(0,140,255,.55),0 15px 55px #000 !important;
    mix-blend-mode:screen !important;
}
.home-icons {
    position:absolute !important;
    z-index:8 !important;
    left:50% !important;
    bottom:55px !important;
    transform:translateX(-50%) !important;
    display:flex !important;
    gap:12px !important;
    justify-content:center !important;
    width:min(720px,92vw) !important;
}
.home-icon-card {
    flex:1;
    min-width:145px;
    padding:14px 10px !important;
    border:1px solid rgba(255,255,255,.20) !important;
    border-radius:16px !important;
    background:rgba(0,8,16,.24) !important;
    backdrop-filter:blur(9px) !important;
    -webkit-backdrop-filter:blur(9px) !important;
    box-shadow:0 10px 35px rgba(0,0,0,.45) !important;
    transition:.2s ease !important;
}
.home-icon-card:hover {
    background:rgba(0,8,16,.42) !important;
    border-color:rgba(125,211,252,.65) !important;
    transform:translateY(-5px) !important;
}
</style>''', unsafe_allow_html=True)