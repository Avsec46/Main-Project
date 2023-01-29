from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

urlpatterns = [
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authorizationcheck',views.methodForAuthenticatedOnly),
    path('user/register',views.user_register,name='user_register'),
    path('complain_detail',views.complainDetail,name='complain_detail'),
]
