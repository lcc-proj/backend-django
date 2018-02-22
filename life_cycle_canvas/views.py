# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from life_cycle_canvas.models import CategoriaCanvas


def index(request):
    categorias = CategoriaCanvas.objects.all()
    return render(request, 'life_cycle_canvas/index.html', locals())