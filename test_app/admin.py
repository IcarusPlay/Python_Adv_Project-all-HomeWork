from django.contrib import admin
from test_app.models import Book, Author, Task, SubTask, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)



class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'categories')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    inlines = [SubTaskInline]  # Задание 1: добавляем инлайн


    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + '...'
        return obj.title

    short_title.short_description = 'Title'

def mark_done(modeladmin, request, queryset):
    queryset.update(status=SubTask.DONE)


mark_done.short_description = 'Mark selected subtasks as Done'


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'task')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    actions = [mark_done]


admin.site.register(Book)
admin.site.register(Author)