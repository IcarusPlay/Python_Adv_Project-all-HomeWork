from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Задание 3: импорты для Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from test_app.views import (
    greetings,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatsView,
    MyTasksView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'api/categories', CategoryViewSet, basename='category')

# Задание 3: настройка схемы Swagger
# PUBLIC=True — документация видна без авторизации (удобно для разработки)
schema_view = get_schema_view(
    openapi.Info(
        title='Task Manager API',
        default_version='v1',
        description='API для управления задачами и подзадачами',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home-page/', greetings),

    # JWT токены
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Tasks
    path('api/tasks/stats/', TaskStatsView.as_view()),
    path('api/tasks/my/', MyTasksView.as_view()),       # Задание 1: мои задачи
    path('api/tasks/', TaskListCreateView.as_view()),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view()),

    # SubTasks
    path('api/subtasks/', SubTaskListCreateView.as_view()),
    path('api/subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view()),

    # Categories через роутер
    path('', include(router.urls)),

    # Задание 3: Swagger и ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
