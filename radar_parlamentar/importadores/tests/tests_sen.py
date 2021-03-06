from django.test import TestCase
import bz2
import os
import xml.etree.ElementTree as etree
from pathlib import Path
from unittest.mock import Mock

from importadores import sen, sen_indexacao
from modelagem import models

XML_TEST = str(Path(sen.MODULE_DIR) / 'dados/senado/ListaVotacoesTest.xml.bz2')

class GeradorSenadoTest(TestCase):

    def test_geracao_da_casa(self):
        casa = sen.CasaLegislativaGerador().gera_senado()
        self.assertEqual(casa.nome_curto, 'sen')

    def test_recupera_a_casa_existente(self):
        casa1 = sen.CasaLegislativaGerador().gera_senado()
        casa2 = sen.CasaLegislativaGerador().gera_senado()
        self.assertEqual(casa1.pk, casa2.pk)


class ImportadorSenadoTest(TestCase):

    def setUp(self):
        casa = sen.CasaLegislativaGerador().gera_senado()
        self.importer = sen.ImportadorVotacoesSenado()

        xml_string = ""
        with bz2.open(XML_TEST, mode='rt', encoding="iso-8859-1") as f:
            xml_string = f.read()

        self.importer._save_votacoes_in_db(xml_string)

    def test_votacao_importada(self):
        votacao = models.Votacao.objects.first()
        self.assertEqual(votacao.resultado, 'R')

    def test_parlamentar_importado(self):
        parlamentar = models.Parlamentar.objects.get(nome='Jader Barbalho')
        self.assertTrue(parlamentar)
        self.assertEqual(parlamentar.genero, 'M')
        self.assertEqual(parlamentar.localidade, 'PA')
        partido = models.Partido.objects.get(nome='PMDB')
        self.assertTrue(partido)
        self.assertEqual(parlamentar.partido.nome, 'PMDB')


class IndexacaoSenadoTest(TestCase):

    def setUp(self):
        casa = sen.CasaLegislativaGerador().gera_senado()
        self.importer = sen.ImportadorVotacoesSenado()

        xml_string = ""
        with bz2.open(XML_TEST, mode='rt', encoding="iso-8859-1") as f:
            xml_string = f.read()

        self.importer._save_votacoes_in_db(xml_string)

        sen_indexacao.indexar_proposicoes()

    def test_proposicoes_importadas(self):
        proposicao = models.Proposicao.objects.first()
        self.assertTrue(proposicao)
        self.assertEqual(proposicao.ano, '2015')
        self.assertEqual(proposicao.sigla, 'PLS')
        self.assertEqual(proposicao.numero, '00131')
