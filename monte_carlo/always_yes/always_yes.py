import zmq


def start(zcontext, in_url, out_url):
    print("starting always_yes")
    # socket for incoming data
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b'00')
    # socket for outgoing data
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    while True:
        isock.recv_string()
        # print("always yes received something")
        # print("always yes sending a yes")
        osock.send_string('Y')
