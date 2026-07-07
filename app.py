import streamlit as st
import threading
import time
from main import SLF_Core

if 'fabric' not in st.session_state:
    st.session_state.fabric = SLF_Core()
    def background_loop():
        while True:
            st.session_state.fabric.execute_tick()
            time.sleep(1)
    threading.Thread(target=background_loop, daemon=True).start()

st.set_page_config(page_title="S.L.F. CONTROL", layout="wide")
st.title("🌐 SOVEREIGN-LOGIC FABRIC // LIVE COMMAND")

col1, col2 = st.columns(2)

with col1:
    st.metric("CORE TEMPERATURE", f"{st.session_state.fabric.state['temp']}°C")
    st.write("### AUDIT LOG")
    logs = st.session_state.fabric.ledger.chain[-10:]
    for entry in reversed(logs):
        st.code(entry['entry'], language='text')

with col2:
    st.write("### INTEGRITY VERIFICATION")
    last_sig = st.session_state.fabric.ledger.chain[-1]['sig']
    st.info(f"BLOCK SIGNATURE: {last_sig[:24]}...")
    if st.session_state.fabric.state['temp'] >= 500:
        st.error("SAFETY SYSTEM ENGAGED")
    else:
        st.success("SYSTEM OPERATING WITHIN PHYSICAL PARAMETERS")

time.sleep(0.5)
st.rerun()
