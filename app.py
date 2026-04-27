import streamlit as st
from supabase import create_client, Client

# 1. Page Config
st.set_page_config(page_title="Beyond Cities", layout="wide")

# Database Connection
SUPABASE_URL = "https://fqmwbqtpuokntbjkcikp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZxbXdicXRwdW9rbnRiamtjaWtwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMwNzA1MSwiZXhwIjoyMDkyODgzMDUxfQ.yzmHMSoMF9vqY-ruCprNE4Gu2yXEeQV_q_tG5CqNu-4"

@st.cache_resource
def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_client()

# 2. UI Styling (Magnifier, Cross, and Slide Suggestions)
st.markdown("""
    <style>
    /* Background Fix */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
                    url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2044&auto=format&fit=crop");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* Header */
    .header-box { text-align: center; padding: 80px 0 20px 0; }
    .main-title { font-family: 'Inter', sans-serif; font-size: 6rem; font-weight: 900; color: #ffffff; margin: 0; text-transform: uppercase; line-height: 1; }
    .tagline { color: #4fc3f7; font-size: 1.1rem; font-weight: 700; letter-spacing: 5px; text-transform: uppercase; margin-top: 15px; }

    /* Search Bar Wrapper with Icons */
    .search-container { position: relative; width: 100%; }
    
    /* Magnifier & Cross styling simulation */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        padding-right: 40px !important; /* Space for icon */
    }
    
    /* Hiding the 'Choose an option' box and making it look like a list */
    .stSelectbox label { display: none; }
    
    /* Animation for Results */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-card {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 45px;
        border-radius: 12px;
        margin-top: 30px;
        animation: slideIn 0.5s ease-out;
    }

    .v-header { font-size: 2.8rem; font-weight: 800; color: #ffffff; border-left: 6px solid #4fc3f7; padding-left: 20px; margin-bottom: 25px; }

    .data-tile { background: rgba(255, 255, 255, 0.03); padding: 18px; border-radius: 8px; margin-bottom: 12px; }
    .tile-label { color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
    .tile-value { color: #ffffff; font-size: 1.3rem; font-weight: 600; }

    /* Footer */
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(0, 0, 0, 0.9); padding: 15px; text-align: center; }
    .footer-text { color: rgba(255, 255, 255, 0.4); font-size: 0.7rem; letter-spacing: 2px; }
    .author { color: #ffffff; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("""
    <div class="header-box">
        <h1 class="main-title">BEYOND CITIES</h1>
        <div class="tagline">RURAL DATA INTELLIGENCE ENGINE</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Search & Suggestion Logic
l, m, r = st.columns([1, 2, 1])

with m:
    # Search input - Placeholder updated to 1 Lakh
    # Streamlit me Magnifier aur Cross button automatic hote hain default search bar me
    # Humne 'selectbox' ko he main search bar banaya hai taaki suggestion niche slide ho
    
    user_input = st.text_input("SEARCH", placeholder="🔍 Search 100,000+ villages instantly... (Type and Select)", label_visibility="collapsed")

    if user_input:
        # Fetching data from Supabase
        res = supabase.table("villages").select("*").ilike("Village Name", f"%{user_input}%").limit(15).execute()
        
        if res.data:
            # Suggestion list (Isse 'Choose an option' wala bar feel nahi hoga, list lagegi)
            options = {f"{r['Village Name']} | {r['Subdistrict Name']} | {r['District Name']}": r for r in res.data}
            
            # Jab user type karega, ye niche list ki tarah dikhega
            selection = st.selectbox("Suggestions", options=list(options.keys()), index=None, label_visibility="collapsed", placeholder="Select from suggestions below ↓")

            if selection:
                v = options[selection]
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

# 5. Footer
st.markdown(f"""
    <div class="footer">
        <div class="footer-text">© 2026 BEYOND CITIES INTELLIGENCE | DEVELOPED BY <span class="author">ASHISH BAJPAI</span></div>
    </div>
    """, unsafe_allow_html=True)
