import data
import pages
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("perfLoggingPrefs",{'enableNetwork':True, 'enablePage': True})
        chrome_options.set_capability("goog:loggingPrefs", {'performance':'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = pages.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_tariff(self):
        self.test_set_route()
        comfort_page = pages.ComfortPage(self.driver)
        comfort_page.select_comfort_tariff()

        requirements_section = self.driver.find_element(By.CLASS_NAME,"form")
        assert requirements_section.is_displayed()

    def test_fill_phone_number(self):
        self.test_select_tariff()
        phone_page = pages.PhoneFilling(self.driver)
        phone_page.set_phone_number()
        assert phone_page.get_phone() == data.phone_number

    def test_add_credit_card(self):
        self.test_fill_phone_number()
        credit_card_page = pages.PaymentFilling(self.driver)
        credit_card_page.set_payment_method()

        requirements_section = self.driver.find_element(By.CLASS_NAME, "form")
        assert requirements_section.is_displayed()

    def test_add_driver_message(self):
        self.test_add_credit_card()
        message_page = pages.DriverMessage(self.driver)
        message_page.set_driver_message()
        assert message_page.get_comment() == data.message_for_driver

    def test_add_blanket(self):
        self.test_add_driver_message()
        switch_button = pages.BlanketSelection(self.driver)
        switch_button.select_blankets()

        requirements_section = self.driver.find_element(By.CLASS_NAME, "form")
        assert requirements_section.is_displayed()

    def test_add_ice_cream(self):
        self.test_add_blanket()
        ice_cream_page = pages.IceCreamSelection(self.driver)
        ice_cream_page.add_ice_cream()
        assert int(ice_cream_page.get_ice_value()) == 2

    def test_taxi_search(self):
        self.test_add_ice_cream()
        taxi_search_page = pages.TaxiReserve(self.driver)
        taxi_search_page.taxi_seek()

        request_button = self.driver.find_element(By.XPATH,"//*[@id='root']/div/div[3]/div[4]")
        assert request_button.is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
