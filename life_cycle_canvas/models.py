# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
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
    oculto = models.BooleanField(default=False)

    def houve_mudanca(self):
        return self.solicitacaomudanca_set.filter(status__in=[SolicitacaoMudanca.STATUS_APROVADA, SolicitacaoMudanca.STATUS_APROVADA_REPLANEJAMENTO]).exists()

    def qtd_solicitacoes_mudancas_pendentes(self):
        return self.solicitacaomudanca_set.filter(status__isnull=True).count()

    def __unicode__(self):
        return '%s (%s)' % (self.conteudo, self.categoria)

    class Meta:
        verbose_name = 'Post-it'
        verbose_name_plural = 'Post-its'


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
    parecer = models.CharField(max_length=120, verbose_name='Parecer', null=True, blank=True)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    usuario_cadastro = models.ForeignKey('auth.User', related_name='usuario_cadastro_solicitacao_mudanca')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    usuario_avaliacao = models.ForeignKey('auth.User', related_name='usuario_avaliacao_solicitacao_mudanca', null=True, blank=True)
    data_avaliacao = models.DateTimeField(null=True, blank=True)

    def aprovar(self, status):
        if not self.status:
            projeto = self.versao_anterior_projeto.projeto
            novo_codigo = projeto.get_codigo_versao_atual() + 1

            self.versao_projeto = VersaoProjeto.objects.create(
                codigo=novo_codigo,
                projeto=projeto
            )
            self.status = status
            self.save()

            self.item_mudanca.oculto = True
            self.item_mudanca.save()

            novo_item = copy.copy(self.item_mudanca)
            novo_item.pk = None
            novo_item.versao_projeto = self.versao_projeto
            novo_item.conteudo = self.solicitacao
            novo_item.save()

    def rejeitar(self):
        self.status = self.STATUS_REJEITADA
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.versao_anterior_projeto = self.item_mudanca.versao_projeto
        super(SolicitacaoMudanca, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


    def __unicode__(self):
        return self.solicitacao

    class Meta:
        verbose_name = 'Solicitação de Mudança'
        verbose_name_plural = 'Solicitações de Mudança'
