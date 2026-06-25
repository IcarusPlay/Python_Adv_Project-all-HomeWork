from django.http import HttpResponse, HttpRequest
from django.utils import timezone

from rest_framework import generics, filters, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from test_app.models import Task, SubTask, Category
from test_app.serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskCreateSerializer,
    CategorySerializer,
)
from test_app.permissions import IsOwnerOrReadOnly


def greetings(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the polls page.")


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    # Задание 1: автоматически пишем текущего юзера как владельца
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # Задание 2: IsOwnerOrReadOnly — изменять/удалять только владелец
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


# Задание 1: представление для получения задач текущего пользователя
# GET /api/tasks/my/ — только мои задачи
class MyTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # фильтруем только задачи текущего пользователя
        return Task.objects.filter(owner=self.request.user)


class TaskStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        total = Task.objects.count()
        by_status = Task.objects.values('status').annotate(count=Count('id'))
        status_counts = {item['status']: item['count'] for item in by_status}
        now = timezone.now()
        overdue = Task.objects.filter(deadline__lt=now).exclude(status=Task.DONE).count()
        return Response({
            'total_tasks': total,
            'by_status': status_counts,
            'overdue_tasks': overdue,
        })


class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    # Задание 1: автоматически пишем текущего юзера как владельца подзадачи
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    # Задание 2: только владелец может менять/удалять
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='count_tasks')
    def count_tasks(self, request):
        categories = Category.objects.annotate(task_count=Count('task'))
        data = [
            {'id': cat.id, 'name': cat.name, 'task_count': cat.task_count}
            for cat in categories
        ]
        return Response(data)
