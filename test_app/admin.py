from django.contrib import admin
from test_app.models import Book, Author, Task, SubTask, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'categories')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'task')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    raw_id_fields = ('task',)


admin.site.register(Book)
admin.site.register(Author)
