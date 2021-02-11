import pandas as pd
from typing import List
import numpy as np
from get_graphs import plot_graphs
import datetime


class DataPlotly(pd.DataFrame):

    def __init__(
            self,
            data=None,
    ):
        super().__init__(data)
        self.start: int = 0
        self.file_names = None
        self.height: int = 0
        self.title: str = ''
        self.asc: bool = True
        self.number = 0
        self.find_beginning()
        self.get_height()
        self.get_names()

    def find_beginning(self) -> int:
        """Function for finding beginning of data series (from which column data starts)

        :return: start column (4th column or 3rd column)
        :rtype: int
        """
        # If we find "Unnamed" in 3rd column then it means we are provided with
        # filenames for each series graph, in that column, so the series will start from
        # 4th column
        if "Unnamed" in self.columns[2]:
            start = 3
        else:
            start = 2
        self.start = start
        return start

    def get_names(self) -> List[str]:
        """Function for getting list of names for png files where the graphs
        will be saved.

        :return: list of names
        :rtype: list of str
        """
        # If we find "Unnamed" in 3rd column then it means we are provided with
        # filenames for each series graph, in that column.
        if "Unnamed" in self.columns[2]:
            names = self[self.columns[2]][
                    3:
                    ].values  # names for graphs are in 3rd column,
            # starting from 4th row, because of df structure
        else:
            name = input(
                "Enter name for your graphs:"
            )  # We need to ask user for filename if there are none in DataFrame
            start = 2  # data starting from column 3rd
            names = [
                name + str(j) for j in range(df.shape[1] - start)
            ]  # Filenames = user input + consecutive numbers
        self.file_names = names
        return names

    def get_height(self) -> int:
        """Function calculating height of the graph based on number of bars

        :return: height of the graphs in pixels
        :rtype: int
        """
        no_of_bars = df.shape[1] - self.start
        graph_height = no_of_bars * 100
        self.height = graph_height
        return graph_height

    def get_title_and_sort(self, number: int) -> str:
        self.number = number
        title = df.iloc[self.number, 0]  # Title for whole graph
        sub_title = df.iloc[self.number, 1]  # Subtitle for whole graph
        title = (
                "<b>" + title + "</b><br><sup>" + sub_title + "</sup>"
        )  # combining title and sub_title into one
        self.title = title
        self.asc = True
        if 'mniej' in self.title:
            self.asc = False
        return title

    def get_series(self, number):
        self.number = number
        data = self.loc[[0, 1, 2, self.number]].T.dropna(thresh=1, subset=[self.number])
        # raw data, sorted
        data = data[self.start:].sort_values(self.number, ascending=self.asc).T
        return data

    def get_y_labels(self, number):
        data = self.get_series(number)
        headers = list(data)  # names of y ticks
        subheaders = list(data.iloc[0])  # sub names for y ticks
        # which y ticks labels should be bold
        bolds = np.array(data.iloc[2])
        bolds = np.where(bolds == 1)[0]

        # Checking if the subheaders are missing values
        if subheaders.count(subheaders[0]) == len(subheaders):
            y = headers  # only headers set to y variable
            # Loop for formatting y ticks
            for ind in range(len(y)):
                if ind in bolds:  # Formatting as bold if found in bolds
                    y[ind] = "<b>" + y[ind] + "</b>"
                y[ind] = y[ind] + "    "  # For better visual appearance

        # We have to combine headers and subheaders into one as y ticks
        else:
            y = []
            for ind in range(len(headers)):
                x = headers[ind]
                # If header name occurred twice,
                # pandas (by transposition) adds .1 at the end
                if x[-2:] == ".1":
                    x = x[:-2]
                temp = subheaders[ind]
                if ind in bolds:
                    y.append(
                        "<b>" + x + "</b>    " + "<br><sup>" + temp + "</sup>    "
                    )  # bold only header if in the bolds
                    # <sup> is for superscript the subheaders
                else:
                    y.append(
                        x + "    <br><sup>" + temp + "</sup>    "
                    )  # only superscript the subheaders
        return y

    def get_colors(self, number):
        data = self.get_series(number)
        # extract colors for each bar
        colors = np.array(data.loc[1].values)
        colors[
            np.argwhere(colors != colors).flatten()
        ] = " grey"  # if color was missing, set to grey
        colors = list(colors)
        # while parsing, occurred some bug, colors codes/names start from second char
        colors = list(map(lambda q: q[1:], colors))
        return colors


def plot_save(graph_plotly, number: int) -> None:
    title = graph_plotly.get_title_and_sort(number)
    x = graph_plotly.get_series(number)
    y = graph_plotly.get_y_labels(number)
    colors = graph_plotly.get_colors(number)
    name = graph_plotly.file_names[number-3]
    plot_graphs(np.array(x.values[3].astype(float)), y, colors, title, name, width=1200,
                height=graph_plotly.height)

a1 = datetime.datetime.now()
path = './data/boincdata.xls'
df = pd.read_excel(io=path)
gp = DataPlotly(df)
for i in range(3, len(df)):
    plot_save(gp, i)
a2 = datetime.datetime.now()
print((a2-a1).total_seconds())