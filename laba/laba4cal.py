from scipy import interpolate
import numpy as np
import xlrd
import plotly.graph_objs as go
from plotly.offline import plot


def graphic_1():
	rb = xlrd.open_workbook('energy_characteristic/v110-2.0 MW.xls',formatting_info=True)
	sheet = rb.sheet_by_index(0)

	x, y = [], []
	for rownum in range(2, sheet.nrows):
	  x.append(round(sheet.row_values(rownum)[0], 2))
	  y.append(round(sheet.row_values(rownum)[1], 2))

	f = interpolate.interp1d(x, y)


	xnew = np.arange(x[0], x[-1], 0.01)
	ynew = f(xnew)
	#plt.plot(x, y, 'o', xnew, ynew, '-')
	#plt.show()

	print(xnew[:10])
	print(ynew[:10])

	trace1 = go.Scatter(
	    x=x,
	    y=y
	)

	data = [trace1]
	layout = go.Layout(
	    # autosize=False,
	    # width=900,
	    # height=500,
	    title="ASasAS",
	    xaxis=dict(
	        title="Дата"
	    ),
	    yaxis=dict(
	        title="Обсяг енергії, кВт*год"
	    )
	)
	fig = go.Figure(data=data, layout=layout)

	plot_div = plot(fig, output_type='div', include_plotlyjs=False)
	return plot_div



#x, y = [], []
#with open("g1.txt") as file:
#  for row in file:
#    x.append(float(row.split()[0]))
#    y.append(float(row.split()[1]))
