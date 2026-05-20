from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    discounted_price = models.FloatField(null=True)
    published_date = models.DateField()
    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
    )


class Author(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=35)
    pseudonym = models.CharField(max_length=20)
    bio = models.TextField(null=True)
    email = models.EmailField(max_length=75, null=True)
    website = models.URLField(null=True)
    age = models.PositiveSmallIntegerField(null=True)
    followers_count = models.PositiveIntegerField(null=True)
    posts_count = models.PositiveIntegerField(null=True)
    comments_count = models.PositiveIntegerField(null=True)
    reputation_score = models.DecimalField(null=True, max_digits=3, decimal_places=2)
    monetisation_income = models.FloatField(null=True)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reading_time = models.DurationField(null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name')
        ]


class Task(models.Model):
    NEW = 'New'
    IN_PROGRESS = 'In progress'
    PENDING = 'Pending'
    BLOCKED = 'Blocked'
    DONE = 'Done'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In progress'),
        (PENDING, 'Pending'),
        (BLOCKED, 'Blocked'),
        (DONE, 'Done'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField('Category')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    deadline = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_task_title')
        ]


class SubTask(models.Model):
    NEW = 'New'
    IN_PROGRESS = 'In progress'
    PENDING = 'Pending'
    BLOCKED = 'Blocked'
    DONE = 'Done'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In progress'),
        (PENDING, 'Pending'),
        (BLOCKED, 'Blocked'),
        (DONE, 'Done'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='subtasks'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    deadline = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_subtask_title')
        ]
