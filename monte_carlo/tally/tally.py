import zmq


def start(zcontext, url, client_url):
    print("Starting Tally")
    zsock = zcontext.socket(zmq.PULL)
    zsock.bind(url)

    osock = zcontext.socket(zmq.PUSH)
    osock.connect(client_url)

    p = q = 0
    while True:
        decision = zsock.recv_string()
        # print("Tally received: " + decision)
        q += 1
        if decision == 'Y':
            p += 4
        # now we need to send the data to the client, instead of printing them
        # print(decision, p, q, p / q)
        result = p / q
        osock.send_string(str(result))
