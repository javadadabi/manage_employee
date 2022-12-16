from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from .models import Work, Task, Employee, Responsibility
from django.db import connection, transaction
from .forms import TaskForm
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.utils import timezone
from django.db.models import Sum


# Create your views here.
@login_required
def employee_list(request):
    employees = Employee.objects.filter().order_by('employee_number', 'tasks__belong_to_work').annotate(
        total_task_duration=Sum('tasks__expected_duration', distinct=True))
    return render(request, 'employee_manager/employee_list.html', context={'employees': employees})


@login_required
def employee_tasks(request, employee_number, employee_slug):
    employee = get_object_or_404(Employee, employee_number=employee_number)
    tasks = employee.tasks.order_by('-created')
    return render(request, 'employee_manager/employee_detail.html', context={'employee': employee, 'tasks': tasks})


@login_required
def task_detail(request, task_pk, task_slug):
    task = get_object_or_404(Task, pk=task_pk)
    return render(request, 'employee_manager/task_detail.html', context={'task': task})


@login_required
def new_task(request, employee_pk, employee_slug):
    # Each user must be able to create a task for himself except staff user
    request_employee = Employee.objects.filter(employee_number=employee_pk).first()
    if not request.user.is_staff and request.user.id != request_employee.user_id:
        raise PermissionDenied("Custom message")
        return
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            task_name = form.cleaned_data['task_name']
            slug = slugify(unidecode(task_name))
            belong_to_work = form.cleaned_data['belong_to_work']
            description = form.cleaned_data['description']
            start_time = form.cleaned_data['start_time']
            expected_duration = form.cleaned_data['expected_duration']
            # if expected_duration:
            #     expected_duration = expected_duration.days * 3600000 + expected_duration.seconds * 1000
            end_time = form.cleaned_data['end_time']
            done = form.cleaned_data['done']
            created = timezone.now()
            updated = timezone.now()
            with connection.cursor() as cursor:
                sql = "INSERT INTO employee_manager_task(task_name, slug, belong_to_work_id, employee_id," \
                      " description, start_time, expected_duration, end_time, done, created, updated) VALUES" \
                      " (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = [task_name, slug, belong_to_work.id, employee_pk, description, start_time, expected_duration,
                          end_time, done, created, updated]
                cursor.execute(sql, values)
                connection.commit()
            # redirect to a new URL:
            return redirect('employee_manager:employee_tasks', employee_pk, employee_slug)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TaskForm()
    return render(request, 'employee_manager/new_task.html', {'form': form, 'employee_pk': employee_pk,
                                                              'employee_slug': employee_slug})


# TODO This class is under construction
@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'employee_manager/edit_task.html'
    pk_url_kwarg = 'task_pk'
    context_object_name = 'task'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(employee_id=self.request.user)

    def form_valid(self, form):
        task = form.save(commit=False)
        task.updated = timezone.now()
        task.save()
        return redirect('employee_manager:employee_tasks', employee_number=task.employee.pk,
                        employee_slug=task.employee.slug)
