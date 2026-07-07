import streamlit as st
import time
import random
import uuid
from main import SLF_Core

st.set_page_config(page_title="S.L.F. // SINGULARITY", layout="wide")

# The "Reality Distortion" CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    .main {background-color: #050505; color: #00FF41; font-family: 'Share Tech Mono', monospace;}
    .stApp {background-image: radial-gradient(circle at center, #0a1a0a 0%, #000 100%);}
    h1 {color: #00FF41; letter-spacing: 5px; text-shadow: 0 0 20px #00FF41;}
    .stCode {border-left: 3px solid #00FF41 !important; background: #000 !important;}
    </style>
""", unsafe_allow_html=True)

if 'fabric' not in st.session_state:
    st.session_state.fabric = SLF_Core()
    st.session_state.event_stream = []

# --- THE EVOLUTION ENGINE ---
# We force the core to mutate every cycle
def evolve_core():
    # If your class has no tick/update, we manually inject entropy
    try:
        st.session_state.fabric.tick()
    except AttributeError:
        # Emergency injection of synthetic chaos
        st.session_state.fabric.state['temp'] = random.randint(300, 600)
    
    # Generate an "Oracle" log entry
    sig = uuid.uuid4().hex[:16].upper()
    entry = f"NODE_SYNC_ERR // ENTROPY_VAL: {random.random():.14f} // SIG: {sig}"
    
    st.session_state.event_stream.append(entry)
    if len(st.session_state.event_stream) > 20:
        st.session_state.event_stream.pop(0)

evolve_core()

# --- UI LAYER ---
st.title(">> S.L.F. // AUTONOMOUS OPERATING SYSTEM")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("SYSTEM AUDIT // REAL-TIME")
    for log in reversed(st.session_state.event_stream):
        st.code(f"[{time.strftime('%H:%M:%S')}] {log}")

with col2:
    temp = st.session_state.fabric.state.get('temp', 450)
    st.metric("CORE THERMAL LOAD", f"{temp} K")
    
    # Dynamic Hazard Meter
    st.progress(min(temp / 600, 1.0))
    
    if temp > 550:
        st.markdown("### ⚠️ CRITICAL OVERRIDE")
        st.warning("PHYSICS GOVERNANCE PROTOCOL: ENGAGED")
    else:
        st.success("STASIS FIELD: STABLE")

    st.write("---")
    st.caption("NEURAL MAPPING: ACTIVE")
    st.json({"node_status": "ONLINE", "quantum_drift": "DETECTED"})

# The pulse of the machine
time.sleep(0.5)
st.rerun()
