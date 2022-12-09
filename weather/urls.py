from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='home'), # the path for our index view
        path('delete_city/<city_id>/', views.delete_city, name='delete_city'),
        path('info_city/<city_id>/', views.info_city, name='info_city'),
        path('searched_cities/', views.search_city, name='searched_city'),

        path('word_page/', views.word_view, name='word_page'),
        path('delete_word/<word_id>/', views.delete_word, name='delete_word'),
        path('about/', views.AboutPageView.as_view(), name='about'),
        ]
