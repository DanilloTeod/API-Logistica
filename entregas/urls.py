from django.urls import path
from entregas.views import motoristas_list, motoristas_detail, caminhao_detail, caminhao_list, pacote_list, pacote_detail

urlpatterns = [
    path('motoristas/', motoristas_list), # path, view que é chamada
    path('motoristas/<int:id>/', motoristas_detail),
    path('caminhoes/', caminhao_list),
    path('caminhoes/<int:id>/', caminhao_detail),
    path('encomendas/', pacote_list),
    path('encomendas/<str:codigo_rastreio>/', pacote_detail)
]

