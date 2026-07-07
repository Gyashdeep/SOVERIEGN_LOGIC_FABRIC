import streamlit as st
import time
from main import SLF_Core

# Configuration
st.set_page_config(page_title="S.L.F. // CORE", layout="wide")

# Custom CSS for aesthetic
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

# Buffer for the UI to hold recent logs
if 'log_buffer' not in st.session_state:
    st.session_state.log_buffer = []

# Perform an engine update (assuming .tick() exists to generate new logs)
# If your core does not have a tick method, trigger your logic here
st.session_state.fabric.tick() 
new_entry = st.session_state.fabric.ledger.chain[-1]['entry']

# Append new log and maintain a rolling window of 15
if not st.session_state.log_buffer or st.session_state.log_buffer[-1] != new_entry:
    st.session_state.log_buffer.append(new_entry)
    if len(st.session_state.log_buffer) > 15:
        st.session_state.log_buffer.pop(0)

st.title(">> S.L.F. // AUTONOMOUS OPERATING SYSTEM")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("PHYSICAL TELEMETRY")
    temp = st.session_state.fabric.state['temp']
    st.metric("CORE TEMP", f"{temp} C")
    
    st.write("### LIVE AUDIT STREAM")
    # Render the buffer in reverse (newest on top)
    for entry in reversed(st.session_state.log_buffer):
        st.code(f"> {entry}", language='text')

with col2:
    st.subheader("GOVERNANCE LAYER")
    last_sig = st.session_state.fabric.ledger.chain[-1]['sig']
    st.text(f"CRYPTO_SIGNATURE:\n{last_sig}")
    
    progress = min(temp / 500, 1.0)
    st.progress(progress)
    
    if temp >= 500:
        st.error("!!! THERMAL CRITICAL // PHYSICS GOVERNANCE ACTIVE !!!")
    else:
        st.success("SYSTEM INTEGRITY: NOMINAL")

# Force loop refresh
time.sleep(1)
st.rerun()
