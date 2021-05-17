import threading
import time
import argparse
import zmq
from monte_carlo.bitsource import bitsource
from monte_carlo.always_yes import always_yes
from monte_carlo.judge import judge
from monte_carlo.pythagoras import pythagoras
from monte_carlo.tally import tally


def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True
    thread.start()


def main(zcontext, arguments):
    if arguments.command == "bitsource":
        pubsub = "tcp://" + arguments.url + ":" + arguments.port
        print("Starting the bitsource service on: {}".format(pubsub))
        start_thread(bitsource.start, zcontext, pubsub)

    elif arguments.command == "always_yes":
        pubsub = "tcp://" + arguments.url + ":" + arguments.port
        pushpull = "tcp://" + arguments.dest + ":" + arguments.dport
        print("Always_yes service receiving data from: {}".format(pubsub))
        print("Sending data to {}".format(pushpull))
        start_thread(always_yes.start, zcontext, pubsub, pushpull)

    elif arguments.command == "judge":
        pubsub = "tcp://" + arguments.url + ":" + arguments.port
        pushpull = "tcp://" + arguments.dest + ":" + arguments.dport
        regrep = "tcp://" + arguments.pythagorasurl + ":" + arguments.pythagorasport
        print("Judge service receiving data from: {}".format(pubsub))
        print("talking to pythagoras service on: {}".format(regrep))
        print("sending data to: {}".format(pushpull))
        start_thread(judge.start, zcontext, pubsub, regrep, pushpull)

    elif arguments.command == "pythagoras":
        regrep = "tcp://" + arguments.url + ":" + arguments.port
        print("Starting the pythagoras service on: {}".format(regrep))
        start_thread(pythagoras.start, zcontext, regrep)

    else:
        pushpull = "tcp://" + arguments.url + ":" + arguments.port
        print("Starting Tally on: {}".format(pushpull))
        start_thread(tally.start, zcontext, pushpull)
    time.sleep(150)


def parsing_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="command", dest="command")
    bitsource_parser = subparsers.add_parser("bitsource")
    always_yes_parser = subparsers.add_parser("always_yes")
    judge_parser = subparsers.add_parser("judge")
    pythagoras_parser = subparsers.add_parser("pythagoras")
    tally_parser = subparsers.add_parser("tally")

    bitsource_parser.add_argument(
        "-u", "--url",
        help="url for the service to listen on (pubsub)"
    )
    bitsource_parser.add_argument(
        "-p", "--port",
        help="port for the service to listen on (pubsub)"
    )

    always_yes_parser.add_argument(
        "-u", "--url",
        help="url for the service to listen on (pubsub)"
    )
    always_yes_parser.add_argument(
        "-p", "--port",
        help="port for the service to listen on (pubsub)"
    )
    always_yes_parser.add_argument(
        "-d", "--dest",
        help="url to send the data to (pushpull)"
    )
    always_yes_parser.add_argument(
        "-dp", "--dport",
        help="destination port for the service to send data to (pushpull)"
    )

    judge_parser.add_argument(
        "-u", "--url",
        help="url for the service to listen on (pubsub)"
    )
    judge_parser.add_argument(
        "-p", "--port",
        help="port for the service to listen on (pubsub)"
    )
    judge_parser.add_argument(
        "-pu", "--pythagorasurl",
        help="url to connect to the pythagoras service (regrep)"
    )
    judge_parser.add_argument(
        "-pp", "--pythagorasport",
        help="port to connect to the pythagoras service (regrep)"
    )
    judge_parser.add_argument(
        "-d", "--dest",
        help="url to send the data to (pushpull)"
    )
    judge_parser.add_argument(
        "-dp", "--dport",
        help="destination port for the service to send data to (pushpull)"
    )

    pythagoras_parser.add_argument(
        "-u", "--url",
        help="url for the service to listen on (regrep)"
    )
    pythagoras_parser.add_argument(
        "-p", "--port",
        help="port for the service to listen on (regrep)"
    )

    tally_parser.add_argument(
        "-u", "--url",
        help="url for the service to listen on (pushpull)"
    )
    tally_parser.add_argument(
        "-p", "--port",
        help="port for the service to listen on (pushpull)"
    )
    arguments = parser.parse_args()
    return arguments


if __name__ == '__main__':
    arguments = parsing_arguments()
    print(arguments)
    main(zmq.Context(), arguments)
