from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from django.views.generic import TemplateView

from django.views import View

from .import plots
from .import laba2cal
from .import laba3cal
from .import laba4cal

import plotly.graph_objs as go
from plotly.offline import plot

from django.shortcuts import redirect

import sqlite3
from collections import Counter

from datetime import datetime 

from .forms import Laba2Form

import site1

from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

#laba3-4
from .models import *
from .forms import *

def main_form(request):
	return render(request, 'date.html', {'media': site1.settings.MEDIA_ROOT})


def laba1(request):
	datetimeObj_1 = datetime.strptime(str(request.session['data_1']), '%d/%m/%Y %H:%M')
	datetimeObj_2 = datetime.strptime(str(request.session['data_2']), '%d/%m/%Y %H:%M')	
	list_dict = plots.dataSampling(datetimeObj_1, datetimeObj_2)
	graphic_1 = plots.graphic_1(list_dict, str(request.session['data_1']), str(request.session['data_2']))
	graphic_2, x, y = plots.graphic_2(list_dict)
	graphic_3 = plots.graphic_3(list_dict)
	graphic_4 = plots.graphic_4(list_dict)

	graphic_5 = plots.graphic_5(datetimeObj_1, datetimeObj_2)
	graphic_6 = plots.graphic_6(datetimeObj_1, datetimeObj_2)

	z = [ (i,j) for i,j in zip(x,y)]

	context = {'data1': request.POST.get('date_1'), 'data2': request.POST.get('date_2'), 'graphic_1': graphic_1,
	'graphic_2': graphic_2,'graphic_3': graphic_3,'graphic_4': graphic_4, 'graphic_5': graphic_5,
	 'graphic_6': graphic_6, 'z':z}

	return context

class FormView(View):

	def get(self, request):
		
		data1 = request.session['data_1']
		data2 = request.session['data_2']

		if data1 == None:
			return render(request, 'graphics.html', {}) 

		return render(request, 'graphics.html', laba1(request))

	def post(self, request):
		if 'laba1' in request.POST:
			
			request.session['data_1'] = request.POST.get('date_1')
			request.session['data_2'] = request.POST.get('date_2')
			
			return render(request, 'graphics.html', laba1(request))
		elif 'laba2' in request.POST:
			request.session['data_1'] = request.POST.get('date_1')
			request.session['data_2'] = request.POST.get('date_2')
			return redirect('/laba/laba2')
		elif 'laba3' in request.POST:
			print(123)
			return redirect('/laba/laba3')
		else:
			request.session['data_1'] = request.POST.get('date_1')
			request.session['data_2'] = request.POST.get('date_2')
			return redirect('/laba/laba4')


def laba2(data1, data2, request, pdf=False):
	datetimeObj_1 = datetime.strptime(data1, '%d/%m/%Y %H:%M')
	datetimeObj_2 = datetime.strptime(data2, '%d/%m/%Y %H:%M')

	list_dict = laba2cal.dataForLaba2(datetimeObj_1, datetimeObj_2)
	
	graphic = laba2cal.graphic(float(request.session['heat_lost']), float(request.session['house_area']), float(request.session['air_temperature']), pdf)
	energy_loss = laba2cal.getEnergyLoss(list_dict, float(request.session['heat_lost']), float(request.session['house_area']), float(request.session['air_temperature']))

	gvp = laba2cal.GVP(request)
	tariff = float(request.session['tariff'])
	tariff_gas = float(request.session['tariff_gas'])
	tariff_coal = float(request.session['tariff_coal'])
	tariff_briquettes = float(request.session['tariff_briquettes'])
	tariff_oak = float(request.session['tariff_oak'])
	tariff_electricity = float(request.session['tariff_electricity'])
	tariffs = [tariff, tariff_gas, tariff_coal, tariff_briquettes, tariff_oak, tariff_electricity]
	histogram = laba2cal.histogram(gvp[1], energy_loss, tariff, tariff_gas, tariff_coal, tariff_briquettes, tariff_oak, tariff_electricity, pdf)
	if pdf:
		return {'graphic': graphic, 'energy_loss': energy_loss, 'data_1': data1, 'data_2': data2,
					'gvp':gvp[0], 'histogram':histogram, 'tariff':tariff, 'tariffs': tariffs, 'media': site1.settings.MEDIA_ROOT, 'histogram_price': laba2cal.histogram_price(True)}
	context = {'graphic': graphic[0], 'energy_loss': energy_loss, 'data_1': data1, 'data_2': data2,
				'gvp':gvp[0], 'histogram':histogram, 'tariff':tariff, 'tariffs': tariffs, 'histogram_price': laba2cal.histogram_price(), 'Q': graphic[1]}
	return context

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
			return render(request, 'laba2calculation.html', laba2(data1, data2, request))


	def post(self, request):
		writeToSessionLaba2(request)
		data1 = request.session['data_1']
		data2 = request.session['data_2']
		return render(request, 'laba2calculation.html', laba2(data1, data2, request))


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


class FormView3(View):
	def get(self, request):
		data = electricalAppliances.objects.all()
		return render(request, 'laba3.html', {'data': data})

	def post(self, request):
		if len(request.POST.getlist('choices')) == 0:
			data = electricalAppliances.objects.all()
			return render(request, 'laba3.html', {'data': data})
		data = electricalAppliances.objects.filter(pk__in=request.POST.getlist('choices'))
		days_of_week = ["Понеділок", "Вівторок", "Середа", "Четверг", "Пятниця","Субота", "Неділя"]
		request.session['id_device'] = request.POST.getlist('choices')
		request.session['tariff_laba3'] = {'tariff_to_100': request.POST.get('tariff_to_100'),
										   'tariff_after_100': request.POST.get('tariff_after_100'),
										   'night_two': request.POST.get('night_two'),
										   'day_two': request.POST.get('day_two'),
										   'night_three': request.POST.get('night_three'),
										   'day_three': request.POST.get('day_three'),
										   'day_pik': request.POST.get('day_pik')}


		return render(request, 'laba3entry.html', {'data': data, 'days_of_week': days_of_week})

	def calculation(request):
		device = {}
		print(request.session['id_device'])
		for id,i in enumerate(request.session['id_device']):
			print(i)
			obj = electricalAppliances.objects.get(id=i)
			device[i] = {'name': obj.name, 'power': obj.power, 'duration': obj.duration,
						 'time_start': request.POST.getlist('time_start')[id*7:id*7+7],
						 'time_end': request.POST.getlist('time_end')[id*7:id*7+7],
						 'time_break': request.POST.getlist('time_break')[id*7:id*7+7],
						 'time_duration': request.POST.getlist('time_duration')[id*7:id*7+7],}
		
		graphics = []

		days_of_week = ["Понеділок", "Вівторок", "Середа", "Четверг", "П'ятниця","Субота", "Неділя"]
		request.session['GEN'] = { k: {} for k in days_of_week}
		request.session['histogram_pick'] = { k: {} for k in days_of_week}
		#print(request.session['GEN']["Понеділок"])

		for i in device:
			graphics.append(laba3cal.graphics(request, device[i]))
		
		#for day in days_of_week:
		#	print(day, request.session['GEN'][day])

		GEN_graphic = laba3cal.GEN_graphic(request, days_of_week)

		histogram_pick = laba3cal.histogram_pick(request,days_of_week)
		histogram = laba3cal.histogram(request, days_of_week, device)

		cost = laba3cal.cost(request, days_of_week)

		context = {'graphics': graphics, 'GEN_graphic': GEN_graphic, 'histogram': histogram[0], 'result_list': histogram[1], 'day': histogram[2], 'price_list': cost[0], 'result': cost[1],'histogram_price': cost[2], 'histogram_pick': histogram_pick}
		return render(request, "laba3calculation.html", context)

	def add_element(request):
		form = electricalAppliancesForm()
		if request.method == 'POST':
			form = electricalAppliancesForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('/laba/laba3/')
		context = {'form': form, 'actions': "Добавити новий пристрій в базу даних", 'action': "Додати"}
		return render(request, 'laba3_element_form.html', context)

	def update_element(request, pk):
		device = electricalAppliances.objects.get(id=pk)
		form = electricalAppliancesForm(instance=device)
		if request.method == 'POST':
			form = electricalAppliancesForm(request.POST, instance=device)
			if form.is_valid():
				form.save()
				return redirect('/laba/laba3/')
		context = {'form': form, 'actions': "Змінити дані електричного пристрою", 'action': "Змінити"}
		return render(request, 'laba3_element_form.html', context)

	def delete_element(request, pk):
		device = electricalAppliances.objects.get(id=pk)
		if request.method == 'POST':
			device.delete()
			return redirect('/laba/laba3/')
		context = {'device': device}
		return render(request, 'laba3delete_element.html', context)





class FormView4(View):

	def get(self, request):
		
		data1 = request.session['data_1']
		data2 = request.session['data_2']

		if data1 == None:
			return render(request, 'laba4.html', {}) 

		#graphic_1 = laba4cal.graphic_1()

		data = Windmills.objects.all()

		dict_data = {}
		for i in data:
			heights = [ (j.height, j.id) for j in Tower.objects.filter(windmills=i.id)]
			prices = [ j.price for j in Tower.objects.filter(windmills=i.id)]
			prices_heights = zip(prices,heights)
			dict_data[i.id] = {'name':i.name, 'price_without_bashta': i.price_without_bashta, 'heights': heights, 'prices': prices_heights}
			

		return render(request, 'laba4.html', {'data1':data1, 'data2': data2, 'dict_data': dict_data})

	def post(self, request):
		data1 = request.session['data_1']
		data2 = request.session['data_2']
		print(request.POST.getlist('choose'))

		if len(request.POST.getlist('choose')) == 1 or 'height' not in request.POST:	
			
			return render(request, 'laba4.html', {'data2': data2, 'error': 'Виберіть тип ВЕУ та його висоту'})

		


		id_windmills = int(request.POST.getlist('choose')[0])
		
		obj_windmills = Windmills.objects.get(id=id_windmills)


		height = int(request.POST['height'])

		print(height, id_windmills)
		datetimeObj_1 = datetime.strptime(str(request.session['data_1']), '%d/%m/%Y %H:%M')
		datetimeObj_2 = datetime.strptime(str(request.session['data_2']), '%d/%m/%Y %H:%M')	
		list_dict = plots.dataSampling(datetimeObj_1, datetimeObj_2)
		#print(list_dict)
		graphic_1 = laba4cal.graphic_1(obj_windmills.name)
		
		try:
			tower_object = Tower.objects.get(windmills=id_windmills, height=height).price
		except Tower.DoesNotExist:
			tower_object = None
		if tower_object == None:	
			return render(request, 'laba4.html', {'data2': data2, 'error': 'Виберіть відповідну висоту до обраного типу ВЕУ!'})
		


		description = [obj_windmills.name, height, obj_windmills.price_without_bashta, tower_object]

		energy = laba4cal.energy(list_dict, height, graphic_1[1], graphic_1[2])
		print("Energy", energy)

		co2 = energy/1000*0.943
		income = round(energy * float(request.POST.get('tariff12')),2)
		OSV = round(co2 * float(request.POST.get('OSV')),2)
		print(request.POST.get('OSV'))


		
		request.session['choose'] = int(request.POST.getlist('choose')[0])
		request.session['height'] = int(request.POST['height'])
		request.session['tariff12'] = request.POST.get('tariff12')
		request.session['OSV'] = request.POST.get('OSV')

		return render(request, 'laba4calculation.html', {'data1': request.session['data_1'], 'data2': request.session['data_2'], 'graphic_1':graphic_1[0], 'description': description, 'energy':round(energy,2), 'co2': round(co2,2), 'income':income, 'OSV': OSV})

	def add_element(request):
		data = Windmills.objects.latest('id')
		print("Last", data.id )
		form = WindmillsForm()
		formTower = TowerForm(initial={'windmills': data.id + 1})
		#formTower = TowerForm()
		if request.method == 'POST':
			form = WindmillsForm(request.POST, request.FILES)
			print(request.POST['windmills'])
			formTower = TowerForm(request.POST)
			if form.is_valid() and formTower.is_valid():
				form.save()
				formTower.save()
				return redirect('/laba/laba4/')
		context = {'form': form,'formTower': formTower, 'actions': "Добавити ВЕУ в базу даних", 'action': "Додати"}
		return render(request, 'laba4_element_form.html', context)

	def update_element(request, pk):
		windmill = Windmills.objects.get(id=pk)
		#tower = Tower.objects.filter(windmills_id=pk)
		#print(tower)

		form = WindmillsForm(instance=windmill)
		#formTower = TowerForm(instance=tower)


		if request.method == 'POST':
			form = WindmillsForm(request.POST, request.FILES, instance=windmill)
			if form.is_valid():
				form.save()
				return redirect('/laba/laba4/')
		context = {'form': form, 'actions': "Змінити дані ВЕУ", 'action': "Змінити"}
		return render(request, 'laba4_element_form.html', context)

	def delete_element(request, pk):
		windmill = Windmills.objects.get(id=pk)
		if request.method == 'POST':
			windmill.delete()
			return redirect('/laba/laba4/')
		print(windmill)
		context = {'windmill': windmill, 'pk': pk}
		return render(request, 'laba4delete_element.html', context)


	def add_height(request, pk):
		form = TowerForm(initial={'windmills': pk})
		#form = TowerForm()
		if request.method == 'POST':
			form = TowerForm(request.POST)
			if form.is_valid():
				print("SAVE")
				form.save()
				return redirect('/laba/laba4/')
		context = {'form': form, 'actions': "Змінити дані ВЕУ", 'action': "Додати"}
		return render(request, 'laba4_add_height.html', context)

	def delete_height(request, pk):
		tower = Tower.objects.get(id=pk)
		tower.delete()
		print("delete tower")
		return redirect('/laba/laba4/')





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




def getpdfPageLaba2(request):
	data1 = request.session['data_1']
	data2 = request.session['data_2']
	template = get_template('pdfLaba2.html')
	html  = template.render(laba2(data1, data2, request, True))
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	else:
		return HttpResponse('ERROR GENERATING PDF')


def getpdfPageLaba4(request):

	template = get_template('pdfLaba4.html')
	html  = template.render(laba4(request))
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	else:
		return HttpResponse('ERROR GENERATING PDF')



def laba4(request):
	id_windmills = request.session['choose']
		
	obj_windmills = Windmills.objects.get(id=id_windmills)


	height = request.session['height']
	datetimeObj_1 = datetime.strptime(str(request.session['data_1']), '%d/%m/%Y %H:%M')
	datetimeObj_2 = datetime.strptime(str(request.session['data_2']), '%d/%m/%Y %H:%M')	
	list_dict = plots.dataSampling(datetimeObj_1, datetimeObj_2)
	#print(list_dict)
	graphic_1 = laba4cal.graphic_1(obj_windmills.name, True)
	description = [obj_windmills.name, height, obj_windmills.price_without_bashta, Tower.objects.get(windmills=id_windmills, height=height).price]

	energy = laba4cal.energy(list_dict, height, graphic_1[1], graphic_1[2])

	co2 = energy/1000*0.943
	income = round(energy * float(request.session['tariff12']),2)
	OSV = round(co2 * float(request.session['OSV']),2)

	return {'data1': request.session['data_1'], 'data2': request.session['data_2'], 'graphic_1':graphic_1[0], 'description': description, 'energy':round(energy,2), 'co2': round(co2,2), 'income':income, 'OSV': OSV, 'media': site1.settings.MEDIA_ROOT}