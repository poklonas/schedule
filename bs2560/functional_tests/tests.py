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

    def check_for_row_in_user_list_table_is_link(self, name):
        table = self.browser.find_element_by_id('user_list')
        rows = table.find_elements_by_link_text(name)
        self.assertNotEqual(rows, []) # if empyty that mean it cant find any link 

    def test_can_make_new_user_and_join_in(self):
        # Mr.fox want to use schedule webapp
        # He open web browser and go to that web
        self.browser.get(self.live_server_url)

        # He saw the title page was "schedule"
        self.assertIn('schedule', self.browser.title)

        # then the words " Hi , Who are you ? " in the center of that web
        center_text = self.browser.find_element_by_tag_name('center')
        head_text =center_text.find_elements_by_tag_name('h1')
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
        # he saw user name " fox ""
        self.check_for_row_in_user_list_table('fox')

        # his friend see that and interesting in this he want user for
        # him self mr.fox fill name "Jay" in input box and make new user again
        input_username = self.browser.find_element_by_id('new_user')
        input_username.send_keys('Jay')
        input_username.send_keys(Keys.ENTER)

        time.sleep(0.5)

        #that page refreash again and show new user in user list
        # that include fox and Jay
        self.check_for_row_in_user_list_table('fox')
        self.check_for_row_in_user_list_table('Jay')

        # he observe the user name that is a link 
        self.check_for_row_in_user_list_table_is_link('fox')
        self.check_for_row_in_user_list_table_is_link('Jay')
        

        # he click his name [that was a link]
        link = self.browser.find_element_by_link_text('fox')
        link.click()

        time.sleep(0.5)

        # then that page change to his user page
        # the title page is "user_page"
        self.assertIn('user_page', self.browser.title)

        # he saw the words " Hi fox " in center of this page
        center_text = self.browser.find_element_by_tag_name('center')
        head_text =center_text.find_elements_by_tag_name('h1')
        self.assertIn('Hi fox', [row.text for row in head_text])

        # he saw the empty table in buttom of this page that show
        table = self.browser.find_element_by_id('table_time')
        rows_day = table.find_elements_by_tag_name('tr')
        first_row = table.find_element_by_id('time')
        colum_time = first_row.find_elements_by_tag_name('th')

        # each row is each day " monday tueday wed .  . .  ."
        self.assertIn('Monday', [row.text for row in rows_day])
        self.assertIn('Tuesday', [row.text for row in rows_day])
        self.assertIn('Wednesday', [row.text for row in rows_day])
        self.assertIn('Thursday', [row.text for row in rows_day])
        self.assertIn('Friday', [row.text for row in rows_day])
        self.assertIn('Saturday', [row.text for row in rows_day])
        self.assertIn('Sunday', [row.text for row in rows_day])

        # and each colum was time start in 0.00 - 23.00 each colum has 1 hr
        for count in range(0, 24):
            if(count < 10):
                count = '0' + str(count)
            self.assertIn(str(count), [colum.text for colum in colum_time])

        # he saw a inputbox for fill a detail of time and start and end of time and day
        

        # he select time 1.00 and 3.00 and fill detail is "Coding",and row of monday
        # then he click button to commit
        # that page refresh to same page
        # he saw Coding in row monday colum 1.00 and 3.00 
        # he close webbrowser
        self.fail("Yeah this complete")


