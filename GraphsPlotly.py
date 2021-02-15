from typing import List

import numpy as np
import pandas as pd


class DataPlotly(pd.DataFrame):
    def __init__(
        self,
        data=None,
    ):
        super().__init__(data)
        self.start: int = 0
        self.file_names = None
        self.title: str = ""
        self.asc: bool = True
        self.number = 0
        self.find_beginning()
        self.get_names()

    def find_beginning(self) -> int:
        """Function for finding beginning of data series (from which column data starts)

        :return: start column (4th column or 3rd column)
        :rtype: int
        """
        # If we find "Unnamed" in 3rd column then it means we are provided with
        # filenames for each series graph, in that column, so the series will start from
        # 4th column
        start = 2
        if "Unnamed" in self.columns[2]:
            start = 3
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
                name + str(j) for j in range(self.shape[1] - start)
            ]  # Filenames = user input + consecutive numbers
        self.file_names = names
        return names

    def set_number(self, number: int) -> None:
        """Function for setting series number

        :param number: series number
        :type number: int
        """
        self.number = number

    def get_title_and_sort(self) -> str:
        """Function parses the data and sets the tile for graph in series.
        Sets the ascending or descending sort type, based on title."

        :return: title for graph
        :rtype: str
        """
        title = self.iloc[self.number, 0]  # Title for whole graph
        sub_title = self.iloc[self.number, 1]  # Subtitle for whole graph
        title = (
            "<b>" + title + "</b><br><sup>" + sub_title + "</sup>"
        )  # combining title and sub_title into one
        self.title = title
        # Set the asc to True or False depending on what is specified in title
        self.asc = True
        if "mniej" in self.title:
            self.asc = False
        return title

    def get_series(self) -> np.ndarray:
        """Function which extracts data series, for specific number, from dataframe.

        :return: Data series
        :rtype: ndarray
        """
        data = (
            self.iloc[self.number, self.start :]
            .dropna()
            .sort_values(ascending=self.asc)
        )
        return np.array(data.values).astype(float)

    def get_y_labels(self) -> List:
        """Function for extracting y_labels in specific order, defined by number and
        sort type (asc/desc) of data series.

        :return: y labels
        :rtype: list
        """
        data = (
            self.iloc[[0, 2, self.number], self.start :]
            .dropna(axis=1, subset=[self.number])
            .sort_values(self.number, axis=1, ascending=self.asc)
        )
        headers = list(data.columns)  # names of y ticks
        subheaders = list(data.iloc[0])  # sub names for y ticks
        # which y ticks labels should be bold
        bolds = np.array(data.iloc[2])
        bolds = np.where(bolds == 1)[0]
        # Checking if the subheaders are missing values, all nan
        if subheaders.count(subheaders[0]) == len(subheaders):
            subheaders = ["" for i in range(len(subheaders))]

        # We have to combine headers and subheaders into one as y ticks
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
                )  # bold header only if in the bolds
                # <sup> is for superscript the subheaders
            else:
                y.append(
                    x + "    <br><sup>" + temp + "</sup>    "
                )  # only superscript the subheaders
        return y

    def get_colors(self) -> List:
        """Function extracting colors of bars for data series specified by number.

        :return: colors for each bar
        :rtype: list
        """
        data = (
            self.iloc[[1, self.number], self.start :]
            .dropna(axis=1, subset=[self.number])
            .sort_values(self.number, axis=1, ascending=self.asc)
        )  # drop nan; sort
        # extract colors for each bar
        colors = np.array(data.loc[1].values)
        colors[
            np.argwhere(colors != colors).flatten()
        ] = " grey"  # if color was missing (nan), set to grey
        colors = list(colors)
        # while parsing, occurred some bug, colors codes/names start from second char
        colors = list(map(lambda q: q[1:], colors))
        return colors
