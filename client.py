import zmq
import time
context = zmq.Context()
try:
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.15.61:5559")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
except Exception as e :
    print(e)

while True:
    print("----------------------")
    message = socket.recv()
    print(f"Received: {message}")
    time.sleep(1)
