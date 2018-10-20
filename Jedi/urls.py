from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('padawan_add/', padawan_auth),
    path('test/', test_view),
    path('jedi/', jedi_take),
    path('candidates', jedi_candidate_sel)
]
