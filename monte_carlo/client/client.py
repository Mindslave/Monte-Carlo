import zmq
#import matplotlib.pyplot as plt
import termplotlib as tpl


def start(zcontext, client_url, bitsource_url):
    # I choose PUSH and PULL sockets because PUBSUB doesn't seem reasonalby
    # since we are not communicating with multiple other services at the
    # same time and REQ/REP doesn't seem reasonably because we do not need
    # to respond to tally neither does the bitsource need to response to us.
    # So PUSH PULL was the only method that I couldn't find an argument against

    # socket to communite with bitsource
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(bitsource_url)

    # listening socket to communicate with tally
    isock = zcontext.socket(zmq.PULL)
    isock.bind(client_url)

    # We only need to send the data to the bitsource once
    value = input("Enter the number of data points: ")
    osock.send_string(value)

    # After this intilization we expect to receive data from tally
    i = 00
    num_of_it = []
    pi_values = []
    while True:
        data = isock.recv_string()
        i += 1
        num_of_it.append(i)
        pi_values.append(float(data))
        print(float(data))
        fig = tpl.figure()
        fig.plot(num_of_it, pi_values, width=75, height=25)
        fig.show()
