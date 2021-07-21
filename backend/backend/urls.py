from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('foodmin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
]
