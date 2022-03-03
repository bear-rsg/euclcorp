from django.urls import path
from . import views

app_name = 'researchdata'

urlpatterns = [
    # Monolingual Corpora
    path('monolingual/', views.InputMonolingualView.as_view(), name='monolingual-input'),
    path('monolingual/results/', views.MonolingualCorporaOutputView.as_view(), name='monolingual-output'),
    # Parallel Corpus
    path('parallel/', views.InputParallelView.as_view(), name='parallel'),
]
