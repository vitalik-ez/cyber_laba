from datetime import datetime, timedelta

import plotly.graph_objs as go
from plotly.offline import plot


def graphics(request, device):
	x = []
	y = []
	
	request.session[device['name']] = {}
	days_of_week = ["Понеділок", "Вівторок", "Середа", "Четверг", "П'ятниця","Субота", "Неділя"]
	for index,day in enumerate(days_of_week):
		count = 0
		start = datetime.strptime(device['time_start'][index], '%H:%M').time()
		end = datetime.strptime(device['time_end'][index], '%H:%M').time()
		time_break = datetime.strptime(device['time_break'][index], '%H:%M').time()

		duration = timedelta(minutes = device['duration'])
		delta = timedelta(hours=start.hour, minutes=start.minute)
		start_delta = timedelta(hours=0, minutes=0)
		range_delta = timedelta(hours=0, minutes=30)

		for i in range(48):
			if start_delta <= delta <= start_delta+range_delta and delta <= timedelta(hours=end.hour, minutes=end.minute):
				count += 1
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
						request.session['histogram_pick'][day][str(delta_gen)] = device['power'] / 1000
						delta_gen += range_gen
				else:
					delta_gen = delta
					range_gen = timedelta(hours=0, minutes=1)
					
					while delta_gen <= delta + duration:
						if str(delta_gen) in request.session['GEN'][day]:
							request.session['GEN'][day][str(delta_gen)] += device['power'] * device['duration'] / 60 / 1000
						else:
							request.session['GEN'][day][str(delta_gen)] = device['power'] * device['duration'] / 60 / 1000

						if str(delta_gen) in request.session['histogram_pick'][day]:
							request.session['histogram_pick'][day][str(delta_gen)] += device['power'] / 1000
						else:
							request.session['histogram_pick'][day][str(delta_gen)] = device['power'] / 1000
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
		

		request.session[device['name']][day] = count	

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
	        title="Обсяг енергії, кВт*год"
	    )
	)
	fig = go.Figure(data=data, layout=layout)

	plot_div = plot(fig, output_type='div', include_plotlyjs=False)
	return plot_div



def GEN_graphic(request, days_of_week):
	for day in days_of_week:
		sort_dict_not = { str(datetime.strptime(i, '%H:%M:%S').time()): request.session['GEN'][day][i]  for i in request.session['GEN'][day]}
		dictionary = sort_dict_not
		list_keys = list(dictionary.keys())
		list_keys.sort()
		sort_dict = {}
		for i in list_keys:
		    sort_dict[i] = sort_dict_not[i]
		request.session['GEN'][day] = sort_dict
	trace1 = go.Scatter(
	    x=[ str(j) + " " + i for i in request.session['GEN'] for j in request.session['GEN'][i] ],
	   	y=[ j for i in request.session['GEN'] for j in request.session['GEN'][i].values() ]
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



def histogram(request, days_of_week, device):

	y = []
	for day in days_of_week:
		y.append(sum(request.session['GEN'][day].values()))
		#print(request.session['GEN'][day])

	result = days_of_week[y.index(max(y))]
	#result = days_of_week.index(result)
	#print(result)
	#print(device)
	device_energy = []
	for i in device:
		
		start = datetime.strptime(device[i]['time_start'][y.index(max(y))], '%H:%M').time()
		end = datetime.strptime(device[i]['time_end'][y.index(max(y))], '%H:%M').time()
		time_break = datetime.strptime(device[i]['time_break'][y.index(max(y))], '%H:%M').time()

		duration = timedelta(minutes = device[i]['duration'])
		delta = timedelta(hours=start.hour, minutes=start.minute)

		#start = timedelta(hours=start.hour, minutes=start.minute)
		end = timedelta(hours=end.hour, minutes=end.minute)
		time_break = timedelta(hours=time_break.hour, minutes=time_break.minute)

		range_gen = timedelta(hours=0, minutes=1)
		current = []
		while delta <= end:
			
			
			delta_gen = delta
			while delta_gen <= delta + duration:
				current.append(device[i]['power'] * device[i]['duration'] / 60 / 1000)
				delta_gen += range_gen

			delta = delta_gen + time_break
		device_energy.append(sum(current))

		print(start)
		print(end)

	print(device_energy)

	result_list = []
	for index,i in enumerate(device):
		result_list.append((device[i]['name'], request.session[device[i]['name']][result], round(device_energy[index],3)))
		#print(device[i]['name'], request.session[device[i]['name']][result])

	trace1 = go.Bar(x=days_of_week, y=y)

	data=go.Data([trace1])
	layout=go.Layout(title="Обсяги споживання електричної енергії (кВтˑгод) для кожної доби тижня", xaxis={'title':"Дні тижня"}, yaxis={'title':'Електрична енергія (кВтˑгод)'})
	figure=go.Figure(data=data,layout=layout)
	plot_div = plot(figure, auto_open=False, output_type='div')

	return (plot_div, result_list, result)

def cost(request, days_of_week):
	price_1, price_2, price_3 = 0,0,0

	count_electricity = []
	for day in days_of_week:
		count_electricity.append(sum(request.session['GEN'][day].values()))
	month = sum(count_electricity) * 4
	
	if month <= 100:
		price_1 = month * float(request.session['tariff_laba3']['tariff_to_100']) / 100
	else:
		price_1 = month * float(request.session['tariff_laba3']['tariff_after_100'])/ 100
	print(price_1)


	suma_to_point_1 = 0
	suma_point_1_to_point_2 = 0
	for day in days_of_week:
		point_1 = timedelta(hours=7, minutes=0)
		point_2 = timedelta(hours=23, minutes=0)
		for i in request.session['GEN'][day]:
			time_current = datetime.strptime(i, '%H:%M:%S').time()
			time_current = timedelta(hours=time_current.hour, minutes=time_current.minute)
			if time_current < point_1 or time_current > point_2:
				suma_to_point_1 += request.session['GEN'][day][i]
			else:
				suma_point_1_to_point_2 += request.session['GEN'][day][i]

	if suma_to_point_1 + suma_point_1_to_point_2 <= 100:
		price_2 = 4 * (0.7 * float(request.session['tariff_laba3']['tariff_to_100']) / 100 * suma_to_point_1 + float(request.session['tariff_laba3']['tariff_to_100']) / 100 * suma_point_1_to_point_2)
	else:
		price_2 = 4 * (0.7 * float(request.session['tariff_laba3']['tariff_after_100']) / 100 * suma_to_point_1 + float(request.session['tariff_laba3']['tariff_after_100']) / 100 * suma_point_1_to_point_2)
	print(price_2)


	tariff_0_4 = 0
	tariff_1_5 = 0
	tariff_1_0 = 0
	
	for day in days_of_week:
		point_1 = timedelta(hours=7, minutes=0)
		point_2 = timedelta(hours=8, minutes=0)
		point_3 = timedelta(hours=11, minutes=0)
		point_4 = timedelta(hours=20, minutes=0)
		point_5 = timedelta(hours=22, minutes=0)
		point_6 = timedelta(hours=23, minutes=0)
		for i in request.session['GEN'][day]:
			time_current = datetime.strptime(i, '%H:%M:%S').time()
			time_current = timedelta(hours=time_current.hour, minutes=time_current.minute)
			if time_current < point_1 or time_current >= point_6:
				tariff_0_4 += request.session['GEN'][day][i]
			elif point_1 <= time_current < point_2 or point_3 <= time_current < point_4 or point_5 <= time_current < point_6:
				tariff_1_0 += request.session['GEN'][day][i]
			elif point_2 <= time_current < point_3 or point_4 <= time_current < point_5:
				tariff_1_5 += request.session['GEN'][day][i]

	if tariff_0_4 + tariff_1_5 + tariff_1_0 <= 100:
		price_3 = 4 * (0.4 * float(request.session['tariff_laba3']['tariff_to_100']) / 100 * tariff_0_4 + float(request.session['tariff_laba3']['tariff_to_100']) / 100 * tariff_1_0 + 1.5 * float(request.session['tariff_laba3']['tariff_to_100']) / 100 * tariff_1_5)
	else:
		price_3 = 4 * (0.4 * float(request.session['tariff_laba3']['tariff_after_100']) / 100 * tariff_0_4 + float(request.session['tariff_laba3']['tariff_after_100']) / 100 * tariff_1_0 + 1.5 * float(request.session['tariff_laba3']['tariff_after_100']) / 100 * tariff_1_5)
	print(price_3)

	price_list = [round(price_1,2), round(price_2,2), round(price_3,2)]
	index_min = price_list.index(min(price_list))
	if index_min == 0:
		result = 'однозонний тариф'
	elif index_min == 1:
		result = 'двозонний тариф'
	else:
		result = 'тризонний тариф'


	trace1 = go.Bar(x=['Однозонний тариф', 'Двозонний тариф', 'Тризонний тариф'], y=price_list)

	data=go.Data([trace1])
	layout=go.Layout(title="Обсяги витрат коштів (грн) на електричну енергії за однозонним, двозонним та тризонним тарифними планами",font=dict(size=11), xaxis={'title':"Тарифний план"}, yaxis={'title':'Вартість, грн'})
	figure=go.Figure(data=data,layout=layout)
	plot_div = plot(figure, auto_open=False, output_type='div')

	return (price_list, result, plot_div)



def histogram_pick(request, days_of_week):

	y = []
	for day in days_of_week:
		y.append(max(request.session['histogram_pick'][day].values()))
		#print(request.session['GEN'][day])

	#result = days_of_week[y.index(max(y))]
	#result_list = []
	#or i in device:
	#	result_list.append((device[i]['name'], request.session[device[i]['name']][result]))
		#print(device[i]['name'], request.session[device[i]['name']][result])

	trace1 = go.Bar(x=days_of_week, y=y)

	data=go.Data([trace1])
	layout=go.Layout(title="Максимальні пікові значення потужності споживання (кВт) для кожної доби тижня", xaxis={'title':"Дні тижня"}, yaxis={'title':'Потужність, кВт'})
	figure=go.Figure(data=data,layout=layout)
	plot_div = plot(figure, auto_open=False, output_type='div')

	return plot_div