from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta


# Create your models here.
from unidecode import unidecode


class Work(models.Model):
    work_title = models.CharField(_('Work title'), max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(_('Description'), blank=True, null=True)
    begin = models.DateTimeField(_('Begin'), default=timezone.now, null=False)
    expected_duration = models.DurationField(_('Expected duration'), blank=True, null=True)
    end = models.DateTimeField(_('End'), auto_now=False, blank=True, null=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    done = models.BooleanField(_('Done'), default=False)

    def __str__(self):
        return self.work_title

    def get_absolute_url(self):
        return reverse('', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.work_title))
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-begin']


class Responsibility(models.Model):
    responsibility_name = models.CharField(_('Responsibility'), max_length=150, primary_key=True)
    slug = models.SlugField(max_length=150, unique=True, null=False)
    rank = models.PositiveSmallIntegerField(_('Rank'), unique=True, default=1, blank=True, null=True)
    description = models.TextField(_('Description'), null=False)
    minimum_salary = models.DecimalField(_('Minimum salary'), max_digits=12, decimal_places=2, blank=True, null=True)
    maximum_salary = models.DecimalField(_('Maximum salary'), max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.responsibility_name

    def get_absolute_url(self):
        return reverse('responsibility_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.responsibility_name))
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['rank']


class Employee(models.Model):
    class Gender(models.TextChoices):
        No_answer = 'N', 'No answer'
        Male = 'M', 'Male'
        Female = 'F', 'Female'
        Other = 'O', 'Other'

    user = models.OneToOneField(User, verbose_name=_('User'), on_delete=models.DO_NOTHING, blank=True, null=True)
    employee_number = models.PositiveIntegerField(_('Employee number'), primary_key=True)
    first_name = models.CharField(_('First name'), max_length=50, default='')
    last_name = models.CharField(_('Last name'), max_length=100, default='')
    slug = models.SlugField(max_length=152)
    gender = models.CharField(_('Gender'), max_length=1, choices=Gender.choices, default=Gender.No_answer)
    hire_date = models.DateField(_('Hire date'), blank=True, null=True)
    salary = models.DecimalField(_('Salary'), max_digits=12, decimal_places=2, blank=True, null=True)
    responsibilities = models.ManyToManyField(Responsibility, verbose_name=_('Responsibility'), blank=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'slug': self.slug})

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.first_name+' '+self.last_name))
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['hire_date', 'last_name', 'first_name']
        indexes = [models.Index(fields=['last_name', 'first_name']), ]


class Task(models.Model):
    task_name = models.CharField(_('Task name'), max_length=200)
    slug = models.SlugField(max_length=200)
    belong_to_work = models.ForeignKey(Work, verbose_name=_('Belong to work'), on_delete=models.DO_NOTHING, related_name
    ='tasks')
    employee = models.ForeignKey(Employee, verbose_name=_('Employee'), on_delete=models.DO_NOTHING, related_name='tasks')
    description = models.TextField(_('Description'), blank=True, null=True)
    start_time = models.DateTimeField(_('Start time'), default=timezone.now, null=False)
    expected_duration = models.DurationField(_('Expected time'), blank=True, null=True)
    end_time = models.DateTimeField(_('End time'), auto_now=False, blank=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    done = models.BooleanField(_('Done'), default=False)

    def __str__(self):
        return self.task_name

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.task_name))
        if self.done:
            if not self.expected_duration and self.end_time:
                self.expected_duration = self.end_time-self.start_time
            elif self.expected_duration and not self.end_time:
                self.end_time = self.start_time + self.expected_duration
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-updated']
        indexes = [models.Index(fields=['task_name']), ]
