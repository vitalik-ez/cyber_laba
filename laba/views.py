from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import NameForm

import logging

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView

from django.views import View

from .import plots

import plotly.graph_objs as go
from plotly.offline import plot


import sqlite3
from collections import Counter

logger = logging.getLogger(__name__)



class IndexView(TemplateView):
    template_name = "index.html"

class Plot1DView(TemplateView):
    template_name = "plot.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot1DView, self).get_context_data(**kwargs)
        context['plot'] = plots.plot1d()
        return context

class FormView(View):

	def get(self, request):
		return render(request, 'plot.html', {})

	def post(self, request):
		 
		data1 = request.POST.get('data1')
		data2 = request.POST.get('data2')
		time = request.POST.get('time')

		graphic = plots.plot1d(data1, data2, time)

		context = {'data1': data1, 'data2': data2, 'time': time, 'plot': graphic}
		return render(request, 'plot.html', context)

class Graph(View):

	def get(self, request):
		return render(request, 'plot_graph.html', {})

	def post(self, request):

		data1 = request.POST.get('data1')
		data2 = request.POST.get('data2')
		time = request.POST.get('time')
		graphic = plots.TemperatureMode(data1, data2, time)

		context = {'data1': data1, 'data2': data2, 'time': time, 'plot': graphic[0], 'x_y': graphic[1]}
		return render(request, 'plot_graph.html', context)




def check_bd(request):
	conn = sqlite3.connect("test_check.db")
	cursor = conn.cursor()
	month_table = ['January', 'February', 'March']
	error = 0
	error_day = 0
	check_month = []
	for i in month_table:
	    sql = f"SELECT * from {i} WHERE number_month IS NULL OR T IS NULL or dd IS NULL"
	    cursor.execute(sql)
	    data = cursor.fetchall()
	    error += len(data)
	    j = 0
	    while j < len(data):
	        sql = f"SELECT * from {i} WHERE id > {data[j][0]} AND dd NOT NULL LIMIT 1"
	        cursor.execute(sql)
	        row = cursor.fetchall()
	        if row[0][0]-data[j][0] == 1:
	            print(" Брати попереднє значення")
	            sql = f"SELECT dd from {i} WHERE id = {data[j][0] - 1} AND dd NOT NULL"
	            cursor.execute(sql)
	            value_true = cursor.fetchall()
	            sql = f"UPDATE {i} SET dd = '{value_true[0][0]}' WHERE id = {data[j][0]}"
	            cursor.execute(sql)
	            conn.commit()
	        else:
	            sql = f"SELECT dd from {i} WHERE id = {data[j][0] - 1} AND dd NOT NULL"
	            cursor.execute(sql)
	            value_1 = cursor.fetchall()
	            sql = f"SELECT dd from {i} WHERE id = {row[0][0]} AND dd NOT NULL"
	            cursor.execute(sql)
	            value_2 = cursor.fetchall()
	            d = (row[0][0] - data[j][0])
	            print("d =", d)
	            if d % 2 == 0:
	                d = d / 2
	            else:
	                d = d / 2 + 0.5
	            sql = f"UPDATE {i} SET dd = '{value_1[0][0]}' WHERE id >= {data[j][0]} AND id < {data[j][0] + d}"
	            cursor.execute(sql)
	            conn.commit()
	            sql = f"UPDATE {i} SET dd = '{value_2[0][0]}' WHERE id >= {data[j][0] + d} AND id <= {row[0][0] - 1}"
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
	    error_day = "Помилка: перевірте всі дні та години в БД."

	conn.close()
	return HttpResponse("Помилок, {}. {}".format(error, error_day))















def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def show_name(request, username):
	return HttpResponse("Hello, {}".format(username))

def new(request):
	# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/laba/temperature')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'test_form.html', {'form': form})
    

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'test_form.html', {'form': form})
