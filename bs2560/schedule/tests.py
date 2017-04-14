from django.core.urlresolvers import resolve
from django.test import TestCase
from schedule.views import home_page

class ScheduleHomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

