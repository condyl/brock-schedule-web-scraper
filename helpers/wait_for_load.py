def wait_for_load(driver, text):
    from time import sleep

    count = 1
    # Wait for the page to load
    print(driver.execute_script("return document.querySelectorAll('[data-program_full_name=\"" + text + "\"]')[0] === null"))
    while driver.execute_script("return document.querySelectorAll('[data-program_full_name=\"" + text + "\"]')[0] === null") != False:
        print("attempt "+str(count)+": "+str(driver.execute_script("return document.querySelectorAll('[data-program_full_name=\"" + text + "\"]')[0] === null")))
        count += 1
        sleep(0.5)