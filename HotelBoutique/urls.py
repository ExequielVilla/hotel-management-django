"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('habitaciones.urls')), #incluye todas las urls del modulo habitaciones
    path('', include('usuarios.urls')), #incluye todas las urls del modulo usuarios
    path('', include('reservas.urls')), #incluye todas las urls del modulo reservas
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:     
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

