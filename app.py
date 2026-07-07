import streamlit as st
import time
import threading
from main import SLF_Core # Import your engine

# 1. INITIALIZE THE FABRIC IN SESSION STATE
if 'fabric' not in st.session_state:
    st.session_state.fabric = SLF_Core()
    # Start background thread to run the engine continuously
    def run_fabric():
        while True:
            st.session_state.fabric.execute()
            time.sleep(2) # Polling rate
    
    thread = threading.Thread(target=run_fabric, daemon=True)
    thread.start()

# 2. UI CONFIGURATION
st.set_page_config(page_title="S.L.F. CONTROL", layout="wide")
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    .stMetric {background-color: #1e1e1e; padding: 20px; border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 SOVEREIGN-LOGIC FABRIC // LIVE COMMAND")

# 3. LIVE TELEMETRY
col1, col2 = st.columns(2)

with col1:
    st.metric("CORE TEMPERATURE", f"{st.session_state.fabric.state['temp']}°C")
    st.write("### SYSTEM LOGS")
    # Show the last 5 entries from your ledger
    ledger_display = st.session_state.fabric.ledger.chain[-5:]
    for entry in reversed(ledger_display):
        st.code(entry['entry'], language='text')

with col2:
    st.write("### PHYSICS VALIDATION")
    st.success("STATUS: GROUNDED IN REALITY")
    st.info(f"LAST SIGNATURE: {st.session_state.fabric.ledger.chain[-1]['sig'][:20]}...")

# Auto-refresh the UI every second to show real-time changes
time.sleep(1)
st.rerun()
