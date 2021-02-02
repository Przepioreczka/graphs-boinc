import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Tuple, Iterable, List, Union


def get_params(df: pd.DataFrame) -> Tuple[int, Iterable[str], int]:
    """This function takes DataFrame and gets parameters necessary for plotting and saving graphs.
    Input Arguments: df must be pandas DataFrame
    Returns:
        start - integer specifying from which row in df we should take data
        names - list of names for each row for each data series, names for png files of plotted graphs
        height - height of graphs depending on number of parameters (bars to plot)"""

    # If we find "Unnamed" in 3rd column then it means we are provided with filenames,
    # for each series graph, in that column.
    if "Unnamed" in df.columns[2]:
        names = df[df.columns[2]][3:].values  # names for graphs in 3rd column, starting from 4th row
        start = 3  # data starting from column 4th

    else:
        name = input('Enter name for your graphs:')  # We need to ask user for filename if there are none in DataFrame
        start = 2  # data starting from column 3rd
        names = [name + str(i) for i in range(df.shape[1] - start)]  # Filenames = user input + consecutive numbers

    no_of_bars = df.shape[1] - start
    graph_height = no_of_bars * 100
    return start, names, graph_height


def get_data_params(path: str, number: int, col_start: Union[2, 3]) -> \
        Tuple[np.ndarray, List[str], List[str], str, str]:
    """ Processing data series, and extracting features necessary for plotting graph
    Input Arguments:
        path - str, path to xls file where data series is stored
        number - int, which row will be processed to plot graph
        col_start - column fom which data series begins
    Return:
        X - prepared data series
        y - prepared y labels/y axis data
        colors - what color will each bar have
        title - title for graph
        sub_title - sub title for graph"""

    # Reading data
    df = pd.read_excel(io=path)
    data = df.loc[[0, 1, 2, number]].T.dropna(thresh=1, subset=[number])

    title = data.iat[0, 3]  # Title for whole graph
    sub_title = data.iat[1, 3]  # Subtitle for whole graph
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
    colors[np.argwhere(colors != colors).flatten()] = ' grey'  # if color was missing, set to grey
    colors = list(colors)
    # while parsing, occurred some bug, colors codes/names start from second char
    colors = list(map(lambda q: q[1:], colors))
    # Checking if the subheaders are missing values
    if subheaders.count(subheaders[0]) == len(subheaders):
        y = headers  # only headers set to y variable
        # Loop for formatting y ticks
        for ind in range(len(y)):
            if ind in bolds:  # Formatting as bold if found in bolds
                y[ind] = '<b>' + y[ind] + '</b>'
            y[ind] = y[ind] + '    '  # For better visual appearance

    # We have to combine headers and subheaders into one as y ticks
    else:
        y = []
        for ind in range(len(headers)):
            x = headers[ind]
            # If header name occurred twice, pandas (by transposition) adds .1 at the end
            if x[-2:] == '.1':
                x = x[:-2]
            temp = subheaders[ind]
            if ind in bolds:
                y.append('<b>' + x + '</b>    ' + '<br><sup>' + temp + '</sup>    ')  # bold only header if in the bolds
                # <sup> is for superscript the subheaders
            else:
                y.append(x + '    <br><sup>' + temp + '</sup>    ')  # only superscript the subheaders

    return np.array(data.values[3].astype(float)), y, colors, title, sub_title


def plot_graphs(x: np.ndarray, y: List[str], colors_bar: Iterable[str], title: str, sub_title: str, im_name: str,
                width=500, height=1500) -> None:
    bar_width = np.zeros(len(x)) + 0.5

    fig = go.Figure(data=[go.Bar(
        x=x, y=y,
        text=x,
        textposition='outside',
        orientation='h',
        marker_color=colors_bar,
        width=bar_width,
    )])

    fig.update_layout(
        autosize=True,
        width=width,
        height=height,
    )
    fig.update_layout(
        title='<b>' + title + '</b><br><sup>' + sub_title + '</sup>',
        title_x=0.5,
        template="plotly_white",
        title_font=dict(size=26, color='black'),

    )
    fig.update_xaxes(color='black')
    fig.update_yaxes(tickfont_size=13, color='black')
    fig.write_image(im_name + '.png', format='png')
