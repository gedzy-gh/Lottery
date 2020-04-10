# Python imports
# coding: utf-8
import logging
from os import name, path
from socket import setdefaulttimeout, socket, AF_INET, SOCK_STREAM
from sys import hexversion

# Custom imports
from worker import crawler


# Main function
def main():
    log.info('Requirements passed!')

    # Begin crawl
    crawler()
    exit(0)


# Function used to check scripts conditions, if true execute main() function
def check():
    # Check python version
    def version():
        if hexversion < 34017776:
            return False
        else:
            return True

    # Check os version
    def os():
        if name != 'posix':
            return False
        else:
            return True

    # Check internet connection
    def online(host='8.8.8.8', port=53, timeout=3):
        try:
            setdefaulttimeout(timeout)
            socket(AF_INET, SOCK_STREAM).connect((host, port))
            return True
        except OSError:
            return False

    # Check tor exist
    def binary():
        if path.isfile('/usr/bin/tor'):
            return True
        else:
            return False

    # Print message to logger object
    if not os():
        log.critical('Python script only runs on Windows.')
    if not version():
        log.critical('Python interpreter out of date.')
    if not online():
        log.critical('Python script requires an internet connection.')
    if not binary():
        log.critical('Python script wants Tor to be installed.')

    # Hold boolean elements in array
    b = [os(), version(), online(), binary()]

    # Quit if any elements is false
    if all(a for a in b):
        return True
    else:
        return False


if __name__ == '__main__':

    # Create & configure main logger
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)

    # Create console handler with a higher log level
    hand = logging.StreamHandler()
    hand.setLevel(logging.INFO)

    # Create formatter & add it to the handler
    # '%(asctime)s' - '%(name)s' - '%(levelname)s' - '%(message)s'
    form = logging.Formatter('  ▪ %(message)s')
    hand.setFormatter(form)

    # Add the handler to the logger
    log.addHandler(hand)

    print('')

    if check():
        main()

    print('')

    exit(1)
