from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
import models

def create_employee(username, password, department, group=None):
    """
    Create employee with given 'username' and 'department'
    """
    user = User.objects.create_user(username=username, password=password)
    employee = models.Employee.objects.create(user=user, department=department)
    if group:
        group, created = Group.objects.get_or_create(name=group)
        user.groups.add(group)
    return employee


class AccountsTests(TestCase):
    def test_denies_anonymous_profile_view(self):
        response = self.client.get(reverse('profile'), follow=True)
        self.assertRedirects(response, 'login/?next=/profile/')
        response = self.client.post(reverse('profile'), follow=True)
        self.assertRedirects(response, 'login/?next=/profile/')

    def test_loged_in_profile_view(self):
        #create employee
        department = models.Department.objects.create(name='Dev')
        employee = create_employee('user100', '123', department)
        #login
        self.client.login(username='user100', password='123')
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)

        user = response.context['user']
        self.assertEqual(user.username, 'user100')

        form = response.context['form']
        self.assertEqual(form['last_name'].value(), '')
        self.assertEqual(form['last_name'].value(), '')
        self.assertEqual(form['email'].value(), '')
        self.assertEqual(form['department'].value(), 'Dev')

    def test_edit_profile_view(self):
        #create employee
        department = models.Department.objects.create(name='Dev')
        employee = create_employee('user100', '123', department)
        #login
        self.client.login(username='user100', password='123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        #check empty form
        form = response.context['form']
        self.assertEqual(form['first_name'].value(), '')
        self.assertEqual(form['last_name'].value(), '')
        self.assertEqual(form['email'].value(), '')
        self.assertEqual(form['department'].value(), 'Dev')
        #set data in POST
        response = self.client.post(reverse('profile'), {
                                    'first_name': 'John',
                                    B'last_name': 'Smith',
                                    'email': 'aaa@bbb.cc',
                                    'department': 'QA'
                                    })
        self.assertRedirects(response, reverse('index'))
        #check data
        response = self.client.get(reverse('profile'))
        form = response.context['form']
        self.assertEqual(form['first_name'].value(), 'John')
        self.assertEqual(form['last_name'].value(), 'Smith')
        self.assertEqual(form['email'].value(), 'aaa@bbb.cc')
        #department field read only in profile
        self.assertEqual(form['department'].value(), 'Dev')

    def test_denies_anonymous_department_view(self):
        response = self.client.get(reverse('add_dep'), follow=True)
        self.assertRedirects(response, '/login/?next=/departments/add')
        response = self.client.post(reverse('add_dep'), follow=True)
        self.assertRedirects(response, '/login/?next=/departments/add')


    def test_denies_employee_without_needed_group(self):
        #create employee
        department = models.Department.objects.create(name='Dev')
        employee = create_employee('user100', '123', department)
        #login
        self.client.login(username='user100', password='123')
        response = self.client.get(reverse('add_dep'))
        self.assertRedirects(response, '/login/?next=/departments/add')

    def test_department_add_with_correct_data(self):
        #create employee
        department = models.Department.objects.create(name='Dev')
        employee = create_employee('user100', '123', department, group='manager')
        #login
        self.client.login(username='user100', password='123')
        response = self.client.post(reverse('add_dep'), {
                                    'name': 'DevService',
                                    'description': 'new department',
                                    'parent': department.id, 
                                    })
        self.assertRedirects(response, reverse('departments_list'))
        #check data
        new_department = models.Department.objects.get(name='DevService')
        self.assertEqual(new_department.description, 'new department')
        self.assertEqual(new_department.parent.name, department.name)

    def test_department_add_without_name_field(self):
        #create employee
        department = models.Department.objects.create(name='Dev')
        employee = create_employee('user100', '123', department, group='manager')
        #login
        self.client.login(username='user100', password='123')
        response = self.client.post(reverse('add_dep'), {})
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertTemplateUsed(response, 'accounts/add_department.html')
        
    def test_department_edit_withot_name(self):
        #prepare data
        department = models.Department.objects.create(name='Dev')
        employee = create_employee('user100', '123', department, group='manager')
        self.client.login(username='user100', password='123')
        #test incorrect department id 
        response = self.client.get(reverse('detail_dep', kwargs={'dep_id': 9999}))
        self.assertEqual(response.status_code, 404)
        #test correct id
        response = self.client.get(reverse('detail_dep', kwargs={'dep_id': department.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/detail_department.html')
        form = response.context['form']
        self.assertEqual(form['name'].value(), 'Dev')
        self.assertEqual(form['description'].value(), None)
        self.assertEqual(form['parent'].value(), None)
        #without name
        response = self.client.post(reverse('add_dep'), {
                                    'name': ''
                                    })
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_department_edit_with_correct_data(self):
        #prepare data
        department = models.Department.objects.create(name='Dev')
        employee = create_employee('user100', '123', department, group='manager')
        self.client.login(username='user100', password='123')

        new_department = models.Department.objects.create(name='DevService')
        response = self.client.post(reverse('detail_dep',
                                    kwargs={'dep_id': new_department.id}), {
                                    'name': 'ServiceDep',
                                    'description': 'service department',
                                    'parent': department.id,
                                    })
        self.assertRedirects(response, reverse('departments_list'))
        response = self.client.get(reverse('detail_dep', kwargs={'dep_id': new_department.id}))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form['name'].value(), 'ServiceDep')
        self.assertEqual(form['description'].value(), 'service department')
        self.assertEqual(form['parent'].value(), department.id)
        self.assertTemplateUsed(response, 'accounts/detail_department.html')

    def test_department_delete_without_login(self):
        response = self.client.get(reverse('delete_dep', kwargs={'dep_id': 1}),
                                   follow=True)
        self.assertRedirects(response, '/login/?next=/departments/delete/1/')
        response = self.client.post(reverse('delete_dep', kwargs={'dep_id': 1}),
                                   follow=True)
        self.assertRedirects(response, '/login/?next=/departments/delete/1/')

    def test_department_delete_without_group(self):
        department = models.Department.objects.create(name='Dev')
        employee = create_employee('user100', '123', department)
        self.client.login(username='user100', password='123')
        response = self.client.get(reverse('delete_dep', kwargs={'dep_id': department.id}),
                                   follow=True)
        self.assertRedirects(response,
                             '/login/?next=/departments/delete/{0}/'.format(department.id))
        response = self.client.post(reverse('delete_dep', kwargs={'dep_id': department.id}),
                                    follow=True)
        self.assertRedirects(response,
                             '/login/?next=/departments/delete/{0}/'.format(department.id))

    def test_department_delete(self):
        department = models.Department.objects.create(name='Dev')
        employee = create_employee('user100', '123', department, group='manager')
        self.client.login(username='user100', password='123')
        response = self.client.post(reverse('delete_dep', kwargs={'dep_id': department.id}),
                                    follow=True)
        departments = models.Department.objects.all()
        self.assertEqual(len(departments), 0)
        response = self.client.get(reverse('detail_dep', kwargs={'dep_id': department.id}))
        self.assertEqual(response.status_code, 404)

    def test_department_delete_not_existed(self):
        department = models.Department.objects.create(name='Dev')
        employee = create_employee('user100', '123', department, group='manager')
        self.client.login(username='user100', password='123')
        response = self.client.post(reverse('delete_dep', kwargs={'dep_id': 99999}),
                                    follow=True)
        self.assertEqual(response.status_code, 404)
