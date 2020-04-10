# Python imports
from re import compile, findall


class Lottery:

    # Target domain
    def __init__(self):

        self.domain = 'https://www.national-lottery.co.uk'
        self.branch = '/results/lotto/draw-history/draw-details/'
        self.path = 'https://www.national-lottery.co.uk/results/lotto/draw-history'

    # Searches relative url's for lotto draw numbers, if found return numbers in an array
    @staticmethod
    def find(soup, url):

        numbers = []
        html = soup.findAll('li')
        slash = compile(r'^.*')

        for li in html:
            found = li.findAll('a', attrs={'href': slash})
            for a in found:
                href = a['href']
                seen = findall(url, href)
                if seen:
                    numbers.append(int(href[-4:]))

        return sorted(set(numbers))

    # Will append draw numbers to the end of the url
    @staticmethod
    def join(number, url):
        path = []
        for i in range(len(number)):
            path.append(url + str(number[i]))
        return path

    # If the last draw number is less than the new numbers, add draw numbers to an array
    @staticmethod
    def update(last, number):
        draws = []
        for i in range(len(number)):
            if last < number[i]:
                draws.append(number[i])
        return draws

    # Function wrapper to extract & format wanted html data
    @staticmethod
    def craft(html, title):

        # Extract html text
        def at(tag, element, name):
            return html.find(tag, attrs={element: name})

        # Get html tag
        def find_tag(string, tag):
            return string.find(tag).text

        # Removes newlines & whitespaces
        def strip_string(s):
            rnl = s.text.replace('\n', '')
            rws = rnl.replace(' ', '')
            return rws

        # Removes strings but keeps numbers
        def strip_number(s):
            modified = ''
            for char in s:
                if char.isdigit():
                    modified += char
            return modified

        # Returns a string at any given length
        def at_string(s, c, i):
            return s.partition(c)[i]

        # Convert string to int
        def string_to_int(s):
            return int(s)

        # Used to get lottery date
        def date():
            data = at('div', 'id', 'section_header')
            return find_tag(data, 'h1')

        # Used to get jackpot
        def jackpot():
            data = at('p', 'id', 'game_header_intro')
            data = strip_string(data)
            data = int(strip_number(data))
            return data

        # Used to get draw numbers
        def draw():
            data = at('span', 'id', 'header_draw_number')
            data = strip_string(data)
            data = int(strip_number(data))
            return data

        # Used to get machine name
        def machine():
            data = at('span', 'id', 'header_draw_machine')
            data = strip_string(data)
            data = at_string(data, ':', 2)
            return data

        # Used to get ball_set
        def _set():
            data = at('span', 'id', 'header_ball_set')
            data = strip_string(data)
            data = at_string(data, ':', 2)
            data = string_to_int(data)
            return data

        # Used to get lotto balls
        def ball():
            data = at('ol', 'class', 'draw_numbers_list clr')
            data = strip_string(data)
            data = str(strip_number(data))
            data = [i + j for i, j in zip(data[::2], data[1::2])]
            data = list(map(int, data))
            return data

        if title == 'Date':
            return date()
        elif title == 'Jackpot':
            return jackpot()
        elif title == 'Draw':
            return draw()
        elif title == 'Machine':
            return machine()
        elif title == 'Set':
            return _set()
        elif title == 'B1':
            return ball()[0]
        elif title == 'B2':
            return ball()[1]
        elif title == 'B3':
            return ball()[2]
        elif title == 'B4':
            return ball()[3]
        elif title == 'B5':
            return ball()[4]
        elif title == 'B6':
            return ball()[5]
        elif title == 'BB':
            return ball()[6]


# Tell the user they have ran the wrong .py file
def main():
    print('Please run python main.py not' + __file__)
    exit(0)


# We've all seen this before :P
if __name__ == "__main__":
    main()
