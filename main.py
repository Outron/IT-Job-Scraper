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
url = "https://justjoin.it"
options = webdriver.ChromeOptions()

# options.add_argument("--headless=new")     #HEADLESS MODE
options.add_experimental_option("detach", True)  # DETACH MODE
driver = webdriver.Chrome(options=options)
driver.set_window_size(800, 1000)
driver.get(url)
time.sleep(3)
output_file = "jobs.pdf"


def click_cookie_button():
    now = datetime.now()
    t = now.strftime("%H")
    if int(t) >= 22 or int(t) <= 6:
        driver.find_element(By.XPATH, value="//*[@id='cookiescript_accept']").click()
    else:
        driver.find_element(
            By.CSS_SELECTOR, value="//*[@id='cookiescript_accept']"
        ).click()


def choose_offer_type():
    offer_type_div = driver.find_element(By.XPATH, value="//div[@role='tablist']")
    offer_type_buttons = offer_type_div.find_elements(By.TAG_NAME, value="button")

    while True:
        try:
            choose = int(
                input("Choose offer type:\n1.All offers\n2.Offers with salary\n")
            )
            if choose in (1, 2):
                if choose == 1:
                    print("Selected offer type: 1.All offers\n")
                    offer_type_buttons[1].click()
                    time.sleep(1)
                    return
                if choose == 2:
                    print("Selected offer type: 2.Offers with salary\n")
                    offer_type_buttons[0].click()
                    time.sleep(1)
                    return
            else:
                print("Incorrect choice")
                print("Choose offer type: all offers[1] / Offers with salary[2]:")
        except ValueError:
            print("Incorrect choice")
            print("Choose offer type: all offers[1] / Offers with salary[2]:")


def choose_tech():
    # click on tech selection button,then get list of technologies
    driver.find_element(
        By.XPATH, value="//button[@name='mobile_categories_filter_button']"
    ).click()
    tech_tab = driver.find_element(
        By.XPATH, value="/html/body/div[6]/div[3]/div/div/div/div[2]"
    )
    tech_list = tech_tab.find_elements(By.TAG_NAME, value="a")

    # Creating a list with names of technologies
    tech_name = []
    for index, element in enumerate(tech_list[0:], start=1):
        tech_name.append(f"{index}.{element.text}")

    # Display names of technologies in columns
    elements_per_column = 5
    elements_to_display = tech_name[0:]
    columns = [
        elements_to_display[i: i + elements_per_column]
        for i in range(0, len(elements_to_display), elements_per_column)
    ]
    for i in range(elements_per_column):
        for col in columns:
            if i < len(col):
                element = col[i]
                print(f"{element:<20}", end="")
        print()

    # choosing technology
    while True:
        try:
            choose = int(input("Choose technology: (type 1-24) "))
            name_of_technology = tech_name[abs(choose - 1)]
            tech_list[abs(choose - 1)].click()
            return print("Selected technology: " + name_of_technology)
        except ValueError:
            print("Incorrect choice")


def filter_settings():
    # extracting names from list without blank space between them, using list comprehension
    def extract_names(elements):
        names = [element.text for element in elements if element.text.strip() != ""]
        return [f"{index + 1}.{name}" for index, name in enumerate(names)]

    # Needed CSS selectors
    more_filters_button_selector = "//button[normalize-space()='More filters']"
    employment_xpath = "//*[@id='filters-more']/div[4]/fieldset/div"
    experience_xpath = "//*[@id='filters-more']/div[3]/fieldset/div"
    apply_settings_button = "button[type='submit']"

    # More filters button click
    driver.find_element(By.XPATH, value=more_filters_button_selector).click()
    time.sleep(1)
    # Take employment buttons and names
    employment_type = driver.find_element(By.XPATH, value=employment_xpath)
    employment_name = employment_type.find_elements(By.TAG_NAME, value="label")
    emp_button = employment_type.find_elements(By.TAG_NAME, value="input")
    name_type_filtered = extract_names(employment_name)

    # Take seniority buttons and names
    experience_type = driver.find_element(By.XPATH, value=experience_xpath)
    seniority_name = experience_type.find_elements(By.TAG_NAME, value="label")
    sen_button = experience_type.find_elements(By.TAG_NAME, value="input")
    name_type_filtered.extend(extract_names(seniority_name))

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
                print(
                    "Selected type of employment: "
                    + name_type_filtered[choose_emp - 1]
                    + "\n"
                )
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
        print("Choose experience type: ")
        try:
            choose_sen = int(input())
            if choose_sen in range(1, 6):
                sen_button[choose_sen - 1].click()
                print(
                    "Selected type of experience: "
                    + name_type_filtered[choose_sen + 4]
                    + "\n"
                )
                driver.find_element(
                    By.CSS_SELECTOR, value=apply_settings_button
                ).click()
                break
            else:
                print("Incorrect choice")

        except ValueError:
            print("Incorrect choice")


def choose_location():
    location_button_xpath = "//button[@name='location_filter_button']"
    poland_locations_xpath = "//*[@ id='filters-location-modal-form']/div/div[3]/div"
    other_locations_poland_xpath = (
        "//*[@id='filters-location-modal-form']/div/div[5]/div"
    )
    top_world_locations_xpath = "//*[@id='filters-location-modal-form']/div/div[4]/div"
    show_offers_button = "//button[@type='submit']"

    # CLICK BUTTONS
    driver.find_element(By.XPATH, value=location_button_xpath).click()
    time.sleep(0.5)

    top_poland_locations = driver.find_element(By.XPATH, value=poland_locations_xpath)
    other_locations_poland = driver.find_element(
        By.XPATH, value=other_locations_poland_xpath
    )
    top_world_locations = driver.find_element(By.XPATH, value=top_world_locations_xpath)

    locations_types = [
        "1.Top Poland locations",
        "2.Other locations Poland",
        "3.Top world locations",
    ]

    def get_location_names(value):
        xpath = ""
        if value == 1:
            xpath = top_poland_locations
        if value == 2:
            xpath = other_locations_poland
        if value == 3:
            xpath = top_world_locations

        location_names = xpath.find_elements(By.TAG_NAME, value="button")
        names = []
        for index, element in enumerate(location_names[:], start=1):
            names.append(f"{index}.{element.text}")

        for n in names:
            print(n)

        # FIX THIS  out of range

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


def get_job_offers():
    full_height_job_offers = driver.find_element(
        By.XPATH, value='//div[@data-virtuoso-scroller="true"]'
    ).size["height"]
    job_offers = driver.find_element(
        By.XPATH, value="//div[@data-test-id='virtuoso-item-list']"
    )
    scroll_page = driver.find_element(
        By.XPATH, value="//div[@data-viewport-type='window']"
    )
    job_xpath_selector = 'div[data-index="0"]'
    jobs = []  # list for scraped jobs and links
    salaries = []  # list for scraped salaries

    def scroll(px):  # function responsible for scrolling site every
        scroll_script = f"window.scrollBy(0, {px})"
        driver.execute_script(scroll_script, scroll_page)
        time.sleep(0.5)

    """
     increase_data_index function is responsible for increasing data-index div attribute in xpath selector 
     of single job offer,
     every increased index is next job offer
    """

    def increase_data_index(
        top, jobs_div_height, job_selector, job_offers_div, job_list, salary_list
    ):
        index = top
        job_offer_height = 0
        total_iterations = jobs_div_height // 68  # 68 is height of single job offer
        pbar = tqdm(total=total_iterations, colour="red")
        pbar.set_description("Scraping...", refresh=True)

        while index <= total_iterations:
            print(index)  # to check index value
            if index > 3:
                if (
                    index % 8 == 0 and index != 0
                ):  # 612 because site is scrolled with 612px
                    scroll(612)

            updated_job_selector = job_selector.replace(f"0", f"{index}")

            try:
                z_element = job_offers_div.find_element(
                    By.CSS_SELECTOR, value=updated_job_selector
                )
                job_offer_height += 68
                print(job_offer_height)  # to check height
                job_names = z_element.find_element(By.TAG_NAME, value="h2")
                link_to_job = z_element.find_element(By.TAG_NAME, value="a")
                salary_values = z_element.find_elements(By.TAG_NAME, value="span")

                job_list.append(job_names.text)
                job_list.append(link_to_job.get_attribute("href"))
                for element in salary_values:
                    salary_list.append(element.get_attribute("innerText"))

                pbar.update(1)
                if job_offer_height >= jobs_div_height:
                    return print("Scraping finished!")
                index += 1

            except NoSuchElementException:
                print("missing element")
                scroll(-800)
                continue

        pbar.close()

    print(full_height_job_offers)  # to check height
    increase_data_index(
        0, full_height_job_offers, job_xpath_selector, job_offers, jobs, salaries
    )

    if len(jobs) == 0:
        return print("No offers found!")

    salary_list_filtered = [
        salary
        for salary in salaries
        if salary.endswith("PLN") or salary == "Undisclosed Salary"
    ]

    def insert_salary_list_and_add_space(joblink_list, salary_list):
        place = 0
        for s in range(2, len(joblink_list) + len(salary_list), 3):
            joblink_list.insert(s, salary_list[place])
            place += 1

        for space in range(
            len(joblink_list) - 1, 0, -1
        ):  # adding space between offers for better visibility
            if space % 3 == 0:  # % 3 because 1 el is name, 2 el is link, 3 el is salary
                joblink_list.insert(space, " ")

    insert_salary_list_and_add_space(jobs, salary_list_filtered)

    for j in jobs:
        print(j)

    print("\nDo you want to save results in pdf file?")
    choose = int(input("1.Yes / 2.No"))
    while True:
        try:
            if choose in (1, 2):
                if choose == 1:
                    save_jobs_to_pdf(jobs, output_file)
                if choose == 2:
                    print("Back to menu...\n")
                    sleep(3)
                    return menu()
        except ValueError:
            print("Incorrect choice")
            choose = int(input("1.Yes / 2.No"))


def save_jobs_to_pdf(jobs_list, output):
    doc = SimpleDocTemplate(output, pagesize=A4)
    styles = getSampleStyleSheet()
    link_style = ParagraphStyle(
        "LinkStyle",
        parent=styles["Normal"],
        textColor=colors.purple,
        underline=1,
    )

    styles.add(link_style)
    file = []
    for item in jobs_list:
        if item == " ":
            # add empty paragraph
            file.append(Spacer(1, 12))
        else:
            # check if link
            if item.startswith("http"):
                file.append(Paragraph(item, styles["LinkStyle"]))
            else:
                file.append(Paragraph(item, styles["Normal"]))

    doc.build(file)
    print("Jobs saved in PDF!")
    print("Returning to the menu...")
    time.sleep(3)
    return menu()


def menu():
    def menu_filters():
        print("SELECT YOUR FILTERS:\n")
        print(
            "1.Choose offer type\n2.Choose technology\n3.Choose location\n"
            "4.Choose employment type and experience\n5.Back"
        )
        while True:
            try:
                choose1 = int(input("Choose: (type 1-5) "))
                if choose1 in (1, 2, 3, 4, 5):
                    if choose1 == 1:
                        choose_offer_type()
                        return menu_filters()
                    if choose1 == 2:
                        choose_tech()
                        return menu_filters()
                    if choose1 == 3:
                        choose_location()
                        return menu_filters()
                    if choose1 == 4:
                        filter_settings()
                        return menu_filters()
                    if choose1 == 5:
                        return menu()
            except ValueError:
                print("Incorrect choice!")

    print("1.SET FILTERS\n2.START SCRAPING!\n3.QUIT")

    while True:
        try:
            choose2 = int(input("Choose: (type 1-3)  "))
            if choose2 in (1, 2, 3):
                if choose2 == 1:
                    return menu_filters()
                if choose2 == 2:
                    return get_job_offers()
                if choose2 == 3:
                    return driver.quit()
        except ValueError:
            print("Incorrect choice!")


click_cookie_button()
time.sleep(0.5)
print(
    "#########################\nWELCOME TO IT JOB SCRAPER\n#########################\n"
)
menu()
