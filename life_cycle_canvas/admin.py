# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from life_cycle_canvas.models import VersaoProjeto, CategoriaCanvas, Projeto, ItemCategoriaCanvas


@admin.register(CategoriaCanvas)
class CategoriaCanvasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'icone', 'codigo_cor_hex')


@admin.register(ItemCategoriaCanvas)
class ItemCategoriaCanvasAdmin(admin.ModelAdmin):
    list_display = ('conteudo', 'categoria')


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'pitch', 'versao_atual')
    list_search = ('titulo', 'local', 'patrocinador', 'cliente')
    date_hierarchy = 'data'
    list_filter = ('gerente_projeto', 'patrocinador', 'cliente')
    exclude = ('indicacao_desempenho',)

    def versao_atual(self):
        return VersaoProjeto.objects.filter(projeto=self).latest('codigo').codigo

    versao_atual.short_description = 'Versão Atual'


@admin.register(VersaoProjeto)
class VersaoProjetoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'projeto',)
    search_fields = ('codigo', 'projeto__nome')
    list_filter = ('codigo', 'projeto',)
