import streamlit as st
from supabase import create_client, Client

# 1. Page Config
st.set_page_config(page_title="Beyond Cities", layout="wide")

# Direct Connection
SUPABASE_URL = "https://fqmwbqtpuokntbjkcikp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZxbXdicXRwdW9rbnRiamtjaWtwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMwNzA1MSwiZXhwIjoyMDkyODgzMDUxfQ.yzmHMSoMF9vqY-ruCprNE4Gu2yXEeQV_q_tG5CqNu-4"

@st.cache_resource
def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_client()

# 2. Advanced UI Styling
st.markdown("""
    <style>
    /* Full Screen Wallpaper Fix */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), 
                    url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2044&auto=format&fit=crop");
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        height: 100vh;
        width: 100vw;
    }

    /* Massive Professional Header */
    .header-container {
        text-align: center;
        padding: 120px 0 40px 0;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 8.5rem; /* Massive size */
        font-weight: 900;
        letter-spacing: -8px;
        color: #0f172a; /* Deep contrast color */
        margin: 0;
        text-transform: uppercase;
        line-height: 0.8;
    }
    .blue-accent { color: #0070f3; } /* Electric Blue for visibility */

    .tagline {
        color: #1e293b;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: 10px;
        text-transform: uppercase;
        margin-top: 30px;
    }

    /* Solid Professional Search Bar */
    div[data-baseweb="input"] {
        background-color: #0f172a !important; /* Solid Dark Theme */
        border: 2px solid #0070f3 !important;
        border-radius: 15px !important;
        padding: 12px !important;
    }
    input {
        color: #ffffff !important;
        font-size: 1.4rem !important;
    }

    /* Result Card (Elite View) */
    .result-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 25px;
        padding: 50px;
        margin-top: 40px;
        box-shadow: 0 50px 100px rgba(0, 0, 0, 0.3);
        border-top: 10px solid #0070f3;
    }
    .village-header {
        font-size: 3.5rem;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 35px;
    }

    .data-tile {
        background: #f1f5f9;
        padding: 25px;
        border-radius: 15px;
        border-right: 6px solid #0070f3;
        margin-bottom: 20px;
    }
    .tile-label { color: #64748b; font-size: 0.9rem; font-weight: 800; text-transform: uppercase; }
    .tile-value { color: #0f172a; font-size: 1.6rem; font-weight: 700; }

    /* Slim & Professional Footer */
    .footer-bar {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0f172a;
        padding: 12px;
        text-align: center;
        z-index: 100;
    }
    .footer-content { 
        color: #94a3b8; 
        font-size: 0.8rem; 
        font-weight: 400; 
        letter-spacing: 3px; 
        text-transform: uppercase;
    }
    .author-name { 
        color: #ffffff; 
        font-weight: 700; 
        border-left: 2px solid #0070f3;
        padding-left: 10px;
        margin-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Heading Section
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">BEYOND <span class="blue-accent">CITIES</span></h1>
        <div class="tagline">Rural Data Intelligence Engine</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Search Logic
l, m, r = st.columns([1, 2, 1])
with m:
    st.markdown("<br>", unsafe_allow_html=True)
    q = st.text_input("QUERY_FIELD", placeholder="Enter Village Name...", label_visibility="collapsed")

    if q:
        res = supabase.table("villages").select("*").ilike("Village Name", f"%{q}%").limit(20).execute()
        
        if res.data:
            options = {f"{r['Village Name']} | {r['Subdistrict Name']} | {r['District Name']}": r for r in res.data}
            sel = st.selectbox("CHOOSE_LOCATION", options=list(options.keys()), index=None)

            if sel:
                v = options[sel]
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="village-header">{v["Village Name"]}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                display_items = [
                    ("District Name", "District Name"), ("District Code", "District Code"),
                    ("Subdistrict Name", "Subdistrict Name"), ("Village Code", "Village Code"),
                    ("Local Body", "Local Body Name"), ("LGD Code", "Local Body Code")
                ]
                
                for i, (label, key) in enumerate(display_items):
                    target = c1 if i % 2 == 0 else c2
                    target.markdown(f"""
                        <div class="data-tile">
                            <div class="tile-label">{label}</div>
                            <div class="tile-value">{v.get(key, 'N/A')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Data not found in intelligence engine.")

# 5. Slim Footer
st.markdown(f"""
    <div class="footer-bar">
        <div class="footer-content">Designed & Developed by <span class="author-name">Ashish Bajpai</span></div>
    </div>
    """, unsafe_allow_html=True)
