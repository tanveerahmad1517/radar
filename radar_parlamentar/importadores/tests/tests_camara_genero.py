from django.test import TestCase
from importadores.camara_genero import _null_to_none
from importadores.camara_genero import parseia_indexacoes
from importadores.camara_genero import proposicoes_indexadas
from importadores.camara_genero import multiple_null_remove
from importadores.camara_genero import parsear_indexacoes_de_proposicoes


class CamaraTest(TestCase):

    def test__null_to_none_com_null(self):
        proposicao = {"Casa": "NULL"}
        self.assertEqual(_null_to_none(proposicao), {"Casa": None})

    def test__null_to_none_sem_null(self):
        proposicao = {"Casa": 1}
        self.assertEqual(_null_to_none(proposicao), {"Casa": 1})

    def test_multiple_null_remove(self):
        lista_proposicoes_null = [{"Casa": 1},
                                  {"Educacao": "NULL"}, {"Transporte": "NULL"}]
        lista_proposicoes = [{"Casa:": 1, "Lar": 2}]
        self.assertEqual(multiple_null_remove(
            lista_proposicoes_null), [{"Casa": 1}, {"Educacao": None},
                                      {"Transporte": None}])
        self.assertEqual(multiple_null_remove(
            lista_proposicoes), [{"Casa:": 1, "Lar": 2}])

    def test_proposicoes_indexadas_partido_lista(self):
        indexados_partido = [{'txtIndexacao': 1, 'txtSiglaPartido': "AL"}]
        lista_proposicoes_partido = [{'txtIndexacao': 1,
                                      'txtSiglaPartido': "AL"}]
        self.assertEqual(proposicoes_indexadas(
            lista_proposicoes_partido), indexados_partido)

    def test_proposicoes_indexadas_partido_errado(self):
        indexados = []
        lista_proposicoes = [{'txtIndexacao': 1,
                              'txtSiglaPartido': "ALLL"}]
        self.assertEqual(proposicoes_indexadas(lista_proposicoes), indexados)

    def test_parseia_indexacoes(self):
        indexacao = "Teste\nRadar.Parlamentar, _radar_parlamentar_"
        self.assertEqual(parseia_indexacoes(indexacao),
                         ['testeradarparlamentar', 'radarparlamentar'])
