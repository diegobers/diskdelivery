from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Agua, Gas


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_aguas'] = Agua.objects.all()
        context['list_gas'] = Gas.objects.all()
        return context