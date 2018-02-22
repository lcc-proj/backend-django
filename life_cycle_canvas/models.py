# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tabnanny import verbose

from django.db import models


class VersaoProjeto(models.Model):
    codigo = models.PositiveIntegerField(verbose_name='Código do Projeto')
    projeto = models.ForeignKey('life_cycle_canvas.Projeto', verbose_name='Projeto', null=True, blank=True)

    def __unicode__(self):
        return 'Versão %s do %s' % (self.codigo, self.projeto)

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
    pitch = models.CharField(max_length=120, verbose_name='Alias')
    indicacao_desempenho = models.PositiveIntegerField(choices=INDICACAO_DESEMPENHO_CHOICES,
                                                       verbose_name='Indicação Geral de Desempenho do Projeto',
                                                       default=INDICACAO_VERDE)
    data = models.DateField(auto_now_add=True)
    local = models.CharField(max_length=120, verbose_name='Local')
    gerente_projeto = models.ForeignKey('auth.User', verbose_name='Gerente do Projeto', null=True, blank=True)
    patrocinador = models.CharField(max_length=120, verbose_name='Patrocinador')
    cliente = models.CharField(max_length=120, verbose_name='Cliente')

    def __unicode__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Projeto, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

        if not self.pk:
            VersaoProjeto.objects.create(
                codigo=1,
                projeto=self
            )

    def get_codigo_versao_atual(self):
        return VersaoProjeto.objects.filter(projeto=self).latest('codigo').codigo

    def versao_atual(self):
        return VersaoProjeto.objects.filter(projeto=self).latest('codigo')


class CategoriaCanvas(models.Model):
    nome = models.CharField(max_length=120, verbose_name='Nome')
    descricao = models.CharField(max_length=120, verbose_name='Descrição')
    icone = models.CharField(max_length=120, verbose_name='Ícone')
    codigo_cor_hex = models.CharField(max_length=7, verbose_name='Código Hexadecimal da Cor')

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Categorias do Canvas'
        verbose_name_plural = 'Categorias do Canvas'


class ItemCategoriaCanvas(models.Model):
    conteudo = models.TextField(verbose_name='Conteúdo')
    categoria = models.ForeignKey('life_cycle_canvas.CategoriaCanvas')
    usuario_cadastro = models.ForeignKey('auth.User', related_name='usuario_cadastro_item_canvas', verbose_name='Usuário')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True, null=True, blank=True)
    usuario_atualizacao = models.ForeignKey('auth.User', related_name='usuario_atualizacao_item_canvas', null=True, blank=True)
    versao_projeto = models.ForeignKey('life_cycle_canvas.VersaoProjeto', verbose_name='Versão do Projeto')

    def __unicode__(self):
        return self.conteudo

    class Meta:
        verbose_name = 'Item do Canvas'
        verbose_name_plural = 'Itens do Canvas'


class SolicitacaoMudanca(models.Model):
    STATUS_APROVADA = 0
    STATUS_APROVADA_REPLANEJAMENTO = 1
    STATUS_REJEITADA = 2

    STATUS_CHOICES = (
        (STATUS_APROVADA, 'Aprovada'),
        (STATUS_APROVADA_REPLANEJAMENTO, 'Aprovada com replanejamento'),
        (STATUS_REJEITADA, 'Rejeitada'),
    )

    versao_anterior_projeto = models.ForeignKey('life_cycle_canvas.VersaoProjeto', related_name='versao_anterior')
    versao_projeto = models.ForeignKey('life_cycle_canvas.VersaoProjeto', related_name='nova_versao', null=True, blank=True)
    item_mudanca = models.ForeignKey('life_cycle_canvas.ItemCategoriaCanvas', verbose_name='Item do Canvas')
    solicitacao = models.TextField(verbose_name='Solicitação')
    solicitante = models.CharField(max_length=120, verbose_name='Solicitante')
    origem = models.CharField(max_length=120, verbose_name='Origem')
    parecer = models.CharField(max_length=120, verbose_name='Parecer')
    status = models.PositiveIntegerField(choices=STATUS_CHOICES)

    usuario_cadastro = models.ForeignKey('auth.User', related_name='usuario_cadastro_solicitacao_mudanca')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    usuario_avaliacao = models.ForeignKey('auth.User', related_name='usuario_avaliacao_solicitacao_mudanca')
    data_avaliacao = models.DateTimeField()

    def __unicode__(self):
        return self.solicitacao

    class Meta:
        verbose_name = 'Solicitação de Mudança'
        verbose_name_plural = 'Solicitações de Mudança'
