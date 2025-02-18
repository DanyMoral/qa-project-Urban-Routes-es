import data
import helpers
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

class ComfortPage:
    request_a_taxi_button = (By.CSS_SELECTOR, ".button.round")
    comfort_tariff = (By.XPATH, "//div[@class='tcard-icon']/img[@src='/static/media/kids.075fd8d4.svg']")

    def __init__(self, driver):
        self.driver = driver

    def request_button(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.request_a_taxi_button))
        self.driver.find_element(*self.request_a_taxi_button).click()

    def click_comfort_button(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.comfort_tariff))
        self.driver.find_element(*self.comfort_tariff).click()

    def select_comfort_tariff(self):
        self.request_button()
        self.click_comfort_button()

class PhoneFilling:
    phone_field = (By.CLASS_NAME, 'np-button')
    fill_phone_number = (By.ID, "phone")
    next_phone_button = (By.XPATH, "//div[@class='buttons']/button[text()='Siguiente']")
    sms_field = (By.XPATH, "/html/body/div/div/div[1]/div[2]/div[2]/form/div[1]/div[1]/input")
    confirm_button = (By.XPATH, "//div[@class='buttons']/button[text()='Confirmar']")

    def __init__(self, driver):
        self.driver = driver

    def click_phone_field(self):
        self.driver.find_element(*self.phone_field).click()

    def set_phone(self):
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located(self.fill_phone_number))
        self.driver.find_element(*self.fill_phone_number).send_keys(data.phone_number)

    def get_phone(self):
        return self.driver.find_element(*self.fill_phone_number).get_property('value')

    def click_next_phone_button(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.next_phone_button))
        self.driver.find_element(*self.next_phone_button).click()

    def get_sms(self):
        return WebDriverWait(self.driver,5).until((expected_conditions.element_to_be_clickable(self.sms_field)))

    def set_phone_sms(self):
        code = helpers.retrieve_phone_code(self.driver)
        self.get_sms().send_keys(code)

    def click_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    def set_phone_number(self):
        self.click_phone_field()
        self.set_phone()
        self.click_next_phone_button()
        self.set_phone_sms()
        self.click_confirm_button()

class PaymentFilling:
    payment_field = (By.CLASS_NAME, 'pp-text')
    add_card_checkbox = (By.CLASS_NAME, 'pp-plus-container')
    card_number_field = (By.XPATH,"//*[@id='number']")
    card_code_field = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/div[2]/div[2]/input")
    card_row = (By.CLASS_NAME, 'plc')
    add_button = (By.XPATH, "//div[@class='pp-buttons']/button[text()='Agregar']")
    close_payment_window = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/button")

    def __init__(self, driver):
        self.driver = driver

    def click_payment_field(self):
        self.driver.find_element(*self.payment_field).click()

    def click_add_card_checkbox(self):
        self.driver.find_element(*self.add_card_checkbox).click()

    def set_card_number(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.card_number_field))
        self.driver.find_element(*self.card_number_field).send_keys(data.card_number)

    def get_card_number(self):
        return WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located(self.card_number_field))

    def click_card_code_field(self):
        self.driver.find_element(*self.card_code_field).click()

    def set_card_code(self):
        self.driver.find_element(*self.card_code_field).send_keys(data.card_code)
        time.sleep(3)

    def get_card_code(self):
        return WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located(self.card_code_field))

    def tab_key(self):
        self.driver.find_element(*self.card_code_field).send_keys(Keys.TAB)

    def click_add_button(self):
        self.driver.find_element(*self.add_button).click()

    def close_payment_method_window(self):
        self.driver.find_element(*self.close_payment_window).click()

    def set_payment_method(self):
        self.click_payment_field()
        self.click_add_card_checkbox()
        self.set_card_number()
        self.set_card_code()
        self.tab_key()
        self.click_add_button()
        self.close_payment_method_window()

class DriverMessage:
    driver_message = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[3]/div/label")
    input_message = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[3]/div/input")

    def __init__(self, driver):
        self.driver = driver

    def scroll_down(self):
        element = self.driver.find_element(*self.driver_message)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click_comment_section(self):
        self.driver.find_element(*self.driver_message).click()

    def add_comment(self):
        self.driver.find_element(*self.input_message).send_keys(data.message_for_driver)
        time.sleep(3)

    def get_comment(self):
        return self.driver.find_element(*self.input_message).get_property('value')

    def set_driver_message(self):
        self.scroll_down()
        self.click_comment_section()
        self.add_comment()

class BlanketSelection:
    blanket_scarves_section = (By.CLASS_NAME, "r r-type-switch")
    blanket_switch = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span")

    def __init__(self, driver):
        self.driver = driver

    def scroll_down(self):
        element = self.driver.find_element(*self.blanket_scarves_section)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def select_blankets(self):
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located(self.blanket_switch))
        self.driver.find_element(*self.blanket_switch).click()
        time.sleep(3)

class IceCreamSelection:
    qty_ice_cream = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]")
    counter_value = (By.XPATH,"/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]")

    def __init__(self, driver):
        self.driver = driver

    def select_ice_cream(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.qty_ice_cream))
        element = self.driver.find_element(*self.qty_ice_cream)
        element.click()
        element.click()
        time.sleep(3)

    def get_ice_value(self):
        return self.driver.find_element(*self.counter_value).text

    def add_ice_cream(self):
        self.select_ice_cream()

class TaxiReserve:
    taxi_seek_button = (By.CLASS_NAME,'smart-button-wrapper')

    def __init__(self, driver):
        self.driver = driver

    def taxi_seek(self):
        self.driver.find_element(*self.taxi_seek_button).click()