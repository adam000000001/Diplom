from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('package/<int:package_id>/', views.package_detail, name='package_detail'),
    path('order/<int:order_id>/payment/', views.payment, name='payment'),
    path('order/<int:order_id>/success/', views.order_success, name='order_success'),
]