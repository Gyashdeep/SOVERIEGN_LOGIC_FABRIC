import streamlit as st
import threading
import time
from main import SLF_Core

# 1. ENGINE INITIALIZATION
if 'fabric' not in st.session_state:
    st.session_state.fabric = SLF_Core()
    def background_loop():
        while True:
            st.session_state.fabric.execute_tick()
            time.sleep(1)
    threading.Thread(target=background_loop, daemon=True).start()

st.set_page_config(page_title="S.L.F. CONTROL", layout="wide")
st.title("🌐 SOVEREIGN-LOGIC FABRIC // LIVE COMMAND")

# 2. THE STABLE UI LAYER
col1, col2 = st.columns(2)

# Safety check: Ensure the ledger is not empty before accessing
ledger_chain = st.session_state.fabric.ledger.chain

with col1:
    st.metric("CORE TEMPERATURE", f"{st.session_state.fabric.state['temp']}°C")
    st.write("### AUDIT LOG")
    if ledger_chain:
        logs = ledger_chain[-10:]
        for entry in reversed(logs):
            st.code(entry['entry'], language='text')

with col2:
    st.write("### INTEGRITY VERIFICATION")
    # Robust check for the signature
    if ledger_chain:
        last_sig = ledger_chain[-1]['sig']
        st.info(f"BLOCK SIGNATURE: {last_sig[:24]}...")
    else:
        st.warning("INITIALIZING FABRIC...")
        
    if st.session_state.fabric.state['temp'] >= 500:
        st.error("SAFETY SYSTEM ENGAGED")
    else:
        st.success("SYSTEM OPERATING WITHIN PHYSICAL PARAMETERS")

time.sleep(0.5)
st.rerun()
