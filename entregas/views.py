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

@api_view(http_method_names=["GET", "PUT"]) # PUT -> editar
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

    if(request.method == "PUT"): # substituindo uma entidade
        obj = get_object_or_404(Motorista, id=id) # busca o objeto no banco
        # quero alterar os valores/atributos que vieram no request
        
        # Validação
        data = request.data
        serializer = MotoristaSerializers(data=data)

        if(serializer.is_valid()):
            validated_data = serializer.validated_data
            obj.nome = validated_data.get("nome", obj.nome) 
            # tento substituir pelo novo valor, caso não tenha valor
            # já seto o obj.nome (val original) como default

            obj.cpf = validated_data.get("cpf", obj.cpf) 
            obj.cnh = validated_data.get("cnh", obj.cnh) 
            obj.telefone = validated_data.get("telefone", obj.telefone) 
            obj.endereco = validated_data.get("endereco", obj.endereco) 
            obj.ativo = validated_data.get("ativo", obj.ativo) 
            obj.data_nascimento = validated_data.get("data_nascimento", obj.data_nascimento) 

            #acima eu apenas substitui os valores do obj que esta em memoria, ainda preciso persistir no db
            obj.save()
            return JsonResponse(serializer.data, status=200) # 200, atualizando
        return JsonResponse(serializer.errors, status=400) # bad request
        
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

@api_view(http_method_names=["GET", "PUT"])
def caminhao_detail(request, id):
    if(request.method == "GET"):
        obj = get_object_or_404(Caminhao, id=id)
        serializer = CaminhaoSerializers(obj)
        return JsonResponse(serializer.data)

    if(request.method == "PUT"):
        obj = get_object_or_404(Caminhao, id=id)

        data = request.data # pega os dados da request PUT
        
        # Validação
        serializer = CaminhaoSerializers(data=data)

        if(serializer.is_valid()):
            validated_data = serializer.validated_data
            nome_motorista = request.data.get("motorista")
            # .create() não aceita um campo many to many
            # Retirar o nome do motorista do validated_data
            validated_data.pop("motorista", None)
        
            # Substituir a entidade
            obj.placa = validated_data.get("placa", obj.placa)
            obj.modelo = validated_data.get("modelo", obj.modelo)
            # Busca o motorista no banco de dados usando o nome
            motorista_obj, created = Motorista.objects.get_or_create(nome=nome_motorista)
            obj.motorista.set([motorista_obj])
            obj.save()

            return JsonResponse(CaminhaoSerializers(obj).data, status=200) 
            # 200, atualizando, serializo novamente porque apaguei validated_data.pop("motorista", None)

        return JsonResponse(serializer.errors, status=400)
    
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

@api_view(http_method_names=["GET", "PUT"])
def pacote_detail(request, codigo_rastreio):
    if(request.method == "GET"):
        pacotes = get_object_or_404(Pacote, codigo_rastreio=codigo_rastreio)
        serializer = PacoteSerializers(pacotes)
        return JsonResponse(serializer.data)

    if(request.method == "PUT"):
        obj = get_object_or_404(Pacote, codigo_rastreio=codigo_rastreio) 
        # busca o objeto pelo codigo de rastreio no db
        data = request.data # pega os dados da request PUT

        # Validação
        serializer = PacoteSerializers(data=data) # serializando o objeto, dados que vieram da request

        if(serializer.is_valid()):
            validated_data = serializer.validated_data

            motorista_nome = request.data.get("motorista")
            if motorista_nome:
                # Busca ou cria o motorista
                motorista_obj, created = Motorista.objects.get_or_create(nome=motorista_nome)
                obj.motorista = motorista_obj  # Agora repassa a INSTÂNCIA, não a string!

                # Substituindo os demais campos simples
                obj.codigo_rastreio = validated_data.get("codigo_rastreio", obj.codigo_rastreio)
                obj.destino = validated_data.get("destino", obj.destino)
                obj.cliente = validated_data.get("cliente", obj.cliente)
                obj.status = validated_data.get("status", obj.status)
                obj.telefone = validated_data.get("telefone", obj.telefone)

                obj.save()

                # CORREÇÃO 3: Reserializa a instância atualizada do banco
                return JsonResponse(PacoteSerializers(obj).data, status=200)
            """
            # Substituindo a entidade no db
            obj.codigo_rastreio = validated_data.get("codigo_rastreio", obj.codigo_rastreio)
            obj.destino = validated_data.get("destino", obj.destino)
            obj.cliente = validated_data.get("cliente", obj.cliente)
            obj.motorista = validated_data.get("motorista", obj.motorista)
            obj.status = validated_data.get("status", obj.status)
            obj.telefone = validated_data.get("telefone", obj.telefone)

            obj.save()
            return JsonResponse(serializer.data, status=200)
        """
        return JsonResponse(serializer.errors, status=400)