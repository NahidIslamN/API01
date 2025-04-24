
from django.urls import path

from .views import userregisterview, userlogin, ProductView

urlpatterns = [
    path('register/', userregisterview.as_view(), name='register'),
    path('login/', userlogin.as_view(), name="login"),
    path('products/', ProductView.as_view(), name='products')
    
]
