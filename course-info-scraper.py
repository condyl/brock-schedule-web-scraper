from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re
import json

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

create_database("brocku_available_courses")
create_table("brocku_available_courses", 
             "program_requirements",
             ["program_code VARCHAR(4)",
                "program_name VARCHAR(255)",
                "program_style VARCHAR(255)",
                "year_1_requirements TEXT(10000)",
                "year_1_credit_amount INT(2)",
                "year_2_requirements TEXT(10000)",
                "year_2_credit_amount INT(2)",
                "year_3_requirements TEXT(10000)",
                "year_3_credit_amount INT(2)",
                "year_4_requirements TEXT(10000)",
                "year_4_credit_amount INT(2)",
                "year_5_requirements TEXT(10000)",
                "year_5_credit_amount INT(2)",
                "year_6_requirements TEXT(10000)",
                "year_6_credit_amount INT(2)"
             ]
            )

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
    ["five",5],
    ["four and one-half",4.5],
    ["four",4],
    ["three and one-half",3.5],
    ["three",3],
    ["two and one-half",2.5],
    ["two",2],
    ["one and one-half",1.5],
    ["one",1],
    ["one-half",0.5],
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

#program_names = [program_names[0], program_names[1]]
program_names = ["Computer Science"]

for program in program_names:
    program_button = driver.find_element(By.PARTIAL_LINK_TEXT, program)
    program_code = program_button.get_attribute("href").split("/")
    program_code = program_code[-1][:4].upper()

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

            program_style = rows[i-1].text

            required_courses = []
            required_credits = []

            table_data = rows[i].find_element(By.TAG_NAME, "td")

            years_data = table_data.find_elements(By.CLASS_NAME, "webcallist")

            for year in years_data:
                #print("NEW YEAR ------------------------------------------------------")
                specific_year = year.find_element(By.TAG_NAME, "tbody")
                dot_jots = specific_year.find_elements(By.TAG_NAME, "tr")
                required_courses_yearly = []
                required_credits_yearly = []
                for dot_jot in dot_jots:
                    dot_jot_element = dot_jot.find_elements(By.TAG_NAME, "td")[1]
                    dot_jot_text = dot_jot_element.text
                    dot_jot_inner_html = dot_jot_element.get_attribute("innerHTML")
                    #print(dot_jot_text)

                    added_credit_number = False
                    for credit_number in number_of_credits:
                        if credit_number[0] in dot_jot_text.lower():
                            required_credits_yearly.append(credit_number[1])
                            added_credit_number = True
                            #print(credit_number + " from:")
                            break
                    if not added_credit_number: required_credits_yearly.append("ALL")
                    
                    if "social sciences context" in dot_jot_text.lower(): required_courses_yearly.append("SSCC")
                    elif "humanities context" in dot_jot_text.lower(): required_courses_yearly.append("HUCC")
                    elif "science context" in dot_jot_text.lower(): required_courses_yearly.append("SCCC")
                    elif "elective" in dot_jot_text.lower(): required_courses_yearly.append("ELEC")
                    else: 
                        result = re.split('(from)|;|(or)', dot_jot_text)
                        if "from" in result:
                            result = result[result.index("from") + 1:]
                        while "or" in result: result.remove("or")
                        result = list(filter(None, result))
                        result = [ele for ele in result if ele.strip()]
                        for i in range(len(result)):
                            result[i] = result[i].strip()

                        for i in range(len(result)):
                            result[i] = list(filter(None,re.split(',|( and)',result[i])))
                            while " and" in result[i]: result[i].remove(" and")
                            current_course_prefix = ""
                            for j in range(len(result[i])):
                                result[i][j] = result[i][j].strip()
                                if (result[i][j][:4].isupper() and result[i][j][:4].isalpha()): current_course_prefix = result[i][j][:4]
                                else: result[i][j] = current_course_prefix + " " + result[i][j]
                                result[i][j] = result[i][j].strip()

                        required_courses_yearly.append(result)
                required_courses.append(required_courses_yearly)
                required_credits.append(required_credits_yearly)
                
            required_courses_json = []
            required_credits_json = []
            for i in range(len(required_courses)):
                required_courses_json.append(json.dumps(required_courses[i]))
                required_credits_json.append(json.dumps(required_credits[i]))
            print(len(required_courses))
            if len(required_courses) == 3: 
                insert_row("brocku_available_courses", "program_requirements", 
                        ["program_code", "program_name", "program_style", "year_1_requirements", "year_1_credit_amount",  "year_2_requirements", "year_2_credit_amount", "year_3_credit_amount", "year_3_requirements"],
                        [program_code, program, program_style, required_courses_json[0], required_credits_json[0], required_courses_json[1], required_credits_json[1], required_courses_json[2], required_credits_json[2]]
                        )
            elif len(required_courses) == 4:
                insert_row("brocku_available_courses", "program_requirements", 
                        ["program_code", "program_name", "program_style", "year_1_requirements", "year_1_credit_amount",  "year_2_requirements", "year_2_credit_amount", "year_3_requirements", "year_3_credit_amount", "year_4_requirements", "year_4_credit_amount"],
                        [program_code, program, program_style, required_courses_json[0], required_credits_json[0], required_courses_json[1], required_credits_json[1], required_courses_json[2], required_credits_json[2], required_courses_json[3], required_credits_json[3]]
                        )
            elif len(required_courses) == 5:
                insert_row("brocku_available_courses", "program_requirements", 
                        ["program_code", "program_name", "program_style", "year_1_requirements", "year_1_credit_amount",  "year_2_requirements", "year_2_credit_amount", "year_3_requirements", "year_3_credit_amount", "year_4_requirements", "year_4_credit_amount", "year_5_requirements", "year_5_credit_amount"],
                        [program_code, program, program_style, required_courses_json[0], required_credits_json[0], required_courses_json[1], required_credits_json[1], required_courses_json[2], required_credits_json[2], required_courses_json[3], required_credits_json[3], required_courses_json[4], required_credits_json[4]]
                        )
            elif len(required_courses) == 6:
                insert_row("brocku_available_courses", "program_requirements", 
                        ["program_code", "program_name", "program_style", "year_1_requirements", "year_1_credit_amount",  "year_2_requirements", "year_2_credit_amount", "year_3_requirements", "year_3_credit_amount", "year_4_requirements", "year_4_credit_amount", "year_5_requirements", "year_5_credit_amount", "year_6_requirements", "year_6_credit_amount"],
                        [program_code, program, program_style, required_courses_json[0], required_credits_json[0], required_courses_json[1], required_credits_json[1], required_courses_json[2], required_credits_json[2], required_courses_json[3], required_credits_json[3], required_courses_json[4], required_credits_json[4], required_courses_json[5], required_credits_json[5]]
                        )

                    
                    





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
