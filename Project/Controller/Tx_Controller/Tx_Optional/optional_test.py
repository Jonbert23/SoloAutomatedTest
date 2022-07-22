from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time 
from datetime import datetime
from ....models import TxMinerDefaultTest
from .... import db
import sqlite3
import re


def optionalTestTx(driver, test_code, test_month):
    driver.implicitly_wait(1000000000)