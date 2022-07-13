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

    def waitForElement(self, driver):
        self.waited = True
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.xpath))
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
# Message to future eyd: Need to find way to require the implementation of the getValue method of children classes inherting the Element class.

class InputElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "value")

    def findElement(self, driver):
        self.instantiated = True

        if not self.waited:
            self.waitForElement(driver)

        self.element = driver.find_element(by = By.XPATH, value=self.xpath)
    
    def getValue(self):
        if self.element == None: 
            raise Exception("Element not instantiated.")

        return self.element.get_attribute('value')

class TextElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "value")

    def findElement(self, driver):
        self.instantiated = True

        if not self.waited:
            self.waitForElement(driver)

        try:
            self.element = driver.find_element(by = By.XPATH, value=self.xpath)
        except:
            pass
    
    def getValue(self):
        if self.element == None: 
            raise Exception("Element not instantiated.")

        return self.element.text

class CollectionElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "collection")

    def findElement(self, driver):
        self.instantiated = True

        if not self.waited:
            self.waitForElement(driver)

        self.element = driver.find_elements(by = By.XPATH, value=self.xpath)

    def getValue(self):
        if self.element == None: 
            raise Exception("Element not instantiated.")

        return len(self.element)

class ClickableElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "button")

    def findElement(self, driver):
        self.instantiated = True

        if not self.waited:
            self.waitForElement(driver)

        self.element = driver.find_element(by = By.XPATH, value=self.xpath)

    def click(self, driver):
        if self.element == None: 
            raise Exception("Element not instantiated.")
        webdriver.ActionChains(driver).move_to_element(self.element).click(self.element).perform()
        # self.element.click()

# BEYOND ARE HARDCODED XPATHS, NEED TO CHANGE IMPLEMENTATION LATER TO INCOPORATE DATABASE CALLS
# OTHER IS TO IMPLEMENT A DIFFERENT METHOD OF GETTING XPATHS SUCH THAT CHANGES IN CONFIGURATION WILL NOT BREAK THE CODE

class EodXpath:
    booked_prod = InputElement("booked_production", '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[1]/div[2]/input')
    daily_net_prod = InputElement("daily_net_prod", '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[2]/div[2]/input')
    daily_gross_prod = InputElement('daily_gross_prod', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[3]/div[2]/input')
    ofc_sched_vs_goal = InputElement('office sched vs goal', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[4]/div[2]/input')
    general = InputElement('general', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[6]/div[2]/input')
    ortho_prod = InputElement('ortho_prod', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[7]/div[2]/input')
    perio_prod = InputElement('perio_prod', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[8]/div[2]/input')
    endo = InputElement('endo', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[9]/div[2]/input')
    oral_surgery_prod = InputElement('oral_surgery_prod', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[10]/div[2]/input')
    clear_aligners = InputElement('clear_aligners', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[11]/div[2]/input')
    num_providers = InputElement('number_providers', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[15]/div[2]/input')
    adp = InputElement('adp', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[16]/div[2]/input')
    specialty = InputElement('specialty', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[19]/div[2]/input')
    total_pts_seen = InputElement('total_points_seen', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[22]/div[2]/input')
    total_office_visits = InputElement('total_office_visits', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[23]/div[2]/input')
    total_appts_changed = InputElement('appointments_changed', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[25]/div[2]/input')
    total_appts_cancel = InputElement('appointments_cancelled', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[26]/div[2]/input')
    guest_with_appt = InputElement('guests_with_future_appts', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[27]/div[2]/input')
    hyg_reserve = InputElement('hyg_reserve', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[29]/div[2]/input')
    hyg_cap = InputElement('hyg_cap', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[30]/div[2]/input')
    react_made = InputElement('react_made', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[31]/div[2]/input')
    unsched_treat = InputElement('unsched_treat', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[32]/div[2]/input')
    restore_appts = InputElement('restore_appts', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[33]/div[2]/input')
    recalls_made = InputElement('recalls_made', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[34]/div[2]/input')
    collection = InputElement('collection','/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[13]/div[2]/input')
    adjustments = InputElement('adjustments', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[12]/div[2]/input')
    case_acceptance = InputElement('case_acceptance','/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[20]/div[2]/input')
    missing_ref = InputElement('missing_ref', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[24]/div[2]/input')
    no_show = InputElement('no_show', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[17]/div[2]/input')
    daily_coll = InputElement('daily_coll', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[14]/div[2]/input')
    hyg_reapp = InputElement('hyg_reapp', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[28]/div[2]/input')
    new_patients = InputElement('new_patients', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[21]/div[2]/input')
    same_day_treat = InputElement('same_day_treat', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[18]/div[2]/input')
    pt_portion = InputElement('pt_portion', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[5]/div[2]/input')

class BreakdownXpath:
    collection = ClickableElement('collection', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[13]/div[1]/div/span/a')
    adjustments = ClickableElement('adjustments', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[12]/div[1]/div/span/a')
    case_acceptance = ClickableElement('case_acceptance', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[20]/div[1]/label/span/a')
    missing_ref = ClickableElement('missing_ref', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[24]/div[1]/label/div/a')
    no_show = ClickableElement('no_show', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[17]/div[1]/label/div/a')
    daily_coll = ClickableElement('daily_coll', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[14]/div[1]/label/div/a')
    hyg_reapp = ClickableElement('hyg_reapp', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[28]/div[1]/label/div/a')
    new_patients = ClickableElement('new_patients', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[21]/div[1]/label/div/a')
    same_day_treat = ClickableElement('same_day_treat', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[18]/div[1]/label/div/a')
    pt_portion = ClickableElement('pt_portion', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[5]/div[1]/label/div/a')

# june 21 and some other dates for missing ref and new patients
class ModalMetricXpath:
    collection = TextElement('collection', '/html/body/div[1]/main/div[3]/div[9]/div/div/div[3]/div[1]/div/table/tfoot/tr/td[6]')
    adjustments = TextElement('adjustments', '/html/body/div[1]/main/div[3]/div[2]/div/div/div[3]/div[1]/div/table/tfoot/tr/td[6]')
    case_acceptance = TextElement('case_acceptance', '/html/body/div[1]/main/div[3]/div[9]/div/div/div[2]/div[1]/div/table/tfoot/tr[1]/td[6]')
    # missing ref is number of rows
    missing_ref = CollectionElement('missing_ref', '/html/body/div[1]/main/div[3]/div[7]/div/div/div[2]/div[2]/div/table/tbody/tr')
    no_show = TextElement('no_show', '/html/body/div[1]/main/div[3]/div[4]/div/div/div[2]/div[2]/div/table/tr/td[2]/strong/span')
    daily_coll = TextElement('daily_coll', '/html/body/div[1]/main/div[3]/div[3]/div/div/div[2]/div[2]/div/table/tr/td[4]/strong/span')
    hyg_reapp = TextElement('hyg_reapp', '/html/body/div[1]/main/div[3]/div[8]/div/div/div[2]/div[2]/div/table/tr/td[3]/strong/span')
    # new patients is number of rows
    new_patients = CollectionElement('new_patients', '/html/body/div[1]/main/div[3]/div[6]/div/div/div[2]/table/tbody/tr')
    same_day_treat = TextElement('same_day_treat', '/html/body/div[1]/main/div[3]/div[5]/div/div/div[2]/div[2]/div/table/tr[2]/td[5]/strong/span')
    pt_portion = TextElement('pt_portion', '/html/body/div[1]/main/div[3]/div[1]/div/div/div[2]/div[2]/div/table/tr[1]/td[2]/strong/span')

class ModalCloseBtnXpath:
    collection = ClickableElement('collection', '/html/body/div[1]/main/div[3]/div[9]/div/div/div[1]/button')
    adjustments = ClickableElement('adjustments', '/html/body/div[1]/main/div[3]/div[2]/div/div/div[1]/button')
    case_acceptance = ClickableElement('case_acceptance', '/html/body/div[1]/main/div[3]/div[9]/div/div/div[1]/button')
    missing_ref = ClickableElement('missing_ref', '/html/body/div[1]/main/div[3]/div[7]/div/div/div[1]/button')
    no_show = ClickableElement('no_show', '/html/body/div[1]/main/div[3]/div[4]/div/div/div[1]/button')
    daily_coll = ClickableElement('daily_coll', '/html/body/div[1]/main/div[3]/div[3]/div/div/div[1]/button')
    hyg_reapp = ClickableElement('hyg_reapp', '/html/body/div[1]/main/div[3]/div[8]/div/div/div[1]/button')
    new_patients = ClickableElement('new_patients', '/html/body/div[1]/main/div[3]/div[6]/div/div/div[1]/button')
    same_day_treat = ClickableElement('same_day_treat', '/html/body/div[1]/main/div[3]/div[5]/div/div/div[1]/button')
    pt_portion = ClickableElement('pt_portion', '/html/body/div[1]/main/div[3]/div[1]/div/div/div[1]/button')

class EodSetupXpath:
    date_picker = '//*[@class="vue-daterange-picker w-full"]'
    prev_month = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/table/thead/tr/th[1]'
    next_month = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/table/thead/tr/th[3]'
    curr_month_year = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/table/thead/tr/th[2]'
    date_table = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/table/tbody'
    location_picker = '/html/body/div[1]/main/div[1]/div/div/div/div[2]/div/div[2]'
    refresh_btn = '/html/body/div[1]/main/div[1]/div/div/div/div[3]/button'

