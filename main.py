import data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code
time.sleep(3)

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
    request_a_taxi_button = (By.CLASS_NAME, 'button round')
    comfort_tariff = (By.ID, 'tariff-card-4')

    def __init__(self, driver):
        self.driver = driver

    def request_button(self):
        self.driver.find_element(*self.request_a_taxi_button).click()

    def wait_for_load_tariff_section(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'modal')))

    def click_comfort_button(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def select_comfort_tariff(self):
        self.request_button()
        self.wait_for_load_tariff_section()
        self.click_comfort_button()

class PhoneFilling:
    tariff_cards = (By.CLASS_NAME, 'tariff-cards')
    phone_section = (By.CLASS_NAME, 'np-text')
    fill_phone_number = (By.ID, 'phone')
    next_phone_button = (By.XPATH, ".//form[@class='buttons']/button[text()='Siguiente']")
    confirm_button = (By.XPATH, ".//form[@class='buttons']/button[text()='Confirmar']")

    def __init__(self, driver):
        self.driver = driver

    def wait_for_load_phone_section(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.tariff_cards))

    def click_phone_section(self):
        self.driver.find_element(*self.phone_section).click()

    def set_phone(self):
        self.driver.find_element(*self.fill_phone_number).send_keys(data.phone_number)

    def get_phone(self):
        return self.driver.find_element(*self.fill_phone_number).get_property('value')

    def click_next_phone_button(self):
        self.driver.find_element(*self.next_phone_button).click()

    def retrieve_phone_code(self):
        return retrieve_phone_code(self.driver)

    def set_phone_code(self):
        self.driver.find_element(*self.fill_phone_number).send_keys(self.retrieve_phone_code())

    def click_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    def set_phone_number(self):
        self.click_phone_section()
        self.set_phone()
        self.get_phone()
        self.click_next_phone_button()
        self.set_phone_code()
        self.click_confirm_button()

class PaymentFilling:
    payment_section = (By.CLASS_NAME, 'pp-text')
    add_card_checkbox = (By.CLASS_NAME, 'pp-plus-container')
    card_number_section = (By.ID,'number')
    card_code_section = (By.ID, 'code')
    card_row = (By.CLASS_NAME, 'plc')
    add_button = (By.XPATH, ".//form[@class='pp-buttons']/button[text()='Agregar']")
    checkbox_button = (By.XPATH, ".//form[@class='pp-checkbox']/button[text()='Agregar']")
    close_payment_window = (By.CLASS_NAME, 'checkbox')

    def __init__(self, driver):
        self.driver = driver

    def click_payment_section(self):
        self.driver.find_element(*self.payment_section).click()

    def click_add_card_checkbox(self):
        self.driver.find_element(*self.add_card_checkbox).click()

    def set_card_number(self):
        self.driver.find_element(*self.card_number_section).send_keys(data.card_number)

    def get_card_number(self):
        return self.driver.find_element(*self.card_number_section).get_property('value')

    def set_card_code(self):
        self.driver.find_element(*self.card_code_section).send_keys(data.card_code)

    def get_card_code(self):
        return self.driver.find_element(*self.card_code_section).get_property('value')

    def click_different_area(self):
        self.driver.find_element(*self.card_row).click()

    def click_add_button(self):
        self.driver.find_element(*self.add_button).click()

    def close_payment_method_window(self):
        self.driver.find_element(*self.close_payment_window).click()

    def set_payment_method(self):
        self.click_payment_section()
        self.click_add_card_checkbox()
        self.set_card_number()
        self.get_card_number()
        self.set_card_code()
        self.get_card_code()
        self.click_different_area()
        self.click_add_button()
        self.close_payment_method_window()

class DriverMessage:
    driver_message = (By.ID, 'comment')
    input_message = (By.CLASS_NAME, 'label')

    def __init__(self, driver):
        self.driver = driver

    def click_comment_section(self):
        self.driver.find_element(*self.driver_message).click()

    def add_comment(self):
        self.driver.find_element(*self.input_message).send_keys(data.message_for_driver)

    def set_driver_message(self):
        self.click_comment_section()
        self.add_comment()

class BlanketSelection:
    blanket_scarves_section = (By.XPATH, ".//form[@class='r r-type-switch']/button[text()='Manta y pañuelos']")

    def __init__(self, driver):
        self.driver = driver

    def select_blankets(self):
        self.driver.find_element(*self.blanket_scarves_section).click()

class IceCreamSelection:
    ice_cream = (By.XPATH, ".//form[@class='counter-plus']/button[text()='+']")

    def __init__(self, driver):
        self.driver = driver

    def select_ice_cream(self):
        element = self.driver.find_element(*self.ice_cream)
        element.click()
        element.click()

class TaxiReserve:
    taxi_seek_button = (By.CLASS_NAME,'smart-button-wrapper')

    def __init__(self, driver):
        self.driver = driver

    def taxi_seek(self):
        self.driver.find_element(*self.taxi_seek_button).click()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        service = Service()
        cls.driver = webdriver.Chrome(service=service, options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        time.sleep(5)

    def test_select_tariff(self):
        self.test_set_route()
        time.sleep(5)
        comfort_page = ComfortPage(self.driver)
        comfort_page.select_comfort_tariff()

    def test_fill_phone_number(self):
        self.test_set_route()
        time.sleep(5)
        self.test_select_tariff()
        time.sleep(5)
        phone_page = PhoneFilling(self.driver)
        phone_page.set_phone_number()
        assert phone_page.get_phone() == data.phone_number

    def test_add_credit_card(self):
        self.test_set_route()
        time.sleep(5)
        self.test_select_tariff()
        time.sleep(5)
        self.test_fill_phone_number()
        time.sleep(5)
        credit_card_page = PaymentFilling(self.driver)
        credit_card_page.set_payment_method()
        assert credit_card_page.get_card_number()
        assert credit_card_page.get_card_code()

    def test_add_driver_message(self):
        self.test_set_route()
        time.sleep(5)
        self.test_select_tariff()
        time.sleep(5)
        self.test_fill_phone_number()
        time.sleep(5)
        self.test_add_credit_card()
        time.sleep(5)
        message_page = DriverMessage(self.driver)
        message_page.set_driver_message()
        assert message_page == data.message_for_driver

    def test_add_blanket(self):
        self.test_set_route()
        time.sleep(5)
        self.test_select_tariff()
        time.sleep(5)
        self.test_fill_phone_number()
        time.sleep(5)
        self.test_add_credit_card()
        time.sleep(5)
        self.test_add_driver_message()
        time.sleep(5)
        switch_button = BlanketSelection(self.driver)
        switch_button.select_blankets()

    def test_add_ice_cream(self):
        self.test_set_route()
        time.sleep(5)
        self.test_select_tariff()
        time.sleep(5)
        self.test_fill_phone_number()
        time.sleep(5)
        self.test_add_credit_card()
        time.sleep(5)
        self.test_add_driver_message()
        time.sleep(5)
        self.test_add_blanket()
        time.sleep(5)
        ice_cream_adding = IceCreamSelection(self.driver)
        ice_cream_adding.select_ice_cream()
        assert ice_cream_adding == 2

    def test_taxi_search(self):
        self.test_set_route()
        time.sleep(5)
        self.test_select_tariff()
        time.sleep(5)
        self.test_fill_phone_number()
        time.sleep(5)
        self.test_add_credit_card()
        time.sleep(5)
        self.test_add_driver_message()
        time.sleep(5)
        self.test_add_blanket()
        time.sleep(5)
        self.test_add_ice_cream()
        time.sleep(5)
        taxi_search_page = TaxiReserve(self.driver)
        taxi_search_page.taxi_seek()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
