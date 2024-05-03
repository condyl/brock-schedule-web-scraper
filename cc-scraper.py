from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

import os

from database import create_database,create_table
from helpers.wait_for_load import wait_for_load

options = Options()
options.add_argument('--window-size=1920,1080')
options.add_argument('--headless')
options.add_argument("--log-level=3")
options.page_load_strategy = 'normal'

driver = webdriver.Chrome(options=options)
driver.get("https://brocku.ca/guides-and-timetables/timetables/")

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
             ["course_code VARCHAR(4)",
                "course_number VARCHAR(4)",
                "course_type VARCHAR(10)",
                "course_days VARCHAR(10)",
                "course_time VARCHAR(10)"
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

#for program in programs:
#
#    #manually fix specific programs
#    if program == "Education": program = "Education "
#
#    #wait_for_load(driver, program)
#    sleep(2.5)
#    #if program == "Education": sleep(5)
#    program_button = driver.find_element(By.XPATH, "//a[@data-program_full_name='{}']".format(program))
#    actions.move_to_element(program_button).perform()
#    driver.execute_script("arguments[0].scrollIntoView();", program_button)
#    program_button.click()
#    print(driver.current_url)
#    sleep(0.5)
#    driver.execute_script("arguments[0].scrollIntoView();", show_programs_button_element)
#    show_programs_button_element.click()

program = "Computer Science"
program_button = driver.find_element(By.XPATH, "//a[@data-program_full_name='{}']".format(program))
actions.move_to_element(program_button).perform()
driver.execute_script("arguments[0].scrollIntoView();", program_button)
program_button.click()
print(driver.current_url)

sleep(1.5)
course_table = driver.find_elements(By.XPATH, "//table[@class='course-table course-listing']")
print(course_table)
course_table_body = course_table.find_element(By.TAG_NAME, "tbody")
print(course_table_body)




sleep(0.5)
driver.execute_script("arguments[0].scrollIntoView();", show_programs_button_element)
show_programs_button_element.click()

    

