from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_user_list_table(self, name):
        table = self.browser.find_element_by_id('user_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(name, [row.text for row in rows])

    def test_can_make_new_user_and_join_in(self):
        # Mr.fox want to use schedule webapp
        # He open web browser and go to that web
        self.browser.get(self.live_server_url)

        # He saw the title page was "schedule"
        self.assertIn('schedule', self.browser.title)

        # then the words " Hi , Who are you ? " in the center of that web
        center_text = self.browser.find_elements_by_tag_name('center')
        self.assertIn("Hi , Who are you ?", [row.text for row in center_text])
        head_text = self.browser.find_elements_by_tag_name('h1')
        self.assertIn("Hi , Who are you ?", [row.text for row in head_text])

        # he saw the input box in buttom of that page
        # he fill his name and enter button to make new user
        input_username = self.browser.find_element_by_id('new_user')
        self.assertEqual(
                input_username.get_attribute('placeholder'),
                'user name'
        )
        input_username.send_keys('fox')
        input_username.send_keys(Keys.ENTER)
        
        time.sleep(0.5)# wait for data     

        # that page refresh and show new user in user list
        # he saw user name " fox "
        self.check_for_row_in_user_list_table('fox')

        # he click that link 
        # then that page change to " ..... .. "
        # he saw the words " Hello Fox " in center of this page
        # he saw the empty table in buttom of this page that show
        # each row is each day " monday tueday wed .  . .  ."
        # and each colum was time start in 0.00 - 23.00 each colum has 1 hr
        # in buttom of each row has a button for select 
        # he saw a inputbox for fill a detail of time
        # he select time 1.00 and 3.00 and fill detail is "Coding",and row of monday
        # then he click button to commit
        # that page refresh to same page
        # he saw Coding in row monday colum 1.00 and 3.00 
        # he close webbrowser
        self.fail("Yeah this complete")


