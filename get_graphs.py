from typing import List

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from GraphsPlotly import DataPlotly


def plot_graphs(
    x: np.ndarray,
    y: List[str],
    colors_bar: List[str],
    title: str,
    im_name: str,
    width=500,
    xlim=None,
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
        height=len(x) * 100,
    )
    # specifying title, title position, font
    fig.update_layout(
        title=title,
        title_x=0.5,
        template="plotly_white",
        title_font=dict(size=26, color="black"),
    )
    if xlim:
        fig.update_layout(xaxis_range=xlim)
    # fixing visual presentation
    fig.update_xaxes(color="black")
    fig.update_yaxes(tickfont_size=15, color="black")
    # saving graph to png file with given name
    fig.write_image(im_name + ".png", format="png")


def plot_save(graph_plotly: DataPlotly, number: int) -> None:
    """Function for saving one data series from graph_plotly data

    :param graph_plotly: data series specified by number
    :type graph_plotly: DataPlotly
    :param number: which data series to plot
    :type number: int
    """
    graph_plotly.set_number(number)  # setting number (row) of data series
    title = (
        graph_plotly.get_title_and_sort()
    )  # extracting title and setting sort (asc/desc)
    x = graph_plotly.get_series()  # extracting series data in proper order
    y = graph_plotly.get_y_labels()  # extracting labels in proper order
    colors = graph_plotly.get_colors()  # extracting colors in proper order
    name = graph_plotly.file_names[number - 3]  # extracting file name to save
    plot_graphs(x, y, colors, title, name, width=1200)


def multiple_save(path: str):
    """Function for extracting data and saving graphs of all series in xls file.

    :param path: path to xls file
    :type path: str
    """
    df = pd.read_excel(io=path)
    gp = DataPlotly(df)
    for i in range(3, len(df)):  # rows with data series starts from 4th row
        plot_save(gp, i)


def compare_plot(path: str):
    """Function plotting and saving graph which is comparison
    of two data series in xls file.

    :param path: path to xls file
    :type path: str
    """
    df = pd.read_excel(io=path)
    # from which row in dataframe columns proper data starts
    start = df.iloc[:, 1].first_valid_index()
    filename = df.iloc[:, 2].dropna().values  # file name should be in 3rd column
    if not filename:  # if none provided ask for it
        filename = [input("Enter name for your graph: ")]
    title = df.iloc[:, 0].dropna().values  # title and subtitle in first column
    # in subtitle should be specified which series will be referential series
    if df.columns[-1] in title[1]:
        ref = -1
        norm = -2
    else:
        ref = -2
        norm = -1
    title = "<b>" + "</b><br>".join(title)
    series_names = df.iloc[:, 1].dropna().values  # name of each bar (y labels)
    ref_series = df.iloc[start:, ref].dropna().values  # 100% - referential series
    series = df.iloc[start:, norm].dropna().values
    perc_series = series / ref_series * 100 - 100  # calculate percentage difference
    perc_series = np.around(perc_series.astype(float))  # round the result
    inds = perc_series.argsort()  # get indexes sorted by series
    x, y = perc_series[inds], series_names[inds]  # sort series and names by above
    plot_graphs(
        x,
        y,
        list(
            np.where(x < 0, "red", "green")
        ),  # set negative bars to red, others to green
        title,
        filename[0],
        width=1200,
        xlim=[
            -max(abs(perc_series)) - 3,
            max(abs(perc_series)) + 3,
        ],  # symmetric xlim
    )
