from django.urls import path, include
from task import views
from rest_framework.routers import DefaultRouter

app_name = 'task'

router = DefaultRouter()

router.register('', views.TaskViewSet)

urlpatterns = [
	path('', include(router.urls))
]