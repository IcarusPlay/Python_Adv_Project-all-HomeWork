from django.db import models

# def get_disc_price_according_orig_price():
#     ...

class Book(models.Model):
    title = models.CharField(max_length=100)  # VarChar(255)
    description = models.TextField()
    price = models.FloatField()
    # discounted_price = models.FloatField()  # NOT NULL
    # discounted_price = models.FloatField(default=0.0)  # DEFAULT 0.0
    # discounted_price = models.FloatField(default=get_disc_price_according_orig_price)  # DEFAULT 0.0
    discounted_price = models.FloatField(null=True)  # NULLABLE
    published_date = models.DateField()

    # связи
    author = models.ForeignKey(
        'Author',
        # on_delete=models.DO_NOTHING,
        # on_delete=models.PROTECT,
        # on_delete=models.SET_DEFAULT, # (!!!!!!!!!! требует доп параметра default=)
        on_delete=models.SET_NULL, # (!!!!!!!!!! требует доп параметра null=True)
        null=True,
        # on_delete=models.SET(), # принимает как объект какую-то функцию, которая должна примениться к объектам
        # on_delete=models.CASCADE,

        related_name='books'
    )

# Миграции и управление моделями отвечают ИСКЛЮЧИТЕЛЬНО ЗА DDL категорию запросов

# DDL query -> Data Definition Language
# DML query -> Data Manipulation Language
# """
# CREATE TABLE IF NOT EXISTS 'test_app_book' (
#     id ...
#     title VarChar(100) NOT NULL
#     description TEXT NOT NULL
#     published_date DATE
# )
# """

class Author(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=35)
    pseudonym = models.CharField(max_length=20)
    bio = models.TextField(null=True)
    email = models.EmailField(max_length=75, null=True)
    # URLValidator() "под капотом" будет проверять, что строка начинается с http:// или https://
    website = models.URLField(null=True)

    # Integer fields
    age = models.PositiveSmallIntegerField(null=True)
    followers_count = models.PositiveIntegerField(null=True)
    posts_count = models.PositiveIntegerField(null=True)
    comments_count = models.PositiveIntegerField(null=True)
    reputation_score = models.DecimalField(
        null=True,
        max_digits=3,  # как много символов должно быть в общем
        decimal_places=2  # из всего этого кол-ва как много должно быть после точки
    )  #  1.00 | 3.75 | 5.00 | 4.99 | 2.01
    monetisation_income = models.FloatField(null=True)

# monday = 14.99
# friday = 14.999999999999999999999999
# nickname = 'QnWr8AoKs' => 'qnwr8aoks'


# BigIntegerField             # [-15_000_000 | 15_000_000]
# IntegerField                # [-1_000_000 | 1_000_000]
# PositiveBigIntegerField     # [0 | 15_000_000]
# PositiveIntegerField        # [1_000_000]
# SmallIntegerField           # [-32_000 | 32_000]
# PositiveSmallIntegerField   # [0 | 32_000]
#
# FloatField                  # 1.1231231232 | 123123123.123232 | 7.313
# DecimalField                # 13.333 | 11.001 | 1.001



class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    #  auto_now_add И auto_now параметры "под капотом" автоматичеки ставят ещё и параметр editable = False
    created_at = models.DateTimeField(auto_now_add=True)  # Срабатывает ОДИН раз ПРИ СОЗДАНИИ ОБЪЕКТА
    updated_at = models.DateTimeField(auto_now=True)  # Срабатывает ВСЕГДА. И при создании, И ПРИ ОБНОВЛЕНИИ
    reading_time = models.DurationField(
        null=True
    )




# РАБОТА СО СВЯЗЯМИ
# models.OneToOneField  # o2o => один к одному
# models.ManyToManyField  # m2m => многие ко многим
# models.ForeignKey  # o2m => один ко многим