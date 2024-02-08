# This file is used to handle the pipe hahaha. That's why I called it shawty
# because then I can say 'yeah, shawty handles the pipe' ohhh I am such a goober
# anyway this is like my 7th iteration of the pipe logic BUT hopefully the last

# USAGE
# in class you want to use it in (server.py and gui.py in my case)
# gui.py
# conn1 = Pipe(duplex=True)
# pipe = PingPong(conn1, true, gui)
# pipe.start()
#
# server.py
# conn2 = Pipe(duplex=True)
# pipe = PingPong(conn2, false, server)
# pipe.start()

from time import sleep
from multiprocessing import Process

class PingPong:
    def __init__(self, connection, send_first, name):
        self.connection = connection
        self.send_first = send_first
        self.name = name
        self.message = ''

    def generate_send(self, value):
        # Block
        sleep(.5)
        # Report
        print(f'>sending {value} from {self.name}', flush=True)
        # Send value
        try:
            self.connection.send(value)
        except Exception as e:
            print(f"Could not send message ({value})\n{e}")

    def pingpong(self):
        print(f'Process {self.name} Running', flush=True)
        # Check if this process should seed the process
        if self.send_first:
            self.generate_send(0)
        # Run until limit reached
        while True:
            # Read a value
            value = self.connection.recv()
            if value != 'IDLE':
                # Report
                print(f'>received {value} by {self.name}', flush=True)
                # update actual message
                self.message = value
                # Check for stop
                if value == 'CLOSE':
                    break
            # send IDLE message
            self.generate_send('IDLE')

        print(f'Process {self.name} Done', flush=True)

    def get_message(self):
        return self.message

    def start(self):
        # Create player
        player = Process(target=self.pingpong)
        # Start player
        player.start()
        # Wait for player to finish
        player.join()

