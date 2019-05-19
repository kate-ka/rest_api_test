from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]
