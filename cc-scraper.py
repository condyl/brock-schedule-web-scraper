from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

import os

from database import create_database,create_table, insert_row
from helpers.wait_for_load import wait_for_load

options = Options()
options.add_argument('--window-size=1920,1080')
options.add_argument('--headless')
options.add_argument("--log-level=3")
options.page_load_strategy = 'normal'

driver = webdriver.Chrome(options=options)
driver.get("https://brocku.ca/guides-and-timetables/timetables/")
driver.implicitly_wait(5)

actions = ActionChains(driver)

# Get the options for the type and session dropdowns
print("Getting options for type dropdowns...")
type_select_element = driver.find_element(By.ID, "type")
type_options = type_select_element.text.split("\n")
#print(type_options)
type_select = Select(type_select_element)

print("Getting options for session dropdowns...")
session_select_element = driver.find_element(By.ID, "session")
session_options = session_select_element.text.split("\n")
#print(session_options)
session_select = Select(session_select_element)

print("Getting the show programs button...")
show_programs_button_element = driver.find_element(By.ID, "list-programs")

# Select options and show programs
print("Selecting options and showing programs...")
type_select.select_by_visible_text(type_options[1])
session_select.select_by_visible_text(session_options[1])
show_programs_button_element.click()

### NOW ON "AVAILABLE PROGRAMS" PAGE ###
#print(driver.current_url)
print("Creating database and table (if not already created)...")
create_database("brocku_available_courses")
create_table("brocku_available_courses", 
             "course_times",
             ["course_code VARCHAR(9)",
                "course_type VARCHAR(10)",
                "course_days VARCHAR(10)",
                "course_time VARCHAR(20)"
             ]
            )

sleep(1) # there has to be a better way to do this
print("Getting all programs...")
lists_of_programs = driver.find_elements(By.XPATH, "//ul[@class='col']")
programs = []
for program_list in lists_of_programs:
    all_programs = program_list.find_elements(By.TAG_NAME, "li")
    for program in all_programs:
        program_text = program.find_element(By.TAG_NAME, "a").text
        programs.append(program_text)

print("Getting all program courses...")

for program in programs:

    #manually fix specific programs
    if program == "Education": program = "Education "

    #wait_for_load(driver, program)
    sleep(2.5)
    #if program == "Education": sleep(5)
    program_button = driver.find_element(By.XPATH, "//a[@data-program_full_name='{}']".format(program))
    actions.move_to_element(program_button).perform()
    driver.execute_script("arguments[0].scrollIntoView();", program_button)
    program_button.click()
    print(driver.current_url)

    driver.implicitly_wait(1.5)
    course_table = driver.find_element(By.XPATH, "//table[@class='course-table course-listing']")
    #course_table_body = course_table.find_element(By.TAG_NAME, "tbody")
    #courses = course_table_body.find_elements(By.TAG_NAME, "tr")
    courses = course_table.find_elements(By.XPATH, "//tr[contains(@class, 'course-row')]")
    for course in courses:
        arrow = course.find_element(By.CLASS_NAME, "arrow")
        
        actions.move_to_element(arrow).perform()
        driver.execute_script("arguments[0].scrollIntoView();", arrow)
        arrow.click()
        sleep(3)
        
        course_code = course.find_element(By.CLASS_NAME, "course-code").text.strip()
        course_type = course.find_element(By.CLASS_NAME, "type").text.strip()
        course_info = course.find_element(By.CLASS_NAME, "data").find_element(By.CLASS_NAME, "course-details-data")
        course_description = course_info.find_element(By.CLASS_NAME, "description")
        course_vitals = course_info.find_element(By.CLASS_NAME, "vitals").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")

        course_name = course.find_element(By.CLASS_NAME, "title").text.strip()
        course_description_text = course_description.find_element(By.CLASS_NAME, "page-intro").text
        active_days = []
        possible_days = []
        for vital in course_vitals:
            if "Duration" in vital.text: course_duration = vital.text
            if "Time" in vital.text: course_time = vital.text
            if "Section" in vital.text: course_section = vital.text
            if "Instructor" in vital.text: course_instructor = vital.text
            if "S M T W T F S" in vital.text: 
                possible_days = vital.find_elements(By.TAG_NAME, "th")
                active_days = vital.find_elements(By.CLASS_NAME, "active")

        if (course_type == "ASY"): course_time = "Time: Asynchronous"
        if (course_type == "PRO"): course_time = "Time: Project Course"

        for day in possible_days:
            if (day in active_days): active_days.append(day.text)

        course_days = ""
        for i in range(len(possible_days)):
            for day in active_days:
                if day == possible_days[i]:
                    if (i == 4): 
                        course_days += "R "
                    else:
                        course_days += day.text + " "

        print(course_code, course_type)
        insert_row("brocku_available_courses", "course_times", 
                ["course_code", "course_type", "course_days", "course_time"],
                [course_code, course_type, course_days.strip(), course_time]
                )

    #close course
    actions.move_to_element(arrow).perform()
    driver.execute_script("arguments[0].scrollIntoView();", arrow)
    arrow.click()
    sleep(0.5)


    sleep(0.5)
    driver.execute_script("arguments[0].scrollIntoView();", show_programs_button_element)
    show_programs_button_element.click()

#program = "Computer Science"

    

    

