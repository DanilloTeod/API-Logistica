from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import ProtectedError

from entregas.models import Motorista, Caminhao, Pacote
from entregas.serializers import MotoristaSerializers, CaminhaoSerializers, PacoteSerializers

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins, generics

class MotoristaList(
    mixins.ListModelMixin, # Adicionar o mixin de listage e criacao
    mixins.CreateModelMixin,
    generics.GenericAPIView # Classe generica
): # Class based views

    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializers

    def get(self, request, *args, **kwargs):
        #self.list(request, *args, **kwargs) # Argumentos nao nomeados e argumentos nomeados
        #queryset = Motorista.objects.all() # QuerySet, consulta
        # Preciso retornar em json
        # Serializers
        #serializer = MotoristaSerializers(queryset, many=True)
        # many=True -> uma lista de objetos
        # JsonResponse -> HEADER
        #return JsonResponse(serializer.data, safe=False)

        # Deve-se informar o model (queryset)/consulta para fazer a listagem
        # e qual o serializer usado (como os objetos serão representados para quem está consumindo a api)
        return self.list(request, *args, **kwargs) # Argumentos nao nomeados e argumentos nomeados

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
"""""
        data = request.data 
        # JSON que vem com os valores
        # {"nome": "", ...}
        # Antes de criar os dados no DB, é preciso fazer a validacao

        # VALIDAÇÃO
        serializer = MotoristaSerializers(data=data) 
        # ao inves de passar um obj como queryset ou uma instancia
        # é passado um data=data
        if(serializer.is_valid()): # verifica se os valores estao de acordo
            serializer.save() # Vai chamar o metodo create em serializers.py para criar uma nova instancia da classe
            return JsonResponse(serializer.data, status=201) # 201 = created
        return JsonResponse(serializer.errors, status=400)
"""

""" Function based views get e post motorista_list 
@api_view(http_method_names=["GET", "POST"]) # O que o path permite
def motoristas_list(request):
    if(request.method == "GET"):
        queryset = Motorista.objects.all() # QuerySet, consulta

        # Preciso retornar em json
        # Serializers
        serializer = MotoristaSerializers(queryset, many=True)
        # many=True -> uma lista de objetos

        # JsonResponse -> HEADER
        return JsonResponse(serializer.data, safe=False)

    if(request.method == "POST"):
        data = request.data 
        # JSON que vem com os valores
        # {"nome": "", ...}
        # Antes de criar os dados no DB, é preciso fazer a validacao

        # VALIDAÇÃO
        serializer = MotoristaSerializers(data=data) 
        # ao inves de passar um obj como queryset ou uma instancia
        # é passado um data=data
        if(serializer.is_valid()): # verifica se os valores estao de acordo
            serializer.save() # Vai chamar o metodo create em serializers.py para criar uma nova instancia da classe
            return JsonResponse(serializer.data, status=201) # 201 = created
        
        return JsonResponse(serializer.errors, status=400)
"""

class MotoristaDetail(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView,
):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializers

    def get(self, request, *args, **kwargs): # get(self, request, id) # o ID será injetado por padrão nos *args e **kwargs 
        #obj = get_object_or_404(Motorista, id=id)
        # Preciso retornar em json
        # Serializers
        #serializer = MotoristaSerializers(obj)
        # o atributo serializer agora, terá os "sub-atributos" 
        # serializer.nome, serializer.cpf ...
        # JsonResponse -> HEADER
        #return JsonResponse(serializer.data)
        return self.retrieve(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        #obj = get_object_or_404(Motorista, id=id) # busca o objeto no banco
        # quero alterar os valores/atributos que vieram no request
        # Validação
        #data = request.data
        #serializer = MotoristaSerializers(instance=obj ,data=data, partial=True)

        #if(serializer.is_valid()):
        #    serializer.save()
        #    return JsonResponse(serializer.data, status=200) # 200, atualizando
        #return JsonResponse(serializer.errors, status=400) # bad request
        return self.partial_update(request, *args, **kwargs)
        # self.update
    def delete(self, request, *args, **kwargs):
        #obj = get_object_or_404(Motorista, id=id) # busca o objeto no banco
        #try:
        #    obj.delete()
        #    return Response(status=204) # 204 = no content, resposta sem corpo 
        #except ProtectedError:
        #    return JsonResponse({"erro": "Não é possível excluir este motorista pois ele está vinculado a registros ativos."}, status=400)
        return self.destroy(request, *args, **kwargs)

""" Function based views get e post motorista_detail
@api_view(http_method_names=["GET", "PATCH", "DELETE"]) # PUT -> editar, PATCH -> editar parcial (mais util)
def motoristas_detail(request, id):
    if(request.method == "GET"):
        obj = get_object_or_404(Motorista, id=id)
        
        # Preciso retornar em json
        # Serializers

        serializer = MotoristaSerializers(obj)
        # o atributo serializer agora, terá os "sub-atributos" 
        # serializer.nome, serializer.cpf ...

        # JsonResponse -> HEADER
        return JsonResponse(serializer.data)

    if(request.method == "PATCH"): # substituindo uma entidade
        obj = get_object_or_404(Motorista, id=id) # busca o objeto no banco
        # quero alterar os valores/atributos que vieram no request
        
        # Validação
        data = request.data
        serializer = MotoristaSerializers(instance=obj ,data=data, partial=True)

        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=200) # 200, atualizando
        return JsonResponse(serializer.errors, status=400) # bad request
    
    if (request.method == "DELETE"):
        obj = get_object_or_404(Motorista, id=id) # busca o objeto no banco
        try:
            obj.delete()
            return Response(status=204) # 204 = no content, resposta sem corpo 
        except ProtectedError:
            return JsonResponse({"erro": "Não é possível excluir este motorista pois ele está vinculado a registros ativos."}, status=400)
"""


class CaminhaoList(mixins.ListModelMixin,
                   mixins.CreateModelMixin, 
                   generics.GenericAPIView): # Classe Generica
    
    queryset = Caminhao.objects.all()
    serializer_class = CaminhaoSerializers

    def perform_create(self, serializer):
        nome_motorista = self.request.data.get("motorista")
        # DRF executa o save repassando os parametros adicionais
        serializer.save(nome_motorista=nome_motorista)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
""" Function based view caminhao_list
@api_view(http_method_names=["GET", "POST"])
def caminhao_list(request):
    if(request.method == "GET"):
        queryset = Caminhao.objects.all()
        serializer = CaminhaoSerializers(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    if(request.method == "POST"):
        data = request.data
        # VALIDACAO
        serializer = CaminhaoSerializers(data=data)

        if(serializer.is_valid()):
            nome_motorista = request.data.get("motorista")
            caminhao_criado = serializer.save(nome_motorista=nome_motorista) # Passando o parametro para o create

            return JsonResponse(CaminhaoSerializers(caminhao_criado).data, status=201)
        return JsonResponse(serializer.errors, status=400)
"""

class CaminhaoDetail(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView,
):
    queryset = Caminhao.objects.all()
    serializer_class = CaminhaoSerializers

    def perform_update(self, serializer):
        motorista_nome = self.request.data.get("motorista")
        serializer.save(motorista_nome=motorista_nome)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
"""Function based view caminhao_detail
@api_view(http_method_names=["GET", "PATCH", "DELETE"])
def caminhao_detail(request, id):
    if(request.method == "GET"):
        obj = get_object_or_404(Caminhao, id=id)
        serializer = CaminhaoSerializers(obj)
        return JsonResponse(serializer.data)

    if(request.method == "PATCH"):
        obj = get_object_or_404(Caminhao, id=id)
        #data = request.data # pega os dados da request PUT
        # Validação
        serializer = CaminhaoSerializers(instance=obj, data=request.data, partial=True)

        if(serializer.is_valid()):
            motorista_nome = request.data.get("motorista")
            caminhao_atualizado = serializer.save(motorista_nome=motorista_nome)
            return JsonResponse(CaminhaoSerializers(caminhao_atualizado).data, status=200) 
            # 200, atualizando, serializo novamente porque apaguei validated_data.pop("motorista", None)
        return JsonResponse(serializer.errors, status=400)

    if(request.method == "DELETE"):
        obj = get_object_or_404(Caminhao, id=id)
        try:
            obj.delete()
            return Response(status=204) # 204 = no content, resposta sem corpo
        
        except ProtectedError:
            return JsonResponse({"erro": "Não é possível excluir este motorista pois ele está vinculado a registros ativos."}, status=400)    
"""

class PacoteList(
    mixins.ListModelMixin, # Adicionar o mixin de listage e criacao
    mixins.CreateModelMixin,
    generics.GenericAPIView # Classe generica
): # Class based views
    queryset = Pacote.objects.all()
    serializer_class = PacoteSerializers
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

""" Function based view pacote_list
@api_view(http_method_names=["GET", "POST"]) # APIView
def pacote_list(request):
    if(request.method == "GET"):
        queryset = Pacote.objects.all()
        serializer = PacoteSerializers(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    if(request.method == "POST"):
        data = request.data
        # VALIDACAO
        serializer = PacoteSerializers(data=data)

        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
"""

class PacoteDetail(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView,
):
    
    queryset = Pacote.objects.all()
    serializer_class = PacoteSerializers
    lookup_field = 'codigo_rastreio' # Indico ao DRF qual campo utilizado
                                    # para busca
    def perform_update(self, serializer):
        motorista_nome = self.request.data.get("motorista")
        serializer.save(motorista_nome=motorista_nome)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

""" Function based view pacote_detail
@api_view(http_method_names=["GET", "PATCH", "DELETE"])
def pacote_detail(request, codigo_rastreio):
    if(request.method == "GET"):
        pacotes = get_object_or_404(Pacote, codigo_rastreio=codigo_rastreio)
        serializer = PacoteSerializers(pacotes)
        return JsonResponse(serializer.data)

    if(request.method == "PATCH"):
        obj = get_object_or_404(Pacote, codigo_rastreio=codigo_rastreio) 
        # busca o objeto pelo codigo de rastreio no db
        data = request.data # pega os dados da request PUT

        # Validação
        # Quando troca put por patch, deve-se informar ao serializer
        # qual o objeto esta sendo alterado
        serializer = PacoteSerializers(instance=obj, data=data, partial=True) # serializando o objeto, dados que vieram da request
        # partial=True, permite updates parciais, para esta instancia de serializers
        if(serializer.is_valid()):
            motorista_nome = request.data.get("motorista")
            pacote_atualizado = serializer.save(motorista_nome=motorista_nome)
            return JsonResponse(PacoteSerializers(pacote_atualizado).data, status=200)
        return JsonResponse(serializer.errors, status=400)
    if(request.method == "DELETE"):
        obj = get_object_or_404(Pacote, codigo_rastreio=codigo_rastreio)

        try:
            obj.delete()
            return Response(status=204)
        except ProtectedError:
            return JsonResponse({"erro": "Não é possível excluir este motorista pois ele está vinculado a registros ativos."}, status=400)    
"""
