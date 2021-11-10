from django.urls import path
from . import views

app_name = 'researchdata'

urlpatterns = [
    path('test/', views.TestView.as_view(), name='test'),
]
