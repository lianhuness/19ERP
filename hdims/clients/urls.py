from django.urls import path

from . import views

urlpatterns = [
    path('', views.client_index, name='client_index'),
    path('list_all_clients', views.list_all_clients, name='list_all_clients'),
    path('add/', views.add_client, name='add_client'),
    path('edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('<int:client_id>/', views.view_client, name='view_client'),

    path('<int:client_id>/add_contactor', views.add_contactor, name='add_contactor'),
    path('edit_contactor/<int:contactor_id>/', views.edit_contactor, name='edit_contactor'),

    path('view_cp/<int:cp_id>/', views.view_cp, name='view_cp'),
    path('<int:client_id>/add_clientproduct/', views.add_clientproduct, name='add_clientproduct'),
    path('edit_cp_name/<int:cp_id>/', views.edit_cp_name, name='edit_cp_name'),
    path('edit_cp_info/<int:cp_id>/', views.edit_cp_info, name='edit_cp_info'),
    path('expire/<int:cp_id>/<int:expired>/', views.expire_cp, name='expire_cp'),

    path('list_my_orders/', views.list_my_orders, name='list_my_orders'),
    path('list_all_orders/', views.list_all_orders, name='list_all_orders'),
    path('list_all_orders/summaryView', views.list_all_order_summaryView, name='list_all_order_summaryView'),
    path('<int:client_id>/add_clientorder/', views.add_clientorder, name='add_clientorder'),
    path('co/<int:co_id>/', views.view_co, name='view_co'),
    path('co/<int:co_id>/edit/', views.edit_co, name='edit_co'),
    path('co/<int:co_id>/update_status/<str:nxt_action>/', views.update_co_status, name='update_co_status'),
    path('co/<int:co_id>/add_cop', views.add_cop, name='add_cop'),
    path('cop/<int:cop_id>/edit', views.edit_cop, name='edit_cop'),


]