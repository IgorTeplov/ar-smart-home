from django.shortcuts import render
from django.views import View
from random import randint

class Index(View):
	def get(self, request, *args, **kwargs):

		return render(request, 'index.html', {
			'nocache': f'?r={randint(1000000, 9999999)}',
		})
