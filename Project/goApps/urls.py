from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('App/<int:id>/', views.App, name='App'),
    path('points/', views.points, name='points'),
    path('task/', views.task, name='task'),
]

# Serving media files only during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)