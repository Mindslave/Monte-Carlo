import zmq
B = 32


def start(zcontext, in_url, pythagoras_url, out_url):
    print("Starting judge")
    # socket to connect to bitsource service
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    for prefix in b'01', b'10', b'11':
        isock.setsockopt(zmq.SUBSCRIBE, prefix)

    # socket to connect to pythagoras service
    psock = zcontext.socket(zmq.REQ)
    psock.connect(pythagoras_url)

    # socket to connect to tally (client)
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)

    unit = 2 ** (B * 2)  # 2^64-1
    while True:
        bits = isock.recv_string()
        print("Received: " + bits)
        n, m = int(bits[::2], 2), int(bits[1::2], 2)
        psock.send_json((n, m))
        sumsquares = psock.recv_json()
        if sumsquares < unit:
            print("Sending Yes")
            osock.send_string('Y')
        else:
            print("Sending No")
            osock.send_string('N')
