from miApp import views
from django.urls import path


urlpatterns = [
    
    path('inicio_sesionjg/', views.inicio_sesionjg, name='inicio_sesionjg'),
    path('', views.index, name='index'),
    path('logout/', views.signout, name='logout'),
    path('micuenta/', views.micuenta, name='micuenta'),
    path('informes_creados/', views.informes_creados, name='informes_creados'),
    path('recuperarcontra/', views.recuperarcontra, name='recuperarcontra'),
    path('registrarse/', views.registrarse, name='registrarse'), 
    path('aboutus/', views.aboutus, name='aboutus'),
    path('habitaciones/', views.habitaciones, name='habitaciones'),
    path('contacto/', views.contacto, name='contacto'),
    path('cambiar_contra/<int:user_id>/', views.cambiar_contra, name='cambiar_contra'),
    path('addtocar/<codigo>', views.addtocar, name="addtocar"),
    path('dropitem/<codigo>', views.dropitem, name="dropitem"),
    path('reservacion', views.reservacion, name="reservacion"),
    path('agendar/', views.agendar, name='agendar'),
    
]   
