from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
import time

url = 'https://justjoin.it'
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new") HEADLESS MODE
options.add_experimental_option("detach", True)  # DETACHT MODE
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(1)

def Click_Cookie_Button():
    now = datetime.now()
    t = now.strftime("%H")
    if int(t) >= 22 or int(t) <= 6:
        driver.find_element(By.CSS_SELECTOR, value="#root > div.jss220.jss221 > button").click()
    else:
        driver.find_element(By.CSS_SELECTOR, value="#root > div.jss219.jss220 > button").click()

def Night_Mode_On():
    now = datetime.now()
    t = now.strftime("%H")
    if int(t) >= 22 or int(t) <= 6:
        driver.find_element(By.CSS_SELECTOR,
                            value="#root > header > div > div.jss17 > div.jss161 > span > span.MuiButtonBase-root-64.MuiIconButton-root-74.jss183.MuiSwitch-switchBase-176.jss165.MuiSwitch-colorSecondary-178 > span > input").click()
    else:
        driver.find_element(By.CSS_SELECTOR,
                            value="#root > header > div > div.jss17 > div.jss161 > span > span.MuiButtonBase-root-64.MuiIconButton-root-74.jss182.MuiSwitch-switchBase-175.jss165.MuiSwitch-colorSecondary-177 > span > input").click()

def Choose_Offer_Type():
    while True:
        try:
            choose = int(input("Choose offer type:\n1.All offers\n2.Offers with salary"))
            if choose in (1, 2):
                if choose == 1:
                    print("Selected offer type: 1.All offers\n")
                    driver.find_element(By.CSS_SELECTOR,
                                        value="#root > div.css-1smbjja > div.css-kkhecm > div > div.css-p1iqw4 > div.css-1x7tcfa > a.css-67yi4f").click()
                    time.sleep(1)
                    return
                if choose == 2:
                    print("Selected offer type: 2.Offers with salary\n")
                    driver.find_element(By.CSS_SELECTOR,
                                        value="#root > div.css-1smbjja > div.css-kkhecm > div > div.css-p1iqw4 > div.css-1x7tcfa > a.css-1pow96e").click()
                    time.sleep(1)
                    return
            else:
                print("Incorrect choice")
                print("Choose offer type: all offers[1] / Offers with salary[2]:")
        except ValueError:
            print("Incorrect choice")
            print("Choose offer type: all offers[1] / Offers with salary[2]:")

def Choose_Tech():
    # click on tech selection button,then get list of technologies
    driver.find_element(By.CSS_SELECTOR, value="#root > div.css-1ho6o7a > div > button:nth-child(3)").click()
    tech_tab = driver.find_element(By.CSS_SELECTOR,
                                   value="body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogContent-root.MuiDialogContent-dividers")
    tech_list = tech_tab.find_elements(By.XPATH, value='//a[@aria-disabled="false"]')

    # Creating a list with names of technologies
    tech_name = []
    for index, element in enumerate(tech_list[3:], start=1):
        tech_name.append(f"{index}.{element.text}")

    # Display names of technologies in colmuns
    elements_per_column = 5
    elements_to_display = tech_name[0:]
    columns = [elements_to_display[i:i + elements_per_column] for i in
               range(0, len(elements_to_display), elements_per_column)]
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
            name_of_technology = tech_name[abs(choose - 1)]
            tech_list[abs(choose + 2)].click()
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
    for employment in name_type_filtered[:4]:
        print(employment)

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
    for seniority in name_type_filtered[4:]:
        print(seniority)

    # Make seniority type choose
    while True:
        print("Choose seniority type: ")
        try:
            choose_sen = int(input())
            if choose_sen in range(1, 5):
                sen_button[choose_sen - 1].click()
                print("Selected type of seniority: " + name_type_filtered[choose_sen + 3] + "\n")
                driver.find_element(By.CSS_SELECTOR, value=apply_settings_button).click()
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
    driver.find_element(By.CSS_SELECTOR, value=location_button_selector).click()
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, value=other_locations_poland_button_selector).click()

    top_poland_locations = driver.find_element(By.CSS_SELECTOR, value=poland_locations_selector)
    other_locations_poland = driver.find_element(By.CSS_SELECTOR, value=other_locations_poland_selector)
    top_world_locations = driver.find_element(By.CSS_SELECTOR, value=top_world_locations_selector)
    locations_types = ["1.Top Poland locations", "2.Other locations Poland", "3.Top world locations"]

    def get_top_poland_names():
        top_poland_locations_names = top_poland_locations.find_elements(By.TAG_NAME, value='a')
        names = []
        for index, element in enumerate(top_poland_locations_names[:], start=1):
            names.append(f"{index}.{element.text}")

        for n in names:
            print(n)

        choose = int(input("Choose city: "))
        top_poland_locations_names[choose - 1].click()
        print("\nSelected city: " + names[choose - 1])

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

            if choice in (1, 2, 3):
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
    full_height_job_offers = driver.find_element(By.CSS_SELECTOR, value='#root > div.css-1smbjja > div.css-kkhecm > div > div.css-110u7ph > div:nth-child(1) > div > div').size['height']
    job_offers = driver.find_element(By.XPATH, value="//div[@class='css-rinife']")
    jobs = []  # list for scraped jobs

    def scroll():
        scroll_script = "arguments[0].scrollTop += 612;"
        driver.execute_script(scroll_script, job_offers)
        time.sleep(1)

    job_xpath_selector = 'div[style="position: absolute; left: 0px; top: 0px; height: 68px; width: 100%;"]'

    def increase_top(top, jobs_div_height, job_selector, job_offers_div, job_list):
        z = top
        while z <= jobs_div_height - 204:  # -204 because the last 204px doesnt contain job offers
            # print(z) to check top value

            if z % 612 == 0 and z != 0:  # 612 because site is scrolled with 612px
                scroll()

            updated_job_selector = job_selector.replace(f'top: 0px', f'top: {z}px')
            try:
                z_element = job_offers_div.find_element(By.CSS_SELECTOR, value=updated_job_selector)
                job_names = z_element.find_element(By.TAG_NAME, value="img")
                link_to_job = z_element.find_element(By.TAG_NAME, value="a")
                job_list.append(job_names.get_attribute('alt'))
                job_list.append(link_to_job.get_attribute('href'))
                z += 68
            except NoSuchElementException:
                break

    # print(full_height_job_offers) to check height
    increase_top(0, full_height_job_offers, job_xpath_selector, job_offers, jobs)
    if len(jobs) == 0:
        return print("Nie znaleziono żadnych ofert!")

    for i in range(len(jobs) - 1, 0, -1):
        if i % 2 == 0:
            jobs.insert(i, ' ')

    for j in jobs:
        print(j)

    print("\nDo you want to save results in pdf file?")
    choose = int(input("1.Yes / 2.No"))
    while True:
        try:
            if choose in (1,2):
                if choose == 1:
                    Save_Jobs_To_Pdf(jobs,output_file)
                if choose == 2:
                    print("Back to menu...\n")
                    time.sleep(2)
                    return Menu()
        except ValueError:
            print("Incorrect choice")
            choose = int(input("1.Yes / 2.No"))

def Save_Jobs_To_Pdf(jobs_list, output):
    doc = SimpleDocTemplate(output, pagesize = A4)
    styles = getSampleStyleSheet()
    link_style = ParagraphStyle(
        'LinkStyle',
        parent=styles['Normal'],
        textColor=colors.purple,
        underline=1,
    )

    styles.add(link_style)
    story = []

    for item in jobs_list:
        if item == ' ':
            # Dodaj spację jako pusty akapit
            story.append(Spacer(1, 12))
        else:
            # Sprawdź, czy to jest link (np. zaczyna się od "http")
            if item.startswith("http"):
                story.append(Paragraph(item, styles['LinkStyle']))
            else:
                story.append(Paragraph(item, styles['Normal']))

    doc.build(story)

def Menu():
    def Menu_filters():
        print("SELECT YOUR FILTERS:\n")
        print("1.Choose offer type\n2.Choose technology\n3.Choose location\n4.Choose employment type and seniority\n5.Back")
        choose1 = int(input("Choose: (type 1-4)"))
        while True:
            try:
                if choose1 in (1, 2, 3, 4, 5):
                    if choose1 == 1:
                        Choose_Offer_Type()
                        return Menu_filters()
                    if choose1 == 2:
                        Choose_Tech()
                        return Menu_filters()
                    if choose1 == 3:
                        Choose_Location()
                        return Menu_filters()
                    if choose1 == 4:
                        Filter_Settings()
                        return Menu_filters()
                    if choose1 == 5:
                        return Menu()
            except ValueError:
                print("Incorrect choice")
                choose1 = int(input("Choose: (type 1-4)"))

    print("1.SET FILTERS\n2.START SCRAPING!\n3.QUIT")
    choose2 = int(input("Choose: (type 1-3)"))
    while True:
        try:
            if choose2 in (1 ,2, 3):
                if choose2 == 1:
                    return Menu_filters()
                if choose2 == 2:
                    Get_Job_Offers()
                    print("Back to menu")
                if choose2 == 3:
                    return
        except ValueError:
            print("Incorrect choice")
            choose2 = int(input("Choose: (type 1-3)"))

output_file = "jobs.pdf"
Click_Cookie_Button()
time.sleep(0.5)
Night_Mode_On()
print("#########################\nWELCOME TO IT JOB SCRAPER\n#########################\n")
# Menu()
Choose_Tech()
Get_Job_Offers()
