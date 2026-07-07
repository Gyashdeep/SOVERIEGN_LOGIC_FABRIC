import streamlit as st
import time
from main import SLF_Core

# Configuration for a "Terminal" look
st.set_page_config(page_title="S.L.F. // CORE", layout="wide")

# Custom CSS for that 0.0000000000001% aesthetic
st.markdown("""
    <style>
    .main {background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace;}
    .stMetric {border: 1px solid #00FF41; padding: 15px; border-radius: 0px;}
    h1 {color: #00FF41; text-shadow: 0 0 10px #00FF41;}
    code {background-color: #1a1a1a !important; color: #00FF41 !important;}
    </style>
""", unsafe_allow_html=True)

# State initialization
if 'fabric' not in st.session_state:
    st.session_state.fabric = SLF_Core()

st.title(">> S.L.F. // AUTONOMOUS OPERATING SYSTEM")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("PHYSICAL TELEMETRY")
    temp = st.session_state.fabric.state['temp']
    st.metric("CORE TEMP", f"{temp} C")
    
    st.write("### LIVE AUDIT STREAM")
    # Display the ledger as a retro terminal feed
    logs = st.session_state.fabric.ledger.chain[-15:]
    for entry in reversed(logs):
        st.code(f"> {entry['entry']}", language='text')

with col2:
    st.subheader("GOVERNANCE LAYER")
    last_sig = st.session_state.fabric.ledger.chain[-1]['sig']
    st.text(f"CRYPTO_SIGNATURE:\n{last_sig}")
    
    # Visual "Heartbeat" of the engine
    progress = min(temp / 500, 1.0)
    st.progress(progress)
    
    if temp >= 500:
        st.error("!!! THERMAL CRITICAL // PHYSICS GOVERNANCE ACTIVE !!!")
    else:
        st.success("SYSTEM INTEGRITY: NOMINAL")

# Force loop refresh
time.sleep(1)
st.rerun()
