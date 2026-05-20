import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from test_app.models import Task, SubTask



# 1. CREATE


task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status=Task.NEW,
    deadline=timezone.now() + timedelta(days=3),
)

SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status=SubTask.NEW,
    deadline=timezone.now() + timedelta(days=2),
    task=task,
)

SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status=SubTask.NEW,
    deadline=timezone.now() + timedelta(days=1),
    task=task,
)


# 2. READ


new_tasks = Task.objects.filter(status=Task.NEW)
print(new_tasks)

overdue_done_subtasks = SubTask.objects.filter(
    status=SubTask.DONE,
    deadline__lt=timezone.now(),
)
print(overdue_done_subtasks)



# 3. UPDATE


task = Task.objects.get(title="Prepare presentation")
task.status = Task.IN_PROGRESS
task.save(update_fields=['status'])

subtask = SubTask.objects.get(title="Gather information")
subtask.deadline = timezone.now() - timedelta(days=2)
subtask.save(update_fields=['deadline'])

subtask = SubTask.objects.get(title="Create slides")
subtask.description = "Create and format presentation slides"
subtask.save(update_fields=['description'])


# 4. DELETE

task = Task.objects.get(title="Prepare presentation")
task.delete()
