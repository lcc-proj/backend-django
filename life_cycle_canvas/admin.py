# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from life_cycle_canvas.models import VersaoProjeto, CategoriaCanvas, Projeto, ItemCategoriaCanvas, SolicitacaoMudanca

admin.site.site_header = 'LifeCycleCanvas Change Manager'

# @admin.register(CategoriaCanvas)
# class CategoriaCanvasAdmin(admin.ModelAdmin):
#     list_display = ('nome', 'descricao', 'icone', 'codigo_cor_hex')


@admin.register(ItemCategoriaCanvas)
class ItemCategoriaCanvasAdmin(admin.ModelAdmin):
    list_display = ('conteudo', 'categoria')
    exclude = ('data_cadastro', 'data_atualizacao', 'usuario_atualizacao', 'oculto')


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'pitch', 'versao_atual')
    list_search = ('titulo', 'local', 'patrocinador', 'cliente')
    date_hierarchy = 'data'
    list_filter = ('gerente_projeto', 'patrocinador', 'cliente')
    exclude = ('indicacao_desempenho',)

    def versao_atual(self, obj):
        return VersaoProjeto.objects.filter(projeto=obj).latest('codigo').codigo

    versao_atual.short_description = 'Versão Atual'


@admin.register(VersaoProjeto)
class VersaoProjetoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'projeto',)
    search_fields = ('codigo', 'projeto__nome')
    list_filter = ('codigo', 'projeto',)


@admin.register(SolicitacaoMudanca)
class SolicitacaoMudancaAdmin(admin.ModelAdmin):
    list_display = (
        'solicitante', 'solicitante', 'origem',
        'parecer', 'data_avaliacao', 'status', 'versao_anterior_projeto', 'versao_projeto'
    )
    search_fields = ('solicitacao',)
    list_filter = ('status',)
    exclude = ('versao_anterior_projeto', 'versao_projeto', 'data_cadastro', 'usuario_avaliacao', 'data_avaliacao', 'parecer', 'status')