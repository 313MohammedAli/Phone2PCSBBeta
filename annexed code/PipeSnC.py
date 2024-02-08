'''
This class will be passed to server.py and gui.py to organize the pipe connections
This should make it easier to debug and increase over code readibility

SnC = Server and Client
'''
import time

import win32pipe
import win32file
import threading

class PipeSnC:
    def __init__(self, pipe_name):
        self.pipe_name = r'\\.\pipe\{}'.format(pipe_name)
        self.pipe_handle = None
        self.connected = False

    def create_server(self):
        try:
            self.pipe_handle = win32pipe.CreateNamedPipe(
                self.pipe_name,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                1, 65536, 65536,
                0,
                None
            )
        except Exception as e:
            print(f"Could not create server: {e}\n")
    def connect_to_client(self):
        try:
            win32pipe.ConnectNamedPipe(self.pipe_handle, None)
            self.connected = True
            print(f"Client connected to pipe handle: {self.pipe_handle}")
        except Exception as e:
            print(f"Coud not connect to client: {e}")

    def connect_to_server(self):
        try:
            self.pipe_handle = win32file.CreateFile(
                self.pipe_name,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            self.connected = True
            print(f"Server connected to pipe handle: {self.pipe_handle}")
        except Exception as e:
            print(f"Failed to connect to the pipe: {e}")
            self.connected = False

    def send_message(self, message):
        try:

            if self.connected:
                print(f"Sending message: {message}")
                try:
                    result, _ = win32file.WriteFile(self.pipe_handle, message.encode())
                    print(f"Successfully sent message: {message}")
                except Exception as e:
                    print(f"Could not write to pipe: {e}")
                if result != 0:
                    print(f"Failed to send message, WriteFile returned {result}")
        except Exception as e:
            print(f"Could not send message: {e}")

    def receive_message(self):
        try:
            if self.connected:
                result, data = win32file.ReadFile(self.pipe_handle, 4096)
                if result == 0:
                    return data.decode()
                else:
                    print(f"Failed to read message, ReadFile returned {result}")
            return None
        except Exception as e:
            print(f"Could not receive messages: {e}")
            time.sleep(1)

    def close_pipe(self):
        try:
            if self.connected:
                win32file.CloseHandle(self.pipe_handle)
                self.connected = False
        except Exception as e:
            print(f"Could not close pipe: {e}")
    def start_receiving(self, callback):
        print("Start receiving initialized")
        def receive_thread():
            print("received_thread function on right now\n")
            while self.connected:
                try:
                    message = self.receive_message()
                    print(f"Message Received: {message}")
                except Exception as e:
                    print(f"Could not receive message: {e}")
                    time.sleep(1)
                try:
                    if message is not None:
                        callback(message)
                except Exception as e:
                    print(f"Callback failed: {e}")

        try:
            self.receive_thread = threading.Thread(target=receive_thread)
            self.receive_thread.start()
        except Exception as e:
            print(f"Could not start thread for receiving messages: {e}")

