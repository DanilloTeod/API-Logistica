from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from entregas.models import Motorista, Caminhao, Pacote
from entregas.serializers import MotoristaSerializers, CaminhaoSerializers, PacoteSerializers

from rest_framework.response import Response
from rest_framework.decorators import api_view

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
            validated_data = serializer.validated_data

            # Com os dados validados, pode-se criar um obj "Motorista"
            Motorista.objects.create(
                nome = validated_data["nome"],
                cpf = validated_data["cpf"],
                cnh = validated_data["cnh"],
                endereco = validated_data["endereco"],
                telefone = validated_data["telefone"],
                data_nascimento = validated_data["data_nascimento"],
                ativo = validated_data["ativo"]
            )
            return JsonResponse(serializer.data, status=201) # 201 = created
        return JsonResponse(serializer.errors, status=400)

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
            validated_data = serializer.validated_data
            nome_motorista = request.data.get("motorista")
            #print(nome_motorista)
            # .create() não aceita um campo many to many
            # Retirar o nome do motorista do validated_data
            validated_data.pop("motorista", None)

            caminhao = Caminhao.objects.create(
                placa = validated_data["placa"],
                modelo = validated_data["modelo"]
            )

            if nome_motorista:
                # Busca o motorista no banco de dados usando o nome
                motorista_obj, created = Motorista.objects.get_or_create(nome=nome_motorista)
                caminhao.motorista.set([motorista_obj])

            serializer = CaminhaoSerializers(caminhao)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(http_method_names=["GET"])
def caminhao_detail(request, id):
    obj = get_object_or_404(Caminhao, id=id)
    serializer = CaminhaoSerializers(obj)
    return JsonResponse(serializer.data)

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
            validated_data = serializer.validated_data
            Pacote.objects.create(
                codigo_rastreio = validated_data["codigo_rastreio"],
                cliente = validated_data["cliente"],
                motorista = Motorista.objects.get(nome=(validated_data["motorista"])),
                status = validated_data["status"],
                destino = validated_data["destino"],
                telefone = validated_data["telefone"]
            )
            #Motorista.objects.get() pegar o id a partir do nome do objeto
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(http_method_names=["GET"])
def pacote_detail(request, codigo_rastreio):
    pacotes = get_object_or_404(Pacote, codigo_rastreio=codigo_rastreio)
    serializer = PacoteSerializers(pacotes)
    return JsonResponse(serializer.data)