from django.contrib import admin

from . import models


@admin.register(models.Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'create_time')
    raw_id_fields = ('user',)
    search_fields = ("title",)


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('create_time', '__str__')
    raw_id_fields = ('user', 'paper')
    search_fields = ("paper__title",)
    # readonly_fields = ('party',)


@admin.register(models.Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('paper',)
    raw_id_fields = ('paper',)


@admin.register(models.Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('paper', 'user', 'create_time')
    list_select_related = ['paper', 'user']
    raw_id_fields = ('user', 'paper')
    search_fields = ("paper__title", "user__first_name")
    # readonly_fields = ('party',)


@admin.register(models.Fault)
class FaultAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'paper', 'question_id', 'user', 'times', 'corrected')
    list_filter = ('corrected',)
    date_hierarchy = 'update_time'
    raw_id_fields = ('paper', 'user')
