from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from itertools import chain
url = 'https://justjoin.it'
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new") HEADLESS MODEgi9
options.add_experimental_option("detach", True)  # DETACHT MODE
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(2)

def Click_Cookie_Button():
    driver.find_element(By.CSS_SELECTOR, value = "#root > div.jss220.jss221 > button").click()

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

def Filter_Settings():
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

def Get_Job_Offers():
    full_height_job_offers = driver.find_element(By.CSS_SELECTOR, value = '#root > div.css-1smbjja > div.css-kkhecm > div > div.css-110u7ph > div:nth-child(1) > div > div').size['height']
    height_job_offers = driver.find_element(By.CSS_SELECTOR, value = '#root > div.css-1smbjja > div.css-kkhecm > div > div.css-110u7ph > div:nth-child(1) > div').size['height']
    z = height_job_offers

    names = []
    links = []
    salaries = []

    while full_height_job_offers > height_job_offers:
        job_offers = driver.find_element(By.CSS_SELECTOR, value="#root > div.css-1smbjja > div.css-kkhecm > div > div.css-110u7ph > div:nth-child(1) > div > div")
        job_names = job_offers.find_elements(By.TAG_NAME, value="img")
        link_to_job = job_offers.find_elements(By.TAG_NAME, value="a")
        job_salary = job_offers.find_elements(By.XPATH, value="//div[contains(text(), 'PLN') or contains(text(), 'Undisclosed Salary')]")
        time.sleep(1)

        for name in job_names:
            print(name.get_attribute('alt'))
            names.append(name.get_attribute('alt'))
        for link in link_to_job:
            links.append(link.get_attribute('href'))
        for salary in job_salary:
            salaries.append(salary.text)

        scroll_script = "arguments[0].scrollTop += 1076;"
        driver.execute_script(scroll_script,job_offers)
        height_job_offers += z
        time.sleep(1)

    salaries_filtered = [x for x in salaries if x not in '']
    combined_list = list(chain(*zip(names, salaries_filtered, links)))
    print(list(combined_list))

Click_Cookie_Button()
time.sleep(1)
Night_Mode_On()
time.sleep(1)
Filter_Settings()

#Choose_Offer_Type()


# with open("source.html", "w", encoding='utf-8') as f:
#     f.write(driver.page_source)
#     f.close()
