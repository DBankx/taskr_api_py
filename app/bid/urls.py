from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bid import views

app_name = 'bid'

router = DefaultRouter()

router.register('bid', views.BidView)

urlpatterns = [
	path('<str:id>/', views.ListCreateBidApiView.as_view(), name='list-create'),
	path('manage', include(router.urls))
]