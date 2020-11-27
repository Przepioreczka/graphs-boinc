from get_graphs import get_data_params, plot_graphs
import pandas as pd
import sys
sys.tracebacklimit = 0
direc = input('Enter path to your data:')
# direc = '/home/przepioreczka/graphs-boinc/wykresy1.xls'
DF = pd.read_excel(io=direc)
count = list(range(3, len(DF)))
bars = DF.shape[1]-3
height = bars * 100
name = input('Enter name for your graphs:')

for i in count:
    x, y, colors, title, sub_title = get_data_params(direc, i)
    plot_graphs(x, y, colors, title, sub_title, name+str(i)+'.png', width=1200, height=height)
