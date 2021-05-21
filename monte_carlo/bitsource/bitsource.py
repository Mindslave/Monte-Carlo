import time
import random
import zmq
B = 32


def start(zcontext, url, listen_client_url):
    print("Starting Bitsource Server")
    isock = zcontext.socket(zmq.PULL)
    isock.bind(listen_client_url)
    # first we wait to receive the number of data points from the client
    while True:
        print("Waiting for data points from client on: " + listen_client_url)
        data_points = isock.recv_string()
        print("Received data from client: " + data_points)
        break
    isock.close()

    zsock = zcontext.socket(zmq.PUB)
    zsock.bind(url)
    try:
        for i in range(int(data_points)):
            zsock.send_string(ones_and_zeros(int(B) * 2))
            print("sending: " + str(ones_and_zeros(int(B) * 2)))
            time.sleep(0.01)
    except ValueError:
        print("Please enter a valid integer value for the number of data points")
        exit(1)


def ones_and_zeros(data_points):
    return bin(random.getrandbits(int(data_points))).lstrip('0b').zfill(int(data_points))
