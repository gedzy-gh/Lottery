import pandas as pd
import numpy as np
import statistics


class Analysis:

    def __init__(self, path):
        self.file = path

    def sheet(self):
        sheet = pd.read_csv(self.file, engine='python')
        return sheet

    def draws(self):
        sheet = self.sheet()
        sheet = sheet.sort_values(by='Id', ascending=True)
        sheet = sheet[['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'BB']]
        return sheet

    def average(self):
        sheet = self.draws()
        c1, c2 = sheet.columns[:-1], sheet.columns[-1]
        l1, l2 = [round(sheet[n].mean()) for n in c1], [round(sheet[c2].mean())],
        l1, l2 = [int(i) for i in l1], [int(i) for i in l2]
        return sorted(l1) + l2

    def popular(self, opt=0):
        sheet = self.draws()
        c1, c2 = sheet.columns[:-1], sheet.columns[-1]
        l1, l2 = [sheet[name].mode() for name in c1], [round(sheet[c2].mean())]
        print(list(l1))
        exit()
        #print(list(l1))
        #l3 = list(sorted(l1) + l2)
        #if opt == 0:
        #    return l3
        #elif opt == 1:
        #    #return sorted([max(set(i), key=l3.count) for i in sorted(l3)])


def main():
    f = '/home/gedzy/Documents/AG/Hobbies/Programming/Pycharm/TNL/data/history.csv'
    lotto = Analysis(f)
    lotto.popular(1)
    lotto.average()


if __name__ == '__main__':
    main()
