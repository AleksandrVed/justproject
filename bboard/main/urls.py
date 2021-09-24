from django.urls import path
from . import views
from .views import other_page

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/login/', views.BBLoginView.as_view(), name='login'),
    path('accounts/logout/', views.BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/change', views.ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/password/change/', views.BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path('accounts/register/done/', views.RegisterDoneView.as_view(), name='register_done'),
]