from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('admin_1/', views.admin_1, name='admin_1'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)