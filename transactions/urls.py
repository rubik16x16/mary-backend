from django.urls import path
from .import views

app_name = 'transactions'
urlpatterns = [
	path('', views.TransactionsAccountList.as_view(), name='list'),
	path('<int:pk>/', views.TransactionsDetail.as_view(), name='detail')
]
