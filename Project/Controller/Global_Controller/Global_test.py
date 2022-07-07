from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .Global_xpath import LoginXpath
from flask import flash

class Login:
    @staticmethod
    def login(driver, url, username, password):
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=d)
        # driver.implicitly_wait(30)

        res = Login.openUrl(driver, url)

        if not res["success"]:
            flash(res["message"], category="error")
            driver.quit()
            return False


        username_xpath = LoginXpath.username
        password_xpath = LoginXpath.password
        loginbtn_xpath = LoginXpath.login_btn

        # landing page
        
        res = Login.authenticate(driver, username_xpath, password_xpath, loginbtn_xpath, username, password)
        
        if not res['success']:
            flash(res["message"], category="error")
            driver.quit()
            return False

        return driver

    @staticmethod
    def authenticate(driver, username_xpath, password_xpath, loginbtn_xpath, username, passwd):
        # email = WebDriverWait(driver, 120).until(
        #     EC.presence_of_element_located((By.XPATH, f"{username}"))
        # )
        email = driver.find_element(by=By.XPATH, value=f'{username_xpath}')
        email.send_keys(username)
        password = driver.find_element(by=By.XPATH, value=f'{password_xpath}')
        password.send_keys(passwd)
        loginbtn = driver.find_element(by=By.XPATH, value=f'{loginbtn_xpath}')

        loginbtn.click()

        try:
            # element = WebDriverWait(driver, 120).until(
            #     EC.presence_of_element_located((By.XPATH, LoginXpath.login_error))
            # )
            element = WebDriverWait(driver, 120).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, LoginXpath.login_error)), 
                    EC.presence_of_element_located((By.XPATH, LoginXpath.main_header))
                )
            )
            # element = driver.find_element(
            #     by = By.XPATH,
            #     value = LoginXpath.main_header
            # )
            # print(f"{element} {element.text}")
            print("Login success")

            if "These credentials do not match our records" in element.text:
                return {
                    "success": False,
                    "message": "Invalid credentials."
                }
            
        except Exception as e:
            print(e)
        return{
            "success": True
        }

    @staticmethod
    def openUrl(driver, url):
        driver.get(url)
        
        try:
            # element = WebDriverWait(driver, 120).until(
            #     EC.presence_of_element_located((By.XPATH, LoginXpath.no_vpn))
            # )

            element = driver.find_element(
                by = By.XPATH,
                value = LoginXpath.no_vpn
            ).text
            if "Network Error" in element:
                
                return {
                    "success": False,
                    "message": "Not connected to the Jarvis Network."
                }
            else:
                print("Connected to Jarvis Network")
        except Exception as e:
            pass

        try:
            # element = WebDriverWait(driver, 120).until(
            #     EC.presence_of_element_located((By.XPATH, LoginXpath.logo_xpath))
            # )
            element = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, LoginXpath.logo_xpath))
            )
            # element = driver.find_element(
            #     by = By.XPATH,
            #     value = LoginXpath.logo_xpath
            # )
            print(f"Valid URL {element}")
        except Exception as e:
            print("Invalid Url")
            return {
                "success": False,
                "message": "Invalid Jarvis Analytics URL."
            }

        return {
            "success": True
        }
