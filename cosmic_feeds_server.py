import zmq
import time
import json

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://192.168.15.61:5559")

while True:
    message = "{'scripcode': 'AUDCHF.', 'ltp': 0.58751, 'ltq': 0.0, 'bid': 0.58747, 'bidqty': 0.0, 'ask': 0.58755, 'askqty': 0.0}"
    socket.send(json.dumps(message).encode('utf-8'))
    print(f"Sent: {message}")
    time.sleep(1)
