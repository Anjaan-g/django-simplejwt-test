from django.urls import path, include
from .routers import router

app_name = 'product'
urlpatterns = [
    path('',include(router.urls))
]
