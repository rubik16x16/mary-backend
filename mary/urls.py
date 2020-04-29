from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from auth.views import MyTokenObtainPairView

user_patterns = ([
	path('accounts/', include('user_accounts.urls')),
	path('', include('transactions.urls')),
	path('', include('transaction_categories.urls'))
], 'user')

urlpatterns = [
  path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
	path('user/', include(user_patterns))
]
