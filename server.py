import bluetooth
import time
import re
def main(q):
    import uuid

    print("Server.py started")
    bt_mac = str(':'.join(re.findall('..', '%012x' % uuid.getnode())).encode())

    # formatting address
    bt_mac = bt_mac[1:]
    bt_mac = bt_mac.replace("'", "")

    # Initial Setup for Bluetooth, creating a socket, and binding to a Bluetooth adapter
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_socket.bind((bt_mac, bluetooth.PORT_ANY))
    server_socket.listen(1)

    # UUID is just an identifier for Bluetooth connection
    uuid = "00001101-0000-1000-8000-00805F9B34FB"  # SPP
    bluetooth.advertise_service(server_socket, "SampleServerL2CAP", service_id=uuid, service_classes=[uuid])

    while True:
        print("Waiting for incoming connection...")
        ## pipe.send_message('Waiting for incoming connection...')
        q.put("Waiting for incoming connection...")
        time.sleep(4)
        ## pipe.send_message("Mannn this connection takin so long")
        q.put("Mannn this connection takin so long")
        time.sleep(4)

        q.put("4")
        time.sleep(3)
        ## pipe.send_message("bruh")

    server_socket.close()
