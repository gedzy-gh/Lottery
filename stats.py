from random import randint, choice
import matplotlib.pyplot as plt
import numpy as np

from sheet import CSV

import statistics

class HeatMap:

    def __init__(self, data=None):

        if data:
            self.data = data
        else:
            self.data = self.pool(10)

        self.pattern = []

        self.range = [range(1, 10),
                      range(10, 20),
                      range(20, 30),
                      range(30, 40),
                      range(40, 50),
                      range(50, 60)]

    # Generates a random lottery list
    @staticmethod
    def pool(size=10):

        def p():
            n, s = [i for i in range(1, 59)], [0] * 6
            for i in range(len(s)):
                s[i] = choice(n)
                n.pop(n.index(s[i]))
            yield sorted(s)

        r = []
        for i in range(1, size):
            r = p()

        return r

    @staticmethod
    def __group(l, r):

        def group(lis, ran):
            a = []
            for e in lis:
                if e in ran:
                    a.append(e)
            return a

        pg = []
        for i, v in enumerate(r):
            pg.append(group(l, v))

        pl = []
        t = [0] * len(pg)
        c = 1
        for i, v in enumerate(pg):
            s = len(v)
            t[i] = s
            if s > 1:
                if s != t[i - 1]:
                    c = 1
                for j in range(s):
                    pl.append(s * c)
                c += 1
            else:
                if s == 1:
                    pl.append(0)

        del pg, t, c
        return pl

    def simulate(self):
        for v in self.data:
            self.pattern.append(self.__group(v, self.range))
        return self.data, self.pattern

    @staticmethod
    def graph(data, height=1):

        d, p = data[0], data[1]

        row, col = len(d[len(d) - height:len(d)]) + 1, len(d[0]) + 1
        start1, end1 = len(d) - height, len(d)
        start2, end2 = len(p) - height, len(p)

        tit_rows = ['D' + str(i) for i in range(1, row)]
        tit_cols = ['B' + str(i) for i in range(1, col)]

        val = np.array(d[start1:end1])
        col_map_val = p[start2:end2]

        fig, axi = plt.subplots()

        map_name = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']
        axi.imshow(col_map_val, cmap='Wistia')

        # START

        lists = []
        for i in range(len(d[0])):
            lists.append([item[i] for item in d[start1:end1]])

        nlists = []
        for i in range(len(lists)):
            a = np.array(lists[i])
            counts = np.bincount(a)
            nlists.append(np.argmax(counts))

        slists = []
        for i in range(len(lists)):
            slists.append(round(statistics.mean(lists[i])))

        print('Popular =', sorted(nlists))
        print('Average =', sorted(slists))

        # We want to show all ticks...
        axi.set_xticks(np.arange(len(tit_cols)))
        axi.set_yticks(np.arange(len(tit_rows)))

        # ... and label them with the respective list entries
        axi.set_xticklabels(tit_cols)
        axi.set_yticklabels(tit_rows)

        # Loop over data dimensions and create text annotations.
        for i in range(len(tit_rows)):
            for j in range(len(tit_cols)):
                axi.text(j, i, val[i, j], ha="center", va="center", color="black")

        axi.set_title("Lottery Heat Map")
        plt.rcParamsOrig = ["figure.constrained_layout.use"]
        plt.show()


if __name__ == '__main__':
    path = '/home/gedzy/Documents/AG/Hobbies/Programming/Pycharm/TNL/data/history.csv'
    sheet = CSV()
    #esults = sheet.draws()
    #lottery = HeatMap(results)
    #results = lottery.simulate()
    #lottery.graph(results, height=len(results[0])) # len(results[0]))

    data = sheet.read()
    draws = data[['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'BB']]
    print(draws.mean())
