from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
	path('register/', views.RegisterUserApiView.as_view(), name='register'),
	path('login/', views.LoginUserApiView.as_view(), name='login'),
	path('profile/', views.ProfileUserApiView.as_view(), name='profile')
]