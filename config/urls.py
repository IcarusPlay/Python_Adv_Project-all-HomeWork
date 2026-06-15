from django.contrib import admin
from django.urls import path

from test_app.views import (
    greetings,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatsView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
)

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
]
