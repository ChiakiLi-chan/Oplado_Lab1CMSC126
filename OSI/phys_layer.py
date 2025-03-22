class PhysicalLayer:
    def __init__(self):
        """Simulates a physical layer without real network communication."""
        print("[Physical Layer] Initialized.")

    def send(self, data):
        """Simulates sending binary data."""
        binary_data = self.text_to_binary(data)
        print(f"[Physical Layer] Transmitting raw data: {binary_data}")
        return binary_data  # Return to simulate transmission

    def receive(self, binary_data):
        """Simulates receiving binary data."""
        text_data = self.binary_to_text(binary_data)
        print(f"[Physical Layer] Received and decoded data: {text_data}")
        return text_data  # Return to simulate reception

    @staticmethod
    def text_to_binary(text):
        """Ensures the input is a string before converting to binary."""
        if isinstance(text, bytes):
            text = text.decode()  # Decode bytes to string
        elif not isinstance(text, str):
            text = str(text)  # Convert non-string to string

        return ' '.join(format(ord(c), '08b') for c in text)

    @staticmethod
    def binary_to_text(binary_data):
        """Decodes binary data back to text."""
        try:
            # Split the binary data into 8-bit chunks
            byte_data = binary_data.split()

            # Ensure each chunk is 8 bits, and convert each chunk to a character
            return ''.join(chr(int(b, 2)) for b in byte_data if len(b) == 8)
        except ValueError as e:
            print(f"[ERROR] Invalid binary data: {e}")
            return ""
