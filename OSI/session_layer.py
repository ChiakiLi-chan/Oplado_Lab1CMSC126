import random

class SessionLayer:
    def __init__(self):
        """Manages session states and synchronization."""
        self.sessions = {}

    def start_session(self):
        """Starts a new session and changes state."""
        session_id = random.randint(10000, 99999)
        self.sessions[session_id] = "CONNECTED"
        print(f"[Session Layer] Session {session_id} started.")
        return session_id

    def end_session(self, session_id):
        """Ends the session and resets state."""
        if session_id in self.sessions:
            self.sessions[session_id] = "DISCONNECTED"
            print(f"[Session Layer] Session {session_id} ended.")
        else:
            print(f"[ERROR] Session {session_id} not found!")

    def attach_session_info(self, payload):
        """Adds session metadata to the payload."""
        session_id = random.randint(10000, 99999)
        self.sessions[session_id] = "CONNECTED"
        session_data = f"SessionID:{session_id}|{payload}"
        print(f"\n[Session Layer] Attaching session information...\n{session_data}\n")
        return f"{session_id}|{payload}".encode()

    def parse_session_info(self, session_data):
        print(f"[DEBUG] Session Layer - Raw session data received: {session_data}")

        if not isinstance(session_data, str) or not session_data:
            print("[ERROR] Session data is not a valid string or is empty!")
            return None

        try:
            session_id, payload = session_data.split("|", 1)  # Split on the first "|", session_id is ignored
            session_id = session_id.replace("b'", "")
            print(f"[DEBUG] Decoded session data - Session ID: {session_id}, Payload: {payload}")
            # Optionally validate session ID if needed (e.g., check if it's numeric)
            if not session_id.isdigit():
                print("[ERROR] Invalid session ID format! Must be a numeric value.")
                return None

            # **ONLY RETURN FINAL PAYLOAD** for further processing
            return payload

        except ValueError:
            print("[ERROR] Invalid session data format! Expected format: session_id|payload")
            return None

