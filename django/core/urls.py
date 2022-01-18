from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('', include('general.urls')),
    path('corpus/', include('researchdata.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
