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

# 2. UI Styling (Wide Spacing + Thin Large Font + Clean Footer)
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), 
                    url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2044&auto=format&fit=crop");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* THE MEGA HEADER - THIN & SPACED */
    .header-box { text-align: center; padding: 50px 0 10px 0; }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 13.5rem; /* Pehle se bada size */
        font-weight: 300;   /* Patla font rkha h (Lightweight) */
        color: #FFFFFF;
        margin: 0;
        text-transform: uppercase;
        line-height: 0.9;
        letter-spacing: 15px; /* Letter door-door rkhne ke liye */
        text-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    
    @media (max-width: 768px) {
        .main-title { 
            font-size: 4.5rem; 
            letter-spacing: 5px; 
            font-weight: 400;
        }
    }

    .tagline {
        color: #4fc3f7;
        font-size: 1.5rem;
        font-weight: 600;
        letter-spacing: 10px;
        text-transform: uppercase;
        margin-top: 25px;
    }

    /* Search & Suggestions */
    div[data-baseweb="popover"] { top: 65px !important; bottom: auto !important; }
    
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }

    /* Result Cards */
    .result-card {
        background: rgba(15, 23, 42, 0.96);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px;
        border-radius: 20px;
        margin-top: 40px;
        animation: slideIn 0.8s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(50px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .v-header {
        font-size: 3.5rem;
        font-weight: 700;
        color: #FFFFFF;
        border-left: 10px solid #4fc3f7;
        padding-left: 25px;
        margin-bottom: 35px;
    }

    .data-tile {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    .tile-label { color: #94a3b8; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; }
    .tile-value { color: #FFFFFF; font-size: 1.6rem; font-weight: 500; }

    /* CLEAN DARK FOOTER */
    .footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #000000;
        padding: 20px;
        text-align: center;
        z-index: 1000;
        border-top: 2px solid #4fc3f7;
    }
    .footer-text { 
        color: #FFFFFF; 
        font-size: 1rem; 
        font-weight: 400;
        letter-spacing: 1px;
    }
    .author-name { 
        color: #4fc3f7; 
        font-weight: 700; 
        text-transform: uppercase;
        margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("""
    <div class="header-box">
        <h1 class="main-title">BEYOND<br>CITIES</h1>
    </div>
    <div style="text-align:center;">
        <div class="tagline">RURAL INTELLIGENCE ENGINE</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Engine Logic
l, m, r = st.columns([1, 2, 1])

with m:
    st.markdown("<br>", unsafe_allow_html=True)
    sc1, sc2 = st.columns([0.88, 0.12])
    with sc1:
        q = st.text_input("SEARCH", placeholder="🔍 Search villages...", label_visibility="collapsed")
    with sc2:
        st.button("GO")

    if q:
        res = supabase.table("villages").select("*").ilike("Village Name", f"%{q}%").limit(20).execute()
        
        if res.data:
            options = {f"{r['Village Name']} | {r['Subdistrict Name']} | {r['District Name']}": r for r in res.data}
            sel = st.selectbox("LIST", options=list(options.keys()), index=None, label_visibility="collapsed", placeholder="Select village ↓")

            if sel:
                v = options[sel]
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="v-header">{v["Village Name"]}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                d_map = [
                    ("District", "District Name"), ("District Code", "District Code"),
                    ("Subdistrict", "Subdistrict Name"), ("Village Code", "Village Code"),
                    ("Local Body", "Local Body Name"), ("LGD Code", "Local Body Code")
                ]
                
                for i, (label, key) in enumerate(d_map):
                    target = c1 if i % 2 == 0 else c2
                    target.markdown(f"""
                        <div class="data-tile">
                            <div class="tile-label">{label}</div>
                            <div class="tile-value">{v.get(key, 'N/A')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# 5. Clean Footer
st.markdown(f"""
    <div class="footer">
        <span class="footer-text">© 2026 BEYOND CITIES | DEVELOPED BY <span class="author-name">ASHISH BAJPAI</span></span>
    </div>
    """, unsafe_allow_html=True)
