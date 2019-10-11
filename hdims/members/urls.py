from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='member_index'),
    path('login/', views.member_login, name='member_login'),
    path('logout/', views.member_logout, name='member_logout'),
    path('add/', views.add, name='add_member'),
    path('edit/<int:member_id>/', views.edit, name='edit_member'),
]