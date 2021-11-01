from django.urls import path
from . import views
from .views import other_page

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:rubric_pk>/<int:pk>/', views.detail, name='detail'),
    path('<int:pk>', views.by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/login/', views.BBLoginView.as_view(), name='login'),
    path('accounts/logout/', views.BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/change', views.ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/delete', views.DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/<int:pk>/', views.profile_bb_detail, name='profile_bb_detail'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/password/change/', views.BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path('accounts/register/done/', views.RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/activate/<str:sign>/', views.user_activate, name='register_activate'),
]