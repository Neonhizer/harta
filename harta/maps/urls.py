# from django.urls import path
# from . import views

# urlpatterns = [
#     path('harta', views.harta, name='harta'), 
#     path('street', views.streetview, name='street'),
#     path('aula', views.scrape_bizbrasov, name='aula'),
#     path('get_images/', views.get_images, name='get_images'),

# ]


from django.urls import path
from . import views

urlpatterns = [
    path('harta', views.harta, name='harta'),
    path('get_images/', views.get_images, name='get_images'),
    path('aula/', views.aula, name='aula'),
    path('street/', views.streetview, name ='street' )
]
