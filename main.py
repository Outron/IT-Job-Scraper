from selenium import webdriver
import time
from selenium.webdriver.common.by import By
url = 'https://justjoin.it'
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(2)
def click_cookie_button():
    driver.find_element(By.CSS_SELECTOR, value = "#root > div.jss220.jss221 > button").click()
def night_mode_on():
    driver.find_element(By.CSS_SELECTOR, value = "#root > header > div > div.jss17 > div.jss161 > span > span.MuiButtonBase-root-64.MuiIconButton-root-74.jss183.MuiSwitch-switchBase-176.jss165.MuiSwitch-colorSecondary-178 > span > input").click()
def choose_offer_type():
    print("choose offer type (all offers[1] / Offers with salary[2]:")
    while True:
        try:
            choose = int(input())
            if choose in (1,2):
                if choose == 1:
                    return driver.find_element(By.CSS_SELECTOR, value="#root > div.css-1smbjja > div.css-kkhecm > div > div.css-p1iqw4 > div.css-1x7tcfa > a.css-67yi4f").click()
                if choose == 2:
                    return driver.find_element(By.CSS_SELECTOR, value="#root > div.css-1smbjja > div.css-kkhecm > div > div.css-p1iqw4 > div.css-1x7tcfa > a.css-1pow96e").click()
            else:
                print("Incorrect choose")
                print("Choose offer type: all offers[1] / Offers with salary[2]:")
        except ValueError:
            print("Incorrect choose")
            print("Choose offer type: all offers[1] / Offers with salary[2]:")

def choose_tech():
    driver.find_element(By.CSS_SELECTOR, value = "#root > div.css-1ho6o7a > div > button:nth-child(3)").click()
    tech_list = driver.find_element(By.CSS_SELECTOR, value = "body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogContent-root.MuiDialogContent-dividers")
    tech = tech_list.find_elements(By.XPATH, value = '//a[@aria-disabled="false"]')
    for t in tech:
        print(t.text)


click_cookie_button()
time.sleep(1)
night_mode_on()
time.sleep(1)
choose_offer_type()
time.sleep(1)
choose_tech()


# choose_offer_type()
# with open("source.html", "w", encoding='utf-8') as f:
#     f.write(driver.page_source)
#     f.close()
