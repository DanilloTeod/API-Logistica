from rest_framework import serializers, fields

class MotoristaSerializers(serializers.Serializer):
    nome = serializers.CharField(max_length=150)
    cpf = serializers.CharField(max_length=14)
    cnh = serializers.CharField(max_length=20)
    telefone = serializers.CharField(max_length=14)
    endereco = serializers.CharField(max_length=100)
    ativo = serializers.BooleanField()
    data_nascimento = fields.DateField(input_formats=['%d/%m/%Y'])

class CaminhaoSerializers(serializers.Serializer):
        placa = serializers.CharField(max_length=8) 
        # unique pois não podemos ter um mesmo caminhao com a mesma placa
        # verbose_name -> nome que aparece dentro do painel adm na parte de editar/ver placa do caminhao
        modelo = serializers.CharField(max_length=100)
        motorista = serializers.SlugRelatedField(many=True, read_only=True, slug_field='nome')

class PacoteSerializers(serializers.Serializer):
    codigo_rastreio = serializers.CharField(max_length=50)
    destino = serializers.CharField(max_length=150)
    cliente = serializers.CharField(max_length=150)
    motorista = serializers.CharField(max_length=150)
    status = serializers.CharField(max_length=15)
    telefone = serializers.CharField(max_length=14)

