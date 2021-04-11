from django.urls import path
from .views import log, add_question, start_exam, answer_exam
urlpatterns = [
    path("log/", log, name='log'),
    path("add/", add_question, name='add'),
    path("start_exam/", start_exam, name='start'),
    path("answer_exam/", answer_exam, name='answer')
]
