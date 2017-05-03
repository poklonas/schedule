from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from schedule.views import *
from schedule.models import *

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

class ScheduleUserPageTest(TestCase):

    def test_root_url_resolves_to_user_page_view(self):
        found = resolve('/0')
        self.assertEqual(found.func, user_page)

    def remove_csrf(self, html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def test_user_page_have_right_title(self):
        user = User(name='user_one')
        user.save()
        request = HttpRequest()
        response = user_page(request, user_id=user.pk)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>user_page</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))

    def test_user_page_return_correct_html(self):
        user = User(name='')
        user.save()
        request = HttpRequest()
        response = user_page(request, user_id=user.pk)
        expected_html = render_to_string('schedule/userpage.html')
        self.assertEqual(self.remove_csrf(response.content.decode()), 
                         self.remove_csrf(expected_html))

    def test_user_page_has_table_element_id_table_time(self):
        expected_html = render_to_string('schedule/userpage.html')
        self.assertIn("<table id='table_time'>", self.remove_csrf(expected_html))

    def test_user_page_has_element_id_time(self):
        user = User(name='')
        user.save()
        request = HttpRequest()
        response = user_page(request, user_id=user.pk)
        expected_html = render_to_string('schedule/userpage.html')
        self.assertIn("<tr id ='time'>", self.remove_csrf(expected_html))

    def test_user_page_has_colum_for_show_all_time(self):
        expected_html = render_to_string('schedule/userpage.html')
        for count in range(0, 24):
            if(count < 10):
                count = '0' + str(count)
            self.assertIn(str(count), self.remove_csrf(expected_html))

    def test_user_page_has_rows_for_show_any_day(self):
        expected_html = render_to_string('schedule/userpage.html')
        list_of_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in list_of_day:
            self.assertIn(day, self.remove_csrf(expected_html))

    def set_activity_each_day_for_new_user(self, user_id):
    	self.make_activity_each_time_for_a_day( "Monday" ,user_id)
    	self.make_activity_each_time_for_a_day( "Tuesday" ,user_id)
    	self.make_activity_each_time_for_a_day( "Wednesday" ,user_id)
    	self.make_activity_each_time_for_a_day( "Thursday" ,user_id)
    	self.make_activity_each_time_for_a_day( "Friday" ,user_id)
    	self.make_activity_each_time_for_a_day( "Saturday" ,user_id)
    	self.make_activity_each_time_for_a_day( "Sunday" ,user_id)

    def make_activity_each_time_for_a_day(self, day_in, user_id):
    	user = User.objects.get(pk=user_id)
    	for count in range(0, 24):
    		Activity.objects.create(user=user, detail="", time=count, day=day_in).save()


    def test_user_page_can_save_a_POST_request(self):
        user = User(name='user_one')
        user.save()
        self.set_activity_each_day_for_new_user(user.pk)
        request = HttpRequest()
        request.method = 'POST'
        request.POST['detail'] = 'user_one'
        request.POST['start_time'] = 2
        how_many_hour = 5
        request.POST['how_many_hour'] = how_many_hour
        request.POST['day_selecter'] = 'Monday'
        reponse = add_new_activity(request, user_id=user.pk)
        for count_time in range(2, 7):
            self.assertEqual(Activity.objects.get(user=user, day='Monday', 
            	                                  time=count_time).detail,
            	                                  'user_one')

    def test_user_page_rediracts_after_POST(self):
        user = User(name='user_one')
        user.save()
        self.set_activity_each_day_for_new_user(user.pk)
        request = HttpRequest()
        request.method = 'POST'
        request.POST['detail'] = 'user_one'
        request.POST['start_time'] = 2
        how_many_hour = 5
        request.POST['how_many_hour'] = how_many_hour
        request.POST['day_selecter'] = 'Monday'
        response = add_new_activity(request, user_id=user.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/'+str(user.pk))

    def test_user_page_only_save_activity_when_necessary(self):
        user = User(name='user_one')
        user.save()
        self.set_activity_each_day_for_new_user(user.pk)
        request = HttpRequest()
        user_page(request, user_id=user.pk)
        self.assertEqual(Activity.objects.count(), 168)

    def test_user_page_remove_same_time_activity_when_it_same_time(self):
        user = User(name='user_one')
        user.save()
        self.set_activity_each_day_for_new_user(user.pk)
        exten_activity = Activity.objects.get(time=1, 
                                              day='Monday')
        exten_activity.setDetail('new')
        exten_activity.set_time_left(5)
        exten_activity.set_connected(False)
        exten_activity.save()
        for count in range(1, 5):
            time_left = 5 - count 
            time = count + 1
            exten_activity = Activity.objects.get(time=time, 
                                                  day='Monday')
            exten_activity.setDetail('new')
            exten_activity.set_time_left(time_left)
            exten_activity.set_connected(True)
            exten_activity.save()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['detail'] = 'user_one'
        request.POST['start_time'] = 2
        how_many_hour = 5
        request.POST['how_many_hour'] = how_many_hour
        request.POST['day_selecter'] = 'Monday'
        response = add_new_activity(request, user_id=user.pk)
        extend_colum = Activity.objects.get(user=user, day='Monday', time=1)
        self.assertEqual('', extend_colum.detail)



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
      
class ActivityModelTest(TestCase):
    
    def test_saving_and_retrieving_activity(self):
        user = User(name='user')
        user.save()
        activity_one = Activity(user=user, detail='first_activity', time=1, day='Monday')
        activity_one.save()
        activity_two = Activity(user=user, detail='second_activity', time=1, day='Friday')
        activity_two.save()
        all_activity = Activity.objects.all()
        self.assertEqual(all_activity.count(), 2)
        first_activity = all_activity[0]
        second_activity = all_activity[1]
        self.assertEqual(first_activity.detail, 'first_activity')
        self.assertEqual(second_activity.detail, 'second_activity')