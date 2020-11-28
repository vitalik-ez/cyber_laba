from scipy import interpolate
import numpy as np
import xlrd
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime, date, timedelta
import site1

def graphic_1(name, pdf=False):
	print(site1.settings.MEDIA_ROOT)
	rb = xlrd.open_workbook(site1.settings.MEDIA_ROOT + "energy_characteristic/" + name + ".xls",formatting_info=True)
	sheet = rb.sheet_by_index(0)

	x, y = [], []
	for rownum in range(2, sheet.nrows):
	  x.append(round(sheet.row_values(rownum)[0], 2))
	  y.append(round(sheet.row_values(rownum)[1], 2))

	f = interpolate.interp1d(x, y)
	#xnew = np.arange(x[0], x[-1], 0.01)
	xnew = [ i for i in np.arange(x[0], x[-1], 0.01)]
	ynew = f(xnew)

	trace1 = go.Scatter(
	    x=x,
	    y=y
	)

	data = [trace1]
	layout = go.Layout(
	    # autosize=False,
	    # width=900,
	    # height=500,
	    title="Енергетична характеристика ВЕУ (" + name + ")",
	    xaxis=dict(
	        title="Швидкість вітру, м/с"
	    ),
	    yaxis=dict(
	        title="Потужність, кВт"
	    )
	)
	fig = go.Figure(data=data, layout=layout)
	if pdf:
		fig.write_image("report_images/laba4.png")
	plot_div = plot(fig, output_type='div', include_plotlyjs=False)
	return (plot_div, xnew, ynew)

def speed(x, height):
	speed_list = []
	for i in x:
		speed_list.append(round((i * (height/10)**0.14),2))
	return speed_list

def energy(list_dict, height, xnew, ynew):
	d = {}
	for i in list_dict:
	    if i['FF'] in d:
	        tm3 = timedelta(hours=0, minutes=30, seconds=0)
	        d[i['FF']] = d[i['FF']] + tm3
	    else:
	    	if i['FF'] * (height/10)**0.14 >= min(xnew):
	        	d[i['FF']] = timedelta(hours=0, minutes=30, seconds=0)


	x = [ i for i in d.keys() ]
	x = speed(x, height)
	y = [ i.days * 24 + i.seconds/3600 if i.days != 0 else i.seconds / 3600 for i in d.values() ]
	xnew = [ round(i,2) for i in xnew]
	x_min = min(xnew)
	power = []
	for i in x:
		index = xnew.index(i)
		power.append(ynew[index])

	energy = []
	for i,j in zip(power, y):
		energy.append(i*j)
	return sum(energy)


#x, y = [], []
#with open("g1.txt") as file:
#  for row in file:
#    x.append(float(row.split()[0]))
#    y.append(float(row.split()[1]))
