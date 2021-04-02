#-*- coding: utf-8 -*-
from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView
from django.db.models import Count
from django.db.models import Sum
from mailer.models import Company


class IndexView(ListView):
    template_name = "mailer/index.html"
    model = Company
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context