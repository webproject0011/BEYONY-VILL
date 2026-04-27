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

# 2. Exact UI Styling (Matching your Screenshot)
st.markdown("""
    <style>
    /* Full Page Background with Exact Dark Overlay */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2044&auto=format&fit=crop");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* Main Header Section */
    .header-box {
        text-align: center;
        padding: 100px 0 20px 0;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 6.5rem; /* Massive Font */
        font-weight: 900;
        letter-spacing: -2px;
        color: #ffffff;
        margin: 0;
        text-transform: uppercase;
        line-height: 1;
    }
    .tagline {
        color: #4fc3f7; /* Matching the blue in your pic */
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-top: 20px;
    }

    /* Search Bar - Exactly like the Screenshot */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.12) !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 10px !important;
        color: #ffffff !important;
    }
    input {
        color: #ffffff !important;
        font-size: 1.1rem !important;
    }
    ::placeholder { color: rgba(255, 255, 255, 0.5) !important; }

    /* Result Card View */
    .result-card {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px;
        border-radius: 12px;
        margin-top: 40px;
    }
    .v-header {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 30px;
        border-left: 8px solid #4fc3f7;
        padding-left: 20px;
    }
    .data-tile {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .tile-label { color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
    .tile-value { color: #ffffff; font-size: 1.4rem; font-weight: 600; }

    /* Professional Fixed Footer */
    .footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: rgba(0, 0, 0, 0.9);
        padding: 15px;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    .footer-text {
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .author { color: #ffffff; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Construction
st.markdown("""
    <div class="header-box">
        <h1 class="main-title">BEYOND CITIES</h1>
        <div class="tagline">RURAL DATA INTELLIGENCE ENGINE</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Engine Logic
l, m, r = st.columns([1, 2, 1])
with m:
    st.markdown("<br>", unsafe_allow_html=True)
    q = st.text_input("SEARCH_FIELD", placeholder="Search 600,000+ villages instantly...", label_visibility="collapsed")

    if q:
        res = supabase.table("villages").select("*").ilike("Village Name", f"%{q}%").limit(20).execute()
        
        if res.data:
            options = {f"{r['Village Name']} | {r['Subdistrict Name']} | {r['District Name']}": r for r in res.data}
            sel = st.selectbox("CHOOSE_VILLAGE", options=list(options.keys()), index=None, label_visibility="collapsed")

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

# 5. Exact Footer
st.markdown(f"""
    <div class="footer">
        <div class="footer-text">© 2026 BEYOND CITIES INTELLIGENCE | DEVELOPED BY <span class="author">ASHISH BAJPAI</span></div>
    </div>
    """, unsafe_allow_html=True)
