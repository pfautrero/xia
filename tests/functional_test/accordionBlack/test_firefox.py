# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os

if os.name != 'nt':
    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(1024, 768))
    display.start()



class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "file://"+os.path.dirname(os.path.abspath(__file__))+"/index.html"
        self.maxDiff=5000
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_init(self):
        driver = self.driver
        driver.get(self.base_url)
        self.assertEqual("Titre du document", driver.find_element_by_id("title").text)
        self.assertTrue(driver.find_element_by_id("title").is_displayed())
        self.assertEqual("Titre de l'image", driver.find_element_by_id("collapsecomment-heading").text)
        self.assertTrue(driver.find_element_by_id("collapsecomment-heading").is_displayed())
        self.assertEqual("Titre du rectangle ***gras*** **italique**", driver.find_element_by_id("collapse0-heading").text)
        self.assertTrue(driver.find_element_by_id("collapse0-heading").is_displayed())
        self.assertEqual("Titre de l'ellipse", driver.find_element_by_id("collapse1-heading").text)
        self.assertTrue(driver.find_element_by_id("collapse1-heading").is_displayed())
        self.assertEqual(u"Titre de l'étoile {{{Texte brut}}}", driver.find_element_by_id("collapse2-heading").text)
        self.assertTrue(driver.find_element_by_id("collapse2-heading").is_displayed())
        self.assertEqual("Titre de ligne", driver.find_element_by_id("collapse3-heading").text)
        self.assertTrue(driver.find_element_by_id("collapse3-heading").is_displayed())
        self.assertEqual("Titre bezier", driver.find_element_by_id("collapse4-heading").text)
        self.assertTrue(driver.find_element_by_id("collapse4-heading").is_displayed())
        self.assertEqual("son 2", driver.find_element_by_id("collapse5-heading").text)
        self.assertTrue(driver.find_element_by_id("collapse5-heading").is_displayed())
        self.assertEqual("Son 1", driver.find_element_by_id("collapse6-heading").text)
        self.assertTrue(driver.find_element_by_id("collapse6-heading").is_displayed())
        self.assertEqual("""Description de l'image<video controls="" preload="none" data-state="none">
	            <source type="video/mp4" src="../media-share/1.mp4">
	            <source type="video/ogg" src="../media-share/1.ogv">
	            <source type="video/webm" src="../media-share/1.webm">
            </video>

        """, driver.find_element_by_xpath("//div[@id='collapsecomment']/div").get_attribute('innerHTML'))
        self.assertTrue(self.is_element_present(By.XPATH, "//div[@id='collapsecomment']/div/video"))

        
        assert """Description du rectangle <b>gras</b> <em>italique</em><div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#" data-password=""" in driver.find_element_by_xpath("//div[@id='collapse0']/div").get_attribute('innerHTML')
        assert """Voici la vidéo :<video controls="" preload="none" data-state="autostart">
	            <source type="video/mp4" src="../media-share/1.mp4">
	            <source type="video/ogg" src="../media-share/1.ogv">
	            <source type="video/webm" src="../media-share/1.webm">
            </video>""" in driver.find_element_by_xpath("//div[@id='collapse0']/div").get_attribute('innerHTML')
        self.assertTrue(self.is_element_present(By.XPATH, "id('collapse0')/div/video"))
        self.assertEqual("""
          <div class="accordion-inner">Description de l'ellipse<ul>
<li>une liste  <a href="http://dane.ac-versailles.fr" target="_blank">Le site de la Dane</a></li><li>de puces</li><ul>
<li>sur 2</li><li>niveaux</li><br>
</ul>
</ul>
Quelle est la bonne réponse ?<img src="../media-share/1.jpg">

          </div>
      """, driver.find_element_by_xpath("//div[@id='collapse1']").get_attribute('innerHTML'))
        self.assertTrue(self.is_element_present(By.XPATH, "id('collapse1')/div/img"))
        self.assertEqual("""
          <div class="accordion-inner">Description de l'étoile<ul>
 <a href="http://dane.ac-versailles.fr" target="_blank">Le site de la Dane</a></ul>
<pre>Texte brut</pre>
<br>
<img src="../media-share/1.gif">

          </div>
      """, driver.find_element_by_xpath("//div[@id='collapse2']").get_attribute('innerHTML'))
        self.assertTrue(self.is_element_present(By.XPATH, "id('collapse2')/div/img"))
        self.assertEqual("""
          <div class="accordion-inner">Description de ligne1<br>
<video controls="" preload="none" data-state="autostart">
	            <source type="video/mp4" src="../media-share/1.mp4">
	            <source type="video/ogg" src="../media-share/1.ogv">
	            <source type="video/webm" src="../media-share/1.webm">
            </video>
<br>

          </div>
      """, driver.find_element_by_xpath("//div[@id='collapse3']").get_attribute('innerHTML'))
        self.assertTrue(self.is_element_present(By.XPATH, "id('collapse3')/div/video"))
        self.assertEqual("""
          <div class="accordion-inner">Description de beziertracer
<hr>
une ligne<br>
<img src="../media-share/1.png">

          </div>
      """, driver.find_element_by_xpath("//div[@id='collapse4']").get_attribute('innerHTML'))
        self.assertTrue(self.is_element_present(By.XPATH, "id('collapse4')/div/img"))
        assert """<div class="accordion-inner">le son 2 ! <audio controls="" data-state="autostart">
	            <source type="audio/ogg" src="../media-share/1.ogg">
	            <source type="audio/mp3" src="../media-share/1.mp3">
            </audio>
<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#" data-target=""" in driver.find_element_by_xpath("//div[@id='collapse5']").get_attribute('innerHTML')
        assert """La réponse 2</ul>
</div>
LA réponse à la question<br>

          </div>
      """ in driver.find_element_by_xpath("//div[@id='collapse5']").get_attribute('innerHTML')
        self.assertTrue(self.is_element_present(By.XPATH, "id('collapse5')/div/audio"))
        self.assertEqual("""
          <div class="accordion-inner">le son 1 !<audio controls="" data-state="none">
	            <source type="audio/ogg" src="../media-share/1.ogg">
	            <source type="audio/mp3" src="../media-share/1.mp3">
            </audio>

          </div>
      """, driver.find_element_by_xpath("//div[@id='collapse6']").get_attribute('innerHTML'))
        self.assertTrue(self.is_element_present(By.XPATH, "id('collapse6')/div/audio"))
        self.check_element()
        driver.find_element_by_css_selector("a.infos").click()
        self.assertEqual("Michaël Nourry", driver.find_element_by_xpath("//article[@id='popup_text']").text)

        self.check_element("id('popup')")
        
        
    def test_nav_1(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("collapsecomment-heading").click()
        self.check_element("collapsecomment")
        driver.find_element_by_id("collapse0-heading").click()
        self.check_element("collapse0")
        driver.execute_script(self.click_zone("Son 1"))
        driver.execute_script(self.click_zone("Son 1"))
        self.check_element("collapse6")
        driver.find_element_by_xpath("//div[@id='canvas']/div/canvas[4]").click()
        self.check_element("collapse6")
        driver.find_element_by_id("collapse5-heading").click()
        self.check_element("collapse5")
        driver.find_element_by_id("collapse6-heading").click()
        self.check_element("collapse6")
        driver.find_element_by_id("collapsecomment-heading").click()
        driver.find_element_by_id("collapse0-heading").click()
        driver.find_element_by_link_text("Super ma question").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("147")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        assert "La réponse !" not in driver.find_element_by_xpath("//div[@id='collapse0']/div").text 
        
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("1a")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        assert "La réponse !" in  driver.find_element_by_xpath("//div[@id='collapse0']/div").text


    def test_nav_2(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_css_selector("a.infos").click()
        self.check_element("popup")
        driver.find_element_by_id("popup_close").click()
        self.check_element()
        driver.execute_script(self.click_zone("son 2"))
        self.check_element("collapse5")
        driver.find_element_by_id("collapse0-heading").click()
        self.check_element("collapse0")
        driver.find_element_by_id("collapse1-heading").click()
        self.check_element("collapse1")
        driver.find_element_by_id("collapse2-heading").click()
        self.check_element("collapse2")
        driver.find_element_by_id("collapse4-heading").click()
        self.check_element("collapse4")
        driver.find_element_by_id("collapse5-heading").click()
        self.check_element("collapse5")
        driver.find_element_by_id("collapse6-heading").click()
        self.check_element("collapse6")
        driver.find_element_by_id("collapsecomment-heading").click()
        self.check_element("collapsecomment")
        driver.find_element_by_id("collapse0-heading").click()
        self.check_element("collapse0")
        self.assertEqual("""Description du rectangle gras italique
Super ma question
Voici la vidéo :""", driver.find_element_by_css_selector("#collapse0 > div.accordion-inner").text)
        driver.find_element_by_id("collapsecomment-heading").click()
        self.check_element("collapsecomment")
        driver.find_element_by_id("collapse0-heading").click()
        self.check_element("collapse0")
        driver.find_element_by_id("collapse4-heading").click()
        self.check_element("collapse4")

    def test_init_1(self):
        driver = self.driver
        self.base_url = "file://"+os.path.dirname(os.path.abspath(__file__))+"/1.html"
        self.test_init()

    def test_nav_1_1(self):
        driver = self.driver
        self.base_url = "file://"+os.path.dirname(os.path.abspath(__file__))+"/1.html"
        self.test_nav_1()

    def test_nav_2_1(self):
        driver = self.driver
        self.base_url = "file://"+os.path.dirname(os.path.abspath(__file__))+"/1.html"
        self.test_nav_2()


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
    def click_zone(self,zone):
        return """
		    for (var i in Kinetic.shapes) {
			    if (Kinetic.shapes[i].attrs['name'] == '"""+zone+"""') {
				    Kinetic.shapes[i].fire('click');
                    break;
			    }
		    }
           """
    def check_element(self,visible="0XXXX0XXXX0"):
        time.sleep(1)
        driver = self.driver
        elements = [
            "id('popup')",
            "id('collapsecomment')/div",
            "//div[@id='collapsecomment']/div/video",
            "id('collapse0')/div",
            "id('collapse0')/div/video",
            "id('collapse1')/div/ul",
            "id('collapse1')/div/img",
            "id('collapse2')/div",
            "id('collapse2')/div/img",
            "id('collapse3')/div",
            "id('collapse3')/div/video",
            "id('collapse4')/div",
            "id('collapse4')/div/img",
            "id('collapse5')/div",
            "id('collapse5')/div/audio",
            "id('collapse6')/div",
            "id('collapse6')/div/audio"
            ]
        for id in elements:
            if id.find(visible)+1:
                self.assertTrue(driver.find_element_by_xpath(id).is_displayed())
            else:
                self.assertFalse(driver.find_element_by_xpath(id).is_displayed())

    def tearDown(self):
        self.driver.quit()
#        self.assertEqual([], self.verificationErrors)
#        display.stop()

if __name__ == "__main__":
    unittest.main()
 
