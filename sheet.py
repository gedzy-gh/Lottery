# Python imports
import logging

import pandas as pd

# Custom import
from config import Directory


# CSV class used to create a spreadsheet & save/update lottery data
class CSV:

    def __init__(self):

        # Set up csv sheet headers & columns
        self.header = ['Id', 'Date', 'Jackpot', 'Draw', 'Machine', 'Set',
                       'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'BB']

        self.column = {'Id': [], 'Date': [], 'Jackpot': [], 'Draw': [], 'Machine': [], 'Set': [],
                       'B1': [], 'B2': [], 'B3': [], 'B4': [], 'B5': [], 'B6': [], 'BB': []}

        # Were the lottery results will be held
        self.results = None

        # Class used for creating folders & files
        self.path = Directory('data', 'history.csv')

    def __enter__(self):

        # Logger object
        logging.getLogger('__main__.' + __name__)

        # Handle directories
        if self.path.is_folder() and not self.path.is_file():
            self.path.delete()

        if not self.path.is_folder():
            self.path.make()
            self.path.change()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Handle directory
        if not self.path.is_file():
            self.path.delete()

        return self

    # Using pandas modules write results to csv sheet
    def write(self):
        try:
            df = pd.DataFrame(data=self.results, columns=self.column)
            df.to_csv(self.path.file, index=False, header=True)
            tidy = df.sort_values(by='Id', ascending=True)
            df.update(tidy)
        except Exception as e:
            raise e

    # Using pandas modules append results to csv sheet
    def append(self, contents):
        try:
            sheet = self.read()
            value = sheet['Id'].max()
            ids = contents['Id']
            for index, key, in enumerate(ids):
                ids[index] = value + key
            sheet = pd.DataFrame(data=contents, columns=self.column)
            sheet.to_csv(self.path.file, mode='a', index=False, header=False)
        except Exception as e:
            raise e

    # Using pandas modules read csv sheet
    def read(self):
        try:
            sheet = pd.read_csv(self.path.file, engine='python')
            sheet = sheet.sort_values(by='Id', ascending=True)
            return sheet
        except Exception as e:
            raise e

    def draws(self):
        try:
            sheet = pd.read_csv(self.path.full, engine='python')
            sheet = sheet.sort_values(by='Id', ascending=True)
            sheet = sheet[['B1', 'B2', 'B3', 'B4', 'B5', 'B6']]
            transformation = [i for i in sheet.values.tolist()]
            return transformation
        except Exception as e:
            raise e

    # Using pandas modules get the last id number
    def last_id_number(self):
        try:
            sheet = pd.read_csv(self.path.file)
            sheet = sheet.sort_values(by='Id', ascending=True)
            value = sheet['Id'].max()
            del sheet
            return value
        except Exception as e:
            raise e

    # Using pandas modules get the last draw number
    def last_draw_number(self):
        try:
            sheet = pd.read_csv(self.path.file, index_col=0)
            order = sheet.sort_values(by='Draw', ascending=True)
            value = order['Draw'].max()
            del order
            return value
        except Exception as e:
            raise e


# Tell the user they have ran the wrong .py file
def main():
    print('Please run python main.py not' + __file__)
    exit(0)


# We've all seen this before :P
if __name__ == "__main__":
    main()
