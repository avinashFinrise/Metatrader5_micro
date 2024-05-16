import zmq
import time

context = zmq.Context()

# SUB socket subscribes to messages
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://192.168.15.63:5599")
sub_socket.setsockopt(zmq.SUBSCRIBE, b"")

# Receive messages
for i in range(10):
    message = sub_socket.recv_string()
    print(f"Received: {message}")
