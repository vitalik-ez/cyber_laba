import datetime
import glob
import logging
import os

import plotly.graph_objs as go
from plotly.offline import plot

#My
import pandas as pd
import sqlite3
from datetime import datetime, date, timedelta




logger = logging.getLogger(__name__)


def plot1d(begin = '2012-01-15', end = '2012-03-23', time='00:30:00'):

    conn = sqlite3.connect("kyiv_three_months.db")
    cursor = conn.cursor()

    datetimeObj = datetime.strptime(time, '%H:%M:%S')
    timeObj = datetimeObj.time()

    #df = pd.read_sql_query(f"SELECT * from January WHERE UTC = '{timeObj}'", con)


    month_table = ['January', 'February', 'March']


    dt_start = datetime.strptime(begin, '%Y-%m-%d')
    dt_end = datetime.strptime(end, '%Y-%m-%d')

    list_dict = []
    if dt_end.month - dt_start.month != 0:
        sql = f"SELECT * from {month_table[dt_start.month - 1]} WHERE UTC = '{timeObj}' AND number_month >= {dt_start.day}"
        cursor.execute(sql)

        for i in cursor.fetchall():
            list_dict.append({'number_month': i[0], 'month': month_table[dt_start.month - 1], 'T': i[2]})

        for i in range(dt_start.month, dt_end.month - 1):
            sql = f"SELECT * from {month_table[i]} WHERE UTC = '{timeObj}'"
            cursor.execute(sql)
            for j in cursor.fetchall():
                list_dict.append({'number_month': j[0], 'month': month_table[i], 'T': j[2]})

        sql = f"SELECT * from {month_table[dt_end.month - 1]} WHERE UTC = '{timeObj}' AND number_month <= {dt_end.day}"
        cursor.execute(sql)
        for i in cursor.fetchall():
            list_dict.append({'number_month': i[0], 'month': month_table[dt_end.month - 1], 'T': i[2]})
    else:
        sql = f"SELECT * from {month_table[dt_start.month - 1]} WHERE UTC = '{timeObj}' AND number_month >= {dt_start.day} AND number_month <= {dt_end.day}"
        cursor.execute(sql)

        for i in cursor.fetchall():
            list_dict.append({'number_month': i[0], 'month': month_table[dt_start.month - 1], 'T': i[2]})

    conn.close()

    #x_data = [  for i in range(len(df_list))]
    trace1 = go.Scatter(
        x=[ str(i['number_month']) + " " + str(i['month']) for i in list_dict],
        y=[ i['T'] for i in list_dict]
    )

    data = [trace1]
    layout = go.Layout(
        # autosize=False,
        # width=900,
        # height=500,
        title="Температурні умови",
        xaxis=dict(
            title="Data"

        ),
        yaxis=dict(
            title="Temperature"
        )
    )
    fig = go.Figure(data=data, layout=layout)
    fig['data'][0]['showlegend']=True
    fig['data'][0]['name']='t\u00b0C'


    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    #logger.info("Plotting number of points {}.".format(len(x_data)))
    return plot_div

def TemperatureMode(begin, end, time):
    conn = sqlite3.connect("kyiv_three_months.db")
    cursor = conn.cursor()
    month_table = ['January', 'February', 'March']

    dt_start = datetime.strptime(begin, '%Y-%m-%d')
    dt_end = datetime.strptime(end, '%Y-%m-%d')

    datetimeObj = datetime.strptime('00:30:00', '%H:%M:%S')
    timeObj = datetimeObj.time()


    list_dict = []
    if dt_end.month - dt_start.month != 0:
        sql = f"SELECT UTC, T from {month_table[dt_start.month - 1]} WHERE number_month >= {dt_start.day}"
        cursor.execute(sql)

        for i in cursor.fetchall():
            list_dict.append({'UTC': i[0], 'T': i[1]})

        for i in range(dt_start.month, dt_end.month - 1):
            sql = f"SELECT UTC, T from {month_table[i]}"
            cursor.execute(sql)
            for j in cursor.fetchall():
                list_dict.append({'UTC': j[0], 'T': j[1]})

        sql = f"SELECT UTC, T from {month_table[dt_end.month - 1]} WHERE number_month <= {dt_end.day}"
        cursor.execute(sql)
        for i in cursor.fetchall():
            list_dict.append({'UTC': i[0], 'T': i[1]})
    else:
        sql = f"SELECT UTC, T from {month_table[dt_start.month - 1]} WHERE number_month >= {dt_start.day} AND number_month <= {dt_end.day}"
        cursor.execute(sql)

        for i in cursor.fetchall():
            list_dict.append({'UTC': i[0], 'T': i[1]})

    d = {}
    for i in list_dict:
        if i['T'] in d:
            tm3 = timedelta(hours=0, minutes=30, seconds=0)
            d[i['T']] = d[i['T']] + tm3
        else:
            d[i['T']] = timedelta(hours=0, minutes=30, seconds=0)

    x = [ i for i in d.keys() ]
    y = [ i.days * 24 + i.seconds/3600 if i.days != 0 else i.seconds / 3600 for i in d.values() ]

    trace1 = go.Bar(x=x, y=y)

    data=go.Data([trace1])
    layout=go.Layout(title="Тривалість температурних режимів", xaxis={'title':'x1'}, yaxis={'title':'x2'})
    figure=go.Figure(data=data,layout=layout)
    plot_div = plot(figure, auto_open=False, output_type='div')

    x_y = [ (i,j) for i, j in zip(x,y)]

    return (plot_div, x_y)

