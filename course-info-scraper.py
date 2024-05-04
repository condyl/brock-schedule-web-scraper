from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re

import os

from database import create_database, create_table, insert_row
from helpers.wait_for_load import wait_for_load

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.page_load_strategy = "normal"

driver = webdriver.Chrome(options=options)
driver.get("https://brocku.ca/webcal/2024/undergrad")
driver.implicitly_wait(5)

actions = ActionChains(driver)

wait = WebDriverWait(driver, 10)

exclude_texts = [
    "How to use this Calendar",
    "Disclaimer",
    "Mission Statement",
    "Academic Regulations and University Policies",
    "Code of Conduct",
    "Academic Computing Information",
    "Undergraduate Sessional Dates",
    "Admissions",
    "Academic Bridging",
    "Fees",
    "Scholarships, Bursaries, Awards and Financial Assistance",
    "Degrees, Certificates, Micro-Certificates and Minors",
    "Co-operative Programs",
    "B.A., B.Sc., General Degrees",
    "International Study and Exchange",
    "University Structure",
    "Faculty and Librarians",
    "Emeriti",
    "Faculty Distinction",
    "Course Anatomy and Glossary of Terms",
]

types_of_pads = [
    "calprepad",
    "calitalicpad"
]

number_of_credits = [
    "five",
    "four and one-half",
    "four",
    "three and one-half",
    "three",
    "two and one-half",
    "two",
    "one and one-half",
    "one",
    "one-half",
]

types_of_credits = [
    "social sciences context",
    "humanities context",
    "science context",
    "elective"
]

xpathquery = "//span[contains(@class, 'contenttitle')]/a["
for exclude_text in exclude_texts:
    xpathquery += "not(contains(text(), '" + exclude_text + "')) and "
xpathquery = xpathquery[:-5]
xpathquery += "]"

programs = driver.find_elements(By.XPATH, xpathquery)

program_names = []
for program in programs:
    program_names.append(program.text)

program_names = [program_names[0], program_names[1]]

for program in program_names:
    program_button = driver.find_element(By.PARTIAL_LINK_TEXT, program)

    actions.move_to_element(program_button).perform()
    driver.execute_script("arguments[0].scrollIntoView();", program_button)
    program_button.click()
    print(driver.current_url)
    sleep(2)

    table = driver.find_element(By.ID, "calendarcontent")
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    for i in range(len(rows)):
        if i % 2 == 0:
            if "Program Note" in rows[i].text:
                program_note = [rows[i].text, rows[i + 1].text]
                
        if "Year 1" in rows[i].text and "." not in rows[i].text:

            table_data = rows[i].find_element(By.TAG_NAME, "td")

            years_data = table_data.find_elements(By.CLASS_NAME, "webcallist")

            for year in years_data:
                #print("NEW YEAR ------------------------------------------------------")
                specific_year = year.find_element(By.TAG_NAME, "tbody")
                dot_jots = specific_year.find_elements(By.TAG_NAME, "tr")
                for dot_jot in dot_jots:
                    dot_jot_element = dot_jot.find_elements(By.TAG_NAME, "td")[1]
                    dot_jot_text = dot_jot_element.text
                    dot_jot_inner_html = dot_jot_element.get_attribute("innerHTML")
                    #print(dot_jot_text)

                    for credit_number in number_of_credits:
                        if credit_number in dot_jot_text.lower():
                            required_credits = credit_number
                            #print(credit_number + " from:")
                            break

                    required_courses = []
                    result = re.split('(from)|;|(or)', dot_jot_text)
                    if "from" in result:
                        result = result[result.index("from") + 1:]
                    while "or" in result: result.remove("or")
                    while ' ' in result: result.remove(' ')
                    result = list(filter(None, result))
                    for i in range(len(result)):
                        result[i] = result[i].strip()

                    for i in range(len(result)):
                        result[i] = result[i].split(", ")
                    

                    print(result)



                    
                    





#                for dot_jot in dot_jots:
#                    print("NEW DOT JOT ------------------------------------------------------")
#                    dot_jot_text = dot_jot.find_elements(By.TAG_NAME, "td")[1].text
#
#                    # how many credits from list
#                    for credit_number in number_of_credits:
#                        if credit_number in dot_jot_text.lower():
#                            print(credit_number + " from:")
#                            break
#
#                    credit_num = ""
#                    # type of credit
#                    for credit_type in types_of_credits:
#                        if credit_type in dot_jot_text.lower():
#                            credit_num = credit_type
#                            print(credit_num)
#                            break
#                    
#
#                    if (credit_num == ""):
#                        links = dot_jot.find_elements(By.TAG_NAME, "a")
#                        for link in links:
#                            print(link.get_attribute("href"))
             
            

    driver.get("https://brocku.ca/webcal/2024/undergrad")
    sleep(2)
