from django.contrib import admin
from test_app.models import Book, Author,Task, SubTask, Category

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Category)