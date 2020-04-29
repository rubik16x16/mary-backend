from django.urls import path
from .import views

app_name = 'transaction_categories'
urlpatterns = [
	path('transaction_categories', views.TransactionCategoriesList.as_view(), name='list'),
	path('transaction_categories/<int:pk>/', views.TransactionCategoryDetail.as_view(), name='detail')
]
