import argparse
import sys
from os import listdir
import datetime
import pandas as pd

from get_graphs import get_data_params, get_params, plot_graphs

parser = argparse.ArgumentParser(
    add_help=True,
    description="You can pass directory to specific xls file or to "
    "directory where xls data is stored. "
    "If not provided in file, "
    "program will ask for filename for png files. ",
)

parser.add_argument("directory", type=str, help="Directory where xls data is stored")
# display help if only program name is passed
parser.parse_args(args=None if sys.argv[1:] else ["--help"])

args = parser.parse_args()

sys.tracebacklimit = 0


def plot_save(directory: str):
    """Function for plotting and saving graphs.

    :param directory: directory to xls data
    :type directory: str
    """
    df = pd.read_excel(io=directory)  # reading xls data
    start, names, height = get_params(df)  # getting specification on how to read data
    # names for files to save later and height of graphs in pixels

    for i in range(3, len(df)):
        # getting proper data for plotting
        x, y, colors, title = get_data_params(directory, i, start)
        file_name = names[i - 3]
        plot_graphs(x, y, colors, title, file_name, width=1200, height=height)

a1 = datetime.datetime.now()
direc = args.directory
# if it's path for specific xls file
if ".xls" == direc[-4:]:
    plot_save(direc)
# if it's path to directory where xls files are stored
else:
    files = listdir(direc)
    for file in files:
        if ".xls" == file[-4:]:
            print("Plotting for " + file)
            plot_save(direc + "/" + file)


a2 = datetime.datetime.now()
print((a2-a1).total_seconds())