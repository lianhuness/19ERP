from django.urls import path

from . import views

urlpatterns = [
    path('', views.account_index, name='account_index'),
    path('add/', views.add_account, name='add_account'),
    path('<int:account_id>/edit/', views.edit_account, name='edit_account'),
    path('<int:account_id>/', views.view_account, name='view_account'),

    # Balance
    path('<int:account_id>/init/', views.init_account_balance, name='init_account_balance'),
    path('<int:account_id>/duizhang/', views.account_duizhang, name='account_duizhang'),

    # Payee
    path('payee_index/', views.payee_index, name='payee_index'),
    path('payee/<int:payee_id>/', views.view_payee, name='view_payee'),
    path('payee_index/add/', views.add_payee, name='add_payee'),
    path('payee/<int:payee_id>/edit/', views.edit_payee, name='edit_payee'),

    # Transaction
    #
    path('transfer/all/', views.list_transaction, name='list_transaction'),
    path('transfer/<int:tran_id>/', views.view_transaction, name='view_transaction'),
    path('transfer/<int:tran_id>/edit/', views.edit_transaction, name='edit_transaction'),

    # 收款/结汇
    path('clientorder/<int:co_id>/add_income/', views.add_income, name='add_income'),
    path('income/<int:income_id>/jiehui/', views.jiehui_income, name='jiehui_income'),

    # 付款
    path('clientorder/<int:co_id>/add_outcome/', views.add_outcome, name='add_outcome'),



]