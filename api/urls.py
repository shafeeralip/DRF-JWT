from django.urls import path
from .views import Items,ItemDetail,login
from rest_framework import routers

# router=routers.DefaultRouter()
# router.register('',Items)


urlpatterns=[
    path('login/',login,name="login"),
    path('items/', Items.as_view(), name='itmes'),
    path('items/<int:pk>/',ItemDetail.as_view(),name="items")
]