import zmq


def start(zcontext, bitsource_url, tally_url):
    # socket to communite with bitsource
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(bitsource_url)

    # socket to communicate with tally
    isock = zcontext.socket(zmq.PULL)
    isock.connect(tally_url)

    value = input("Enter the number of data points: ")
    osock.send(value)
    while True:
        isock.recv_string()
