import random
import json
import socket
import time

class DataLinkLayer:
    def __init__(self):
        """Initialize Data Link Layer with a dynamic MAC table and real device IP."""
        self.mac_address = self.generate_mac()
        self.device_ip = self.get_local_ip()  # Dynamically get device's IP
        self.mac_table = {}  # Dictionary to store IP-to-MAC mappings with timestamps

    def generate_mac(self):
        """Generate a random MAC address (format: XX:XX:XX:XX:XX:XX)."""
        return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

    def get_local_ip(self):
        """Retrieve the local machine's IP address dynamically."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Google's DNS server (doesn't send data)
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"  # Fallback to localhost if error occurs

    def learn_mac(self, ip, mac):
        """Store a dynamically learned MAC address with timestamp."""
        timestamp = time.time()  # Store the current timestamp
        self.mac_table[ip] = {"mac": mac, "timestamp": timestamp}
        print(f"[Data Link Layer] Learned MAC: {mac} for IP: {ip} at {timestamp}")

    def get_mac(self, ip):
        """Retrieve the MAC address for a given IP. If unknown, use broadcast."""
        mac_entry = self.mac_table.get(ip)
        if mac_entry:
            # Optionally, you can add logic to expire old MAC addresses here
            return mac_entry["mac"]
        else:
            return "FF:FF:FF:FF:FF:FF"  # Broadcast address

    def create_frame(self, packet, dest_ip):
        """Encapsulate packet into a MAC frame dynamically."""
        if isinstance(packet, bytes):  # Ensure packet is a string before JSON encoding
            packet = packet.decode()

        src_mac = self.mac_address
        dest_mac = self.get_mac(dest_ip)  # Lookup or use broadcast
        frame = {
            "src_mac": src_mac,
            "dest_mac": dest_mac,
            "payload": packet,
        }
        return json.dumps(frame).encode()

    def parse_frame(self, frame):
        """Extract and process data from a received MAC frame."""
        if isinstance(frame, bytes):
            frame = frame.decode()

        try:
            frame = json.loads(frame)
        except json.JSONDecodeError:
            print("[Data Link Layer] Error: Corrupted frame, cannot decode JSON.")
            return None  # Prevents passing corrupted data

        src_mac = frame.get("src_mac", "Unknown")
        dest_mac = frame.get("dest_mac", "Unknown")
        payload = frame.get("payload", None)

        if not src_mac or not dest_mac or payload is None:
            print("[ERROR] Frame missing essential information.")
            return None  # Prevents crashing later

        print(f"\n[Data Link Layer] Received frame from {src_mac} to {dest_mac}")
        return payload  # Pass to the Network Layer
