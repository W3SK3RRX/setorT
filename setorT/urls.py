from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sistema_gerenciamento.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "sistema_gerenciamento.views.handler404"
