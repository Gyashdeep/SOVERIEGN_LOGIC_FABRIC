import streamlit as st
import time
import threading
from main import SLF_Core

# Ensure the fabric is created ONLY ONCE in the app's lifecycle
if 'fabric' not in st.session_state:
    st.session_state.fabric = SLF_Core()
    
    # Define the background worker
    def background_worker():
        while True:
            st.session_state.fabric.execute_tick()
            time.sleep(1)
            
    # Run the worker in a thread so it doesn't block the UI
    thread = threading.Thread(target=background_worker, daemon=True)
    thread.start()

# Now the UI reads from the exact same object the worker is writing to
st.set_page_config(page_title="S.L.F. // TERMINAL", layout="wide")

st.title(">> S.L.F. // AUTONOMOUS OPERATING SYSTEM")

# Visualization of the industrial control loop


col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("PHYSICAL TELEMETRY")
    temp = st.session_state.fabric.state['temp']
    st.metric("CORE TEMP", f"{temp} C")
    
    st.write("### LIVE AUDIT FEED")
    # This now shows the FULL history because it's reading the shared object
    logs = st.session_state.fabric.ledger.chain 
    for entry in reversed(logs[-15:]):
        st.code(f"> {entry['entry']}", language='text')

with col2:
    st.subheader("SYSTEM GOVERNANCE")
    last_sig = st.session_state.fabric.ledger.chain[-1]['sig']
    st.text(f"CRYPTO_SIGNATURE:\n{last_sig}")
    
    st.progress(min(temp / 500, 1.0))
    if temp >= 500:
        st.error("!!! THERMAL CRITICAL // PHYSICS GOVERNANCE ACTIVE !!!")
    else:
        st.success("SYSTEM INTEGRITY: NOMINAL")

time.sleep(1)
st.rerun()
