import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def htmlGetter(driver, URL):
    driver.get(URL)
    delay = 1
    try:
        ElemPresent = EC.presence_of_element_located((By.ID, 'table'))
        myElem = WebDriverWait(driver, delay).until(ElemPresent)
    except TimeoutException:
        print("")

    return driver.page_source


def dataFormatter(soup):
    try:
        table = soup.find('table')

        heads = []
        for i in table.select('thead th'):
            heads.append(i.text.strip())
        #print(heads)

        datas = []
        # n^2 since airlines is a finite length
        for tr in table.select('tbody tr'):
            for i in tr.select('td'):
                for n in AIRLINES:
                    if (n in i.text.strip()):
                        s = i.text.strip()
                        location = s.find("-")
                        s = s[:location - 1] + " " + s[location - 1:]
                        s = s[:location + 6] + " " + s[location + 6:]
                        s = s.split()
                        if "Air" in s:
                            s.remove("Air")
                        elif "Airlines" in s:
                            s.remove("Airlines")
                        s = s[:len(s) - 1]
                        if "Sunwing" in s[-1]:
                            s[-1] = "Sunwing"

                        if (len(s) > 3):
                            datas.append(s)

        return datas

    except AttributeError as e:
        raise ValueError("No valid table found")

# browser setup
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('/home/false/chromedriver', chrome_options=chrome_options)

# https://stackoverflow.com/questions/13960326/how-can-i-parse-a-website-using-selenium-and-beautifulsoup-in-python

AIRLINES = ["Porter Airlines", "Swoop", "Sunwing Airlines", "Lynx Air"]

arrivalURL = "https://www.flightradar24.com/data/airports/yhz/arrivals"
departureURL = "https://www.flightradar24.com/data/airports/yhz/departures"
nextFlight = "https://www.flightradar24.com/data/aircraft/c-gkqf"

# driver.find_element(By.LINK_TEXT("Load earlier flights")).click()
arrivalHTML = htmlGetter(driver, arrivalURL)
departureHTML = htmlGetter(driver, departureURL)

soupArrival = BeautifulSoup(arrivalHTML, features="html5lib")
soupDeparture = BeautifulSoup(departureHTML, features="html5lib")

arrivals = dataFormatter(soupArrival)
departures = dataFormatter(soupDeparture)

# print("Arriving flights")
opsLog = []

for i in arrivals:
    if "Estimated" in i or "Arrived" in i:
        if "Sunwing" in i[-1]:
            opsLog.append([i[-1], " / ", i[5][2:], "-", "$", " / ", "^", " / Onload: / Offload: / ", "\nFlight notes: \n"])
        else:
            opsLog.append([i[-1], " / ", i[5][2:], "-", "RON", " / ", i[-2], " / Onload: / Offload: / ", "\nFlight notes: \n"])
    elif "Scheduled" in i:
        if "Sunwing" in i[-1]:
            opsLog.append([i[-1], " / ", i[3][2:], "-", "$", " / ", "^", " / Onload: / Offload: / ", "\nFlight notes: \n"])
        else:
            opsLog.append([i[-1], " / ", i[3][2:], "-", "RON", " / ", i[-2], " / Onload: / Offload: / ", "\nFlight notes: \n"])

for i in opsLog:
    reg = i[6]
    for j in departures:
        for k in j:
            if reg in k:
                if "Estimated" in j[0] or "Arrived" in j[0]:
                    i[4] = j[6][2:]
                    departures.remove(j)
                    break
                elif "Scheduled" in j[0]:
                    i[4] = j[3][2:]
                    departures.remove(j)
                    break
                elif "Sunwing" in j[-1]:
                    i[4] = j[6][2:]
                    departures.remove(j)
                    break



"""
for i in arrivals:
    print(i)
"""

print("\n\nOperations log\nRC: \nLeads: \nStaff: \n\nEquipment notes: \n\n")
for i in opsLog:
    s = ""
    for j in i:
        s += j
    print(s)

"""
print("\n\nDeparting flights")
for i in departures:
    print(i)
"""
