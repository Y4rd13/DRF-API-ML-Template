from django.urls import path
from .views import (
    MyCustomView,
    CustomTokenObtainPairView,
    UserCreate,
    CustomTokenRefreshView,
    TestView, # Custom view for testing purposes. Comment to use in production.
)

urlpatterns = [
    path('v1/service/customservice', MyCustomView.as_view(), name='my_custom_view'),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('user/create', UserCreate.as_view(), name='user_create'),
    path('test', TestView.as_view(), name='testView'), # Custom view for testing purposes. Comment to use in production.
]