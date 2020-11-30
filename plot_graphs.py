from get_graphs import get_data_params, plot_graphs, get_params
import pandas as pd
import sys
from os import listdir

sys.tracebacklimit = 0


def plot_save(directory: str):
    DF = pd.read_excel(io=directory)
    start, names, height = get_params(DF)

    for i in range(3, len(DF)):

        x, y, colors, title, sub_title = get_data_params(directory, i, start)
        file_name = names[i-3]+'.png'
        plot_graphs(x, y, colors, title, sub_title, file_name, width=1200, height=height)


direc = input('Enter path to your data:')
if '.xls' == direc[-4:]:
    plot_save(direc)

else:
    files = listdir(direc)
    for file in files:
        if '.xls' == file[-4:]:
            print('Plotting for ' + file)
            plot_save(direc+'/'+file)