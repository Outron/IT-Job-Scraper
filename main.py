from selenium import webdriver
import time
from selenium.webdriver.common.by import By
url = 'https://justjoin.it'
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new") HEADLESS MODEgi9
options.add_experimental_option("detach", True)  # DETACHT MODE
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(2)
def Click_Cookie_Button():
    driver.find_element(By.CSS_SELECTOR, value = "#root > div.jss219.jss220 > button").click()
def Night_Mode_On():
    driver.find_element(By.CSS_SELECTOR, value = "#root > header > div > div.jss17 > div.jss161 > span > span.MuiButtonBase-root-64.MuiIconButton-root-74.jss183.MuiSwitch-switchBase-176.jss165.MuiSwitch-colorSecondary-178 > span > input").click()
def Choose_Offer_Type():
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
                print("Incorrect choice")
                print("Choose offer type: all offers[1] / Offers with salary[2]:")
        except ValueError:
            print("Incorrect choice")
            print("Choose offer type: all offers[1] / Offers with salary[2]:")

def Choose_Tech():
    # click on tech selection button,then get list of technologies
    driver.find_element(By.CSS_SELECTOR, value = "#root > div.css-1ho6o7a > div > button:nth-child(3)").click()
    tech_tab = driver.find_element(By.CSS_SELECTOR, value = "body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogContent-root.MuiDialogContent-dividers")
    tech_list = tech_tab.find_elements(By.XPATH, value = '//a[@aria-disabled="false"]')

    # Creating a list with names of technologies
    tech_name = []
    for index, element in enumerate(tech_list[3:], start=1):
        tech_name.append(f"{index}.{element.text}")

    #Display names of technologies in colmuns
    elements_per_column = 5
    elements_to_display = tech_name[0:]
    columns = [elements_to_display[i:i + elements_per_column] for i in range(0, len(elements_to_display), elements_per_column)]
    for i in range(elements_per_column):
        for col in columns:
            if i < len(col):
                element = col[i]
                print(f"{element:<20}", end="")
        print()

    # choosing technology
    while True:
        try:
            choose = int(input("Choose technology: (type 1-25) "))
            name_of_technology = tech_name[abs(choose-1)]
            tech_list[abs(choose+2)].click()
            return print("Selected technology: " + name_of_technology)
        except ValueError:
            print("Incorrect choice")

def Get_Job_Offers():
    z = driver.find_element(By.CSS_SELECTOR, value = "#root > div.css-1smbjja > div.css-kkhecm > div > div.css-110u7ph > div:nth-child(1) > div > div")
    p = z.find_elements(By.CSS_SELECTOR, value = "#root > div.css-1smbjja > div.css-kkhecm > div > div.css-110u7ph > div:nth-child(1) > div > div > div:nth-child(1)")
    print(p)




#Click_Cookie_Button()
#time.sleep(1)

Night_Mode_On()
time.sleep(1)
Get_Job_Offers()
#Choose_Offer_Type()
#time.sleep(1)
#Choose_Tech()


# choose_offer_type()
# with open("source.html", "w", encoding='utf-8') as f:
#     f.write(driver.page_source)
#     f.close()
