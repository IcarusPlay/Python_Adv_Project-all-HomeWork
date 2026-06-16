from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from test_app.views import (
    greetings,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatsView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    CategoryViewSet,
)

# Задание 1: роутер для CategoryViewSet
router = DefaultRouter()
router.register(r'api/categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home-page/', greetings),

    # Tasks
    path('api/tasks/stats/', TaskStatsView.as_view()),
    path('api/tasks/', TaskListCreateView.as_view()),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view()),

    # SubTasks
    path('api/subtasks/', SubTaskListCreateView.as_view()),
    path('api/subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view()),

    # Categories — через роутер
    path('', include(router.urls)),
]
