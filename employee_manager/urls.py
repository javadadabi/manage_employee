from django.urls import path
from .views import employee_list, employee_tasks, task_detail, new_task

app_name = 'employee_manager'

urlpatterns = [
    # path('', employee_list, name='home'),
    path('<int:employee_number>/<slug:employee_slug>/tasks/', employee_tasks, name='employee_tasks'),
    path('<int:task_pk>/<slug:task_slug>/', task_detail, name='task_detail'),
    path('<int:employee_pk>/<slug:employee_slug>/new-task/', new_task, name='new_task'),
]
