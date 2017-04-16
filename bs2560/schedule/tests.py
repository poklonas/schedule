from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from schedule.views import home_page
from schedule.models import User

import re

class ScheduleHomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_have_right_title(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>schedule</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))

    def remove_csrf(self, html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def test_home_page_return_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('schedule/homepage.html')
        self.assertEqual(self.remove_csrf(response.content.decode()), 
                         self.remove_csrf(expected_html))

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['user_name'] = 'user_one'
        response = home_page(request)
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.name, 'user_one')

    def test_home_page_rediracts_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['user_name'] = 'user_one'
        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_save_user_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(User.objects.count(), 0)

    def test_home_page_display_all_user_list(self):
        User.objects.create(name='user_one')
        User.objects.create(name='user_two')
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('user_one', response.content.decode())
        self.assertIn('user_two', response.content.decode())

    def test_home_page_display_all_user_link(self):
        user_one = User.objects.create(name='user_one')
        user_two = User.objects.create(name='user_two')
        request = HttpRequest()
        response = home_page(request)
        all_link = re.findall(r'href=[\'"]?([^\'" >]+)', response.content.decode())
        self.assertIn('/%d'%user_one.pk, all_link)
        self.assertIn('/%d'%user_two.pk, all_link)

class UserModelTest(TestCase):

    def test_saving_and_retrieving_user(self):
        first_user = User(name='first')
        first_user.save()
        second_user = User(name='second')
        second_user.save()
        all_user = User.objects.all()
        self.assertEqual(all_user.count(), 2)
        first_save_user = all_user[0]
        second_save_user = all_user[1]
        self.assertEqual(first_save_user.name, 'first')
        self.assertEqual(second_save_user.name, 'second')
      
