from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from auth.views import MyTokenObtainPairView

urlpatterns = [
  path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
  path('user/accounts/', include('user_accounts.urls')),
	path('user/accounts/<int:account_pk>/transactions', include('transactions.urls'))
]
