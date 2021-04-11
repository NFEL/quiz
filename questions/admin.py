from django.contrib import admin
from .models import Answer,Questions,Exam
# Register your models here.

admin.site.register(Exam)
admin.site.register(Answer)
admin.site.register(Questions)
