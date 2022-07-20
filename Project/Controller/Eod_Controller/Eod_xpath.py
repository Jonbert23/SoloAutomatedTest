from os import stat
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

class Element:
    def __init__(self, name, xpath, type):
        self.element = None
        self.name = name
        self.xpath = xpath
        self.type = type
        self.instantiated = False
        self.waited = False

    def waitForElement(self, driver, wait_time = 10):
        self.waited = True
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, self.xpath))
            )
        except:
            pass
    
    def waitElementVisibility(self, driver):
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.xpath))
            )
        except:
            pass
    
    def waitElementClickable(self, driver):
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.xpath))
            )
        except:
            pass
    
    def getElement(self):
        if self.instantiated and self.element == None:
            return None
        elif self.instantiated and self.element:
            return self.element
        else:
            raise Exception("Element not instantiated.")
        

# InputElement, CollectionElement, and TextElement implements different getValue() and findElement().
# These are mainly used for Breakdown test as some breakdown values(New patients and Missing referral) are in the form of list instead of indicating a total value.
# However, it can be convenient to use these abstractions in order to wait for elements to load, and by simplifying actions like click()

class InputElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "value")

    def findElement(self, driver, wait_time=10):
        self.instantiated = True

        if not self.waited:
            try:
                self.waitForElement(driver, wait_time)
                self.waitElementVisibility(driver) 
            except Exception as e:
                print(e)

        self.element = driver.find_element(by = By.XPATH, value=self.xpath)
    
    def getValue(self):
        if self.element == None: 
            raise Exception("Element not instantiated.")

        return self.element.get_attribute('value')

class TextElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "value")

    def findElement(self, driver, wait_time=10):
        self.instantiated = True

        if not self.waited:
            self.waitForElement(driver, wait_time)

        try:
            self.element = driver.find_element(by = By.XPATH, value=self.xpath)
        except Exception as e:
            print(e)
    
    def getValue(self):
        if self.element == None: 
            raise Exception("Element not instantiated.")

        return self.element.text

class CollectionElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "collection")

    def findElement(self, driver, wait_time=10):
        self.instantiated = True

        if not self.waited:
            self.waitForElement(driver, wait_time)

        self.element = driver.find_elements(by = By.XPATH, value=self.xpath)

    def getValue(self):
        if self.element == None: 
            raise Exception("Element not instantiated.")

        return len(self.element)

class ClickableElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "button")

    def findElement(self, driver, wait_time=10):
        self.instantiated = True

        if not self.waited:
            self.waitForElement(driver, wait_time)
            self.waitElementClickable(driver)

        self.element = driver.find_element(by = By.XPATH, value=self.xpath)

    def click(self, driver):
        if self.element == None: 
            raise Exception("Element not instantiated.")
        webdriver.ActionChains(driver).move_to_element(self.element).click(self.element).perform()

class EodBreakdown:
    modal_collection = '/html/body/div[1]/main/div[3]/div'
    active_modal = '/html/body/div[1]/main/div[3]/div[not(@style="display: none;")]'

    @staticmethod
    def getCloseModal():
        return ClickableElement("Close Modal", f"{EodBreakdown.active_modal}/div/div/div[1]/button")

    @staticmethod
    def getModalCollection():
        return CollectionElement("Modal Collection", EodBreakdown.modal_collection)

    @staticmethod
    def getModalMetrics():
        return {
            'PT Portion Collections % Today Collected': TextElement('PT Portion Collections % Today Collected', f'{EodBreakdown.active_modal}/div/div/div[2]/div[2]/div/table/tr[1]/td[2]/strong/span'),
            'Adjustments': TextElement('Adjustments', f'{EodBreakdown.active_modal}/div/div/div[3]/div[1]/div/table/tfoot/tr/td[6]'),
            'Collection': TextElement('Collection', f'{EodBreakdown.active_modal}/div/div/div[3]/div[1]/div/table/tfoot/tr/td[6]'),
            'Same Day Treatment': TextElement('Same Day Treatment', f'{EodBreakdown.active_modal}/div/div/div[2]/div[2]/div/table/tr[2]/td[5]/strong/span'),
            'No Show': TextElement('No Show', f'{EodBreakdown.active_modal}/div/div/div[2]/div[2]/div/table/tr/td[2]/strong/span'),
            'New Patients': CollectionElement('New Patients', f'{EodBreakdown.active_modal}/div/div/div[2]/table/tbody/tr'),
            'Patients w/ Missing Referral': CollectionElement('Patients w/ Missing Referral', f'{EodBreakdown.active_modal}/div/div/div[2]/div[2]/div/table/tbody/tr'),
            'Hyg Reappointment': TextElement('Hyg Reappointment', f'{EodBreakdown.active_modal}/div/div/div[2]/div[2]/div/table/tr/td[3]/strong/span'),
            'Case acceptance (%)': TextElement('Case acceptance (%)', f'{EodBreakdown.active_modal}/div/div/div[2]/div[1]/div/table/tfoot/tr[1]/td[6]'),
            'Daily Collection': TextElement('Daily Collection', f'{EodBreakdown.active_modal}/div/div/div[2]/div[2]/div/table/tr/td[4]/strong/span')
        }

class EodSetupXpath:
    date_picker = '//*[@class="vue-daterange-picker w-full"]'
    prev_month = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/table/thead/tr/th[1]'
    next_month = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/table/thead/tr/th[3]'
    curr_month_year = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/table/thead/tr/th[2]'
    date_table = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/table/tbody'
    location_picker = '/html/body/div[1]/main/div[1]/div/div/div/div[2]/div/div[2]'
    refresh_btn = '/html/body/div[1]/main/div[1]/div/div/div/div[3]/button'

    @staticmethod
    def getSubmitBtn():
        return ClickableElement('Submit', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[3]/div[2]/div[2]/button[2]')

    @staticmethod
    def getSendEodEmail():
        return InputElement('Email Input', '//h2[contains(text(), "Send EOD Data - Happy Tooth")]/../../form/div[1]/input')

    @staticmethod
    def getSendEmail():
        return ClickableElement('Send Summary', '//h2[contains(text(), "Send EOD Data - Happy Tooth")]/../../form/div[5]/button')
    
    @staticmethod
    def getSent():
        return TextElement("Summary Sent", '//h2[contains(text(), "Send EOD Data - Happy Tooth")]/../../form/div[5]/span')

    @staticmethod
    def getEmailList():
        return CollectionElement("email list", '//h2[contains(text(), "Send EOD Data - Happy Tooth")]/../../form/div[1]/div[2]/span')

class GmailXpath:
    @staticmethod
    def getEmail():
        return InputElement('Email', '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input')

    @staticmethod
    def getPasswd():
        return InputElement('Password', '//*[@type="password"]')

    @staticmethod
    def getSubmitBtn():
        return ClickableElement('Login Button', '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')

    @staticmethod
    def getEmailList():
        return CollectionElement('Emails', '/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[9]/div/div[1]/div[3]/div/table/tbody/tr')

    @staticmethod
    def getFirstEmail():
        # This will be used to get the email from EOD. A problem arises when the email arrives later than the opening of gmail itself.
        return ClickableElement('First Email', '/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div[1]/div[3]/div/table/tbody/tr[1]')

class EmailData:
    metrics_collection_xpath = '/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/div/table[1]/tbody/tr/td/div/table/tbody/tr/td/div[2]/table/tbody/tr/td/div'

    @staticmethod
    def getMetric(index):
        return {
            "name": TextElement("metric name", f"{EmailData.metrics_collection_xpath}[{index}]/table/tbody/tr/td/div/p"),
            "value": TextElement("metric value", f"{EmailData.metrics_collection_xpath}[{index}]/table/tbody/tr/td/div/span")
        }
    
    @staticmethod
    def getMetricsCollection():
        return CollectionElement("Metrics", '/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/div/table[1]/tbody/tr/td/div/table/tbody/tr/td/div[2]/table/tbody/tr/td/div')

class EodData:
    metrics_collection_xpath = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div'
    bdmetric_collection_xpath = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[./div[1]//a]'

    @staticmethod
    def getMetric(index):
        return {
            "name": TextElement("metric name", f"{EodData.metrics_collection_xpath}[{index}]/div[1]//label"),
            "value": InputElement("metric value", f"{EodData.metrics_collection_xpath}[{index}]/div[2]/input")
        }
    
    @staticmethod
    def getMetricWithBreakdown(index):
        return {
            "name": TextElement("metric name", f"{EodData.bdmetric_collection_xpath}[{index}]/div[1]//label"),
            "value": InputElement("metric value", f"{EodData.bdmetric_collection_xpath}[{index}]/div[2]/input"),
            "open_bd": ClickableElement("Breakdown Button", f"{EodData.bdmetric_collection_xpath}[{index}]/div[1]//a")
        }
    
    @staticmethod
    def getMetricsCollection():
        return CollectionElement("Metrics", EodData.metrics_collection_xpath)
    
    @staticmethod
    def getBdMetricCollection():
        return CollectionElement("Metrics", EodData.bdmetric_collection_xpath)