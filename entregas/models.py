from django.db import models

# Criar as classes para o django ler e montar as tabelas SQL 
# $python3 manage.py makemigrations
# $python3 manage.py migrate 

# Fazer consultas e criar objetos no db $python3 manage.py shell
class Motorista(models.Model):
    """
    nome, cpf, CNH, endereco, data de nascimento, ativo
    """
    # verbose_name -> nome que aparece dentro do painel adm na parte de editar/ver placa do caminhao

    nome = models.CharField(max_length=150, verbose_name="Nome")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    cnh = models.CharField(max_length=20, unique=True, verbose_name="CNH")
    telefone = models.CharField(max_length=14, null=True)
    # Textfield é usado para textos longos, sem limite como o charfield (max_length)
    endereco = models.TextField()
    data_nascimento = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self): # Função que define o que vai aparecer escrito no painel adm
        data_formatada = self.data_nascimento.strftime('%d/%m/%Y') if self.data_nascimento else "Não informada"
        return f"{self.nome} id: {self.id}"

class Caminhao(models.Model):
    placa = models.CharField(max_length=8, unique=True, verbose_name="Placa do Veículo") 
    # unique pois não podemos ter um mesmo caminhao com a mesma placa
    # verbose_name -> nome que aparece dentro do painel adm na parte de editar/ver placa do caminhao
    modelo = models.CharField(max_length=100, verbose_name="Modelo")

    # Referencia a classe Motorista como chave estrangeira, relacionando o caminhao com o motorista
    # mas o caminhao pode ser dirigido por varios motoristas
    # por isso uso o models.ManyToMany
    # blank=True, permite que o caminhao seja cadastrado sem motorista
    # manytomany não usa on_delete nem null
    motorista = models.ManyToManyField(Motorista, blank=True)

    def __str__(self): # Função que define o que vai aparecer escrito no painel adm
        return f"{self.placa} {self.modelo}"

    # Por padrão o django tenta traduzir o plural da palavra caminhao no painel adm
    # dessa forma, adicionarei a sublasse Meta abaixo para corrigir
    class Meta:
        verbose_name = "Caminhão"
        verbose_name_plural = "Caminhões"


class Pacote(models.Model):
    status_code = (('P', 'Pendente'),
                   ('T', 'Em Trânsito'),
                   ('E', 'Entregue'),
                   ('C', 'Cancelado'),
                   )

    # Textfield é usado para textos longos, sem limite como o charfield (max_length)
    codigo_rastreio = models.CharField(max_length=50, unique=True)
    destino = models.TextField()
    cliente = models.CharField(max_length=150, verbose_name="Destinatario", null=True)
    motorista = models.ForeignKey(Motorista, on_delete=models.PROTECT, verbose_name="Motorista Responsável") 
    telefone = models.CharField(max_length=14, null=True)

    # on_delete=models.PROTECT
    # Caso o motorista seja deletado do db por algum motivo
    # Esse atributo proibe essa ação, pois há um produto atrelado ao motorista
    status = models.CharField(max_length=1, choices=status_code, blank=True, default='P')
    # choices= , gera uma lista com a tupla status_code

    def __str__(self): # Função que define o que vai aparecer escrito no painel adm
        return f"{self.codigo_rastreio} - Status: {self.get_status_display()}"

