# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tabnanny import verbose

from django.db import models


class VersaoProjeto(models.Model):
    codigo = models.CharField(max_length=10, verbose_name='Código')
    projeto = models.ForeignKey('life_cycle_canvas.Projeto', verbose_name='Projeto', null=True, blank=True)

    class Meta:
        verbose_name = 'Versão do Projeto'
        verbose_name_plural = 'Versões do Projeto'


class Projeto(models.Model):
    INDICACAO_VERDE = 0
    INDICACAO_AMARELO = 1
    INDICACAO_VERMELHO = 2

    INDICACAO_DESEMPENHO_CHOICES = (
        (INDICACAO_VERDE, 'Verde'),
        (INDICACAO_AMARELO, 'Amarelo'),
        (INDICACAO_VERMELHO, 'Vermelho'),
    )

    titulo = models.CharField(max_length=120, verbose_name='Título')
    pitch = models.CharField(max_length=120, verbose_name='Pitch')
    indicacao_desempenho = models.PositiveIntegerField(choices=INDICACAO_DESEMPENHO_CHOICES,
                                                       verbose_name='Indicação Geral de Desempenho do Projeto')
    data = models.DateField(auto_now_add=True)
    local = models.CharField(max_length=120, verbose_name='Local')
    gerente_projeto = models.ForeignKey('auth.User', verbose_name='Gerente do Projeto', null=True, blank=True)
    patrocinador = models.CharField(max_length=120, verbose_name='Patrocinador')
    cliente = models.CharField(max_length=120, verbose_name='Cliente')

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'


class CategoriaCanvas(models.Model):
    nome = models.CharField(max_length=120, verbose_name='Nome')
    descricao = models.CharField(max_length=120, verbose_name='Descrição')
    icone = models.CharField(max_length=120, verbose_name='Ícone')
    codigo_cor_hex = models.CharField(max_length=7, verbose_name='Código Hexadecimal da Cor')

    class Meta:
        verbose_name = 'Categorias do Canvas'
        verbose_name_plural = 'Categorias do Canvas'


class ItemCategoriaCanvas(models.Model):
    conteudo = models.TextField(verbose_name='Conteúdo')
    categoria = models.ForeignKey('life_cycle_canvas.CategoriaCanvas')
    usuario_cadastro = models.ForeignKey('auth.User', related_name='usuario_cadastro')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    usuario_atualizacao = models.ForeignKey('auth.User', related_name='usuario_atualizacao')
    versao_projeto = models.ForeignKey('life_cycle_canvas.VersaoProjeto')

    class Meta:
        verbose_name = 'Item do Canvas'
        verbose_name_plural = 'Itens do Canvas'
