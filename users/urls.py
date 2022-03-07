from django.urls import path, include
from .views import LoginViewSet
app_name = 'users'

urlpatterns = [
    path('login/',LoginViewSet.as_view(),name='token_obtain_pair')
]
