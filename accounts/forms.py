from django import forms
import models
from django.forms.extras import widgets
from django.contrib.auth.models import User


class SelectEmployeeAndDateForm(forms.Form):
    employee = forms.ModelChoiceField(models.Employee.objects.all()) 
    start_date = forms.DateField(widget=widgets.SelectDateWidget())
    end_date = forms.DateField(widget=widgets.SelectDateWidget())

class EmployeeProfileForm(forms.ModelForm):
   class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'email']

   def __init__(self, *args, **kwargs):
        dep_name = None
        try:
            dep_name = kwargs['dep_name']
            del  kwargs['dep_name']
        except:
            pass

        super(EmployeeProfileForm, self).__init__(*args, **kwargs)
        if dep_name:
            self.fields['department'] = forms.CharField(initial=dep_name)
            self.fields['department'].widget.attrs['readonly'] = True

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

    class Meta:
        model = models.Employee

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task

class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        employee = None
        try:
            employee = kwargs['employee']
            del kwargs['employee']
        except:
            pass
        super(ReportForm, self).__init__(*args, **kwargs)
        if employee:
            self.fields['task'].queryset = models.Task.objects.filter(employee__exact=employee)

    class Meta:
        model = models.Report

        widgets = {
                    'date': widgets.SelectDateWidget(),
                  }

class ProjectForm(forms.ModelForm):
    class Meta:
           model = models.Project
           fields = ['name', 'description', 'start_date',
                     'end_date', 'resolved']
           widgets = {
                       'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
                       'start_date': widgets.SelectDateWidget(),
                       'end_date': widgets.SelectDateWidget(),
                     }

    
class DepartmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self_exclude = False
        try:
            self_exclude = kwargs['self_exclude']
            del  kwargs['self_exclude']
        except:
            pass

        super(DepartmentForm, self).__init__(*args, **kwargs)
        if self_exclude:
            self.fields['parent'].queryset = models.Department.objects.exclude(name=self.instance)

    class Meta:
        model = models.Department
        field = ['name', 'parent', 'description']
        widgets = {
                    'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
                  }
