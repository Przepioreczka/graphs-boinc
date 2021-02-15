from typing import Iterable, List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def get_params(df: pd.DataFrame) -> Tuple[int, Iterable[str], int]:
    """This function takes DataFrame and gets parameters necessary for plotting and
    saving graphs.

    :param df: df must be pandas DataFrame, whole data
    :type df: pandas.DataFrame
    :return: tuple of
        - (start) integer specifying from which row in df we should take data;
        - (names)list of names for each row for each data series,
        - names for png files of plotted graphs;
        - (height) height of graphs depending on number of parameters (bars to plot)
    :rtype: tuple
    """
    # If we find "Unnamed" in 3rd column then it means we are provided with filenames,
    # for each series graph, in that column.
    if "Unnamed" in df.columns[2]:
        names = df[df.columns[2]][
            3:
        ].values  # names for graphs in 3rd column, starting from 4th row
        start = 3  # data starting from column 4th

    else:
        name = input(
            "Enter name for your graphs:"
        )  # We need to ask user for filename if there are none in DataFrame
        start = 2  # data starting from column 3rd
        names = [
            name + str(i) for i in range(df.shape[1] - start)
        ]  # Filenames = user input + consecutive numbers

    no_of_bars = df.shape[1] - start
    graph_height = no_of_bars * 100
    return start, names, graph_height


def get_data_params(
    path: str, number: int, col_start: int
) -> Tuple[np.ndarray, List[str], List[str], str]:
    """Processing data series, and extracting features necessary for plotting graph

    :param path: path to xls file where data series is stored
    :type path: str
    :param number: which row will be processed to plot graph
    :type number: int
    :param col_start: column fom which data series begins, must be 2 or 3
    :type col_start: int
    :return: tuple of
        - (X) prepared data series;
        - (y) prepared y labels/y axis data;
        - (colors) what color will each bar have;
        - (title) title for graph
    :rtype: tuple"""
    # Reading data
    df = pd.read_excel(io=path)
    data = df.loc[[0, 1, 2, number]].T.dropna(thresh=1, subset=[number])

    title = data.iat[0, 3]  # Title for whole graph
    sub_title = data.iat[1, 3]  # Subtitle for whole graph
    title = (
        "<b>" + title + "</b><br><sup>" + sub_title + "</sup>"
    )  # combining title and sub_title into one
    asc = True  # How bars will be sorted - default ascending
    # Information about ascending or descending sort format is in sub_title
    if "mniej" in sub_title:
        asc = False  # descending
    data = data[col_start:].sort_values(number, ascending=asc).T  # raw data, sorted
    headers = list(data)  # names of y ticks
    subheaders = list(data.iloc[0])  # sub names for y ticks
    # which y ticks labels should be bold
    bolds = np.array(data.iloc[2])
    bolds = np.where(bolds == 1)[0]
    # extract colors for each bar
    colors = np.array(data.loc[1].values)
    colors[
        np.argwhere(colors != colors).flatten()
    ] = " grey"  # if color was missing, set to grey
    colors = list(colors)
    # while parsing, occurred some bug, colors codes/names start from second char
    colors = list(map(lambda q: q[1:], colors))
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

    return np.array(data.values[3].astype(float)), y, colors, title


def plot_graphs(
    x: np.ndarray,
    y: List[str],
    colors_bar: List[str],
    title: str,
    im_name: str,
    width=500,
    height=1500,
) -> None:
    """Function for plotting prepared data in plotly library.

    :param x: data series
    :type x: np.ndarray
    :param y: y-axis labels/y axis values
    :type y: list
    :param colors_bar: what color will each bar have
    :type colors_bar: list
    :param title: title of the graph
    :type title: str
    :param im_name: file name to save graph
    :type im_name: str
    :param width: graph width in pixels, default to 500
    :type width: int
    :param height: graph height in pixels, default to 1500
    :type height: int
    """
    # each bar width set to 0.5
    bar_width = np.zeros(len(x)) + 0.5
    # specifying Bar parameters (x data, y data, orientation: horizontal, width of bars)
    fig = go.Figure(
        data=[
            go.Bar(
                x=x,
                y=y,
                text=x,
                textposition="outside",
                orientation="h",
                marker_color=colors_bar,
                width=bar_width,
            )
        ]
    )
    # specifying graph width and height in pixels
    fig.update_layout(
        autosize=True,
        width=width,
        height=height,
    )
    # specifying title, title position, font
    fig.update_layout(
        title=title,
        title_x=0.5,
        template="plotly_white",
        title_font=dict(size=26, color="black"),
    )
    # fixing visual presentation
    fig.update_xaxes(color="black")
    fig.update_yaxes(tickfont_size=13, color="black")
    # saving graph to png file with given name
    fig.write_image(im_name + ".png", format="png")
