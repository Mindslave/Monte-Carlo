import zmq
#import matplotlib.pyplot as plt
import termplotlib as tpl


def start(zcontext, client_url, bitsource_url):
    # socket to communite with bitsource
    # I choose this socket because
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(bitsource_url)

    # listening socket to communicate with tally
    # I choose this socket because we need to constantly
    # listen for new data updates from tally
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
        fig.plot(num_of_it, pi_values, width=75, height=20)
        fig.show()
