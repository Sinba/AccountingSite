from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

class Department(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User)
    department = models.ForeignKey(Department)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Task(models.Model):
    task_name = models.CharField(max_length=100, unique=True)
    employee = models.ForeignKey(Employee)
    project = models.ForeignKey(Project)
    description = models.CharField(max_length=500, null=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name

class Report(models.Model):
    task = models.ForeignKey(Task)
    date = models.DateField()
    elapsed_time_in_hour = models.PositiveIntegerField()

    class Meta:
        unique_together = ('task', 'date')
