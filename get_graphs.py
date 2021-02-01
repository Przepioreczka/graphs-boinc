import pandas as pd
import numpy as np
import plotly.graph_objects as go


def get_params(df):
    if "Unnamed" in df.columns[2]:
        names = df[df.columns[2]][3:].values
        start = 3
    else:
        name = input('Enter name for your graphs:')
        start = 2
        names = [name + str(i) for i in range(df.shape[1]-start)]

    bars = df.shape[1]-start
    height = bars * 100
    return start, names, height


def get_data_params(path: str, number: int, col_start: int):
    DF = pd.read_excel(io=path)
    data = DF.loc[[0, 1, 2, number]].T.dropna(thresh=1, subset=[number])
    title = data.iat[0, 3]
    sub_title = data.iat[1, 3]
    asc = True
    if "mniej" in sub_title:
        asc = False
    data = data[col_start:].sort_values(number, ascending=asc).T
    headers = list(data)
    subheaders = list(data.iloc[0])
    bolds = np.array(data.iloc[2])
    bolds = np.where(bolds == 1)[0]
    colors = np.array(data.loc[1].values)
    colors[np.argwhere(colors != colors).flatten()] = ' grey'
    colors = list(colors)
    colors = list(map(lambda x: x[1:], colors))
    if subheaders.count(subheaders[0]) == len(subheaders):
        conn = headers
        for ind in range(len(conn)):
            if ind in bolds:
                conn[ind] = '<b>' + conn[ind] + '</b>'
            conn[ind] = conn[ind] + '    '
    else:
        conn = []
        for ind in range(len(headers)):
            x = headers[ind]
            if x[-2:] == '.1': x = x[:-2]
            y = subheaders[ind]
            if ind in bolds:
                conn.append('<b>' + x + '</b>    ' + '<br><sup>' + y + '</sup>    ')
            else:
                conn.append(x + '    <br><sup>' + y + '</sup>    ')

    return np.array(data.values[3].astype(float)), conn, colors, title, sub_title


def plot_graphs(x, y, colorsbar, title, sub_title, im_name, width=500, height=1500):
    barwidth = np.zeros(len(x)) + 0.5

    fig = go.Figure(data=[go.Bar(
        x=x, y=y,
        text=x,
        textposition='outside',
        orientation='h',
        marker_color=colorsbar,
        width=barwidth,
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
    fig.write_image(im_name+'.png', format='png')
