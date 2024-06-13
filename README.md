**This code implements a simple chat application with a server and client written in Python**

**Client (ChatClient class):**

->        Connects to a server at a specified host and port **(default: localhost and port 5556)**.
->        Creates a separate thread to receive messages from the server.
->        Provides methods to send messages to the server and display received messages in a (GUI).
->        The GUI is built using the **tkinter library** and includes a chat area, an entry field for typing messages, and a send button.

**Server (ChatServer class):**

->        Listens for incoming connections on a specified host and port.
->        Maintains a list of connected clients.
->        Creates a separate thread to handle each connected client.
->        The client handling thread receives messages from the client, formats them with the client's address, broadcasts them to all connected clients (except the sender), and handles any errors that occur during communication.
