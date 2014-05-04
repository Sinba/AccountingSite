from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'},name='logout'),
    url(r'^employees/$', views.employees_list, name='employees_list'),
    url(r'^employee/add$', views.employee_add, name='employee_add'),
    url(r'^employee/detail/(?P<usr_id>\d+)/$', views.employee_detail, name='employee_detail'),
    url(r'^employee/delete/(?P<usr_id>\d+)/$', views.employee_delete, name='employee_delete'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^projects/$', views.ProjectsView.as_view(), name='projects_list'),
    url(r'^projects/add$', views.add_project, name='project_add'),
    url(r'^projects/detail/(?P<prj_id>\d+)/$', views.project_detail, name='project_detail'),
    url(r'^projects/delete/(?P<prj_id>\d+)/$', views.project_delete, name='project_delete'),
    url(r'^departments/$', views.departments_list, name='departments_list'),
    url(r'^departments/add$', views.department_add, name='add_dep'),
    url(r'^departments/(?P<dep_id>\d+)/$', views.department_detail, name='detail_dep'),
    url(r'^departments/delete/(?P<dep_id>\d+)/$', views.department_delete, name='delete_dep'),
    url(r'^tasks/$', views.task_list, name='task_list'),
    url(r'^task/add$', views.task_add, name='task_add'),
    url(r'^task/detail/(?P<task_id>\d+)/$', views.task_detail, name='task_detail'),
    url(r'^profile/report/add$', views.report_add, name='report_add'),
    url(r'^profile/report/all$', views.report_all_for_employee, name='report_all_for_employee'),
    url(r'^employee/statistics$', views.employee_statistics, name='employee_statistics'),
    url(r'^projects/report/(?P<prj_id>\d+)/$', views.project_report, name='project_report'),
)
