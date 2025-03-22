import random
from datalink_layer import DataLinkLayer
from network_layer import NetworkLayer
from transport_layer import TransportLayer
from session_layer import SessionLayer
from presentation_layer import PresentationLayer
from application_layer import ApplicationLayer
from phys_layer import PhysicalLayer

class OSISimulation:
    def __init__(self):
        """Initialize all OSI layers."""
        self.physical = PhysicalLayer()
        self.data_link = DataLinkLayer()
        self.network = NetworkLayer()
        self.transport = TransportLayer()
        self.session = SessionLayer()
        self.presentation = PresentationLayer()
        self.application = ApplicationLayer()

    def get_dynamic_dest_ip(self):
        """Dynamically determines the destination IP based on learned MAC addresses."""
        if self.data_link.mac_table:
            # Get a random destination IP from known MAC table entries
            return random.choice(list(self.data_link.mac_table.keys()))
        else:
            return "192.168.1.255"  # Broadcast as fallback


    def send_data(self, method, url, message):
        """Simulates sending data through the OSI model."""

        print("\n This is the server side of the OSI model.")

        print("\n[Application Layer] Creating HTTP request...")
        request = self.application.create_http_request(method, url, message)

        print("\n[Presentation Layer] Encoding & encrypting data...")
        encoded_data = self.presentation.encode_data(request)

        session_data = self.session.attach_session_info(encoded_data)

        segment = self.transport.create_segment(session_data)

        sender_ip = self.data_link.device_ip 
        dest_ip = self.get_dynamic_dest_ip() 
        checksum = self.transport.calculate_checksum(segment)
        packet = self.network.create_packet(sender_ip, dest_ip, segment, checksum)
        print(f"\n[Network Layer] Created packet: {packet}")


        print("\n[Data Link Layer] Framing data with MAC headers...")
        frame = self.data_link.create_frame(packet, dest_ip)

        print("\n[Physical Layer] Transmitting raw data...")
        transmitted_data = self.physical.send(frame)  # No need for client.start()

        print("\n[Physical Layer] Simulated transmission complete!\n")
        return transmitted_data  # Pass to receiver

    def receive_data(self, transmitted_data):
        print("\nWe have reached the client side of this OSI simulation.")

        print("\n[Physical Layer] Receiving raw data...")
        frame = self.physical.receive(transmitted_data)  # Use `receive()` instead of `start()`

        if frame is None:
            print("[ERROR] No frame received at Physical Layer!")
            return

        print(f"[DEBUG] Frame received: {frame}")

        print("\n[Data Link Layer] Extracting data from MAC frame...")
        packet = self.data_link.parse_frame(frame)

        if packet is None:
            print("[ERROR] Data Link Layer failed to extract a valid packet!")
            return

        print(f"[DEBUG] Packet received: {packet}")

        print("\n[Network Layer] Extracting payload from IP packet...")
        _, _, segment = self.network.parse_packet(packet)  # Extract only the payload

        if segment is None:
            print("[ERROR] Network Layer failed to extract a valid segment!")
            return

        print(f"[DEBUG] Segment received: {segment}")

        print("\n[Transport Layer] Extracting segment & verifying integrity...")
        session_data = self.transport.parse_segment(segment)

        if session_data is None:
            print("[ERROR] Transport Layer did not return valid session data!")
            return

        print(f"[DEBUG] Session data received: {session_data}")

        print("\n[Session Layer] Verifying session info...")
        encoded_data = self.session.parse_session_info(session_data)

        if encoded_data is None:
            print("[ERROR] Session Layer did not return valid encoded data!")
            return

        print(f"[DEBUG] Encoded data received: {encoded_data}")

        print("\n[Presentation Layer] Decoding & decrypting data...")
        request = self.presentation.decode_data(encoded_data)

        if request is None:
            print("[ERROR] Presentation Layer failed to decode the request!")
            return

        print(f"[DEBUG] Request received: {request}")

        return request  # Ensure function returns correctly



if __name__ == "__main__":
    osi_sim = OSISimulation()

    # Simulate sending data
    transmitted_data = osi_sim.send_data("GET", "/home", "Hello, OSI Model!")

    # Simulate receiving data
    osi_sim.receive_data(transmitted_data)
