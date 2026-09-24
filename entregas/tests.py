#from django.test import TestCase
from rest_framework.test import APITestCase
# Create your tests here.
import json

class TestListagemMotoristas(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get("/api/motoristas/") # requisição a api
        data = json.loads(response.content) # json para python, mesmo que o json esteja em binario
        self.assertEqual(data, []) # verifica se a resposta condiz com uma lista vazia

"""
    def test_listagem_de_motoristas_criados(self):
        motorista_serializado = {"nome": "Hugo da silva", "cpf": "12345678", "cnh": "87654321", "telefone": None, "endereco": "Rua do joao, numero 72, ES/Vitoria", "ativo": True, "data_nascimento": None}
        response = self.client.get("/api/motoristas/")
        data = json.loads(response.content)
        #self.asser
        self.assertEqual(data, motorista_serializado)
"""