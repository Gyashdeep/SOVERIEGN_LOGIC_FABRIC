import time
import hashlib
import threading
from datetime import datetime

class Ledger:
    def __init__(self):
        self.chain = []
        self.record("GENESIS", "SYSTEM_BOOT")
    
    def record(self, action, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp}|{action}|{status}"
        signature = hashlib.sha256(entry.encode()).hexdigest()
        self.chain.append({"entry": entry, "sig": signature})

class PhysicalSafetyLayer:
    def __init__(self):
        self.constraints = {'max_temp': 500}

    def validate(self, action, state):
        if action['type'] == 'HEAT_UP' and state['temp'] >= self.constraints['max_temp']:
            return False, "SAFETY_VIOLATION: THERMAL_LIMIT"
        return True, "SAFE"

class SLF_Core:
    def __init__(self):
        self.state = {'temp': 450}
        self.safety = PhysicalSafetyLayer()
        self.ledger = Ledger()
        self.lock = threading.Lock() # Protect state during UI reads

    def execute_tick(self):
        with self.lock:
            # Reasoning: Decision Engine
            action = {"type": "HEAT_UP", "value": 10}
            
            # Validation: Physics Sandbox
            is_valid, reason = self.safety.validate(action, self.state)
            
            # Execution
            if is_valid:
                self.state['temp'] += action['value']
                self.ledger.record(action, "EXECUTED")
            else:
                self.ledger.record(action, f"BLOCKED: {reason}")
