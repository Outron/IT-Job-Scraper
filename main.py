from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from tqdm import tqdm
import time
from time import sleep

# URL: https://justjoin.it/
# WebDriver: Chrome
url = 'https://justjoin.it'
options = webdriver.ChromeOptions()

#options.add_argument("--headless=new")  # HEADLESS MODE
options.add_experimental_option("detach", True)  # DETACHT MODE
driver = webdriver.Chrome(options=options)
driver.set_window_size(800,1000)
driver.get(url)
time.sleep(3)

def Click_Cookie_Button():
    now = datetime.now()
    t = now.strftime("%H")
    if int(t) >= 22 or int(t) <= 6:
        driver.find_element(By.XPATH("///*[@id='__next']/div[3]/button"))
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
                    driver.find_element(By.XPATH,
                                        value="/html/body/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/div/div[1]/div[1]/div/div/button[2]").click()
                    time.sleep(1)
                    return
                if choose == 2:
                    print("Selected offer type: 2.Offers with salary\n")
                    driver.find_element(By.XPATH,
                                        value="/html/body/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/div/div[1]/div[1]/div/div/button[1]").click()
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
    driver.find_element(By.XPATH, value="//button[normalize-space()='Tech']").click()
    tech_tab = driver.find_element(By.XPATH, value="//div[@class='css-1ff3op5']")
    tech_list = tech_tab.find_elements(By.XPATH, value="//div[@class='css-1k38fl6']")

    # Creating a list with names of technologies
    tech_name = []
    for index, element in enumerate(tech_list[1:], start=1):
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
            tech_list[abs(choose)].click()
            return print("Selected technology: " + name_of_technology)
        except ValueError:
            print("Incorrect choice")

def Filter_Settings():
    # extracting names from list without blank space between them, using list comprehension
    def Extract_Names(elements):
        names = [element.text for element in elements if element.text.strip() != '']
        return [f"{index + 1}.{name}" for index, name in enumerate(names)]

    # Needed CSS selectors
    more_filters_button_selector = "//button[normalize-space()='More filters']"
    employment_selector = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[2]/form[1]/div[4]/fieldset[1]/div[1]"
    seniority_selector = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[2]/form[1]/div[3]/fieldset[1]/div[1]"
    apply_settings_button = "button[type='submit']"

    # More filters button click
    driver.find_element(By.XPATH, value=more_filters_button_selector).click()
    time.sleep(1)
    # Take employment buttons and names
    employment_type = driver.find_element(By.XPATH, value=employment_selector)
    employment_name = employment_type.find_elements(By.TAG_NAME, value="label")
    emp_button = employment_type.find_elements(By.TAG_NAME, value="input")
    name_type_filtered = Extract_Names(employment_name)

    # Take seniority buttons and names
    seniority_type = driver.find_element(By.XPATH, value=seniority_selector)
    seniority_name = seniority_type.find_elements(By.TAG_NAME, value="label")
    sen_button = seniority_type.find_elements(By.TAG_NAME, value="input")
    name_type_filtered.extend(Extract_Names(seniority_name))

    # Print the filtered and enumerated names of employment
    for employment in name_type_filtered[:5]:
        print(employment)

    # Make employment type choose
    while True:
        print("Choose employment type: ")
        try:
            choose_emp = int(input())
            if choose_emp in range(1, 6):
                emp_button[choose_emp - 1].click()
                print("Selected type of employment: " + name_type_filtered[choose_emp - 1] + "\n")
                break
            else:
                print("Incorrect choice")

        except ValueError:
            print("Incorrect choice")

    # Print the filtered and enumerated names of seniority
    for seniority in name_type_filtered[5:]:
        print(seniority)

    # Make seniority type choose
    while True:
        print("Choose seniority type: ")
        try:
            choose_sen = int(input())
            if choose_sen in range(1, 6):
                sen_button[choose_sen - 1].click()
                print("Selected type of seniority: " + name_type_filtered[choose_sen + 4] + "\n")
                driver.find_element(By.CSS_SELECTOR, value=apply_settings_button).click()
                break
            else:
                print("Incorrect choice")

        except ValueError:
            print("Incorrect choice")

def Choose_Location():
    # CSS SELECTORS
    location_button_selector = "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/button[1]"
    poland_locations_selector = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/form[1]/div[1]/div[3]/div[1]"
    other_locations_poland_selector = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/form[1]/div[1]/div[5]/div[1]"
    top_world_locations_selector = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/form[1]/div[1]/div[4]/div[1]"
    show_offers_button = "//button[@type='submit']"

    # CLICK BUTTONS
    driver.find_element(By.XPATH, value=location_button_selector).click()
    time.sleep(0.5)

    top_poland_locations = driver.find_element(By.XPATH, value=poland_locations_selector)
    other_locations_poland = driver.find_element(By.XPATH, value=other_locations_poland_selector)
    top_world_locations = driver.find_element(By.XPATH, value=top_world_locations_selector)
    locations_types = ["1.Top Poland locations", "2.Other locations Poland", "3.Top world locations"]

    def get_location_names(value):
        xpath = ''
        if value == 1:
            xpath = top_poland_locations
        if value == 2:
            xpath = other_locations_poland
        if value == 3:
            xpath = top_world_locations

        location_names = xpath.find_elements(By.TAG_NAME, value='button')
        names = []
        for index, element in enumerate(location_names[:], start=1):
            names.append(f"{index}.{element.text}")

        for n in names:
            print(n)

        choose = int(input("Choose city: "))
        location_names[choose - 1].click()
        driver.find_element(By.XPATH, value=show_offers_button).click()
        print("\nSelected city: " + names[choose - 1])

    while True:
        try:
            for i in locations_types:
                print(i)
            choice = int(input("Choose location: "))

            if choice in (1, 2, 3):
                return get_location_names(choice)
            else:
                print("\nIncorrect choice\n")

        except ValueError:
            print("\nIncorrect choice\n")

def Get_Job_Offers():
    full_height_job_offers = driver.find_element(By.XPATH, value='//div[@data-virtuoso-scroller="true"]').size['height']
    job_offers = driver.find_element(By.XPATH, value="//div[@data-test-id='virtuoso-item-list']")
    scroll_page = driver.find_element(By.XPATH, value="/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[2]")
    job_xpath_selector = 'div[data-index="0"]'
    jobs = []  # list for scraped jobs and links
    salaries = []  # list for scraped salaries

    def scroll(px):  # function responsible for scrolling site every
        scroll_script = f'window.scrollBy(0, {px})'
        driver.execute_script(scroll_script, scroll_page)
        time.sleep(0.5)

    # increase data index function is responsible for increasing data-index div attribute in xpath selector of single job offer,
    # every increased index is next job offer
    def increase_data_index(top, jobs_div_height, job_selector, job_offers_div, job_list, salary_list):
        index = top
        job_offer_height = 0
        total_iterations = jobs_div_height // 68   # 68 is height of single job offer
        pbar = tqdm(total=total_iterations, colour = "red")
        pbar.set_description("Scraping...", refresh=True)

        while index <= total_iterations:
            print(index)  # to check index value
            if index > 3:
                if index % 1 == 0 and index != 0:  # 612 because site is scrolled with 612px
                    scroll(100)

            updated_job_selector = job_selector.replace(f'0', f'{index}')

            try:
                z_element = job_offers_div.find_element(By.CSS_SELECTOR, value=updated_job_selector)
                job_offer_height += 68
                print(job_offer_height)  # to check height
                job_names = z_element.find_element(By.TAG_NAME, value="h2")
                link_to_job = z_element.find_element(By.TAG_NAME, value="a")
                salary_values = z_element.find_elements(By.TAG_NAME, value="span")

                job_list.append(job_names.text)
                job_list.append(link_to_job.get_attribute('href'))
                for element in salary_values:
                    salary_list.append(element.get_attribute('innerText'))

                pbar.update(1)
                if job_offer_height >= jobs_div_height:
                    return print("Scraping finished!")
                index += 1

            except NoSuchElementException:
                print("brak elementu")
                scroll(-250)
                continue

        pbar.close()

    # print(full_height_job_offers) # to check height
    increase_data_index(0, full_height_job_offers, job_xpath_selector, job_offers, jobs, salaries)

    if len(jobs) == 0:
        return print("Nie znaleziono żadnych ofert!")

    salary_list_filtered = [salary for salary in salaries if salary.endswith("PLN") or salary == "Undisclosed Salary"]

    def insert_salary_list_and_add_space(JobLink_list, salary_list):
        place = 0
        for s in range(2, len(JobLink_list)+len(salary_list), 3):
            JobLink_list.insert(s, salary_list[place])
            place += 1

        for space in range(len(JobLink_list) - 1, 0, -1):  # adding space between offers for better visibility
            if space % 3 == 0:  # % 3 because 1 el is name, 2 el is link, 3 el is salary
                JobLink_list.insert(space, ' ')

    insert_salary_list_and_add_space(jobs,salary_list_filtered)

    for j in jobs:
        print(j)

    return jobs

    # print("\nDo you want to save results in pdf file?")
    # choose = int(input("1.Yes / 2.No"))
    # while True:
    #     try:
    #         if choose in (1,2):
    #             if choose == 1:
    #                 Save_Jobs_To_Pdf(jobs,output_file)
    #             if choose == 2:
    #                 print("Back to menu...\n")
    #                 sleep(3)
    #                 return Menu()
    #     except ValueError:
    #         print("Incorrect choice")
    #         choose = int(input("1.Yes / 2.No"))

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
    file = []
    for item in jobs_list:
        if item == ' ':
            # add empty paragraph
            file.append(Spacer(1, 12))
        else:
            # check if link
            if item.startswith("http"):
                file.append(Paragraph(item, styles['LinkStyle']))
            else:
                file.append(Paragraph(item, styles['Normal']))

    doc.build(file)
    print("Saved!")
    print("Returning to the menu...")
    time.sleep(3)
    return Menu()

def Menu():
    def Menu_filters():
        print("SELECT YOUR FILTERS:\n")
        print("1.Choose offer type\n2.Choose technology\n3.Choose location\n4.Choose employment type and seniority\n5.Back")
        while True:
            try:
                choose1 = int(input("Choose: (type 1-5)"))
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
                print("Incorrect choice!")


    print("1.SET FILTERS\n2.START SCRAPING!\n3.QUIT")

    while True:
        try:
            choose2 = int(input("Choose: (type 1-3)"))
            if choose2 in (1, 2, 3):
                if choose2 == 1:
                    return Menu_filters()
                if choose2 == 2:
                    return Get_Job_Offers()
                if choose2 == 3:
                    return quit()
        except ValueError:
            print("Incorrect choice!")



output_file = "jobs.pdf"
#Click_Cookie_Button()
time.sleep(0.5)
#Night_Mode_On()
print("#########################\nWELCOME TO IT JOB SCRAPER\n#########################\n")
Menu()
