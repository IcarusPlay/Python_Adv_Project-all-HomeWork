from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Задание 1: импортируем views для JWT токенов
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from test_app.views import (
    greetings,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatsView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    CategoryViewSet,
)


router = DefaultRouter()
router.register(r'api/categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home-page/', greetings),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # POST /api/token/refresh/ — обновить access токен через refresh токен
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/tasks/stats/', TaskStatsView.as_view()),
    path('api/tasks/', TaskListCreateView.as_view()),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view()),


    path('api/subtasks/', SubTaskListCreateView.as_view()),
    path('api/subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view()),


    path('', include(router.urls)),
]
