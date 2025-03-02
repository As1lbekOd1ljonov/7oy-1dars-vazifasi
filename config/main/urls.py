from django.urls import path
from .views import (
    index, color_detail, brand_detail, car_detail, user_register,
    user_login, user_logout, profile, send_message_to_email)
urlpatterns = [
    path('', index, name='index'),

    path('color/<int:color_id>/', color_detail, name='color_detail'),

    path('brand/<int:brand_id>/', brand_detail, name='brand_detail'),

    path('car/<int:car_id>/', car_detail    , name='car_detail'),

    path('register/', user_register, name='user_register'),

    path('login/', user_login, name='user_login'),

    path('logout/', user_logout, name='user_logout'),
    path('profile/<str:username>', profile, name='profile'),

    path('send_message/', send_message_to_email, name='send_message'),

]