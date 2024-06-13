import socket
import threading

class ChatServer:
    def _init_(self, host='127.0.0.1', port=5556):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        print(f'Server started on {host}:{port}')
    
    def broadcast(self, message, sender_socket):
        clients_to_remove = []
        for client_socket in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(message)
                except Exception as e:
                    print(f"Error sending message to {client_socket}: {e}")
                    clients_to_remove.append(client_socket)

        for client_socket in clients_to_remove:
            try:
                self.clients.remove(client_socket)
            except ValueError:
                pass

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                message = client_socket.recv(1024)
                if message:
                    formatted_message = f"{client_address}: {message.decode('utf-8')}".encode('utf-8')
                    print(f'Received: {formatted_message.decode("utf-8")}')
                    self.broadcast(formatted_message, client_socket)
            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def run(self):
        while True:
            client_socket, client_address = self.server.accept()
            print(f'New connection from {client_address}')
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if _name_ == "_main_":
    chat_server = ChatServer()
    chat_server.run()