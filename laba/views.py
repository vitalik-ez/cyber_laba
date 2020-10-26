from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from django.views.generic import TemplateView

from django.views import View

from .import plots
from .import laba2cal

import plotly.graph_objs as go
from plotly.offline import plot

from django.shortcuts import redirect

import sqlite3
from collections import Counter

from datetime import datetime 

from .forms import Laba2Form

import site1

def main_form(request):
	return render(request, 'date.html', {'media': site1.settings.MEDIA_ROOT})

class FormView(View):

	def get(self, request):
		
		data1 = request.session['data_1']
		data2 = request.session['data_2']

		if data1 == None:
			return render(request, 'graphics.html', {}) 

		datetimeObj_1 = datetime.strptime(data1, '%d/%m/%Y %H:%M')
		datetimeObj_2 = datetime.strptime(data2, '%d/%m/%Y %H:%M')
		
		list_dict = plots.dataSampling(datetimeObj_1, datetimeObj_2)
		graphic_1 = plots.graphic_1(list_dict, data1, data2)
		graphic_2, x, y = plots.graphic_2(list_dict)
		graphic_3 = plots.graphic_3(list_dict)
		graphic_4 = plots.graphic_4(list_dict)

		graphic_5 = plots.graphic_5(datetimeObj_1, datetimeObj_2)
		graphic_6 = plots.graphic_6(datetimeObj_1, datetimeObj_2)

		z = [ (i,j) for i,j in zip(x,y)]

		context = {'data1': data1, 'data2': data2, 'graphic_1': graphic_1,
		'graphic_2': graphic_2,'graphic_3': graphic_3,'graphic_4': graphic_4, 'graphic_5': graphic_5,
		 'graphic_6': graphic_6, 'z':z}
		return render(request, 'graphics.html', context)

	def post(self, request):
		if 'laba1' in request.POST:
			datetimeObj_1 = datetime.strptime(request.POST.get('date_1'), '%d/%m/%Y %H:%M')
			datetimeObj_2 = datetime.strptime(request.POST.get('date_2'), '%d/%m/%Y %H:%M')
			
			request.session['data_1'] = request.POST.get('date_1')
			request.session['data_2'] = request.POST.get('date_2')

			list_dict = plots.dataSampling(datetimeObj_1, datetimeObj_2)
			graphic_1 = plots.graphic_1(list_dict, request.POST.get('date_1'), request.POST.get('date_2'))
			graphic_2, x, y = plots.graphic_2(list_dict)
			graphic_3 = plots.graphic_3(list_dict)
			graphic_4 = plots.graphic_4(list_dict)

			graphic_5 = plots.graphic_5(datetimeObj_1, datetimeObj_2)
			graphic_6 = plots.graphic_6(datetimeObj_1, datetimeObj_2)

			z = [ (i,j) for i,j in zip(x,y)]

			context = {'data1': request.POST.get('date_1'), 'data2': request.POST.get('date_2'), 'graphic_1': graphic_1,
			'graphic_2': graphic_2,'graphic_3': graphic_3,'graphic_4': graphic_4, 'graphic_5': graphic_5,
			 'graphic_6': graphic_6, 'z':z}
			return render(request, 'graphics.html', context)
		else:
			request.session['data_1'] = request.POST.get('date_1')
			request.session['data_2'] = request.POST.get('date_2')
			return redirect('/laba/laba2')

class FormView2(View):

	def get(self, request):

		data1 = request.session['data_1']
		data2 = request.session['data_2']

		if data1 == None:
			return render(request, 'laba2.html', {}) 

		if 'heat_lost' not in request.session:
			laba2Form = Laba2Form()
			context = {'data1': data1, 'data2':data2, 'form': laba2Form}
			return render(request, 'laba2.html', context)
		else:
			print("POST Перейти по вкладці зчитати введені раніше дані і відобразити")
			datetimeObj_1 = datetime.strptime(data1, '%d/%m/%Y %H:%M')
			datetimeObj_2 = datetime.strptime(data2, '%d/%m/%Y %H:%M')

			list_dict = laba2cal.dataForLaba2(datetimeObj_1, datetimeObj_2)
			
			graphic = laba2cal.graphic(float(request.session['heat_lost']), float(request.session['house_area']), float(request.session['air_temperature']))
			energy_loss = laba2cal.getEnergyLoss(list_dict, float(request.session['heat_lost']), float(request.session['house_area']), float(request.session['air_temperature']))

			gvp = laba2cal.GVP(request)
			tariff = float(request.session['tariff'])
			tariff_gas = float(request.session['tariff_gas'])
			tariff_coal = float(request.session['tariff_coal'])
			tariff_briquettes = float(request.session['tariff_briquettes'])
			tariff_oak = float(request.session['tariff_oak'])
			tariff_electricity = float(request.session['tariff_electricity'])
			tariffs = [tariff, tariff_gas, tariff_coal, tariff_briquettes, tariff_oak, tariff_electricity]
			histogram = laba2cal.histogram(gvp[1], energy_loss, tariff, tariff_gas, tariff_coal, tariff_briquettes, tariff_oak, tariff_electricity)

			context = {'graphic': graphic, 'energy_loss': energy_loss, 'data_1': data1, 'data_2': data2,
						'gvp':gvp[0], 'histogram':histogram, 'tariff':tariff, 'tariffs': tariffs, 'histogram_price': laba2cal.histogram_price()}
			return render(request, 'laba2calculation.html', context)


	def post(self, request):
		writeToSessionLaba2(request)
		data1 = request.session['data_1']
		data2 = request.session['data_2']

		datetimeObj_1 = datetime.strptime(data1, '%d/%m/%Y %H:%M')
		datetimeObj_2 = datetime.strptime(data2, '%d/%m/%Y %H:%M')

		list_dict = laba2cal.dataForLaba2(datetimeObj_1, datetimeObj_2)
		
		graphic = laba2cal.graphic(float(request.POST.get('heat_lost')), float(request.POST.get('house_area')), float(request.POST.get('air_temperature')))
		energy_loss = laba2cal.getEnergyLoss(list_dict, float(request.POST.get('heat_lost')), float(request.POST.get('house_area')), float(request.POST.get('air_temperature')))

		gvp = laba2cal.GVP(request)
		tariff = float(request.session['tariff'])
		tariff_gas = float(request.session['tariff_gas'])
		tariff_coal = float(request.session['tariff_coal'])
		tariff_briquettes = float(request.session['tariff_briquettes'])
		tariff_oak = float(request.session['tariff_oak'])
		tariff_electricity = float(request.session['tariff_electricity'])
		tariffs = [tariff, tariff_gas, tariff_coal, tariff_briquettes, tariff_oak, tariff_electricity]
		histogram = laba2cal.histogram(gvp[1], energy_loss, tariff, tariff_gas, tariff_coal, tariff_briquettes, tariff_oak, tariff_electricity)

		context = {'graphic': graphic, 'energy_loss': energy_loss, 'data_1': data1, 'data_2': data2,
					'gvp':gvp[0], 'histogram':histogram, 'tariff':tariff, 'tariffs': tariffs, 'histogram_price': laba2cal.histogram_price()}
		return render(request, 'laba2calculation.html', context)



def writeToSessionLaba2(request):
	request.session['heat_lost'] = request.POST.get('heat_lost')
	request.session['house_area'] = request.POST.get('house_area')
	request.session['number_people'] = request.POST.get('number_people')
	request.session['incoming_temperature'] = request.POST.get('incoming_temperature')
	request.session['end_temperature'] = request.POST.get('end_temperature')
	request.session['shower_temperature'] = request.POST.get('shower_temperature')
	request.session['count_shower'] = request.POST.get('count_shower')
	request.session['bath_temperature'] = request.POST.get('bath_temperature')
	request.session['count_bath'] = request.POST.get('count_bath')
	request.session['air_temperature'] = request.POST.get('air_temperature')
	request.session['count_litters_shower'] = request.POST.get('count_litters_shower')
	request.session['count_litters_bath'] = request.POST.get('count_litters_bath')
	if request.POST.get('duration') != None:
		request.session['duration'] = request.POST.get('duration')
	else:
		request.session['power'] = request.POST.get('power')

	request.session['tariff'] = request.POST.get('tariff')
	request.session['tariff_gas'] = request.POST.get('tariff_gas')
	request.session['tariff_coal'] = request.POST.get('tariff_coal')
	request.session['tariff_briquettes'] = request.POST.get('tariff_briquettes')
	request.session['tariff_oak'] = request.POST.get('tariff_oak')
	request.session['tariff_electricity'] = request.POST.get('tariff_electricity')

def clear_session(request):
	del request.session['heat_lost']
	if 'duration' in request.session:
		del request.session['duration']
	if 'power' in request.session:
		del request.session['power']
	return HttpResponseRedirect('/laba/laba2')

def check_bd(request):
	conn = sqlite3.connect("main.db")
	cursor = conn.cursor()
	month_table = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	error = 0
	error_day = 0
	check_month = []
	for i in month_table:
	    sql = f"SELECT * from {i} WHERE number_month IS NULL OR T IS NULL"
	    cursor.execute(sql)
	    data = cursor.fetchall()
	    error += len(data)
	    j = 0
	    while j < len(data):
	        sql = f"SELECT * from {i} WHERE id > {data[j][0]} AND T NOT NULL LIMIT 1"
	        cursor.execute(sql)
	        row = cursor.fetchall()
	        if row[0][0]-data[j][0] == 1:
	            print(" Брати попереднє значення")
	            sql = f"SELECT T from {i} WHERE id = {data[j][0] - 1} AND T NOT NULL"
	            cursor.execute(sql)
	            value_1 = cursor.fetchall()
	            sql = f"SELECT T from {i} WHERE id = {data[j][0] + 1} AND T NOT NULL"
	            cursor.execute(sql)
	            value_2 = cursor.fetchall()
	            value_average = (value_1[0][0] + value_2[0][0])/2
	            sql = f"UPDATE {i} SET T = '{value_average}' WHERE id = {data[j][0]}"
	            cursor.execute(sql)
	            conn.commit()
	        else:
	            sql = f"SELECT T from {i} WHERE id = {data[j][0] - 1} AND T NOT NULL"
	            cursor.execute(sql)
	            value_1 = cursor.fetchall()
	            sql = f"SELECT T from {i} WHERE id = {row[0][0]} AND T NOT NULL"
	            cursor.execute(sql)
	            value_2 = cursor.fetchall()
	            d = (row[0][0] - data[j][0])
	            print("d =", d)
	            if d % 2 == 0:
	                d = d / 2
	            else:
	                d = d / 2 + 0.5
	            sql = f"UPDATE {i} SET T = '{value_1[0][0]}' WHERE id >= {data[j][0]} AND id < {data[j][0] + d}"
	            cursor.execute(sql)
	            conn.commit()
	            sql = f"UPDATE {i} SET T = '{value_2[0][0]}' WHERE id >= {data[j][0] + d} AND id <= {row[0][0] - 1}"
	            cursor.execute(sql)
	            conn.commit()
	            j += row[0][0] - data[j][0] - 1
	        j += 1

	    sql = f"SELECT number_month from {i}"
	    cursor.execute(sql)
	    data = cursor.fetchall()
	    list_day = []
	    for i in data:
	        list_day.append(i[0])
	    c = Counter(list_day)
	    check = [ True  for i in range(data[0][0],data[-1][0] + 1) if c[i] == 48]
	    check = True if len(check) == data[-1][0] else False
	    check_month.append(check)
	if all(check_month):
	    error_day = "Всі дні та всі часи"
	else:
	    error_day = "Перевірте всі дні та години в БД"

	for i in month_table:
	    sql = f"SELECT * from {i} WHERE FF < 0"
	    cursor.execute(sql)
	    data = cursor.fetchall()
	    j = 0
	    while j < len(data):
	    	ff = data[j][5] * (-1)
	    	sql = f"UPDATE {i} SET FF = '{ff}' WHERE id = {data[j][0]}"

	    	cursor.execute(sql)
	    	conn.commit()
	    	j += 1

	conn.close()
	return redirect('/laba/check_error')



def сheck_error(request):
	conn = sqlite3.connect("main.db")
	cursor = conn.cursor()
	month_table = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	error = 0
	error_day, error_speed, error_speed_list = 0, 0, []
	error_list = []
	check_month = []
	for i in month_table:
	    sql = f"SELECT * from {i} WHERE number_month IS NULL OR T IS NULL OR FF IS NULL"
	    cursor.execute(sql)
	    data = cursor.fetchall()
	    error += len(data)
	    if len(data) > 0:
	    	error_list.append(str(data[0][1]) + " " + i + " " + data[0][2] + "  T=" + str(data[0][3]))
	    
	    sql = f"SELECT number_month from {i}"
	    cursor.execute(sql)
	    data = cursor.fetchall()
	    list_day = []
	    for i in data:
	        list_day.append(i[0])
	    c = Counter(list_day)
	    check = [ True  for i in range(data[0][0],data[-1][0] + 1) if c[i] == 48]
	    check = True if len(check) == data[-1][0] else False
	    check_month.append(check)
	if all(check_month):
	    error_day = "Всі дні та всі часи"
	else:
	    error_day = "Перевірте всі дні та години в БД"

	for i in month_table:
	    sql = f"SELECT * from {i} WHERE FF < 0"
	    cursor.execute(sql)
	    data = cursor.fetchall()
	    error_speed += len(data)
	    if len(data) > 0:
	    	error_speed_list.append(str(data[0][1]) + " " + i + " " + data[0][2] + " FF=" + str(data[0][5]))

	conn.close()
	
	if error == 0 and error_day == "Всі дні та всі часи" and error_speed == 0:
		errors = {'succeed': 'Всі дані в базі даних перевірені. Пропусків в даті та часі немає. Все вірно'}
	else:
		if error != 0:
			error = 'Пропуски в стовпці температури: ' + str(error)
		if error_day == "Перевірте всі дні та години в БД":
			error_day = 'Пропусків в даті та часі: ' + str(error_day)
		if error_speed !=0:
			error_speed = "Від'ємні значення у стовпці швидкості вітру: " + str(error_speed)
		return render(request, 'check_bd.html', { 'error_t': error, 'error_day': error_day,'error_list': error_list, 'error_speed':error_speed, 'error_speed_list':error_speed_list})
	return render(request, 'check_bd.html', errors)

from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa



def getpdfPageLaba2(request):
	template = get_template('pdfLaba2.html')
	html  = template.render(calculationLaba2(request))
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	else:
		return HttpResponse('ERROR GENERATING PDF')


def calculationLaba2(request):
	data1 = request.session['data_1']
	data2 = request.session['data_2']

	datetimeObj_1 = datetime.strptime(data1, '%d/%m/%Y %H:%M')
	datetimeObj_2 = datetime.strptime(data2, '%d/%m/%Y %H:%M')

	list_dict = laba2cal.dataForLaba2(datetimeObj_1, datetimeObj_2)
	
	graphic = laba2cal.graphic(float(request.session['heat_lost']), float(request.session['house_area']), float(request.session['air_temperature']), True)
	energy_loss = laba2cal.getEnergyLoss(list_dict, float(request.session['heat_lost']), float(request.session['house_area']), float(request.session['air_temperature']))

	gvp = laba2cal.GVP(request)
	tariff = float(request.session['tariff'])
	tariff_gas = float(request.session['tariff_gas'])
	tariff_coal = float(request.session['tariff_coal'])
	tariff_briquettes = float(request.session['tariff_briquettes'])
	tariff_oak = float(request.session['tariff_oak'])
	tariff_electricity = float(request.session['tariff_electricity'])
	tariffs = [tariff, tariff_gas, tariff_coal, tariff_briquettes, tariff_oak, tariff_electricity]
	histogram = laba2cal.histogram(gvp[1], energy_loss, tariff, tariff_gas, tariff_coal, tariff_briquettes, tariff_oak, tariff_electricity, True)

	return {'graphic': graphic, 'energy_loss': energy_loss, 'data_1': data1, 'data_2': data2,
				'gvp':gvp[0], 'histogram':histogram, 'tariff':tariff, 'tariffs': tariffs, 'media': site1.settings.MEDIA_ROOT, 'histogram_price': laba2cal.histogram_price(True)}