import streamlit as st
import time
import threading
from main import SLF_Core

@st.cache_resource
def get_fabric():
    fabric = SLF_Core()
    def background_loop():
        while True:
            fabric.execute_tick()
            time.sleep(1)
    threading.Thread(target=background_loop, daemon=True).start()
    return fabric

fabric = get_fabric()

st.set_page_config(page_title="S.L.F. CONTROL", layout="wide")
st.title("🌐 SOVEREIGN-LOGIC FABRIC // LIVE COMMAND")

col1, col2 = st.columns(2)

with col1:
    with fabric.lock: # Ensure thread-safe read
        current_temp = fabric.state['temp']
        logs = fabric.ledger.chain[-10:]
    
    st.metric("CORE TEMPERATURE", f"{current_temp}°C")
    st.write("### AUDIT LOG")
    for entry in reversed(logs):
        st.code(entry['entry'], language='text')

with col2:
    with fabric.lock:
        last_sig = fabric.ledger.chain[-1]['sig']
    
    st.write("### INTEGRITY VERIFICATION")
    st.info(f"BLOCK SIGNATURE: {last_sig[:24]}...")
    
    if current_temp >= 500:
        st.error("SAFETY SYSTEM ENGAGED: THERMAL LIMIT REACHED")
    else:
        st.success("SYSTEM OPERATING WITHIN PHYSICAL PARAMETERS")

time.sleep(1)
st.rerun()
