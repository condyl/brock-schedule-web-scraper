from helpers.database import query
import itertools

courses = ["ASTR 1P02","COSC 2P13","COSC 3P32","COSC 3P99","STAT 1P98","COSC 2P03"]

times = []

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
        try: # if we can append to the list --> it exists
            module_counts[course_option[2][:3]].append(course_option)
        except: # if we can't append to the list --> it doesn't exist --> create it
            module_counts[course_option[2][:3]] = [course_option]

    # get all possible combinations of course options
    options = list(itertools.product(*module_counts.values())) 
    
    times.append(options)

print("\nTIMES: ")
# get all possible combinations of course options for all courses
valid_times = []
all_times = list(itertools.product(*times)) 
for time in all_times:
    #print(time)
    days = {
        "M": [],
        "T": [],
        "W": [],
        "R": [],
        "F": []
    }
    for course in time:
        for course_option in course:
            #print(course_option[4])
            if "M" in course_option[3]: days["M"].append([int(course_option[4][:4].strip()), int(course_option[4][-4:].strip())])
            if "T" in course_option[3]: days["T"].append([int(course_option[4][:4].strip()), int(course_option[4][-4:].strip())])
            if "W" in course_option[3]: days["W"].append([int(course_option[4][:4].strip()), int(course_option[4][-4:].strip())])
            if "R" in course_option[3]: days["R"].append([int(course_option[4][:4].strip()), int(course_option[4][-4:].strip())])
            if "F" in course_option[3]: days["F"].append([int(course_option[4][:4].strip()), int(course_option[4][-4:].strip())])

    valid = True
    for day in days:
        days[day] = sorted(days[day])
        for i in range(len(days[day]) - 1):
            if days[day][i][1] > days[day][i + 1][0]:
                valid = False
        
    if valid:
        valid_times.append(time)
    print(days)


for v in valid_times:
    print("\n")
    for course in v:
        for module in course:
            print(module)






    

