import streamlit as st
import time
from main import SLF_Core

st.set_page_config(page_title="S.L.F. // CORE", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace;}
    .stMetric {border: 1px solid #00FF41; padding: 15px; border-radius: 0px;}
    </style>
""", unsafe_allow_html=True)

if 'fabric' not in st.session_state:
    st.session_state.fabric = SLF_Core()

if 'log_buffer' not in st.session_state:
    st.session_state.log_buffer = []

# --- FIX: CALL THE CORRECT METHOD ---
# Check if your object has a method like 'update', 'step', etc.
# If your class is designed to run automatically, you might not need to call anything here.
if hasattr(st.session_state.fabric, 'tick'):
    st.session_state.fabric.tick()
elif hasattr(st.session_state.fabric, 'update'):
    st.session_state.fabric.update()

# Safely extract latest log
try:
    new_entry = st.session_state.fabric.ledger.chain[-1]['entry']
    if not st.session_state.log_buffer or st.session_state.log_buffer[-1] != new_entry:
        st.session_state.log_buffer.append(new_entry)
        if len(st.session_state.log_buffer) > 15:
            st.session_state.log_buffer.pop(0)
except (AttributeError, IndexError):
    pass # Ledger might be empty

st.title(">> S.L.F. // AUTONOMOUS OPERATING SYSTEM")

# ... [Rest of your layout code remains the same] ...

time.sleep(1)
st.rerun()
