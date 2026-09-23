from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from entregas.models import Motorista, Caminhao, Pacote
from entregas.serializers import MotoristaSerializers, CaminhaoSerializers, PacoteSerializers

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(http_method_names=["GET"])
def motoristas_list(request):
    queryset = Motorista.objects.all() # QuerySet, consulta

    # Preciso retornar em json
    # Serializers
    serializer = MotoristaSerializers(queryset, many=True)
    # many=True -> uma lista de objetos

    # JsonResponse -> HEADER
    return JsonResponse(serializer.data, safe=False)

@api_view(http_method_names=["GET"])
def motoristas_detail(request, id):
    obj = get_object_or_404(Motorista, id=id)
    
    # Preciso retornar em json
    # Serializers

    serializer = MotoristaSerializers(obj)
    # o atributo serializer agora, terá os "sub-atributos" 
    # serializer.nome, serializer.cpf ...

    # JsonResponse -> HEADER
    return JsonResponse(serializer.data)

@api_view(http_method_names=["GET"])
def caminhao_list(request):
    queryset = Caminhao.objects.all()
    serializer = CaminhaoSerializers(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(http_method_names=["GET"])
def caminhao_detail(request, id):
    obj = get_object_or_404(Caminhao, id=id)
    serializer = CaminhaoSerializers(obj)
    return JsonResponse(serializer.data)

@api_view(http_method_names=["GET"]) # APIView
def pacote_list(request):
    queryset = Pacote.objects.all()
    serializer = PacoteSerializers(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(http_method_names=["GET"])
def pacote_detail(request, codigo_rastreio):
    pacotes = get_object_or_404(Pacote, codigo_rastreio=codigo_rastreio)
    serializer = PacoteSerializers(pacotes)
    return JsonResponse(serializer.data)