from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('campaña/', views.mostrar_campañas, name='mostrar_campañas'), 
    path('historial-donaciones/', views.historial_donaciones, name='listar_donaciones'),
    path('crear-donacion/', views.crear_donacion, name='crear_donacion'),

    path('crear-campaña/', views.crear_campaña, name='crear_campaña'), 
    path('campaña/<int:campaña_id>/editar/', views.editar_campaña, name='editar_campaña'),
    path('campaña/<int:campaña_id>/eliminar/', views.eliminar_campaña, name='eliminar_campaña'),



    path('registro/ong/', views.registrar_ong, name='registro_ong'),
    path('registro/donante/', views.registrar_donante, name='registro_donante'),
    path('logout/', views.salir, name='logout'),

]
