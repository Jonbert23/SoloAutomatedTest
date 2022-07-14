import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Project.Controller.Global_Controller.Global_xpath import CalendarMonthPicketXpath

class MonthPicker:
    
    def Cal_monthPicker(driver, month):
        driver.get('https://solo.next.jarvisanalytics.com/calendar/appointments/month')
        
        driver.implicitly_wait(1000000)
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div[2]/button')))
        
        for i in range(5000):
            month_year = driver.find_element(By.XPATH, CalendarMonthPicketXpath.month_year).text
            month_test = datetime.strptime(month_year, '%B %Y')
            month_test = month_test.strftime("%Y-%m")
        
            if month_test > month:
                driver.find_element(By.XPATH, CalendarMonthPicketXpath.arrow_back).click()
            if month_test < month:
                driver.find_element(By.XPATH, CalendarMonthPicketXpath.arrow_next).click()
            if month_test == month:
                print('Done Finding Date')
                break
