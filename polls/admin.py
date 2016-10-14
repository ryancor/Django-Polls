from django.contrib import admin

from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date of Question', {'fields': ['pub_date']}),
    ]
admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['choice_text']}),
        ('Votes', {'fields': ['votes']}),
    ]
admin.site.register(Choice, ChoiceAdmin)
