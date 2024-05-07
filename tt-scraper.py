from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time

import os
from datetime import datetime

from helpers.database import create_database,create_table, insert_row

start_time = time()

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
             ["id INT AUTO_INCREMENT PRIMARY KEY",
                "course_code VARCHAR(9)",
                "course_name VARCHAR(100)",
                "course_type VARCHAR(10)",
                "course_days VARCHAR(10)",
                "course_start_time TIME",
                "course_end_time TIME",
                "course_start_date DATE",
                "course_end_date DATE",
                "course_instructor VARCHAR(100)"
             ]
            )

sleep(1) # there has to be a better way to do this()
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
    sleep(5)

    if program == "Education": program_button = driver.find_element(By.XPATH, "//a[@data-program_full_name='Education ']")
    else: program_button = driver.find_element(By.XPATH, "//a[@data-program_full_name='{}']".format(program))

    actions.move_to_element(program_button).perform()
    driver.execute_script("arguments[0].scrollIntoView();", program_button)
    program_button.click()
    print(driver.current_url)

    sleep(5)
    try:
        course_table = driver.find_element(By.XPATH, "//table[@class='course-table course-listing']")
        courses = course_table.find_elements(By.XPATH, "//tr[contains(@class, 'course-row')]")
    except:
        courses = []
    for course in courses:
        st_course = time()
        arrow = course.find_element(By.CLASS_NAME, "arrow")
        
        actions.move_to_element(arrow).perform()
        driver.execute_script("arguments[0].scrollIntoView();", arrow)
        arrow.click()
        sleep(5)
        
        course_code = course.find_element(By.CLASS_NAME, "course-code").text.strip()
        course_type = course.find_element(By.CLASS_NAME, "type").text.strip()
        course_info = course.find_element(By.CLASS_NAME, "data").find_element(By.CLASS_NAME, "course-details-data")
        course_description = course_info.find_element(By.CLASS_NAME, "description")
        course_vitals = course_info.find_element(By.CLASS_NAME, "vitals").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")

        course_name = course.find_element(By.CLASS_NAME, "title").text.strip()
        active_days = []
        possible_days = []
        for vital in course_vitals:
            if "Duration" in vital.text: 
                course_duration = vital.text[10:].split(" to ")
                course_start_date = datetime.strptime(course_duration[0], '%b %d, %Y').strftime('%Y-%m-%d')
                course_end_date = datetime.strptime(course_duration[1], '%b %d, %Y').strftime('%Y-%m-%d')
            if "Time" in vital.text: 
                course_time = vital.text[6:]
                course_start_time = course_time[:4].strip()+"00"
                course_end_time = course_time[-4:].strip()+"00"
            if "Section" in vital.text: course_section = vital.text[8:]
            if "Instructor" in vital.text: course_instructor = vital.text[12:]
            if "S M T W T F S" in vital.text: 
                possible_days = vital.find_elements(By.TAG_NAME, "th")
                active_days = vital.find_elements(By.CLASS_NAME, "active")
        
        if "Time" not in course_info.find_element(By.CLASS_NAME, "vitals").find_element(By.TAG_NAME, "ul").text:
            course_start_date = "000000"
            course_end_date = "000000"
        if "Duration" not in course_info.find_element(By.CLASS_NAME, "vitals").find_element(By.TAG_NAME, "ul").text:
            course_duration = ""
        if "Section" not in course_info.find_element(By.CLASS_NAME, "vitals").find_element(By.TAG_NAME, "ul").text:
            course_section = ""
        if "Instructor" not in course_info.find_element(By.CLASS_NAME, "vitals").find_element(By.TAG_NAME, "ul").text:
            course_instructor = ""
        if "S M T W T F S" not in course_info.find_element(By.CLASS_NAME, "vitals").find_element(By.TAG_NAME, "ul").text:
            course_days = ""

        if (course_type == "ASY"): course_time = ""
        if (course_type == "PRO"): course_time = ""
        if (course_type == "FLD"): course_time = ""
        if (course_type == "IFT"): course_time = ""
        if (course_type == "INT"): course_time = ""
        if (course_type == "ONM"): course_time = ""

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

        insert_row("brocku_available_courses", "course_times", 
                ["course_code", "course_name", "course_type", "course_days", "course_start_time", "course_end_time", "course_start_date", "course_end_date", "course_instructor"],
                [course_code, course_name, course_type, course_days.strip(), course_start_time, course_end_time, course_start_date, course_end_date, course_instructor]
                )

        #close course
        actions.move_to_element(arrow).perform()
        driver.execute_script("arguments[0].scrollIntoView();", arrow)
        arrow.click()
        sleep(3)
        et_course = time()
        print("Course: ", course_code, course_type, "| Time: ", str(et_course - st_course)[:6], " seconds")

    driver.execute_script("arguments[0].scrollIntoView();", show_programs_button_element)
    show_programs_button_element.click()

end_time = time()

elapsed_time = str(end_time - start_time)[:6]
print("Elapsed time: ", elapsed_time, " seconds")
