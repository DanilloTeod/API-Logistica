from rest_framework import serializers, fields
from entregas.models import Motorista, Caminhao, Pacote

class MotoristaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Motorista # Aponta para o medelo que estará sendo Serializado -> models.py
        fields = ['id', 'nome', 'cpf', 'cnh', 'telefone', 'endereco', 'ativo', 'data_nascimento']
    #nome = serializers.CharField(max_length=150)
    #cpf = serializers.CharField(max_length=14)
    #cnh = serializers.CharField(max_length=20)
    #telefone = serializers.CharField(max_length=14)
    #endereco = serializers.CharField(max_length=100)
    #ativo = serializers.BooleanField()
    #data_nascimento = fields.DateField(input_formats=['%Y-%m-%d'])

    def create(self, validated_data):
        # Com os dados validados, pode-se criar um instance "Motorista"
        motorista = Motorista.objects.create(
            nome = validated_data["nome"],
            cpf = validated_data["cpf"],
            cnh = validated_data["cnh"],
            endereco = validated_data["endereco"],
            telefone = validated_data["telefone"],
            data_nascimento = validated_data["data_nascimento"],
            ativo = validated_data["ativo"]
        )
        return motorista

    def validate(self, attrs): 
        telefone = attrs.get("telefone", "") # Pega o campo telefone e caso não exista, pega valor vazio "" 
        if not telefone.startswith("+55"): # Codigo não br
            raise serializers.ValidationError("Telefone deve estar associado a um número Brasileiro") # VALIDATE FEITO APENAS PARA APRENDIZADO/TESTE
        return attrs # Retorna os proprios dados

    def update(self, instance, validated_data): # Subistitui os dados que vieram da requisição (validated_data) pelos dados que ja estao no db (instace) 
        instance.nome = validated_data.get("nome", instance.nome) 
        # tento substituir pelo novo valor, caso não tenha valor
        # já seto o instance.nome (val original) como default

        instance.cpf = validated_data.get("cpf", instance.cpf) 
        instance.cnh = validated_data.get("cnh", instance.cnh) 
        instance.telefone = validated_data.get("telefone", instance.telefone) 
        instance.endereco = validated_data.get("endereco", instance.endereco) 
        instance.ativo = validated_data.get("ativo", instance.ativo) 
        instance.data_nascimento = validated_data.get("data_nascimento", instance.data_nascimento) 

        #acima eu apenas substitui os valores do instance que esta em memoria, ainda preciso persistir no db
        instance.save()
        return instance
    
class CaminhaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Caminhao
        fields = ['placa', 'modelo', 'motorista']

    #placa = serializers.CharField(max_length=8) 
    # unique pois não podemos ter um mesmo caminhao com a mesma placa
    # verbose_name -> nome que aparece dentro do painel adm na parte de editar/ver placa do caminhao
    #modelo = serializers.CharField(max_length=100)
    motorista = serializers.SlugRelatedField(many=True, read_only=True, slug_field='nome')

    def create(self, validated_data): # Valor padrao para nome de motorista
        nome_motorista = validated_data.pop('nome_motorista', None)
        caminhao = Caminhao.objects.create(
                placa = validated_data["placa"],
                modelo = validated_data["modelo"]
            )

        if nome_motorista:
            # Busca o motorista no banco de dados usando o nome
            motorista_obj, created = Motorista.objects.get_or_create(nome=nome_motorista)
            caminhao.motorista.set([motorista_obj])

        return caminhao

    def update(self, instance, validated_data):
        motorista_nome = validated_data.pop("motorista_nome", None)
        # .create() não aceita um campo many to many
        # Retirar o nome do motorista do validated_data
        #validated_data.pop("motorista", None)

        if motorista_nome:
        # Substituir a entidade
            motorista_obj, created = Motorista.objects.get_or_create(nome=motorista_nome)
            instance.motorista.set([motorista_obj])
        else: # O campo motorista não foi enviado no patch
            pass

        instance.placa = validated_data.get("placa", instance.placa)
        instance.modelo = validated_data.get("modelo", instance.modelo)

        instance.save()
        return instance
    
class PacoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pacote
        fields = ['codigo_rastreio', 'destino', 'cliente', 'motorista', 'status', 'telefone']
    #codigo_rastreio = serializers.CharField(max_length=50)
    #destino = serializers.CharField(max_length=150)
    #cliente = serializers.CharField(max_length=150)
    #status = serializers.CharField(max_length=15)
    #telefone = serializers.CharField(max_length=14)
    motorista = serializers.CharField(max_length=150)

    def create(self, validated_data):
        pacote = Pacote.objects.create(
            codigo_rastreio = validated_data["codigo_rastreio"],
            cliente = validated_data["cliente"],
            motorista = Motorista.objects.get(nome=(validated_data["motorista"])),
            status = validated_data["status"],
            destino = validated_data["destino"],
            telefone = validated_data["telefone"]
        )
        #Motorista.objects.get() pegar o id a partir do nome do objeto
        return pacote
    
    def update(self, instance, validated_data):
        motorista_nome = validated_data.pop("motorista_nome", None)
        if motorista_nome:
            # Busca ou cria o motorista
            motorista_obj, created = Motorista.objects.get_or_create(nome=motorista_nome)
            instance.motorista.set([motorista_obj])  # Agora repassa a INSTÂNCIA, não a string!

        else: # O campo motorista não foi enviado no patch
            pass

            # Substituindo campos simples
        instance.codigo_rastreio = validated_data.get("codigo_rastreio", instance.codigo_rastreio)
        instance.destino = validated_data.get("destino", instance.destino)
        instance.cliente = validated_data.get("cliente", instance.cliente)
        instance.status = validated_data.get("status", instance.status)
        instance.telefone = validated_data.get("telefone", instance.telefone)
        instance.save()
        return instance
