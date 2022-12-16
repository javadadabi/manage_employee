from django.contrib import admin
from .models import Employee, Work, Task, Responsibility


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_number', 'slug', 'first_name', 'last_name', 'gender',
                    'hire_date', 'salary']
    prepopulated_fields = {'slug': ('first_name', 'last_name',)}
    raw_id_fields = ['user', ]
    list_editable = ['salary']


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['work_title', 'slug', 'description', 'begin_time', 'expected_duration', 'end_time', 'created', 'updated',
                    'done']
    prepopulated_fields = {'slug': ('work_title',)}
    list_editable = ['done']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'slug', 'belong_to_work', 'description', 'start_time', 'expected_duration', 'end_time',
                    'created', 'updated', 'done']
    list_editable = ['done']
    prepopulated_fields = {'slug': ('task_name',)}


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ['responsibility_name', 'slug', 'rank', 'description', 'minimum_salary', 'maximum_salary']
    prepopulated_fields = {'slug': ('responsibility_name', )}
