import sqlite3
from datetime import datetime, timedelta

import plotly.graph_objs as go
from plotly.offline import plot

from collections import OrderedDict

def dataForLaba2(datetimeObj_1, datetimeObj_2):
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
            list_dict.append({'number_month': i[1], 'month': month_table[datetimeObj_1.month - 1], 'T': i[3], 'UTC': i[2]})

        for i in range(datetimeObj_1.month, datetimeObj_2.month - 1):
            sql = f"SELECT * from {month_table[i]}"
            cursor.execute(sql)
            for j in cursor.fetchall():
                list_dict.append({'number_month': j[1], 'month': month_table[i], 'T': j[3], 'UTC': j[2]})

        sql = f"SELECT * from {month_table[datetimeObj_2.month - 1]} WHERE id <= {id_2} AND number_month <= {datetimeObj_2.day}"
        cursor.execute(sql)
        for i in cursor.fetchall():
            list_dict.append({'number_month': i[1], 'month': month_table[datetimeObj_2.month - 1], 'T': i[3], 'UTC': i[2]})
    else:

        sql = f"SELECT * from {month_table[datetimeObj_1.month - 1]} WHERE id >= {id_1} AND id <= {id_2} AND number_month >= {datetimeObj_1.day} AND number_month <= {datetimeObj_2.day}"
        cursor.execute(sql)

        for i in cursor.fetchall():
            list_dict.append({'number_month': i[1], 'month': month_table[datetimeObj_1.month - 1], 'T': i[3], 'UTC': i[2]})

    conn.close()
    return list_dict



def graphic(heat_lost, house_area, air_temperature, pdf = False):
    heat_lost /= 1000 # Квт/м2
    t_external = -22
    # point_1 = (t_external, heat_lost*house_area)
    # point_2 = (air_temperature, 0)
    x_default, y_default = [], []
    k = (heat_lost * house_area - 0) / (t_external - 20)
    b = 0 - k * 20
    for i in range(t_external, 21):
        x_default.append(i)
        y_default.append(k * i + b)
    
    x, y = [], []
    #k = (heat_lost * house_area - 0) / (t_external - air_temperature)
    if air_temperature != 20:
        b = 0 - k * air_temperature
        for i in range(t_external, int(air_temperature) + 1):
            x.append(i)
            y.append(k*i+b)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y))
    fig.add_trace(go.Scatter(x=x_default, y=y_default))

    fig.update_layout(
        # autosize=False,
        width=1100,
        # height=500,
        title="Характеристика потреб будівлі у тепловій енергії на опалення.",
        xaxis=dict(
            title="Температура, t\u00b0C"
        ),
        yaxis=dict(
            title="Q, кВт"
        )
    )
    if air_temperature != 20:
        fig['data'][0]['showlegend']=True
        fig['data'][0]['name']='Залежність тепловтрат від Т зовн при Т внутр = ' + str(air_temperature) + '\u00b0C'
    fig['data'][1]['showlegend'] = True
    fig['data'][1]['name'] = 'Залежність тепловтрат від Т зовн при Т внутр = 20\u00b0C'
    if pdf:
        fig.write_image("report_images/fig0.png")
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return (plot_div, "Q = " + str(round(k, 2)) + " * T зовн. повітря + " + str(round(b, 2)))


def getEnergyLoss(list_dict, heat_lost, house_area, air_temperature):
    heat_lost /= 1000 # кВт
    d = {}
    for i in list_dict:
        if i['T'] in d:
            tm3 = timedelta(hours=0, minutes=30, seconds=0)
            d[i['T']] = d[i['T']] + tm3
        else:
            d[i['T']] = timedelta(hours=0, minutes=30, seconds=0)

    x = [i for i in d.keys()]
    y = [i.days * 24 + i.seconds / 3600 if i.days != 0 else i.seconds / 3600 for i in d.values()]
    dictionary = dict(zip(x, y))
    list_keys = list(dictionary.keys())
    list_keys.sort()
    sort_dict = {}
    for i in list_keys:
        sort_dict[i] = d[i]
    t_external = -22
    k = (heat_lost * house_area - 0) / (t_external - air_temperature)
    b = 0 - k * air_temperature
    W = 0
    for i in range(t_external, int(air_temperature) + 1):
        if i in sort_dict:
            t = sort_dict[i]
            if t.days != 0:
                t = t.days * 24 + t.seconds / 3600
            else:
                t = t.seconds / 3600
            W += (k * i + b) * t

    return round(W,2)


def GVP(request):
    count_shower = int(request.session['count_shower'])
    shower_temperature = float(request.session['shower_temperature'])
    count_litters_shower = float(request.session['count_litters_shower'])
    shower_temperature = float(request.session['shower_temperature'])

    incoming_temperature = float(request.session['incoming_temperature'])
    end_temperature = float(request.session['end_temperature'])

    bath_temperature = float(request.session['bath_temperature'])
    count_bath = int(request.session['count_bath'])
    count_litters_bath = float(request.session['count_litters_bath'])
    bath_temperature = float(request.session['bath_temperature'])

    q_shower = count_shower * count_litters_shower
    q_bath = count_bath * count_litters_bath

    q_shower_t = q_shower * (shower_temperature - incoming_temperature)/(end_temperature - incoming_temperature)
    q_bath_t = q_bath * (bath_temperature - incoming_temperature)/(end_temperature - incoming_temperature)

    q_t = (q_shower_t + q_bath_t) / 998.23

    W = 1.163 * q_t * (end_temperature - incoming_temperature)

    if 'duration' in request.session:
        P = W / int(request.session['duration'])
        return ['Енергія необхідна для нагріву води ' + str(round(W, 3)) + ' кВт·год. Теплова потужність нагрівача: ' + str(round(P, 3)) + ' кВт.', W]
    else:
        t = W / int(request.session['power'])
        return ['Енергія необхідна для нагріву води ' + str(round(W, 3)) +' кВт·год. Час нагрівання бака ГВП: ' + str(round(t, 3)) + ' год.', W]


def histogram(W, energy_loss, tariff, tariff_gas, tariff_coal, tariff_briquettes, tariff_oak, tariff_electricity, pdf = False):
    #W_tariff = tariff * W
    energy_loss_tariff = tariff * energy_loss / 1163
    
    gas = 0.1075 * energy_loss * tariff_gas / 1000
    coal = 0.1792 * energy_loss * tariff_coal / 1000
    briquettes = 0.1953 * energy_loss * tariff_briquettes / 1000
    oak = 0.287 * energy_loss * tariff_oak / 1000
    electricity = 1.01 * energy_loss * tariff_electricity


    #x = ["Теплозабезпечення від централізованої мережі",
    #     "Автономне теплозабезпечення від газового котла",
    #     "Автономне теплозабезпечення від вугільного котла",
    #     "Автономне теплозабезпечення від дров’яного котла", 
    #     "Автономне теплозабезпечення від котла, що працює на деревних пелетах",
    #     "Автономне теплозабезпечення від електричного котла"]
    x = ["Централізована мережа",
         "Газовий котел",
         "Вугільний котел",
         "Дров’яний котел", 
         "Котел, що працює на деревних пелетах",
         "Електричний котел"]
    
    y = [round(energy_loss_tariff,2),round(gas,2),round(coal,2),round(oak,2), round(briquettes,2), round(electricity,2)]
    y_1 = [16499,25200,25120,23990,24650,25190]
    data = [go.Bar(
       x = x,
       y = y
    )]
    if pdf:
        layout=go.Layout(title="Експлуатаційні витрати на опалення", xaxis={'title':'Вид системи теплозабезпечення'}, yaxis={'title':'Витрати (грн)'})
    else:
        layout=go.Layout(title="Експлуатаційні витрати на опалення для різних варіантів реалізації системи теплозабезпечення", xaxis={'title':'Види систем теплозабезпечення'}, yaxis={'title':'Витрати (грн)'})
        
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        font=dict(
            size=12,
        )
    )
    #fig.add_trace(go.Bar(x=x, y=y_1))
    #fig['data'][0]['showlegend']=True
    #fig['data'][0]['name']='Експлуатаційні витрати'
    #fig['data'][1]['showlegend'] = True
    #fig['data'][1]['name'] = 'Вартість котлів'

    if pdf:
        fig.write_image("report_images/fig1.png")
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def histogram_price(pdf = False):
    x = ["Газовий котел(BOSCH WBN2000-24C)",
         "Твердопаливний котел (Kraft 25 кВт)",
         "Електричний котел(BOSCH HEAT 3500 24 кВт)"]

    y = [16499,25200,25190]
    data = [go.Bar(
       x = x,
       y = y
    )]
    layout=go.Layout(title="Вартість котлів", xaxis={'title':'Вид системи теплозабезпечення'}, yaxis={'title':'Вартість (грн)'})
    
    fig = go.Figure(data=data, layout=layout)
    fig['data'][0]['showlegend']=True
    fig['data'][0]['name']='Вартість котлів'
    if pdf:
        fig.write_image("report_images/fig2.png")
    
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
