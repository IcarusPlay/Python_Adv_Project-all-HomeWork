from django.contrib import admin
from django.urls import path

from test_app.views import (
    greetings,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskStatsView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home-page/', greetings),

    # Tasks
    path('api/tasks/create/', TaskCreateView.as_view()),
    path('api/tasks/stats/', TaskStatsView.as_view()),
    path('api/tasks/', TaskListView.as_view()),
    path('api/tasks/<int:pk>/', TaskDetailView.as_view()),

    # Задание 5: SubTasks
    path('api/subtasks/', SubTaskListCreateView.as_view()),
    path('api/subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view()),
]
