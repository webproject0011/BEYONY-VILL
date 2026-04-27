import streamlit as st
from supabase import create_client, Client

# 1. Page Config
st.set_page_config(page_title="Beyond Cities", layout="wide")

# Direct Connection credentials
SUPABASE_URL = "https://fqmwbqtpuokntbjkcikp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZxbXdicXRwdW9rbnRiamtjaWtwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMwNzA1MSwiZXhwIjoyMDkyODgzMDUxfQ.yzmHMSoMF9vqY-ruCprNE4Gu2yXEeQV_q_tG5CqNu-4"

@st.cache_resource
def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_client()

# 2. Premium UI Styling
st.markdown("""
    <style>
    /* Dark City Backdrop */
    .stApp {
        background: linear-gradient(rgba(10, 15, 30, 0.85), rgba(10, 15, 30, 0.85)), 
                    url("https://images.unsplash.com/photo-1449824913935-59a10b8d2000?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Professional Header Section */
    .header-container {
        text-align: center;
        padding: 60px 0 30px 0;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 5.5rem;
        font-weight: 900;
        letter-spacing: -5px;
        color: #ffffff;
        margin: 0;
        text-transform: uppercase;
        line-height: 0.9;
    }
    .tagline {
        color: #10b981;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 15px;
    }
    .sub-tagline {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 8px;
        letter-spacing: 1px;
    }

    /* Search Input Styling */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
    }

    /* Result Card Styling */
    .result-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        border-radius: 24px;
        margin-top: 30px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
    }
    .village-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 25px;
        border-bottom: 4px solid #10b981;
        display: inline-block;
    }

    /* Data Grid Tiles */
    .data-tile {
        background: rgba(255, 255, 255, 0.02);
        padding: 18px;
        border-radius: 14px;
        border-left: 5px solid #10b981;
        margin-bottom: 12px;
    }
    .tile-label { color: #64748b; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
    .tile-value { color: #f1f5f9; font-size: 1.2rem; font-weight: 600; }

    /* Fixed Footer with Brand Font */
    .footer-bar {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: rgba(2, 6, 23, 0.98);
        padding: 20px;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        z-index: 100;
    }
    .footer-content { color: #94a3b8; font-size: 0.9rem; font-weight: 500; letter-spacing: 1.5px; }
    .author-name { color: #10b981; font-weight: 800; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 3. Dynamic Header
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">BEYOND <span style="color: #10b981;">CITIES</span></h1>
        <div class="tagline">Rural Data Intelligence Engine</div>
        <div class="sub-tagline">Search any village name of Uttar Pradesh</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Functional Engine
l, m, r = st.columns([1, 2, 1])
with m:
    q = st.text_input("SEARCH_FIELD", placeholder="Enter Village Name...", label_visibility="collapsed")

    if q:
        res = supabase.table("villages").select("*").ilike("Village Name", f"%{q}%").limit(30).execute()
        
        if res.data:
            options = {f"{r['Village Name']} | {r['Subdistrict Name']} | {r['District Name']}": r for r in res.data}
            sel = st.selectbox("SELECT LOCATION", options=list(options.keys()), index=None)

            if sel:
                v = options[sel]
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="village-header">{v["Village Name"]}</div>', unsafe_allow_html=True)
                
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
        else:
            st.info("No matching records found for this location.")

# 5. Fixed Branding Footer
st.markdown(f"""
    <div class="footer-bar">
        <div class="footer-content">DEVELOPED BY <span class="author-name">ASHISH BAJPAI</span></div>
    </div>
    """, unsafe_allow_html=True)