from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time 
from datetime import datetime
from ....models import CalendarFilterUse
from ....models import CalendarFilterTesting
from ....models import CalendarMetricTesting
from .... import db
import sqlite3
import re


def perDayTest(driver, test_code, test_date):
    date_test = datetime.strptime(test_date, '%Y-%m-%d')
    date_test = date_test.strftime("%A %B %d, %Y")
    day = date_test.strftime("%d")

    print(day)

    return "Hello"