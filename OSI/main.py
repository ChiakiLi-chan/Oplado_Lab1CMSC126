# main.py
from phys_layer import PhysicalLayer
from datalink_layer import DataLinkLayer
from network_layer import NetworkLayer
from transport_layer import TransportLayer
from session_layer import SessionLayer
from presentation_layer import PresentationLayer
from application_layer import ApplicationLayer

class OSISimulation:
    def __init__(self):
        """Initialize all OSI layers."""
        self.physical = PhysicalLayer(role='server')
        self.data_link = DataLinkLayer()
        self.network = NetworkLayer()
        self.transport = TransportLayer()
        self.session = SessionLayer()
        self.presentation = PresentationLayer()
        self.application = ApplicationLayer()

    def send_data(self, method, url, message):
        """Simulates data transmission through the OSI model."""
        print("\n[Application Layer] Creating HTTP request...")
        request = self.application.create_http_request(method, url, message)

        print("\n[Presentation Layer] Encoding & encrypting data...")
        encoded_data = self.presentation.encode_data(request.decode())

        print("\n[Session Layer] Attaching session information...")
        session_data = self.session.attach_session_info(encoded_data.decode())

        print("\n[Transport Layer] Segmenting & adding error detection...")
        segment = self.transport.create_segment(session_data.decode())

        print("\n[Network Layer] Creating a packet with IP headers...")
        packet = self.network.create_packet(segment.decode(), "192.168.1.10")

        print("\n[Data Link Layer] Framing data with MAC headers...")
        frame = self.data_link.create_frame(packet.decode())

        print("\n[Physical Layer] Transmitting raw data...\n")
        self.physical.start()  # Start the server to listen
        self.physical.send(frame)

    def receive_data(self):
        """Simulates receiving data through the OSI model."""
        print("\n[Physical Layer] Receiving raw data...")
        frame = self.physical.start()

        print("\n[Data Link Layer] Extracting data from MAC frame...")
        packet = self.data_link.parse_frame(frame)

        print("\n[Network Layer] Extracting payload from IP packet...")
        segment = self.network.parse_packet(packet.encode())

        print("\n[Transport Layer] Extracting segment & verifying integrity...")
        session_data = self.transport.parse_segment(segment.encode())

        print("\n[Session Layer] Verifying session info...")
        encoded_data = self.session.parse_session_info(session_data.encode())

        print("\n[Presentation Layer] Decoding & decrypting data...")
        request = self.presentation.decode_data(encoded_data.encode())

        print("\n[Application Layer] Processing HTTP request...\n")
        method, url, body = self.application.parse_http_request(request.encode())

        if method:
            print(f"[Final Output] {method} request to {url} with message: '{body}'")


if __name__ == "__main__":
    simulation = OSISimulation()
    
    # Simulating data transmission
    simulation.send_data("GET", "/home", "Hello, OSI Model!")

    # Simulating data reception
    simulation.receive_data()
