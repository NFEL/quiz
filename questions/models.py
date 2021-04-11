from django.db import models
from django.db.models.fields import CharField, DateTimeField, FloatField, IntegerField
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey, ManyToManyField

User = get_user_model()


class Questions(models.Model):
    QUESTION_CHOICES = [
        (1, "Choice 1"),
        (2, "Choice 2"),
        (3, "Choice 3"),
        (4, "Choice 4"),
    ]
    title = CharField(max_length=100,unique=True)
    choice1 = CharField(max_length=100,)
    choice2 = CharField(max_length=100,)
    choice3 = CharField(max_length=100, null=True, blank=True)
    choice4 = CharField(max_length=100, null=True, blank=True)
    correct_choice  = IntegerField(choices=QUESTION_CHOICES)
    create_at = DateTimeField("Date", auto_now_add=True)


class Answer(models.Model):
    QUESTION_CHOICES = [
        (1, "Choice 1"),
        (2, "Choice 2"),
        (3, "Choice 3"),
        (4, "Choice 4"),
    ]
    user = ForeignKey(User, on_delete=models.CASCADE)
    question = ForeignKey(Questions, on_delete=models.CASCADE)
    answer  = IntegerField(choices=QUESTION_CHOICES, null=True, blank=True)

class Exam(models.Model):
    user = ForeignKey(User , on_delete=models.CASCADE)
    questions = ManyToManyField(Questions)
    answers = ManyToManyField(Answer)
    result = FloatField(null=True)
    answered_at = DateTimeField(auto_now_add=True)
