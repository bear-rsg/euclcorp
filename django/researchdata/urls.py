from django.urls import path
from . import views

app_name = 'researchdata'

urlpatterns = [
    # Inputs
    path('monolingual/', views.InputMonolingualView.as_view(), name='monolingual-input'),
    path('parallel/', views.InputParallelView.as_view(), name='parallel'),
    # Output
    path('results/', views.OutputView.as_view(), name='output'),
]
