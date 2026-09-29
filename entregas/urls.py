from django.urls import path
#from entregas.views import motorista_list, motoristas_detail, caminhao_list, caminhao_detail, pacote_list, pacote_detail
from entregas.views import MotoristaList, MotoristaDetail, CaminhaoList, CaminhaoDetail, PacoteList, PacoteDetail


#   MotoristaList.as_view() chama a classe view como uma funcao

urlpatterns = [
    path('motoristas/', MotoristaList.as_view()), # path, view que é chamada
    path('motoristas/<int:pk>/', MotoristaDetail.as_view()),
    path('caminhoes/', CaminhaoList.as_view()),
    path('caminhoes/<int:pk>/', CaminhaoDetail.as_view()),
    path('encomendas/', PacoteList.as_view()),
    path('encomendas/<str:codigo_rastreio>/', PacoteDetail.as_view(), name='pacote-detail'),
]

