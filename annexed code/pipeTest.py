# example of using a duplex pipe between processes
from time import sleep
from random import random
from multiprocessing import Process
from multiprocessing import Pipe


# generate and send a value
def generate_send(connection, value, name):
    # generate value
    new_value = random()
    # block
    sleep(new_value)
    # update value
    value = value + new_value
    # report
    print(f'>sending {value} from {name}', flush=True)
    # send value
    connection.send(value)


# ping pong between processes
def pingpong(connection, send_first, name):
    print('Process Running', flush=True)
    # check if this process should seed the process
    if send_first:
        generate_send(connection, 0, name)
    # run until limit reached
    while True:
        # read a value
        value = connection.recv()
        # report
        print(f'>received {value} by {name}', flush=True)
        # send the value back
        generate_send(connection, value, name)
        # check for stop
        if value == 'CLOSE':
            break
    print('Process Done', flush=True)


# entry point
if __name__ == '__main__':
    # create the pipe
    conn1, conn2 = Pipe(duplex=True)
    # create players
    player1 = Process(target=pingpong, args=(conn1, True, 'player1'))
    player2 = Process(target=pingpong, args=(conn2, False, 'player2'))
    # start players
    player1.start()
    player2.start()
    # wait for players to finish
    player1.join()
    player2.join()