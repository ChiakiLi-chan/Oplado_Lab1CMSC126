These files simulates  a simplified OSI model using Python. As required, the data moves through all seven layers to simulate real-world network communication with the following processes:
=Physical Layer: Simulated using Python sockets and bit-level operations.
=Data Link Layer: Implements a MAC addressing system and frame transmission.
=Network Layer: Simulates IP addressing and packet routing.
=Transport Layer: Implements TCP-like packet sequencing and error handling.
=Session Layer: Manages connection states and synchronization.
=Presentation Layer: Handles encryption, compression, and encoding.
=Application Layer: Implements HTTP-like request-response communication.

The project has also been accomplished with the following constraints:
-No use of existing network libraries (no Flask, Django, FastAPI, or requests).
-Must use only low-level Python features (e.g., socket, struct, pickle, json).
-Must correctly simulate all seven OSI layers.
-Must use dynamic IP and MAC addressing

Please run main.py and it will simulate the OSI model and the data that passes through each layer is printed in the console.
