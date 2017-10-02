from django.contrib import admin
from .models import Difficulty, Category, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'difficulty', 'text', 'answers')
    inlines = [
        AnswerInline,
    ]

    def answers(self, obj):
        return ' and '.join([str(x) for x in obj.answers.all()])


@admin.register(Difficulty, Category)
class QuestionMetaAdmin(admin.ModelAdmin):
    pass
