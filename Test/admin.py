from django.contrib import admin
from . import models


# Register your models here.


class QuestionWithAnswerInline(admin.TabularInline):
    model = models.QuestionWithAnswer
    extra = 0


class QuestionWithVariantsInline(admin.TabularInline):
    model = models.QuestionWithVariants
    extra = 0


@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionWithAnswerInline, QuestionWithVariantsInline]
    fields = ["test_title", "test_lesson_number", "test_description", "test_timer", "test_author",
              "test_publication_date"]
    list_display = ['test_title']


@admin.register(models.Hint)
class HintsAdmin(admin.ModelAdmin):
    list_display = ['defined_word']


admin.site.register(models.Results)
admin.site.register(models.UsersAnswers)
admin.site.register(models.UserResultTestArchive)
admin.site.register(models.UserFinalResultArchive)
