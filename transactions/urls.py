from django.urls import path
from .import views

app_name = 'transactions'
urlpatterns = [
	path('accounts/<int:account_pk>/transactions', views.TransactionsAccountList.as_view(), name='list'),
	path('transactions/<int:pk>/', views.TransactionsDetail.as_view(), name='detail')
]
