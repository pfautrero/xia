# -*- coding: utf-8 -*-
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


display = Display(visible=0, size=(1024, 768))
display.start()


class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "file://home/gitlab_ci_runner/gitlab-ci-runner/tmp/builds/project-4/images-actives-html5/tests/functional_test/accordion/index.html"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_(self):
        driver = self.driver
        driver.get(self.base_url)
        print("Titre du document")
        #self.assertEqual("Titre du document", driver.find_element_by_id("title").text)
        print("Titre de l'image")
        self.assertEqual("Titre de l'image", driver.find_element_by_id("collapsecomment-heading").text)
        driver.find_element_by_id("collapsecomment-heading").click()
        driver.find_element_by_id("collapse0-heading").click()
        print("TEst alert")
        script = """
		    for (var i in Kinetic.shapes) {
			    if (Kinetic.shapes[i].attrs['name'] == 'Son 1') {
				    Kinetic.shapes[i].fire('click');
			    }
		    }
           """
       # print(script)
       # driver.execute_script("alert('rr');","")
       # driver.switch_to_alert()
       # print("toto")
       # time.sleep(5)
       # driver.execute_script("alert('XX');","")
       # print("totoXX")
       # time.sleep(5)
       # script22="alert('TT');"
       # driver.execute_script("alert('OO');","")
        print("toto")
        driver.execute_script(script)
        time.sleep(5)
        driver.execute_script(script)
        print("toto2")
        time.sleep(5)
        driver.find_element_by_xpath("//div[@id='canvas']/div/canvas[4]").click()
        driver.find_element_by_id("collapse5-heading").click()
        driver.find_element_by_id("collapse6-heading").click()
     #   for i in range(3):
     #       print(i)
     #       try:
     #           if "ee" == self.close_alert_and_get_its_text(): break
     #       except: pass
     #       time.sleep(1)
     #   else: self.fail("time out")
     #   print("okk")    

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        display.stop()

if __name__ == "__main__":
    unittest.main()
