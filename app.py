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

# 2. UI Styling (100% Match with Search Button & Magnifier)
st.markdown("""
    <style>
    /* Full Page Background */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                    url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2044&auto=format&fit=crop");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* HEADER SECTION */
    .header-box { 
        text-align: center; 
        padding-top: 15vh; 
        padding-bottom: 20px; 
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 6rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .tagline {
        color: #4fc3f7;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 15px;
    }

    /* SEARCH INPUT & BUTTON ROW styling */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 4px 0 0 4px !important; /* Rounded only on left */
    }
    
    input { color: white !important; }

    /* SEARCH BUTTON CUSTOM STYLE */
    .stButton > button {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 0 4px 4px 0 !important; /* Rounded only on right */
        height: 45px !important;
        width: 100% !important;
        margin-left: -2px !important; /* Connect with input box */
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #4fc3f7 !important;
        border-color: #4fc3f7 !important;
    }

    /* SUGGESTIONS LIST */
    div[data-baseweb="popover"] {
        top: 50px !important;
        background-color: #1a1c23 !important;
    }

    /* RESULT CARD */
    .result-card {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        border-radius: 8px;
        margin-top: 30px;
    }

    .v-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 25px;
    }

    .data-tile {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    .tile-label { color: #94a3b8; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }
    .tile-value { color: #FFFFFF; font-size: 1.4rem; font-weight: 500; }

    /* FOOTER */
    .footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: rgba(0, 0, 0, 0.9);
        padding: 15px;
        text-align: center;
        z-index: 1000;
    }
    .footer-text { 
        color: rgba(255, 255, 255, 0.4); 
        font-size: 0.75rem; 
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .bold-name { color: rgba(255, 255, 255, 0.8); font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown("""
    <div class="header-box">
        <h1 class="main-title">BEYOND CITIES</h1>
        <div class="tagline">RURAL DATA INTELLIGENCE ENGINE</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Search Engine Logic
l, m, r = st.columns([1, 2, 1])

with m:
    # Creating a tight row for Input + Magnifier Button
    sc1, sc2 = st.columns([0.88, 0.12], gap="small")
    
    with sc1:
        q = st.text_input("SEARCH", placeholder="Search 600,000+ villages instantly...", label_visibility="collapsed")
    
    with sc2:
        # Action trigger button with magnifier
        search_trigger = st.button("🔍")

    if q:
        res = supabase.table("villages").select("*").ilike("Village Name", f"%{q}%").limit(15).execute()
        
        if res.data:
            options = {f"{r['Village Name']} | {r['Subdistrict Name']} | {r['District Name']}": r for r in res.data}
            
            sel = st.selectbox("SELECT", options=list(options.keys()), index=None, label_visibility="collapsed", placeholder="Select from suggestions below ↓")

            if sel:
                v = options[sel]
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="v-header">{v["Village Name"]}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                fields = [
                    ("District", "District Name"), ("District Code", "District Code"),
                    ("Subdistrict", "Subdistrict Name"), ("Village Code", "Village Code"),
                    ("Local Body", "Local Body Name"), ("LGD Code", "Local Body Code")
                ]
                
                for i, (label, key) in enumerate(fields):
                    target = c1 if i % 2 == 0 else c2
                    target.markdown(f"""
                        <div class="data-tile">
                            <div class="tile-label">{label}</div>
                            <div class="tile-value">{v.get(key, 'N/A')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# 5. Footer
st.markdown(f"""
    <div class="footer">
        <div class="footer-text">
            © 2026 BEYOND CITIES INTELLIGENCE | DEVELOPED BY <span class="bold-name">ASHISH BAJPAI</span>
        </div>
    </div>
    """, unsafe_allow_html=True) me
