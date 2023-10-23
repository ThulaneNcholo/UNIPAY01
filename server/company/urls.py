from django.urls import path
from .import views
# images urls 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('company-profile', views.CompnayProfileView, name='company-profile'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)