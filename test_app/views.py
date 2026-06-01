from django.http import HttpResponse, HttpRequest
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count

from test_app.models import Task
from test_app.serializers import TaskSerializer


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
        overdue = Task.objects.filter(
            deadline__lt=now
        ).exclude(status=Task.DONE).count()

        return Response({
            'total_tasks': total,
            'by_status': status_counts,
            'overdue_tasks': overdue,
        })
