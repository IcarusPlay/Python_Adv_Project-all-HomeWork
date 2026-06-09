from django.http import HttpResponse, HttpRequest
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

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


class TaskCreateView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Задание 1: список задач с фильтром по дню недели
class TaskListView(APIView):


    WEEKDAYS = {
        'monday': 1, 'tuesday': 2, 'wednesday': 3,
        'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7,
        'понедельник': 1, 'вторник': 2, 'среда': 3,
        'четверг': 4, 'пятница': 5, 'суббота': 6, 'воскресенье': 7,
    }

    def get(self, request):
        tasks = Task.objects.all()

        day = request.query_params.get('day')  # ?day=вторник
        if day:
            day_number = self.WEEKDAYS.get(day.lower())
            if day_number is None:
                return Response(
                    {'error': f'Неизвестный день недели: {day}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # iso_week_day: 1=понедельник, 7=воскресенье
            tasks = tasks.filter(deadline__iso_week_day=day_number)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskDetailView(APIView):
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


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


# Задание 2: пагинация — 5 объектов на страницу
class SubTaskPagination(PageNumberPagination):
    page_size = 5


# Задание 2 + 3: список подзадач с пагинацией и фильтрами
class SubTaskListCreateView(APIView):

    def get(self, request):
        # сортировка по убыванию даты добавления (задание 2)
        subtasks = SubTask.objects.all().order_by('-created_at')

        # Задание 3: фильтр по названию главной задачи
        task_title = request.query_params.get('task')  # ?task=Сделать домашку
        if task_title:
            subtasks = subtasks.filter(task__title__icontains=task_title)

        # Задание 3: фильтр по статусу подзадачи
        subtask_status = request.query_params.get('status')  # ?status=Done
        if subtask_status:
            subtasks = subtasks.filter(status=subtask_status)

        # пагинация
        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(subtasks, request)
        serializer = SubTaskCreateSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if subtask is None:
            return Response({'error': 'SubTask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if subtask is None:
            return Response({'error': 'SubTask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        subtask = self.get_object(pk)
        if subtask is None:
            return Response({'error': 'SubTask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if subtask is None:
            return Response({'error': 'SubTask not found'}, status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
