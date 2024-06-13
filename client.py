import threading
import tkinter as tk
from tkinter import scrolledtext
import socket

class ChatClient:
    def _init_(self, gui, host='127.0.0.1', port=5556):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        try:
            self.client.connect((host, port))
            self.connected = True
            print(f'Connected to server at {host}:{port}')
        except Exception as e:
            print(f'Failed to connect to server: {e}')
            return
        
        self.gui = gui
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    self.gui.display_message(message)
            except Exception as e:
                print(f'Disconnected from server: {e}')
                self.connected = False
                self.client.close()
                break

    def send_message(self, message):
        if not self.connected:
            print("Not connected to server.")
            return
        try:
            self.client.send(message.encode('utf-8'))
        except Exception as e:
            print(f'Failed to send message: {e}')
            self.connected = False
            self.client.close()

    def disconnect(self):
        if self.connected:
            try:
                self.client.close()
            except Exception as e:
                print(f'Error closing connection: {e}')
            finally:
                self.connected = False
                print("Disconnected from server.")

class ChatGUI:
    def _init_(self):
        self.client = ChatClient(self)

        self.root = tk.Tk()
        self.root.title("Chat Application")

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        self.entry_field = tk.Entry(self.root)
        self.entry_field.pack(padx=20, pady=5, fill=tk.X, expand=False)
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def display_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        message = self.entry_field.get()
        self.client.send_message(message)
        self.entry_field.delete(0, tk.END)

    def on_closing(self):
        self.client.disconnect()
        self.root.destroy()

def start_gui():
    chat_gui = ChatGUI()
    chat_gui.root.mainloop()

if _name_ == "_main_":
    threading.Thread(target=start_gui).start()