import argparse
import sys
from os import listdir

from get_graphs import compare_plot, multiple_save

parser = argparse.ArgumentParser(
    add_help=True,
    description="You can pass directory to specific xls file or to "
    "directory where xls data is stored. "
    "If not provided in file, "
    "program will ask for filename for png files. \n"
    "\nDo not mix normal data with comparison or overlay data "
                "while specifying directory.",
)

parser.add_argument("directory", type=str, help="directory where xls data is stored")
parser.add_argument("--compare", help="plot comparison bar", action="store_true")
parser.add_argument("--overlay", help="plot overlay bar", action="store_true")

# display help if only program name is passed
parser.parse_args(args=None if sys.argv[1:] else ["--help"])

args = parser.parse_args()

# Print only the exception type and value
sys.tracebacklimit = 0
direc = args.directory

fun = multiple_save
if args.compare:
    fun = compare_plot

# if it's path for specific xls file
if ".xls" == direc[-4:]:
    fun(direc, args.overlay)

# if it's path to directory where xls files are stored
else:
    files = listdir(direc)
    for file in files:
        if ".xls" == file[-4:]:
            print("Plotting for " + file)
            fun(direc + file, args.overlay)
