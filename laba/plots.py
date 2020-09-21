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
            title="Date"

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


def RosaWindy(begin, end, time):
    conn = sqlite3.connect("kyiv_three_months.db")
    cursor = conn.cursor()
    month_table = ['January'] #, 'February', 'March']

    for i in month_table:
        sql = f"SELECT dd, FF from {i}"
        cursor.execute(sql)
        data = cursor.fetchall()
        v_max = max([ i[1] for i in data])
        print("V_max = ", v_max)
        range = [ 0, v_max*0.25, v_max*0.5, v_max*0.75, v_max]

        d = {}
        for i in data:
            if i[0] in d:
                if 0 < i[1] <= range[1]:
                    d[i[0]][0] += 1
                if range[1] < i[1] <= range[2]:
                    d[i[0]][1] += 1
                if range[2] < i[1] <= range[3]:
                    d[i[0]][2] += 1
                if range[3] < i[1] <= range[4]:
                    d[i[0]][3] += 1
            else:
                d[i[0]] = [0,0,0,0]
                if 0 < i[1] <= range[1]:
                    d[i[0]] = [1, 0 , 0, 0]
                if range[1] < i[1] <= range[2]:
                    d[i[0]] = [0, 1, 0, 0]
                if range[2] < i[1] <= range[3]:
                    d[i[0]] = [0, 0, 1, 0]
                if range[3] < i[1] <= range[4]:
                    d[i[0]] = [0, 0, 0, 1]


    fig = go.Figure()

    fig.add_trace(go.Barpolar(
        r=[d['Северный'][0], d['С-З'][0], d['Западный'][0], d['Ю-З'][0], d['Южный'][0], d['Ю-В'][0], d['Восточный'][0], d['С-В'][0]],
        name='< ' + str(range[1]) +' m/s',
        marker_color='rgb(0,0,0)'
    ))
    fig.add_trace(go.Barpolar(
        r=[d['Северный'][1], d['С-З'][1], d['Западный'][1], d['Ю-З'][1], d['Южный'][1], d['Ю-В'][1], d['Восточный'][1], d['С-В'][1]],
        name= str(range[1]) + "-" + str(range[2]) + ' m/s',
        marker_color='rgb(158,154,200)'
    ))
    fig.add_trace(go.Barpolar(
        r=[d['Северный'][2], d['С-З'][2], d['Западный'][2], d['Ю-З'][2], d['Южный'][2], d['Ю-В'][2], d['Восточный'][2], d['С-В'][2]],
        name=str(range[2]) + "-" + str(range[3]) + ' m/s',
        marker_color='rgb(203,201,226)'
    ))
    fig.add_trace(go.Barpolar(
        
        r=[d['Северный'][3], d['С-З'][3], d['Западный'][3], d['Ю-З'][3], d['Южный'][3], d['Ю-В'][3], d['Восточный'][3], d['С-В'][3]],
        name=str(range[3]) + "-" + str(range[4]) + ' m/s',
        marker_color='rgb(106,81,163)'
    ))

    fig.update_traces(text=['North', 'N-W','West', 'S-W','South', 'S-E','East', 'N-E' ])
    fig.update_layout(
        title='Wind Speed Distribution in Laurel, NE',
        font_size=16,
        legend_font_size=16,
        #polar_radialaxis_ticksuffix='%',
        polar_angularaxis_rotation=90,

    )
    

    plot_div = plot(fig, auto_open=False, output_type='div')
    return plot_div




def PlotWindActivity(begin, end, time):
    conn = sqlite3.connect("kyiv_three_months.db")
    cursor = conn.cursor()
    month_table = ['January', 'February', 'March']

    dt_start = datetime.strptime(begin, '%Y-%m-%d')
    dt_end = datetime.strptime(end, '%Y-%m-%d')

    datetimeObj = datetime.strptime('00:30:00', '%H:%M:%S')
    timeObj = datetimeObj.time()


    list_dict = []
    if dt_end.month - dt_start.month != 0:
        sql = f"SELECT UTC, FF from {month_table[dt_start.month - 1]} WHERE number_month >= {dt_start.day}"
        cursor.execute(sql)

        for i in cursor.fetchall():
            list_dict.append({'UTC': i[0], 'FF': i[1]})

        for i in range(dt_start.month, dt_end.month - 1):
            sql = f"SELECT UTC, FF from {month_table[i]}"
            cursor.execute(sql)
            for j in cursor.fetchall():
                list_dict.append({'UTC': j[0], 'FF': j[1]})

        sql = f"SELECT UTC, FF from {month_table[dt_end.month - 1]} WHERE number_month <= {dt_end.day}"
        cursor.execute(sql)
        for i in cursor.fetchall():
            list_dict.append({'UTC': i[0], 'FF': i[1]})
    else:
        sql = f"SELECT UTC, FF from {month_table[dt_start.month - 1]} WHERE number_month >= {dt_start.day} AND number_month <= {dt_end.day}"
        cursor.execute(sql)

        for i in cursor.fetchall():
            list_dict.append({'UTC': i[0], 'FF': i[1]})

    d = {}
    for i in list_dict:
        if i['FF'] in d:
            tm3 = timedelta(hours=0, minutes=30, seconds=0)
            d[i['FF']] = d[i['FF']] + tm3
        else:
            d[i['FF']] = timedelta(hours=0, minutes=30, seconds=0)


    x = [ i for i in d.keys() ]
    y = [ i.days * 24 + i.seconds/3600 if i.days != 0 else i.seconds / 3600 for i in d.values() ]

    trace1 = go.Bar(x=x, y=y)

    data=go.Data([trace1])
    layout=go.Layout(title="Розподіл вітрового потенціалу за швидкостями, год", xaxis={'title':'М/С'}, yaxis={'title':'t,ГОД'})
    figure=go.Figure(data=data,layout=layout)
    plot_div = plot(figure, auto_open=False, output_type='div')

    return plot_div