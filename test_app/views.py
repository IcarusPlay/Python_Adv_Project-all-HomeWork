from django.http import HttpResponse, HttpRequest
from django.utils import timezone

from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Count

from test_app.models import Task, SubTask
from test_app.serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskCreateSerializer,
)


def greetings(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the polls page.")


# Задание 1: Generic Views для задач
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # фильтрация по status и deadline
    filterset_fields = ['status', 'deadline']

    # поиск по title и description (?search=...)
    search_fields = ['title', 'description']

    # сортировка по created_at (?ordering=created_at или ?ordering=-created_at)
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # по умолчанию — сначала новые


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskStatsView(APIView):
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


# пагинация для подзадач — 5 на страницу
class SubTaskPagination(PageNumberPagination):
    page_size = 5


# Задание 2: Generic Views для подзадач
class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # фильтрация по status и deadline
    filterset_fields = ['status', 'deadline']

    # поиск по title и description (?search=...)
    search_fields = ['title', 'description']

    # сортировка по created_at (?ordering=created_at или ?ordering=-created_at)
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer


# Задание 1: ModelViewSet для категорий
from rest_framework import viewsets
from rest_framework.decorators import action
from test_app.models import Category
from test_app.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # Задание 1: кастомный метод — кол-во задач в каждой категории
    @action(detail=False, methods=['get'], url_path='count_tasks')
    def count_tasks(self, request):
        # берём все категории и считаем связанные задачи через related_name
        categories = Category.objects.annotate(task_count=Count('task'))
        data = [
            {'id': cat.id, 'name': cat.name, 'task_count': cat.task_count}
            for cat in categories
        ]
        return Response(data)
