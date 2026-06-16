from rest_framework import serializers
from django.utils import timezone
from test_app.models import Task, SubTask, Category


# старый сериализатор оставляем — используется в TaskCreateView и других вьюхах
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
        read_only_fields = ['id', 'created_at']


# Задание 1: created_at только для чтения
class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at']


# Задание 2: проверка уникальности названия категории
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({'name': 'Категория с таким названием уже существует'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        # проверяем что другая категория с таким именем не существует
        if Category.objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({'name': 'Категория с таким названием уже существует'})
        return super().update(instance, validated_data)


# Задание 3: вложенный сериализатор для подзадач
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    # related_name='subtasks' — поэтому указываем именно его
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks']


# Задание 4: валидация deadline — не может быть в прошлом
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_deadline(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError('Дедлайн не может быть в прошлом')
        return value


# Задание 1: сериализатор для CategoryViewSet
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
