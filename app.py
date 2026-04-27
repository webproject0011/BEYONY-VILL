import streamlit as st
from supabase import create_client, Client

# 1. Page Configuration
st.set_page_config(page_title="Beyond Cities", layout="wide")

# Database Connection
SUPABASE_URL = "https://fqmwbqtpuokntbjkcikp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZxbXdicXRwdW9rbnRiamtjaWtwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMwNzA1MSwiZXhwIjoyMDkyODgzMDUxfQ.yzmHMSoMF9vqY-ruCprNE4Gu2yXEeQV_q_tG5CqNu-4"

@st.cache_resource
def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_client()

# 2. UI Styling (Massive & Bright Title + Fixed Suggestions)
st.markdown("""
    <style>
    /* Full Page Background with Day-Time Clarity */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.35)), 
                    url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2044&auto=format&fit=crop");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* MASSIVE & BRIGHT HEADER SECTION */
    .header-box { text-align: center; padding: 80px 0 20px 0; }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 8.5rem; /* Mega Size */
        font-weight: 900;
        color: #ffffff;
        margin: 0;
        text-transform: uppercase;
        line-height: 0.85;
        letter-spacing: -6px;
        /* Bright Glowing Effect */
        text-shadow: 0px 0px 30px rgba(255, 255, 255, 0.8), 0px 10px 40px rgba(0,0,0,0.5);
    }
    .tagline {
        color: #4fc3f7;
        font-size: 1.4rem; /* Increased size */
        font-weight: 700;
        letter-spacing: 7px;
        text-transform: uppercase;
        margin-top: 25px;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }

    /* DROPDOWN PORTAL FIX (Downwards) */
    div[data-baseweb="popover"] {
        top: 65px !important;
        bottom: auto !important;
    }

    /* Search Input & Button Styling */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.25) !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 10px !important;
    }
    
    .stButton > button {
        background-color: #4fc3f7 !important;
        color: white !important;
        border-radius: 10px !important;
        height: 45px !important;
        width: 100% !important;
    }

    /* Slide-Up Animation for Cards */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(60px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .result-card {
        background: rgba(15, 23, 42, 0.96);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 55px;
        border-radius: 20px;
        margin-top: 50px;
        animation: slideUp 0.7s ease-out;
        box-shadow: 0 40px 100px rgba(0,0,0,0.5);
    }

    .v-header {
        font-size: 3.8rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 35px;
        border-left: 12px solid #4fc3f7;
        padding-left: 30px;
    }

    .data-tile {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .tile-label { color: #94a3b8; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }
    .tile-value { color: #ffffff; font-size: 1.7rem; font-weight: 600; }

    /* Professional Footer Branding */
    .footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: rgba(0, 0, 0, 0.95);
        padding: 20px;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        z-index: 1000;
    }
    .footer-text { color: rgba(255, 255, 255, 0.4); font-size: 0.85rem; letter-spacing: 3px; }
    .author { color: #ffffff; font-weight: 800; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown("""
    <div class="header-box">
        <h1 class="main-title">BEYOND CITIES</h1>
        <div class="tagline">RURAL DATA INTELLIGENCE ENGINE</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Functional Engine
l, m, r = st.columns([1, 2, 1])

with m:
    st.markdown("<br>", unsafe_allow_html=True)
    # Modern Input Row
    sc1, sc2 = st.columns([0.88, 0.12])
    with sc1:
        q = st.text_input("SEARCH", placeholder="🔍 Search 100,000+ villages instantly...", label_visibility="collapsed")
    with sc2:
        search_btn = st.button("GO")

    if q:
        res = supabase.table("villages").select("*").ilike("Village Name", f"%{q}%").limit(20).execute()
        
        if res.data:
            options = {f"{r['Village Name']} | {r['Subdistrict Name']} | {r['District Name']}": r for r in res.data}
            
            # This dropdown always opens BELOW by CSS
            sel = st.selectbox("SUGGESTIONS", options=list(options.keys()), index=None, label_visibility="collapsed", placeholder="Select from suggestions below ↓")

            if sel:
                v = options[sel]
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="v-header">{v["Village Name"]}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                display_map = [
                    ("District Name", "District Name"), ("District Code", "District Code"),
                    ("Subdistrict", "Subdistrict Name"), ("Village Code", "Village Code"),
                    ("Local Body", "Local Body Name"), ("LGD Code", "Local Body Code")
                ]
                
                for i, (label, key) in enumerate(display_map):
                    target = c1 if i % 2 == 0 else c2
                    target.markdown(f"""
                        <div class="data-tile">
                            <div class="tile-label">{label}</div>
                            <div class="tile-value">{v.get(key, 'N/A')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# 5. Fixed Branding Footer
st.markdown(f"""
    <div class="footer">
        <div class="footer-text">© 2026 BEYOND CITIES INTELLIGENCE | DEVELOPED BY <span class="author">ASHISH BAJPAI</span></div>
    </div>
    """, unsafe_allow_html=True)
