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







def check_bd():
	pass


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
