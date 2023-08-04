from selenium import webdriver
from datetime import datetime
import time
from selenium.webdriver.common.by import By
from itertools import chain
url = 'https://justjoin.it'
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new") HEADLESS MODEgi9
options.add_experimental_option("detach", True)  # DETACHT MODE
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(1)

def Click_Cookie_Button():
    now = datetime.now()
    t = now.strftime("%H")
    if int(t) >= 22 or int(t) <= 6:
        driver.find_element(By.CSS_SELECTOR, value = "#root > div.jss220.jss221 > button").click()
    else:
        driver.find_element(By.CSS_SELECTOR, value="#root > div.jss219.jss220 > button").click()

def Night_Mode_On():
    now = datetime.now()
    t = now.strftime("%H")
    if int(t) >= 22 or int(t) <= 6:
        driver.find_element(By.CSS_SELECTOR, value="#root > header > div > div.jss17 > div.jss161 > span > span.MuiButtonBase-root-64.MuiIconButton-root-74.jss183.MuiSwitch-switchBase-176.jss165.MuiSwitch-colorSecondary-178 > span > input").click()
    else:
        driver.find_element(By.CSS_SELECTOR, value="#root > header > div > div.jss17 > div.jss161 > span > span.MuiButtonBase-root-64.MuiIconButton-root-74.jss182.MuiSwitch-switchBase-175.jss165.MuiSwitch-colorSecondary-177 > span > input").click()

def Choose_Offer_Type():
    while True:
        try:
            choose = int(input("Choose offer type (all offers[1] / Offers with salary[2]:"))
            if choose in (1,2):
                if choose == 1:
                    print("Selected offer type: 1.All offers\n")
                    return driver.find_element(By.CSS_SELECTOR, value="#root > div.css-1smbjja > div.css-kkhecm > div > div.css-p1iqw4 > div.css-1x7tcfa > a.css-67yi4f").click()
                if choose == 2:
                    print("Selected offer type: 2.Offers with salary\n")
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

def Filter_Settings():
    # extracting names from list without blank space between them, using list comprehension
    def Extract_Names(elements):
        names = [element.text for element in elements if element.text.strip() != '']
        return [f"{index + 1}.{name}" for index, name in enumerate(names)]

    # Needed CSS selectors
    more_filters_button_selector = "#root > div.css-1ho6o7a > div > button.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.css-74bv5i.MuiButton-outlinedSizeSmall.MuiButton-sizeSmall"
    employment_selector = "body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogContent-root.MuiDialogContent-dividers > div:nth-child(5) > div"
    seniority_selector = "body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogContent-root.MuiDialogContent-dividers > div:nth-child(8) > div"
    apply_settings_button = "body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogActions-root.css-1h3quci.MuiDialogActions-spacing > a.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.css-1fivffo"

    # More filters button click
    driver.find_element(By.CSS_SELECTOR, value=more_filters_button_selector).click()

    # Take employment buttons and names
    employment_type = driver.find_element(By.CSS_SELECTOR, value=employment_selector)
    employment_name = employment_type.find_elements(By.TAG_NAME, value="span")
    emp_button = employment_type.find_elements(By.TAG_NAME, value="button")
    name_type_filtered = Extract_Names(employment_name)

    # Take seniority buttons and names
    seniority_type = driver.find_element(By.CSS_SELECTOR, value=seniority_selector)
    seniority_name = seniority_type.find_elements(By.TAG_NAME, value="span")
    sen_button = seniority_type.find_elements(By.TAG_NAME, value="button")
    name_type_filtered.extend(Extract_Names(seniority_name))

    # Print the filtered and enumerated names of employment
    for name in name_type_filtered[:4]:
        print(name)

    # Make employment type choose
    while True:
        print("Choose employment type: ")
        try:
            choose_emp = int(input())
            if choose_emp in range(1, 5):
                emp_button[choose_emp - 1].click()
                print("Selected type of employment: " + name_type_filtered[choose_emp - 1] + "\n")
                break
            else:
                print("Incorrect choice")

        except ValueError:
            print("Incorrect choice")

    # Print the filtered and enumerated names of seniority
    for name in name_type_filtered[4:]:
        print(name)

    # Make seniority type choose
    while True:
        print("Choose seniority type: ")
        try:
            choose_sen = int(input())
            if choose_sen in range(1, 5):
                sen_button[choose_sen - 1].click()
                print("Selected type of seniority: " + name_type_filtered[choose_sen + 3] + "\n")
                driver.find_element(By.CSS_SELECTOR, value = apply_settings_button).click()
                break
            else:
                print("Incorrect choice")

        except ValueError:
            print("Incorrect choice")

def Choose_Location():
    # CSS SELECTORS
    location_button_selector = "#root > div.css-1ho6o7a > div > button:nth-child(2)"
    poland_locations_selector = "body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogContent-root.MuiDialogContent-dividers > div > div:nth-child(2) > div > div > div > div"
    other_locations_poland_button_selector = "body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogContent-root.MuiDialogContent-dividers > div > div:nth-child(4) > button"
    other_locations_poland_selector = "body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogContent-root.MuiDialogContent-dividers > div > div:nth-child(4) > div > div > div > div"
    top_world_locations_selector = "body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogContent-root.MuiDialogContent-dividers > div > div:nth-child(3) > div > div > div > div"

    # CLICK BUTTONS
    driver.find_element(By.CSS_SELECTOR, value = location_button_selector).click()
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, value = other_locations_poland_button_selector).click()

    top_poland_locations = driver.find_element(By.CSS_SELECTOR, value=poland_locations_selector)
    other_locations_poland = driver.find_element(By.CSS_SELECTOR, value = other_locations_poland_selector)
    top_world_locations = driver.find_element(By.CSS_SELECTOR, value = top_world_locations_selector)
    locations_types = ["1.Top Poland locations", "2.Other locations Poland", "3.Top world locations"]

    def get_top_poland_names():
        top_poland_locations_names = top_poland_locations.find_elements(By.TAG_NAME, value='a')
        names = []
        for index, element in enumerate(top_poland_locations_names[:], start=1):
            names.append(f"{index}.{element.text}")

        for n in names:
            print(n)

        choose = int(input("Choose city: "))
        top_poland_locations_names[choose-1].click()
        print("\nSelected city: " + names[choose-1])

    def get_other_locations_poland_names():
        other_locations_poland_names = other_locations_poland.find_elements(By.TAG_NAME, value='a')
        names = []
        for index, element in enumerate(other_locations_poland_names[:], start=1):
            names.append(f"{index}.{element.text}")

        for n in names:
            print(n)

        choose = int(input("Choose city: "))
        other_locations_poland_names[choose - 1].click()
        print("\nSelected city: " + names[choose - 1])

    def get_top_world_locations_names():
        top_world_locations_names = top_world_locations.find_elements(By.TAG_NAME, value='a')
        names = []
        for index, element in enumerate(top_world_locations_names[:], start=1):
            names.append(f"{index}.{element.text}")

        for n in names:
            print(n)

        choose = int(input("\nChoose city: "))
        top_world_locations_names[choose - 1].click()
        print("\nSelected city: " + names[choose - 1])

    while True:
        try:
            for i in locations_types:
                print(i)
            choice = int(input("Choose location: "))

            if choice in (1,2,3):
                if choice == 1:
                    return get_top_poland_names()
                if choice == 2:
                    return get_other_locations_poland_names()
                if choice == 3:
                    return get_top_world_locations_names()
            else:
                print("\nIncorrect choice\n")

        except ValueError:
            print("\nIncorrect choice\n")

def Get_Job_Offers():
    #full_height_job_offers = driver.find_element(By.CSS_SELECTOR, value = '#root > div.css-1smbjja > div.css-kkhecm > div > div.css-110u7ph > div:nth-child(1) > div > div').size['height']
    job_offers = driver.find_element(By.XPATH, value="//div[@class='css-rinife']")
    #job_names = job_offers.find_elements(By.TAG_NAME, value="img")
    #link_to_job = job_offers.find_elements(By.TAG_NAME, value="a")
    #job_salary = job_offers.find_elements(By.XPATH, value="//div[contains(text(), 'PLN') or contains(text(), 'Undisclosed Salary')]")

    names = []
    links = []
    salaries = []

    def scroll():
        scroll_script = "arguments[0].scrollTop += 1000;"
        driver.execute_script(scroll_script, job_offers)
        time.sleep(1)

    k = 'div[style="position: absolute; left: 0px; top: 0px; height: 68px; width: 100%;"]'

    def increase_top(top):
        for f in range(12):
            updated_k = k.replace(f'top: 0px', f'top: {top+(f*68)}px')
            z = job_offers.find_element(By.CSS_SELECTOR, value=updated_k)
            job_names = z.find_elements(By.TAG_NAME, value = "img")
            link_to_job = z.find_elements(By.TAG_NAME, value="a")
            job_salary = z.find_elements(By.XPATH, value="//div[contains(text(), 'PLN') or contains(text(), 'Undisclosed Salary')]")

            for name in job_names:
                names.append(name.get_attribute('alt'))

            for link in link_to_job:
                links.append(link.get_attribute('href'))

            for salary in job_salary:
                salaries.append(salary.text)


    for i in range(2):
        increase_top(816*i)
        scroll()


    salaries_filtered = [x for x in salaries if x not in '']
    combined_list = list(chain(*zip(names, salaries_filtered, links)))

    if len(combined_list) == 0:
        print("Nie znaleziono żadnych ofert!")
    else:
        print(list(combined_list))



Click_Cookie_Button()
time.sleep(1)
Night_Mode_On()
# time.sleep(1)
# Choose_Offer_Type()
# time.sleep(1)
# Choose_Tech()
# time.sleep(1)
# Choose_Location()
# time.sleep(1)
# Filter_Settings()
time.sleep(3)
Get_Job_Offers()
