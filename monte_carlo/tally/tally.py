import zmq


def start(zcontext, url):
    print("Starting Tally")
    zsock = zcontext.socket(zmq.PULL)
    zsock.bind(url)
    p = q = 0
    while True:
        decision = zsock.recv_string()
        # print("Tally received: " + decision)
        q += 1
        if decision == 'Y':
            p += 4
        print(decision, p, q, p / q)
