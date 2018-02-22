# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from life_cycle_canvas.models import CategoriaCanvas, Projeto, ItemCategoriaCanvas, VersaoProjeto, SolicitacaoMudanca


def index(request, pk, codigo_versao=None):
    categorias = CategoriaCanvas.objects.all()
    obj = get_object_or_404(Projeto, pk=pk)
    versoes_projeto = obj.versaoprojeto_set.all().order_by('-id')

    if not codigo_versao:
        versao_projeto = obj.versao_atual()
    else:
        versao_projeto = get_object_or_404(VersaoProjeto, codigo=codigo_versao)

    for categoria in categorias:
        categoria.post_its = ItemCategoriaCanvas.objects.filter(versao_projeto__codigo__lte=versao_projeto.codigo, categoria__pk=categoria.pk)

    return render(request, 'life_cycle_canvas/index.html', locals())

def aprovar(request, pk):
    obj = get_object_or_404(SolicitacaoMudanca, pk=pk)
    obj.aprovar(0)

    obj.usuario_avaliacao = request.user
    obj.data_avaliacao = datetime.datetime.today()
    obj.save()

    return redirect('/dashboard/%s/' % obj.item_mudanca.versao_projeto.projeto.pk)

def aprovar_com_replanejamento(request, pk):
    obj = get_object_or_404(SolicitacaoMudanca, pk=pk)
    obj.aprovar(1)

    obj.usuario_avaliacao = request.user
    obj.data_avaliacao = datetime.datetime.today()
    obj.save()

    return redirect('/dashboard/%s/' % obj.item_mudanca.versao_projeto.projeto.pk)

def rejeitar(request, pk):
    obj = get_object_or_404(SolicitacaoMudanca, pk=pk)
    obj.rejeitar()

    obj.usuario_avaliacao = request.user
    obj.data_avaliacao = datetime.datetime.today()
    obj.save()

    return redirect('/dashboard/%s/' % obj.item_mudanca.versao_projeto.projeto.pk)

def api_postits_canvas(request):
    response = []
    obj = Projeto.objects.last()

    for categoria in CategoriaCanvas.objects.all():
        postits = list({'id': x.id, 'conteudo': x.conteudo, 'oculto': x.oculto} for x in
                       ItemCategoriaCanvas.objects.filter(versao_projeto__codigo__lte=obj.get_codigo_versao_atual(), categoria__pk=categoria.pk))

        response.append({
            'id': categoria.id,
            'nome': categoria.nome,
            'icone': categoria.icone,
            'codigo_cor_hex': categoria.codigo_cor_hex,
            'postits': postits

        })

    return JsonResponse(response, safe=False)
