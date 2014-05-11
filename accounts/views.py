from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.views import generic
import forms
import models

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

def index(request):
    return render(request, 'accounts/index.html') 

@login_required
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    try:
        employee = models.Employee.objects.get(user=user)
        dep = models.Department.objects.get(pk = employee.department_id)
        dep_name = dep.name
    except:
        dep_name=None 
    if request.method == 'GET':
        form = forms.EmployeeProfileForm(instance=user, dep_name=dep_name)
        return render(request, 'accounts/profile.html', {
            "form": form,
        })
    elif request.method == 'POST':
        form = forms.EmployeeProfileForm(request.POST, instance=user)
        form.save()
        return redirect('index')

### Depatment
@login_required
@group_required('manager')
def department_add(request):
    form = forms.DepartmentForm(instance=models.Department())
    if request.method == 'POST':
        form = forms.DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departments_list')
    return render(request, 'accounts/add_department.html', {
                  'form': form
                  })


@login_required
@group_required('manager')
def department_detail(request, dep_id):
    department = get_object_or_404(models.Department, pk=dep_id)
    form = forms.DepartmentForm(instance=department, self_exclude=True)
    if request.method == 'POST':
        form = forms.DepartmentForm(request.POST, instance=department, self_exclude=True)
        if form.is_valid():
            form.save()
            return redirect('departments_list')
    return render(request, 'accounts/detail_department.html', {
                           "form":form,
                           "dep_id": dep_id,
                           })

@login_required
@group_required('manager')
def department_delete(request, dep_id):
    department = get_object_or_404(models.Department, pk=dep_id)
    department.delete()
    return redirect('departments_list')

@login_required
def departments_list(request):
    return render(request, 'accounts/departments.html', {
                           'nodes': models.Department.objects.all(),
                           'employees': models.Employee.objects.all()
                           })


### Employee
@login_required
def employees_list(request):
    employees = models.Employee.objects.all()
    return render(request, 'accounts/employee_list.html',{
                  'employees': employees
                  })

@login_required
@group_required('manager')
def employee_add(request):
    form = forms.UserForm()
    EmployeeFormSet = inlineformset_factory(User,
                                            models.Employee,
                                            form=forms.EmployeeForm,
                                            can_delete=False)
    formset = EmployeeFormSet(instance=User())
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            formset = EmployeeFormSet(request.POST, instance=user)
            if formset.is_valid():
                form.save()
                formset.save()
                return redirect('employees_list')

    return render(request, 'accounts/employee_add.html', {
                  "form": form,
                  "formset": formset,
                  })

@login_required
@group_required('manager')
def employee_detail(request, usr_id=None):
    EmployeeFormSet = inlineformset_factory(User, models.Employee, form=forms.EmployeeForm, can_delete=False)
    user = get_object_or_404(User, pk=usr_id)
    if request.method == 'GET':
        form = forms.UserForm(instance=user)
        formset = EmployeeFormSet(instance=user)
        return render(request, 'accounts/employee_detail.html', {
                      "form": form,
                      "formset": formset,
                      "usr_id": user.id,
                      })
    elif request.method == 'POST':
        form = forms.UserForm(request.POST, instance=user)
        formset = EmployeeFormSet(request.POST, instance=user)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
        return redirect('employees_list')

@login_required
@group_required('manager')
def employee_delete(request, usr_id):
    user = get_object_or_404(User, pk=usr_id)
    user.delete()
    try:
        employee = models.Employee.objects.get(user=user)
        employee.delete()
    except:
        pass
    return redirect('employees_list')


### Task 
@login_required
def task_list(request):
    tasks = models.Task.objects.all()
    return render(request, 'accounts/task_list.html', {
                  "tasks": tasks,
                  })

@login_required
@group_required('manager')
def task_add(request):
    if request.method == 'POST':
        form = forms.TaskForm(request.POST)
        form.save()
        return redirect('task_list')
    else:
        task = models.Task()
        form = forms.TaskForm(instance=task)
        return render(request, 'accounts/task.html', {
                      "form": form
                      })

@login_required
@group_required('manager')
def task_detail(request, task_id):
    task = get_object_or_404(models.Task, pk=task_id)
    if request.method == 'POST':
        form = forms.TaskForm(request.POST, instance=task)
        form.save()
        return redirect('task_list')
    else:
        form = forms.TaskForm(instance=task)
        return render(request, 'accounts/task.html', {
                      "form": form,
                      })

###Report
@login_required
@group_required('manager')
def report_add(request):
    user = get_object_or_404(User, pk=request.user.id)
    employee = get_object_or_404(models.Employee, user=user)
    if request.method == 'POST':
        form = forms.ReportForm(request.POST, employee=employee)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = forms.ReportForm(employee=employee)
    return render(request, 'accounts/report.html', {
                  "form": form,
                  })

@login_required
def report_all_for_employee(request):
    user = get_object_or_404(User, pk=request.user.id)
    employee = get_object_or_404(models.Employee, user=user)
    tasks = models.Task.objects.filter(employee__exact=employee)
    reports = models.Report.objects.filter(task__exact=tasks)
    return render(request, 'accounts/report_all_for_user.html', {
                  "reports": reports,
                  })

@login_required
@group_required('manager')
def employee_statistics(request):
    if request.method == 'POST':
        form = forms.SelectEmployeeAndDateForm(request.POST)
        if form.is_valid():
            tasks = models.Task.objects.filter(employee__exact=form.cleaned_data['employee'])
            reports = models.Report.objects.filter(task__exact=tasks,
                                                   date__gt=form.cleaned_data['start_date'],
                                                   date__lt=form.cleaned_data['end_date'])
            return render(request, 'accounts/report_all_for_user.html', {
                          "reports": reports,
                          })
    else:
        form = forms.SelectEmployeeAndDateForm()
    return render(request, 'accounts/employee_statistics.html', {
                  "form": form,
                   })

@login_required
@group_required('manager')
def project_report(request, prj_id):
    project = get_object_or_404(models.Project, pk=prj_id)
    tasks = models.Task.objects.filter(project__exact=project)
    all_report = {}
    summary_time = 0
    for task in tasks:
        reports= models.Report.objects.filter(task__exact=task)
        time_on_task = 0
        for report in reports:
            time_on_task += report.elapsed_time_in_hour
        all_report[task.task_name] = time_on_task
        summary_time += time_on_task
    return render(request, 'accounts/project_report.html', {
                  "task_reports": all_report,
                  "summary_time": summary_time,
                  })

### Project

@login_required
@group_required('manager')
def add_project(request):
    form = forms.ProjectForm()
    if request.method == 'POST':
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects_list')
    return render(request, 'accounts/add_project.html', {
                  "form": form,
                  })

@login_required
@group_required('manager')
def project_delete(request, prj_id):
    project = get_object_or_404(models.Project, pk=prj_id)
    project.delete()
    return redirect('projects_list')

@login_required
@group_required('manager')
def project_detail(request, prj_id):
    project = get_object_or_404(models.Project, pk=prj_id)
    if request.method == 'GET':
        form = forms.ProjectForm(instance=project)
        return render(request, 'accounts/project_detail.html', {
                               "form":form,
                               "prj_id": prj_id,
                               })
    elif request.method == 'POST':
        form = forms.ProjectForm(request.POST, instance=project)
        form.save()
        return redirect('projects_list')
    
class ProjectsView(generic.ListView):
    template_name = 'accounts/projects_list.html'
    context_object_name = 'all_projects'
    model = models.Project
