# Python imports
import logging
from time import time
from multiprocessing import Process, Queue

# Custom imports
from connect import Tor
from lottery import Lottery
from sheet import CSV


# Crawl domains directories & harvest results, then put results into a spreadsheet
def crawler():
    # Start a queue for each url and harvest results, return the results in a dictionary format
    def compute():

        # The pool returns results unordered, so we have used the tuple to force ordering later
        def worker(x, y):
            path = lottery.domain + url[x]
            contents = tor.get(path)

            data = []
            for title in spreadsheet.header[1:]:
                data.append((x + 1, lottery.craft(contents, title)))

            y.put(data)

        # Set up queuing
        queue = Queue()
        processes = [Process(target=worker, args=(i, queue)) for i in range(len(url))]
        log.info('Multiprocessing results')

        # Start processes
        for p in processes:
            p.start()

        # Join processes
        for p in processes:
            p.join()

        # Put results into an array
        results = [queue.get() for _ in processes]
        length = len(results)

        # Order results
        ordered = []
        for i in range(length):
            for j in results:
                if j[0][0] == i + 1:
                    ordered.append(j)
        del results

        # Put ordered results into a dictionary
        for i in range(len(ordered)):
            for j, k in enumerate(spreadsheet.column):
                if k == 'Id':
                    spreadsheet.column[k].append(ordered[i][0][0])
                else:
                    spreadsheet.column[k].append(ordered[i][j - 1][1])

        # Return array
        return spreadsheet.column

    # Logging module
    log = logging.getLogger('__main__.' + __name__)

    # Start time
    start = time()

    # Try to connect to tor service
    with Tor() as tor:
        log.info('Spoofing session')

        tor.change()
        log.info('Changed IP address to {}'.format(tor.ip()))

        lottery = Lottery()
        log.info('Crawling {}'.format(lottery.domain))

        # Returns html source code by given url
        html = tor.get(lottery.path)

        # Uses Beautiful Soup and returns draw numbers
        numbers = lottery.find(html, lottery.branch)

        # If we could not found any draw numbers, assume domain has updated
        if numbers is None:
            print('\n')
            raise ValueError('Domain has updated their website, script no longer works!')

        # Setup CSV sheet for saving results
        with CSV() as spreadsheet:

            # If previous results don't exist crawl domain
            if not spreadsheet.path.is_file():

                # Array that contains a list of found urls
                url = lottery.join(numbers, lottery.branch)
                log.info('Found {} draw numbers'.format(len(url)))

                # Pass the ordered results to a property
                spreadsheet.results = compute()

                spreadsheet.write()
                log.info('Results saved to {}'.format(spreadsheet.path.name[1]))

            else:

                # Open spreadsheet & get last draw number
                draw = spreadsheet.last_draw_number()

                # Return an array with new digits if greater than the draw number
                found = lottery.update(draw, numbers)

                # Statement to test if array not empty
                if found:
                    log.info('Checking draw numbers')

                    # Array that contains a list of new urls
                    url = lottery.join(found, lottery.branch)
                    log.info('Found {} draw numbers'.format(len(url)))

                    # Append results to spreadsheet
                    spreadsheet.append(compute())
                    log.info('Results appended to {}'.format(spreadsheet.path.name[1]))

                else:
                    log.info('Spreadsheet is up to date!')

    # End time
    end = time()
    log.info('Completed in {} seconds'.format(round(end - start, 2)))
    print('')


# Tell the user they have ran the wrong .py file
def main():
    print('Please run python main.py not ' + __file__)
    exit(0)


# We've all seen this before :P
if __name__ == "__main__":
    main()
