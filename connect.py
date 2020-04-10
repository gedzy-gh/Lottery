# Python imports
import logging
from random import sample, randint, choice
from string import ascii_uppercase, digits
from time import sleep

# Subprocess imports
from subprocess import Popen, PIPE

# Session imports
from bs4 import BeautifulSoup
from fua import Desktop
from requests import Session, ConnectionError
# Stem imports
from stem import Signal
from stem import SocketError
from stem.control import Controller

# Custom imports
from config import Directory


# Can start a Tor process from a torrc file & send requests over a network using session/stem modules
class Tor:

    def __init__(self):

        # Hash string from tor
        self.hash = None

        # Subprocess object
        self.process = None

        # Session object
        self.session = None

        # Random string password
        self.password = self.__generate()

        # Class used for creating folders & files
        self.path = Directory('tor', 'torrc')

    def __enter__(self):

        # Logger object
        self.log = logging.getLogger('__main__.' + __name__)

        # Handle directories
        if self.path.is_folder():
            self.path.delete()

        if not self.path.is_folder():
            self.path.make()
            self.path.change()

            # Get our hash password from tor
            p = Popen(['tor', '--hash-password', self.password], stdout=PIPE)

            with p.stdout:
                stdout = p.communicate()[0]
                self.hash = stdout.decode('ascii')

            # Write a simple torrc file
            with open(self.path.name[1], 'w+') as file:
                file.write('ControlPort 9051' + '\n')
                file.write('HashedControlPassword ' + self.hash)

            self.log.info('Created custom torrc file')

        # Start tor using subprocess module
        p = Popen(['tor', '-f', self.path.name[1]], stdout=PIPE)

        # Read stdout to check if tor successfully started or not
        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                if b'Done' in line:
                    success = True
                    break
                if b'err' in line:
                    success = False
                    break

        # If tor process fails to start raise error, else continue
        if not success:
            raise ValueError('Could not start tor service')
        else:
            self.log.info('Started tor service')
            self.process = p

        # Wait a little
        sleep(7)

        # Spoof session
        self.session = Session()
        self.session.proxies.update(self.__proxy())
        self.session.headers.update(self.__header())

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Handle directory
        self.path.delete()

        # Finally kill the tor process
        self.process.terminate()
        self.process.kill()

        self.log.info('Stopped tor service')

    def change(self):
        try:
            self.log.info('Communicating with stem module')
            with Controller.from_port(port=9051) as control:
                control.authenticate(password=self.password)
                control.signal(Signal.NEWNYM)
                if not control.is_newnym_available():
                    sleep(control.get_newnym_wait())
        except (SocketError, ImportError, Exception) as e:
            print('\n')
            raise e

    def get(self, url):
        try:
            # Using Session module with proxy (socks5) & fake agent
            with self.session as connection:
                # Return urls html source code
                response = connection.request('GET', url).content
                # Beautify html with Soup
                response = BeautifulSoup(response, 'lxml')
            return response
        except (ConnectionError, ImportError, Exception) as e:
            print(e, '\n')
            raise e

    def ip(self):
        try:
            # Using Session() with proxy (socks5) & fake agent
            with self.session as connection:
                # Return urls html source code
                response = connection.request('GET', 'http://ip.42.pl/raw').content
            # Return ip as string
            return response.decode('ascii')
        except (ConnectionError, ImportError, Exception) as e:
            print('\n')
            raise e

    # Returns random characters by given length
    @staticmethod
    def __generate():
        return ''.join(sample(ascii_uppercase + digits, k=randint(8, 16)))

    # Returns a dictionary, used with Session module
    @staticmethod
    def __proxy():
        sock = 'socks5h://' + 'localhost' + ':' + '9050'
        return {'http': sock, 'https': sock}

    # Generates a random agent
    @staticmethod
    def __header():

        win = Desktop.Windows()
        win = [win.SeaMonkey(), win.Opera(), win.Firefox(), win.Chrome(), win.Edge(), win.IE(), win.Saffari()]

        mac = Desktop.macOS()
        mac = [mac.Camino(), mac.Chrome(), mac.Firefox(), mac.Opera(), mac.SeaMonkey()]

        lin = Desktop.Linux()
        lin = [lin.Chrome(), lin.Firefox(), lin.Opera(), lin.SeaMonkey()]

        uni = Desktop.Unix()
        uni = [uni.Opera(), uni.Chrome(), uni.Surf()]

        goo = Desktop.Google_Chrome()
        goo = [goo.Firefox(), goo.Chrome()]

        bsd = Desktop.FreeBSD()
        bsd = [bsd.Chrome(), bsd.Firefox(), bsd.Opera()]

        # Using choice for randomization
        users = [choice(win), choice(mac), choice(lin), choice(uni), choice(goo), choice(bsd)]

        # Delete unwanted variables
        del win, mac, lin, uni, goo, bsd

        # Random agent returns as a dictionary
        return {'User-Agent': users[randint(0, len(users)-1)]}


# Tell the user they have ran the wrong .py file
def main():
    print('Please run python main.py not' + __file__)
    exit(0)


# We've all seen this before :P
if __name__ == "__main__":
    main()
