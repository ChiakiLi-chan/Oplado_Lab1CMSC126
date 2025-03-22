import random

class TransportLayer:
    def __init__(self):
        """Initializes the transport layer with a sequence number."""
        self.sequence_number = random.randint(1000, 9999)
        self.port = random.randint(1024, 65535)
        self.expected_sequence_number = self.sequence_number

    def create_segment(self, payload):
        print(f"Received payload: {payload}")
        """Encapsulates data into a transport segment with a sequence number and checksum."""
        checksum = self.calculate_checksum(payload)
        segment = f"{self.sequence_number}|{payload}|{checksum}"
        print(f"\n[Transport Layer] Created segment:{segment} \n Sequence number:{self.sequence_number}|Payload: {payload}| Checksum: {checksum} \n")  # ✅ Debug print
        return segment.encode()

    def parse_segment(self, segment):
        print(f"[DEBUG] Transport Layer - Raw Segment Received: {segment}")  # ✅ Debug log

        if isinstance(segment, bytes):
            segment = segment.decode()

        print(f"[Transport Layer] Parsed segment: {segment}")

        # Split the segment by the '|' delimiter
        try:
            seq_num, session_number, payload, checksum = segment.split("|", 4)  # Split into 3 parts: seq_num, payload, checksum
            print(f"[Transport Layer] Sequence Number: {seq_num}, Session Number: {session_number} Payload: {payload}, Checksum: {checksum}")
            payload_with_session_number = f"{session_number}|{payload}"
        except ValueError:
            print("[ERROR] Segment format is incorrect!")
            return None

        # Now you can return or further process the parsed parts
        return payload_with_session_number


    @staticmethod
    def calculate_checksum(data):
        """Generates a checksum to detect errors."""
        if isinstance(data, bytes):  # Convert bytes to string before processing
            data = data.decode()

        checksum = str(sum(ord(char) for char in data) % 256)
        print(f"\n[Transport Layer] Calculated checksum: {checksum}\n")  # ✅ Debug print
        return checksum

    def verify_checksum(self, segment):
        """Verifies the checksum of a received segment.""" 
        sequence_number, payload, checksum = segment.split("|")
        calculated_checksum = self.calculate_checksum(payload)
        if calculated_checksum == checksum:
            print(f"[Transport Layer] Checksum verified. Data is intact.")
            return payload
        else:
            print(f"[ERROR] Checksum mismatch! Data may be corrupted.")
            return None

    def handle_out_of_order_segments(self, received_sequence_number):
        """Handles out-of-order segments and retransmission requests."""
        if received_sequence_number != self.expected_sequence_number:
            print(f"[ERROR] Out of order segment. Expected: {self.expected_sequence_number}, Got: {received_sequence_number}")
            # Handle retransmission logic here
        else:
            self.expected_sequence_number += 1  # Move to the next expected sequence number
