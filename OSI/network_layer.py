import random
import struct
import socket
import json
import base64

class NetworkLayer:
    def __init__(self):
        self.ip_address = self.get_current_ip()  # Get actual machine IP
        self.port = random.randint(1024, 65535)

    def get_current_ip(self):
        """Gets the actual IP address of the current machine."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))  # Google's public DNS server
            ip = s.getsockname()[0]  # Get local IP address
        finally:
            s.close()
        return ip

    def create_packet(self, sender_ip, dest_ip, segment, checksum):
        """Creates a network packet with source IP, destination IP, and encoded data."""
        if isinstance(segment, str):
            segment = segment.encode("utf-8")  # Ensure segment is encoded
        elif isinstance(segment, bytes):
            segment = base64.b64encode(segment).decode("utf-8")  # Encode bytes to base64 string

        # Ensure the port is correctly serialized (no bytes objects left)
        port_str = str(self.port)  # Convert port to string to avoid JSON serialization issues

        packet = {
            "src_ip": sender_ip,
            "dest_ip": dest_ip,
            "port": port_str,  # Store port as string
            "payload": segment,
            "checksum": checksum
        }

        print(f"[DEBUG] Network Layer - Packet Payload Before Sending: {segment}")
        print(f"[Network Layer] Created packet: {packet}")
        
        return json.dumps(packet).encode()  # Now it should work without errors

    def parse_packet(self, packet):
        """Parses a received network packet."""
        try:
            if isinstance(packet, bytes):  # Decode bytes to string if necessary
                packet = packet.decode()

            packet = json.loads(packet)  # Parse JSON safely
            print(f"[Network Layer] Received packet: {packet}")

            # Extract src_ip, dest_ip, and payload correctly
            src_ip = packet.get("src_ip")
            dest_ip = packet.get("dest_ip")
            payload = packet.get("payload")

            # Check if payload is base64-encoded (i.e., a string) and decode it if necessary
            try:
                # Attempt to decode from base64 if it's not plain text
                payload = base64.b64decode(payload).decode("utf-8")
                print(f"[Network Layer] Payload Extracted (Base64 decoded): {payload}")
            except Exception as e:
                # If decoding fails, the payload is likely not base64-encoded
                print(f"[Network Layer] Payload Extracted (Plain Text): {payload}")

            # Return src_ip, dest_ip, and payload to simulate correct extraction
            return src_ip, dest_ip, payload

        except Exception as e:
            print(f"[Network Layer] Error parsing packet: {e}")
            return None, None, None  # Return exactly 3 values to avoid unpacking errors

    def verify_checksum(self, packet):
        """Verifies the checksum of the received packet.""" 
        expected_checksum = packet.get("checksum")
        calculated_checksum = self.calculate_checksum(packet["payload"])
        if expected_checksum == calculated_checksum:
            print("[Network Layer] Checksum verified. Data is intact.")
        else:
            print("[ERROR] Checksum mismatch! Data may be corrupted.")
    
    def calculate_checksum(self, data):
        """Simple checksum calculation for packet verification."""
        checksum = sum(ord(c) for c in data) % 256
        return str(checksum)
