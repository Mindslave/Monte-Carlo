import time
import random
import zmq
B = 32


def start(zcontext, url):
    print("Starting Bitsource Server")
    zsock = zcontext.socket(zmq.PUB)
    zsock.bind(url)
    while True:
        zsock.send_string(ones_and_zeros(B * 2))
        time.sleep(0.01)


def ones_and_zeros(digits):
    return bin(random.getrandbits(digits)).lstrip('0b').zfill(digits)
