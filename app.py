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

# 2. Bright Day-Time UI Styling
st.markdown("""
    <style>
    /* Bright Day-Time City Wallpaper */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.2), rgba(0, 0, 0, 0.6)), 
                    url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2044&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Large Header Section */
    .header-container {
        text-align: center;
        padding: 100px 0 60px 0;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 7rem; /* Mega Font size */
        font-weight: 900;
        letter-spacing: -6px;
        color: #ffffff;
        margin: 0;
        text-transform: uppercase;
        line-height: 0.8;
        text-shadow: 2px 2px 30px rgba(0,0,0,0.5);
    }
    .tagline {
        color: #10b981;
        font-size: 2rem; /* Bigger Font */
        font-weight: 700;
        letter-spacing: 8px;
        text-transform: uppercase;
        margin-top: 25px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }

    /* Mega Search Input */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 20px !important;
        padding: 15px !important;
        font-size: 1.5rem !important;
    }

    /* Result Card (Spacious View) */
    .result-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 60px;
        margin-top: 50px;
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.4);
    }
    .village-header {
        font-size: 4rem; /* Big Title */
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 40px;
        border-bottom: 8px solid #10b981;
        display: inline-block;
    }

    /* Data Tiles (Bhara-Bhara look) */
    .data-tile {
        background: #f8fafc;
        padding: 30px;
        border-radius: 20px;
        border-left: 10px solid #10b981;
        margin-bottom: 25px;
    }
    .tile-label { color: #64748b; font-size: 1rem; font-weight: 800; text-transform: uppercase; }
    .tile-value { color: #0f172a; font-size: 1.8rem; font-weight: 700; }

    /* Professional Footer Branding */
    .footer-bar {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #ffffff;
        padding: 25px;
        text-align: center;
        border-top: 1px solid #e2e8f0;
        z-index: 100;
    }
    .footer-content { color: #1e293b; font-size: 1.1rem; font-weight: 600; letter-spacing: 2px; }
    .author-name { 
        color: #10b981; 
        font-weight: 900; 
        text-transform: uppercase; 
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Dynamic Header (3rd line blank as requested)
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">BEYOND <span style="color: #10b981;">CITIES</span></h1>
        <div class="tagline">Rural Data Intelligence Engine</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Search Interface
l, m, r = st.columns([1, 2, 1])
with m:
    # Spacer
    st.markdown("<br>", unsafe_allow_html=True)
    q = st.text_input("SEARCH_ANY_LOCATION", placeholder="Enter Village Name...", label_visibility="collapsed")

    if q:
        res = supabase.table("villages").select("*").ilike("Village Name", f"%{q}%").limit(20).execute()
        
        if res.data:
            options = {f"{r['Village Name']} | {r['Subdistrict Name']} | {r['District Name']}": r for r in res.data}
            sel = st.selectbox("CHOOSE_VILLAGE", options=list(options.keys()), index=None)

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
            st.info("No matching records found in the engine database.")

# 5. Elite Footer
st.markdown(f"""
    <div class="footer-bar">
        <div class="footer-content">DESIGNED & DEVELOPED BY <span class="author-name">ASHISH BAJPAI</span></div>
    </div>
    """, unsafe_allow_html=True)
