from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SpecificDateSelector:
    month_list = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

    def __init__(self, xpath: dict):
        # IMPORTANT! In order to implement this, the "xpath" dictionary should have the following keys:
        # {
        #   "date_picker": <insert date picker xpath>,
        #   "prev_month": <insert prev month button xpath>,
        #   "next_month": <insert next month button xpath>,
        #   "curr_month_year": <insert text with month and year xpath>, On this specific type of calendar, there's text that shows both the month and year, e.g. "Jun 2022"
        #   "date_table": <insert calendar table xpath>,
        # }
        self.date_picker = None
        self.prev_month = None
        self.next_month = None
        self.curr_month_year = None
        self.date_table = None
        self.xpath = xpath
        self.waited = False
        self.instantiated = False

    def initializeCalendar(self, driver):
        self.instantiated = True

        if not self.waited:
            self.waitForCalendar(driver)

        try:
            self.date_picker = driver.find_element(
                by = By.XPATH,
                value = self.xpath['date_picker']
            )
        except:
            raise Exception('Calendar not found.')

    def initializeCalendarButtons(self, driver):
        try:
            self.prev_month = driver.find_element(
                by = By.XPATH,
                value = self.xpath['prev_month']
            )
        except:
            raise Exception('Previous month button not found.')

        try:
            self.next_month = driver.find_element(
                by = By.XPATH,
                value = self.xpath['next_month']
            )
        except:
            raise Exception('Next month button not found.')

        
    def getMonthYear(self, driver):
        try:
            self.curr_month_year = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, self.xpath['curr_month_year']))
            )
        except:
            raise Exception('Month and year not found.')

    def getCalendarDay(self, driver, row, col):
        try:
            self.date_table = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, f"{self.xpath['date_table']}/tr[{row}]/td[{col}]"))
            )
        except:
            raise Exception('Calendar table not found.')


    def waitForCalendar(self, driver):
        self.waited = True
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.xpath['date_picker']))
            )
        except: 
            pass

    def selectDate(self, driver, date: dict):
        # IMPORTANT! To implement this, "date" should be a dictionary with the following keys:
        # {
        #     "month": < Insert month respres in numbers from 1-12 >
        #     "date": < Insert day >
        #     "year": < Insert year >
        # }
        month = int(date["month"]) - 1
        day = date["day"]
        year = int(date["year"])

        self.date_picker.click()
        self.initializeCalendarButtons(driver)
        
        m, y = None, None
        while True:
            self.getMonthYear(driver)
            month_year = self.curr_month_year.text

            m, y = month_year.split(' ')

            y = int(y)
            m = SpecificDateSelector.month_list.index(m)

            if y == year and m == month:
                break
            if y > year or m > month:
                self.prev_month.click()
            else:
                self.next_month.click()

        started = False
        for i in range(2, 8):
            for j in range(1,8):
                self.getCalendarDay(driver, i, j)

                calendarDay = self.date_table.text

                if not started and calendarDay == "1":
                    started = True
                if started and calendarDay == day:
                    self.date_table.click()
                    return