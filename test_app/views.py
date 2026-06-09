from django.http import HttpResponse, HttpRequest
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
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


# Задание 5: создание и список подзадач
class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Задание 5: получение, обновление, удаление конкретной подзадачи
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
        # partial=True — можно передавать не все поля
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
