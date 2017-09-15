from django.contrib import admin
from .models import Difficulty, Category, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]


@admin.register(Difficulty, Category)
class QuestionMetaAdmin(admin.ModelAdmin):
    pass
