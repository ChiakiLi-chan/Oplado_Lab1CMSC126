import base64
import zlib

class PresentationLayer:
    def __init__(self):
        """Handles data transformation before transmission."""
        self.shift_key = 3  # Used for simple encryption

    def encode_data(self, data):
        """Compresses and encodes data for transmission."""
        print(f"[DEBUG] Original data before encoding: {data}")

        if isinstance(data, str):  
            data = data.encode("utf-8")  # Convert string to bytes if necessary

        compressed = zlib.compress(data)  # Compress (handles bytes directly)
        print(f"[DEBUG] Compressed data: {compressed}")

        encoded = base64.b64encode(compressed).decode("utf-8")  # Encode to base64
        print(f"[DEBUG] Encoded data (Base64 string): {encoded}")

        return encoded

    def decode_data(self, encoded_data):
        """Decodes and decompresses data from the presentation layer."""
        print(f"[DEBUG] Encoded data before decoding: {encoded_data}")

        try:
            # Decode the base64-encoded data
            decoded_data = base64.b64decode(encoded_data)  # Decode from base64 (raw bytes)
            print(f"[DEBUG] Decoded Base64 (raw bytes): {decoded_data}")

            # Attempt to decompress the data using zlib
            decompressed_data = zlib.decompress(decoded_data)  # Decompress (returns bytes)
            print(f"[DEBUG] Decompressed data: {decompressed_data}")

            # Convert the decompressed data back into a string (assuming UTF-8 encoding)
            decoded_text = decompressed_data.decode("utf-8")
            print(f"[DEBUG] Final decoded text: {decoded_text}")

            return decoded_text

        except zlib.error as e:
            print(f"[ERROR] Zlib decompression error: {e}")
            return None
        except UnicodeDecodeError as e:
            print(f"[ERROR] Unicode decode error: {e}")
            return None
        except Exception as e:
            print(f"[ERROR] General decoding error: {e}")
            return None

    def caesar_cipher_encrypt(self, text):
        """Encrypts text using a Caesar cipher."""
        if isinstance(text, bytes):  # Convert bytes to string before processing
            text = text.decode()

        return ''.join(chr((ord(c) + self.shift_key) % 256) for c in text)

    def caesar_cipher_decrypt(self, text):
        """Decrypts a Caesar cipher encrypted text."""
        if isinstance(text, bytes):  # Convert bytes to string before processing
            text = text.decode()

        return ''.join(chr((ord(c) - self.shift_key) % 256) for c in text)

    def run_length_encode(self, data):
        """Simple Run Length Encoding (RLE) compression."""
        encoded = []
        i = 0
        while i < len(data):
            count = 1
            while i + 1 < len(data) and data[i] == data[i + 1]:
                i += 1
                count += 1
            encoded.append(f"{data[i]}{count}")
            i += 1
        return ''.join(encoded)

    def run_length_decode(self, data):
        """Decompresses RLE encoded data."""
        decoded = []
        i = 0
        while i < len(data):
            char = data[i]
            count = int(data[i + 1])
            decoded.append(char * count)
            i += 2
        return ''.join(decoded)
