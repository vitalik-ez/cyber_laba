import datetime
import glob
import logging
import os

import plotly.graph_objs as go
from plotly.offline import plot

import pandas as pd
import sqlite3
from datetime import datetime, date, timedelta

import pandas as pd

import csv
from math import floor, ceil

import plotly.express as px

import numpy as np

def dataSampling(datetimeObj_1, datetimeObj_2):
    conn = sqlite3.connect("main.db")
    cursor = conn.cursor()
    month_table = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    sql = f"SELECT id from {month_table[datetimeObj_1.month - 1]} WHERE UTC = '{datetimeObj_1.time()}' AND number_month = {datetimeObj_1.day}"
    cursor.execute(sql)
    id_1 = cursor.fetchall()[0][0]
    sql = f"SELECT id from {month_table[datetimeObj_2.month - 1]} WHERE UTC = '{datetimeObj_2.time()}' AND number_month = {datetimeObj_2.day}"
    cursor.execute(sql)
    id_2 = cursor.fetchall()[0][0]
    list_dict = []
    if datetimeObj_2.month - datetimeObj_1.month != 0:
        sql = f"SELECT * from {month_table[datetimeObj_1.month - 1]} WHERE id >= {id_1} AND number_month >= {datetimeObj_1.day}"
        cursor.execute(sql)

        for i in cursor.fetchall():
            list_dict.append({'number_month': i[1], 'month': month_table[datetimeObj_1.month - 1], 'T': i[3], 'UTC': i[2], 'dd': i[4], 'FF': i[5]})

        for i in range(datetimeObj_1.month, datetimeObj_2.month - 1):
            sql = f"SELECT * from {month_table[i]}"
            cursor.execute(sql)
            for j in cursor.fetchall():
                list_dict.append({'number_month': j[1], 'month': month_table[i], 'T': j[3], 'UTC': j[2], 'dd': j[4], 'FF': j[5]})

        sql = f"SELECT * from {month_table[datetimeObj_2.month - 1]} WHERE id <= {id_2} AND number_month <= {datetimeObj_2.day}"
        cursor.execute(sql)
        for i in cursor.fetchall():
            list_dict.append({'number_month': i[1], 'month': month_table[datetimeObj_2.month - 1], 'T': i[3], 'UTC': i[2], 'dd': i[4], 'FF': i[5]})
    else:

        sql = f"SELECT * from {month_table[datetimeObj_1.month - 1]} WHERE id >= {id_1} AND id <= {id_2} AND number_month >= {datetimeObj_1.day} AND number_month <= {datetimeObj_2.day}"
        cursor.execute(sql)

        for i in cursor.fetchall():
            list_dict.append({'number_month': i[1], 'month': month_table[datetimeObj_1.month - 1], 'T': i[3], 'UTC': i[2], 'dd': i[4], 'FF': i[5]})

    conn.close()
    return list_dict




def graphic_1(list_dict, datetimeObj_1, datetimeObj_2):
    start = datetime.strptime(datetimeObj_1, '%d/%m/%Y %H:%M')
    end = datetime.strptime(datetimeObj_2, '%d/%m/%Y %H:%M') + timedelta(minutes=30)

    def hour_range(start, end):
        while start < end:
            yield start
            start += timedelta(minutes=30)

    date_list = [h.strftime('%d.%m.%Y %H:%M') for h in hour_range(start, end)]
    trace1 = go.Scatter(
        x=[ i for i in date_list],
        #x=[ str(i['number_month']) + "." + i['month'] + ".2012" for i in list_dict],
        y=[ i['T'] for i in list_dict]
    )

    data = [trace1]
    layout = go.Layout(
        # autosize=False,
        # width=900,
        # height=500,
        title="Температурні умови",
        xaxis=dict(
            title="Дата"
        ),
        yaxis=dict(
            title="Температура, t\u00b0C"
        )
    )
    fig = go.Figure(data=data, layout=layout)
    fig['data'][0]['showlegend']=True
    fig['data'][0]['name']='t\u00b0C'

    step = int(floor(len(date_list)/20))
    if step != 0 :
        fig.update_xaxes(tickangle=45, tickmode = 'array', tickvals = date_list[0::step])


    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    #logger.info("Plotting number of points {}.".format(len(x_data)))
    return plot_div

def graphic_2(list_dict):
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
    layout=go.Layout(title="Тривалість температурних режимів", xaxis={'title':"Температура, t\u00b0C"}, yaxis={'title':'Години, t'})
    figure=go.Figure(data=data,layout=layout)
    plot_div = plot(figure, auto_open=False, output_type='div')

    #print(x)
    #print(y)

    return (plot_div, x, y)


def graphic_3(list_dict):
    data = []
    for i in list_dict:
        data.append((i['dd'], i['FF']))
    #print(data)
    v_max = max([ i[1] for i in data])
    #print("V_max = ", v_max)
    range = [ 0, v_max*0.25, v_max*0.5, v_max*0.75, v_max]
    calm = 0
    count = 0
    #change = 0
    d = {}
    for i in data:
        count += 1
        if i[0] == None:
            calm += 1
        #if i[0] == 'Переменный':
            #change += 1
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

    list_dir = ['С-З', 'Северный', 'Переменный', 'Ю-В', 'С-В', 'Восточный', 'Южный', 'Ю-З', 'Западный']
    for i in list_dir:
        if i not in d:
            d[i] = [0, 0, 0, 0]
    fig = go.Figure()

    fig.add_trace(go.Barpolar(
        r=[d['Северный'][0], d['С-З'][0], d['Западный'][0], d['Ю-З'][0], d['Южный'][0], d['Ю-В'][0], d['Восточный'][0], d['С-В'][0]],
        name='< ' + str(range[1]) +' м/с',
        marker_color='rgb(169, 153, 137)'
    ))
    fig.add_trace(go.Barpolar(
        r=[d['Северный'][1], d['С-З'][1], d['Западный'][1], d['Ю-З'][1], d['Южный'][1], d['Ю-В'][1], d['Восточный'][1], d['С-В'][1]],
        name= str(range[1]) + " - " + str(range[2]) + ' м/с',
        marker_color='rgb(212, 180, 131)'
    ))
    fig.add_trace(go.Barpolar(
        r=[d['Северный'][2], d['С-З'][2], d['Западный'][2], d['Ю-З'][2], d['Южный'][2], d['Ю-В'][2], d['Восточный'][2], d['С-В'][2]],
        name=str(range[2]) + " - " + str(range[3]) + ' м/с',
        marker_color='rgb(255, 144, 0)'
    ))
    fig.add_trace(go.Barpolar(
        
        r=[d['Северный'][3], d['С-З'][3], d['Западный'][3], d['Ю-З'][3], d['Южный'][3], d['Ю-В'][3], d['Восточный'][3], d['С-В'][3]],
        name=str(range[3]) + " - " + str(range[4]) + ' м/с',
        marker_color='rgb(81, 45, 56)'
    ))

    fig.update_traces(text=['Північ', 'Північний захід','Захід', 'Південний захід','Південь', 'Південний схід','Схід', 'Північний схід' ])
    fig.update_layout(
        title='Троянда вітрів',
        font_size=16,
        legend_font_size=16,
        #polar_radialaxis_ticksuffix='%',
        polar_angularaxis_rotation=90,
        width=700, height=700,
    )
    n = int(calm/count * 100) / 100
    fig.add_annotation( # add a text callout with arrow
        text=str(n) + "%",  x=0.5, y=0.5, showarrow=False
    )
    
    fig.update_layout(legend=dict(
        title="Швидкіть вітру в м/с",
        orientation="h",
        yanchor="middle",  
        y=-0.1,
        xanchor="center",
        x=0.5,
        font=dict(size=14)),
        polar=dict(hole=0.1, radialaxis=dict(showticklabels=False, ticks='', linewidth=0)),
        margin=dict(t=110),
    )


    plot_div = plot(fig, auto_open=False, output_type='div')
    return plot_div




def graphic_4(list_dict):
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


def graphic_5(datetimeObj_1, datetimeObj_2):

    list_sun = []
    with open('sun.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            list_sun.append(row)

    list_sun = list_sun[2:-1]

    #datetimeObj_1 = datetime.strptime('01/01/2012 09:30', '%d/%m/%Y %H:%M')
    #datetimeObj_2 = datetime.strptime('07/02/2012 14:30', '%d/%m/%Y %H:%M')


    first_point = datetime(datetimeObj_1.year, datetimeObj_1.month, datetimeObj_1.day, datetimeObj_1.hour, datetimeObj_1.minute) - datetime(2012, 1, 1, 0, 0)
    first_point = first_point.days * 24 + first_point.seconds / 3600

    end = datetimeObj_2-datetimeObj_1
    end = end.days * 24 + end.seconds / 3600

    x, y = [], []
    for i in range(floor(first_point - 1), ceil(first_point + end)):
        if i == 8759:
            break
        if list_sun[i][3] != '0':
            x.append(list_sun[i][1] + " " + list_sun[i][0][0:5] + "/2012")
            y.append(int(list_sun[i][3]))

    data = [go.Bar(
       x = x,
       y = y
    )]
    layout=go.Layout(title="Інтенсивність сонячної інсоляції", xaxis={'title':'Дата'}, yaxis={'title':'Вт/м2'})
    fig = go.Figure(data=data, layout=layout)
    step = int(floor(len(x)/20))
    if step != 0 :
        fig.update_xaxes(tickangle=45, tickmode = 'array', tickvals = x[0::step])
    plot_div = plot(fig, auto_open=False, output_type='div')

    return plot_div


def graphic_6(datetimeObj_1, datetimeObj_2):
    list_sun = []
    with open('sun.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            list_sun.append(row)

    list_sun = list_sun[2:-1]


    first_point = datetime(datetimeObj_1.year, datetimeObj_1.month, datetimeObj_1.day, datetimeObj_1.hour, datetimeObj_1.minute) - datetime(2012, 1, 1, 0, 0)
    first_point = first_point.days * 24 + first_point.seconds / 3600

    end = datetimeObj_2-datetimeObj_1
    end = end.days * 24 + end.seconds / 3600

    x, y = [], []
    for i in range(floor(first_point - 1), ceil(first_point + end)):
        if i == 8759:
            break
        if list_sun[i][3] != '0':
            x.append(list_sun[i][1] + " " + list_sun[i][0][0:5] + "/2012")
            y.append(int(list_sun[i][3]))    

    d = {}
    for i in y:
        if i in d:
            tm3 = timedelta(hours=1, minutes=0, seconds=0)
            d[i] = d[i] + tm3
        else:
            d[i] = timedelta(hours=1, minutes=0, seconds=0)
    #print(d)

    x = [ i for i in d.keys() ]
    y = [ i.days * 24 + i.seconds/3600 if i.days != 0 else i.seconds / 3600 for i in d.values() ]

    trace1 = go.Bar(x=x, y=y)
    #print(x)
    #print(y)

    data=go.Data([trace1])
    layout=go.Layout(title="Тривалість режимів сонячної активності", xaxis={'title':'Вт/м2'}, yaxis=dict(title='t,ГОД'))
    figure=go.Figure(data=data,layout=layout)
    #figure.update_yaxes(type="log", range=[0,80]) # log range: 10^0=1, 10^5=100000
    #figure.update_xaxes() # linear range

    #figure.update_xaxes(type="log")
    figure.update_yaxes(type="log", range=[np.log10(0), np.log10(80)])
    #figure.update_yaxes(range=[0, 0.4], row=1, col=1)
    plot_div = plot(figure, auto_open=False, output_type='div')

    #x_y = [ (i,j) for i, j in zip(x,y)]

    return plot_div




