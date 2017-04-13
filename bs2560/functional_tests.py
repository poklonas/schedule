from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_visit_to_right_webap(self):
        # Mr.fox want to use schedule webapp
        # He open web browser and go to that web
        # He saw the title page was "...."
        # then the words " Hi Who are you " in the center of that web
        # and that show list of user he want to make news user for him
        # he saw the input box in buttom of that page 
        # he fill his name and enter button to make new user
        # that page refresh and show new user in user list
        # he saw user name " fox "
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




if __name__ == '__main__':  #7
    unittest.main(warnings='ignore')  #8
