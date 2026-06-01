from django.contrib import admin
from django.urls import path

from test_app.views import (
    greetings,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskStatsView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home-page/', greetings),


    path('api/tasks/create/', TaskCreateView.as_view()),


    path('api/tasks/stats/', TaskStatsView.as_view()),


    path('api/tasks/', TaskListView.as_view()),
    path('api/tasks/<int:pk>/', TaskDetailView.as_view()),
]
