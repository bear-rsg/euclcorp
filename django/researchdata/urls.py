from django.urls import path
from . import views

app_name = 'researchdata'

urlpatterns = [
    path('monolingual/', views.MonolingualCorporaView.as_view(), name='monolingual'),
    path('parallel/', views.ParallelCorpusView.as_view(), name='parallel'),
]
