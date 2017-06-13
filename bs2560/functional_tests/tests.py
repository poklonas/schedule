from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_user_list_table(self, name):
        table = self.browser.find_element_by_id('user_list')
        rows = table.find_elements_by_tag_name('a')
        self.assertIn(name, [row.text for row in rows])

    def find_text_of_row_and_time_of_day_in_table(self, day, time):
        table = self.browser.find_element_by_id('table_time')
        rows = table.find_elements_by_tag_name('tr')
        for row in rows:
            th_row = row.find_element_by_tag_name('th')
            if (th_row.text == day):
                colums = row.find_elements_by_tag_name('td')
                count = 0;
                for colum in colums:
                    if count < time:
                        count = count + 1
                    else:
                        return colum.text


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

        # then the words "LOGIN" in the center of that web and REGISTER below
        center_text = self.browser.find_element_by_tag_name('center')
        head_text =center_text.find_elements_by_tag_name('h1')
        self.assertIn("LOGIN", [row.text for row in head_text])
        self.assertIn("Register", [row.text for row in head_text])

        # he saw the input box in buttom of that page
        # he fill his name ,password and email and enter button to make new user
        input_username = self.browser.find_element_by_id('new_user')
        self.assertEqual(
                input_username.get_attribute('placeholder'),
                'user name'
        )
        input_username.send_keys('fox')

        #fill password
        input_password = self.browser.find_element_by_id('new_pass')
        self.assertEqual(
                input_password.get_attribute('placeholder'),
                'user password'
        )
        input_password.send_keys('123456')

		#fill email
        input_email = self.browser.find_element_by_id('new_email')
        self.assertEqual(
                input_email.get_attribute('placeholder'),
                'user email'
        )
        input_email.send_keys('fox@hotmail.com')

        input_email.send_keys(Keys.ENTER)
        time.sleep(0.5)  # wait for data     

		# then that page refreash to homepage 
        # he want to login , he fill email and password and enter

        input_password = self.browser.find_element_by_id('login_pass')
        self.assertEqual(
                input_password.get_attribute('placeholder'),
                'user password'
        )
        input_password.send_keys('123456')

		#fill email
        input_email = self.browser.find_element_by_id('login_email')
        self.assertEqual(
                input_email.get_attribute('placeholder'),
                'user email'
        )
        input_email.send_keys('fox@hotmail.com')

        input_email.send_keys(Keys.ENTER)
        time.sleep(0.5)  #wait for data

        # then that page change to his user page
        # the title page is "user_page"
        self.assertIn('user_page', self.browser.title)

        # he saw the words " Hi fox " in center of this page
        center_text = self.browser.find_element_by_tag_name('center')
        head_text =center_text.find_elements_by_tag_name('h1')
        self.assertIn('Hi fox', [row.text for row in head_text])

        # he saw the empty table in buttom of this page that show
        table = self.browser.find_element_by_id('table_time')
        rows_day = table.find_elements_by_tag_name('th')
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

        # and each colum was time start in 00.00 - 23.00 each colum has 1 hr
        for count in range(0, 24):
            if(count < 10):
                count = '0' + str(count)
            self.assertIn(str(count), [colum.text for colum in colum_time])

        # he saw a inputbox for fill a detail of time and start and how_many_hour and day
        detail_inputbox = self.browser.find_element_by_id('detail')
        day_inputbox = self.browser.find_element_by_id('day_selecter')
        start_time_selec = self.browser.find_element_by_id('start_time')
        how_many_hour = self.browser.find_element_by_id('how_many_hour')

        # he select time 1.00 and 3.00 hr and fill detail is "Coding",and row of monday
        detail_inputbox.send_keys('Coding')
        day_inputbox.send_keys('Monday')
        start_time_selec.send_keys(1)
        how_many_hour.send_keys(3)
        # then he click button to commit
        how_many_hour.send_keys(Keys.ENTER)

        time.sleep(0.5)
        # that page refresh to same page
        # the title page is "user_page"
        self.assertIn('user_page', self.browser.title)

        time.sleep(0.5)
        # he saw Coding in row monday colum 1.00 to 3.00 
        self.assertIn('Coding', self.find_text_of_row_and_time_of_day_in_table('Monday', 1))
        # oh that was wrong time ! he want to change it  he fill imformation agian but time change to 2 to 4
        detail_inputbox = self.browser.find_element_by_id('detail')
        day_inputbox = self.browser.find_element_by_id('day_selecter')
        start_time_selec = self.browser.find_element_by_id('start_time')
        how_many_hour = self.browser.find_element_by_id('how_many_hour')
        detail_inputbox.send_keys('Coding')
        day_inputbox.send_keys('Monday')
        start_time_selec.send_keys(2)
        how_many_hour.send_keys(3)
        how_many_hour.send_keys(Keys.ENTER)
        time.sleep(0.5)

        # browser go to confirm page that show list of collide activity he click yes button to confirm it
        self.assertIn('confirm_add', self.browser.title)
        button_confirm = self.browser.find_element_by_id('yes_input')
        button_confirm.send_keys(Keys.ENTER)
        time.sleep(0.5)
        
        # now he saw Coding in row monday colum 2 to 4 and cant see in 1
        self.assertIn('Coding', self.find_text_of_row_and_time_of_day_in_table('Monday', 2))
        self.assertNotIn('Coding', self.find_text_of_row_and_time_of_day_in_table('Monday', 1))

        # and then he was make misstake by set a time after 23 it 24 it over flow !?
        detail_inputbox = self.browser.find_element_by_id('detail')
        day_inputbox = self.browser.find_element_by_id('day_selecter')
        start_time_selec = self.browser.find_element_by_id('start_time')
        how_many_hour = self.browser.find_element_by_id('how_many_hour')
        detail_inputbox.send_keys('Coding')
        day_inputbox.send_keys('Monday')
        start_time_selec.send_keys(23)
        how_many_hour.send_keys(3)
        how_many_hour.send_keys(Keys.ENTER)
        time.sleep(0.5)
        #but it ok he show it nothing change , but have a word "Error! : Your select time after 23.00 It cant , please Try another time" in center 
        center_text = self.browser.find_element_by_tag_name('center')
        head_text =center_text.find_elements_by_tag_name('strong')
        self.assertIn("Error! : Your select time after 23.00 It cant , please Try another time", [row.text for row in head_text])

        # he dont care it and ,he saw a link LOGOUT in top left
        link_back = self.browser.find_element_by_link_text('LOGOUT')

        # he click to return a homepage
        link_back.click()
        time.sleep(0.5)

        # He saw the title page was "schedule"
        self.assertIn('schedule', self.browser.title)
        
        # he close webbrowser
        self.fail("Yeah this complete")


