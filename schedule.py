from helpers.database import query
import itertools

courses = ["COSC 1P02"]

for course in courses:
    course_options = query("SELECT * FROM `course_times_spring_2024` WHERE `course_code` LIKE '{}'".format(course), "brocku_available_courses")
    #print(course_options)
    modules = []
    module_counts = {}
    # get all modules needed for course & how many options there are
    for course_option in course_options:
        if course_option[2][:3] not in modules:
            modules.append(course_option[2][:3])

        # separate course options by module
        try: 
            module_counts[course_option[2][:3]].append(course_option)
        except: 
            module_counts[course_option[2][:3]] = [course_option]

    options = list(itertools.product(*module_counts.values())) # get all possible combinations of course options

    #print(modules)
    #for m in module_counts:
    #    print(module_counts[m])

