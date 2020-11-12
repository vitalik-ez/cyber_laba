from datetime import datetime, timedelta

import plotly.graph_objs as go
from plotly.offline import plot


def graphics(request, device):
	x = []
	y = []
	days_of_week = ["Понеділок", "Вівторок", "Середа", "Четверг", "П'ятниця","Субота", "Неділя"]
	for index,day in enumerate(days_of_week):
		
		start = datetime.strptime(device['time_start'][index], '%H:%M').time()
		end = datetime.strptime(device['time_end'][index], '%H:%M').time()
		time_break = datetime.strptime(device['time_break'][index], '%H:%M').time()

		duration = timedelta(minutes = device['duration'])
		delta = timedelta(hours=start.hour, minutes=start.minute)
		start_delta = timedelta(hours=0, minutes=0)
		range_delta = timedelta(hours=0, minutes=30)

		


		for i in range(48):
			if start_delta <= delta <= start_delta+range_delta and delta <= timedelta(hours=end.hour, minutes=end.minute):
				x.append(str(delta) + " (" + day + ")")
				y.append(0)
				x.append(str(delta) + " (" + day + ")")
				y.append(device['power'] * device['duration'] / 60 / 1000) # * device['duration'] / 60
				x.append(str(delta + duration)  + " (" + day + ")")
				y.append(device['power'] * device['duration'] / 60 / 1000) # * device['duration'] / 60
				x.append(str(delta + duration)  + " (" + day + ")")
				y.append(0)

				if str(delta) not in request.session['GEN'][day]:

					# встановлюю по хвилино для тривалості
					delta_gen = delta
					range_gen = timedelta(hours=0, minutes=1)
					while delta_gen <= delta + duration:
						request.session['GEN'][day][str(delta_gen)] = device['power'] * device['duration'] / 60 / 1000
						delta_gen += range_gen
				else:
					delta_gen = delta
					range_gen = timedelta(hours=0, minutes=1)
					
					while delta_gen <= delta + duration:
						if str(delta_gen) in request.session['GEN'][day]:
							request.session['GEN'][day][str(delta_gen)] += device['power'] * device['duration'] / 60 / 1000
						else:
							request.session['GEN'][day][str(delta_gen)] = device['power'] * device['duration'] / 60 / 1000
						delta_gen += range_gen
					


				delta += duration + timedelta(hours=time_break.hour, minutes=time_break.minute)
				start_delta += range_delta
			else:
				x.append(str(start_delta) + " (" + day + ")")
				y.append(0)

				if str(start_delta) not in request.session['GEN'][day]:
					request.session['GEN'][day][str(start_delta)] = 0
				#else:
				#	request.session['GEN'][day][str(start_delta)] += device['power'] * device['duration'] / 60 / 1000

				start_delta += range_delta

			#print(request.session['GEN'][day])
			#print(str(delta))
			

	trace1 = go.Scatter(
	    x=x,
	    y=y
	)

	data = [trace1]
	layout = go.Layout(
	    # autosize=False,
	    # width=900,
	    # height=500,
	    title=device['name'],
	    xaxis=dict(
	        title="Дата"
	    ),
	    yaxis=dict(
	        title="Потужність, кВт"
	    )
	)
	fig = go.Figure(data=data, layout=layout)

	plot_div = plot(fig, output_type='div', include_plotlyjs=False)
	return plot_div



def GEN_graphic(request):
	days_of_week = ["Понеділок", "Вівторок", "Середа", "Четверг", "П'ятниця","Субота", "Неділя"]
	x = [0]
	y = [0]
	#print(list(request.session['GEN']["Понеділок"].keys()))
	#print([ str(j) + " " + i for i in request.session['GEN'] for j in request.session['GEN'][i] ])
	#print([ j for i in request.session['GEN'] for j in request.session['GEN'][i].values() ])
	#for i in sorted(request.session['GEN']["Понеділок"]):
	for day in days_of_week:
		sort_dict_not = { str(datetime.strptime(i, '%H:%M:%S').time()): request.session['GEN'][day][i]  for i in request.session['GEN'][day]}
		dictionary = sort_dict_not
		list_keys = list(dictionary.keys())
		list_keys.sort()
		sort_dict = {}
		for i in list_keys:
		    sort_dict[i] = sort_dict_not[i]
		request.session['GEN'][day] = sort_dict
	#print(i)
	trace1 = go.Scatter(
	    #x=[ i for i in [list(request.session['GEN'][day].keys()) for day in days_of_week]],
	    #y=[ i for i in [list(request.session['GEN'][day].values()) for day in days_of_week]]
	    x=[ str(j) + " " + i for i in request.session['GEN'] for j in request.session['GEN'][i] ],
	   	y=[ j for i in request.session['GEN'] for j in request.session['GEN'][i].values() ]
	   	#x=x,
	   	#y=y
	)

	data = [trace1]
	layout = go.Layout(
	    # autosize=False,
	    # width=900,
	    # height=500,
	    title="Графік електричного навантаження (ГЕН)",
	    xaxis=dict(
	        title="Дата"
	    ),
	    yaxis=dict(
	        title="Потужність, кВт*год"
	    )
	)
	fig = go.Figure(data=data, layout=layout)

	plot_div = plot(fig, output_type='div', include_plotlyjs=False)
	return plot_div
