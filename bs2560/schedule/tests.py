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