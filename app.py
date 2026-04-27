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

# 2. UI Styling (Brightness + Dropdown Downwards + Button Fix)
st.markdown("""
    <style>
    /* Background with 40% Brightness Overlay */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                    url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2044&auto=format&fit=crop");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* Header Styling */
    .header-box { text-align: center; padding: 60px 0 20px 0; }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 7rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
        text-transform: uppercase;
        line-height: 1;
        text-shadow: 0px 8px 30px rgba(0,0,0,0.4);
    }
    .tagline {
        color: #4fc3f7;
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-top: 15px;
    }

    /* FORCE SUGGESTIONS DOWNWARDS (PORTAL FIX) */
    div[data-baseweb="popover"] {
        top: 65px !important;
        bottom: auto !important;
    }

    /* Professional Search Bar Styling */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
    }

    /* Animation for results */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .result-card {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px;
        border-radius: 15px;
        margin-top: 40px;
        animation: slideUp 0.6s ease-out;
    }

    .v-header {
        font-size: 3.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 30px;
        border-left: 8px solid #4fc3f7;
        padding-left: 20px;
    }

    .data-tile {
        background: rgba(255, 255, 255, 0.04);
        padding: 22px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .tile-label { color: #94a3b8; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; }
    .tile-value { color: #ffffff; font-size: 1.5rem; font-weight: 600; }

    /* Footer */
    .footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: rgba(0, 0, 0, 0.9);
        padding: 15px;
        text-align: center;
        z-index: 1000;
    }
    .footer-text { color: rgba(255, 255, 255, 0.5); font-size: 0.8rem; letter-spacing: 2px; }
    .author { color: #ffffff; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown("""
    <div class="header-box">
        <h1 class="main-title">BEYOND CITIES</h1>
        <div class="tagline">RURAL DATA INTELLIGENCE ENGINE</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Search & Suggestion Engine
l, m, r = st.columns([1, 2, 1])

with m:
    # Adding a columns layout for Search Bar + Button
    sc1, sc2 = st.columns([0.85, 0.15])
    
    with sc1:
        q = st.text_input("SEARCH", placeholder="Search 100,000+ villages...", label_visibility="collapsed")
    
    with sc2:
        search_clicked = st.button("🔍") # This acts as the magnifier search trigger

    # Logical Trigger: Show results if typed OR button clicked
    if q:
        res = supabase.table("villages").select("*").ilike("Village Name", f"%{q}%").limit(15).execute()
        
        if res.data:
            options = {f"{r['Village Name']} | {r['Subdistrict Name']} | {r['District Name']}": r for r in res.data}
            
            # This dropdown now opens BELOW the search bar
            sel = st.selectbox("CHOOSE", options=list(options.keys()), index=None, label_visibility="collapsed", placeholder="Suggestions list ↓")

            if sel:
                v = options[sel]
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="v-header">{v["Village Name"]}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                fields = [
                    ("District Name", "District Name"), ("District Code", "District Code"),
                    ("Subdistrict", "Subdistrict Name"), ("Village Code", "Village Code"),
                    ("Local Body", "Local Body Name"), ("LGD Code", "Local Body Code")
                ]
                
                for i, (lab, key) in enumerate(fields):
                    target = c1 if i % 2 == 0 else c2
                    target.markdown(f"""
                        <div class="data-tile">
                            <div class="tile-label">{lab}</div>
                            <div class="tile-value">{v.get(key, 'N/A')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# 5. Fixed Footer
st.markdown(f"""
    <div class="footer">
        <div class="footer-text">© 2026 BEYOND CITIES INTELLIGENCE | DEVELOPED BY <span class="author">ASHISH BAJPAI</span></div>
    </div>
    """, unsafe_allow_html=True)
