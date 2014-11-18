# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os


display = Display(visible=0, size=(1024, 768))
display.start()



class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "file://"+os.path.dirname(os.path.abspath(__file__))+"/index.html"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_init(self):
        driver = self.driver
        driver.get(self.base_url)
        self.assertEqual("Titre du document", driver.find_element_by_id("title").text)
        self.assertEqual("Titre de l'image", driver.find_element_by_id("collapsecomment-heading").text)
        self.assertEqual("Titre du rectangle ***gras*** **italique**", driver.find_element_by_id("collapse0-heading").text)
        self.assertEqual("Titre de l'ellipse", driver.find_element_by_id("collapse1-heading").text)
        self.assertEqual("Titre de l'étoile {{{Texte brut}}}", driver.find_element_by_id("collapse2-heading").text)
        self.assertEqual("Titre de ligne", driver.find_element_by_id("collapse3-heading").text)
        self.assertEqual("Titre bezier", driver.find_element_by_id("collapse4-heading").text)
        self.assertEqual("son 2", driver.find_element_by_id("collapse5-heading").text)
        self.assertEqual("Son 1", driver.find_element_by_id("collapse6-heading").text)
    def test_nav(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("collapsecomment-heading").click()
        driver.find_element_by_id("collapse0-heading").click()
        script = """
		    for (var i in Kinetic.shapes) {
			    if (Kinetic.shapes[i].attrs['name'] == 'Son 1') {
				    Kinetic.shapes[i].fire('click');
			    }
		    }
           """
        driver.execute_script(script)
 #       time.sleep(5)
        driver.find_element_by_xpath("//div[@id='canvas']/div/canvas[4]").click()
        driver.find_element_by_id("collapse5-heading").click()
        driver.find_element_by_id("collapse6-heading").click() 
        
    def test_click(self):
        driver = self.driver
        driver.get(self.base_url)
        try: self.assertTrue(driver.find_element_by_xpath("//div[@id='collapse4']/div/hr").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Description de beziertracer \n une ligne", driver.find_element_by_xpath("//div[@id='collapse4']/div").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("a.infos").click()
        driver.find_element_by_id("popup_close").click()
        driver.find_element_by_id("collapse0-heading").click()
        driver.find_element_by_id("collapse1-heading").click()
        driver.find_element_by_id("collapse2-heading").click()
        driver.find_element_by_id("collapse4-heading").click()
        driver.find_element_by_id("collapse5-heading").click()
        driver.find_element_by_id("collapse6-heading").click()
        driver.find_element_by_id("collapsecomment-heading").click()
        driver.find_element_by_id("collapsecomment-heading").click()
        driver.find_element_by_id("collapse0-heading").click()
        driver.find_element_by_css_selector("#collapse0 > div.accordion-inner").click()
        self.assertEqual("Description du rectangle gras italiqueRéponse:Voici la vidéo :", driver.find_element_by_css_selector("#collapse0 > div.accordion-inner").text)
        driver.find_element_by_id("collapsecomment-heading").click()
        driver.find_element_by_id("collapse0-heading").click()
        self.assertEqual("Description de l'image", driver.find_element_by_css_selector("div.accordion-inner").text)
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "#collapse0 > div.accordion-inner > video"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual("", driver.find_element_by_css_selector("#collapse0 > div.accordion-inner > video").text)
        self.assertEqual("Description de beziertracer \n une ligne", driver.find_element_by_css_selector("//div[@id='collapse4']/div").text)
        driver.find_element_by_id("collapse4-heading").click()

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
 