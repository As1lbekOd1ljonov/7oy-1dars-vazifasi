from django.urls import path
from .views import (
    IndexListView, ColorDetailView, BrandDetailView, CarDetailView, UserRegisterView,
    UserLoginView, UserLogoutView, UserProfileView, SendMailView, CommentManageView, AddBrandView, CarCreateView,
    AddColorView, CarUpdateView, CarDeleteView, )




urlpatterns = [
    path('', IndexListView.as_view(), name='index'),

    path('color/<int:pk>/', ColorDetailView.as_view(), name='color_detail'),

    path('brand/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),

    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path("car/manage/<int:pk>/update/", CarUpdateView.as_view(), name='car_update'),
    path("car/manage/<int:pk>/delete/", CarDeleteView.as_view(), name='car_delete'),

    path('car/<int:car_id>/comment/', CommentManageView.as_view(), name='comment_manage'),

    path('register/', UserRegisterView.as_view(), name='user_register'),

    path('login/', UserLoginView.as_view(), name='user_login'),

    path('logout/', UserLogoutView.as_view(), name='user_logout'),

    path('profile/<str:username>', UserProfileView.as_view(), name='profile'),

    path('send_message/', SendMailView.as_view(), name='send_message'),

    path('add_brand/', AddBrandView.as_view(), name='add_brand'),
    path('add_car/', CarCreateView.as_view(), name='add_cars'),
    path('add_color/', AddColorView.as_view(), name='add_color'),

]