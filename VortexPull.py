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
from selenium.webdriver.support.select import Select

"""
using a webdriver, obtains the HTML for any given webpage. 
login restricted sites will only return login pages and will have to be dealt
with accordingly.
"""
def htmlGetter(driver, URL):
    driver.get(URL)
    #select = Select()
    
    # Problem line, need to fix item selection on dropdown.
    driver.find_element("id", "ajax_recordsdates").click()
    
    Select(driver.find_element("id", "ajax_recordsdates")).select_by_visible_text("Today")
    delay = 2
    try:
        ElemPresent = EC.presence_of_element_located((By.ID, 'table'))
        myElem = WebDriverWait(driver, delay).until(ElemPresent)
    except TimeoutException:
        print("")

    return driver.page_source

"""
Formats a table from vortex into python usable data (a list)
Should format all relevant html if everything is input for that day
"""
def dataFormatter(soup):
    try:
        table = soup.find('table', class_="datatable") # finds databable in vortex
        datas = [] # empty list to hold table entries
        
        # O(n^2) since airlines is a finite length
        for tr in table.select('tbody tr'):
            s = []
            for i in tr.select('td'):
                s.append(i.text.strip())
            datas.append(s)
        return datas

    except AttributeError as e:
        raise ValueError("No valid table found")

"""
Generates an operations log in the following format
# ['Landed', '9:46', 'AM', '9:55', 'AM', 'WO160', 'Hamilton(YHM)', 'B738', 'C-GYSD', 'Swoop']
    #       Airline / Flt: XXX-XXX / Reg: XXX / Bags Off: XXX / Bags On: XXX / 
    #       Flight Notes: 
    #       Arrival Time: XXX
    #       Scheduled Arr: XXX
    #       Departure Time: XXX
    #       Scheduled Dep: XXX
"""
def makeOps(airline, inbound, outbound, reg, arrTime, depTime):
    return [airline, " / Flt: ", inbound, "-", outbound, 
            " / Reg: ", reg, 
            " / Bags Off: / Bags On: / ", 
            "\nFlight notes: ", 
            "\nArrival Time: ", arrTime,
            "\nDeparture Time: ", depTime,]
    



# browser setup
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('/home/false/chromedriver', chrome_options=chrome_options)

# https://stackoverflow.com/questions/13960326/how-can-i-parse-a-website-using-selenium-and-beautifulsoup-in-python


# https://www.thepythoncode.com/article/automate-login-to-websites-using-selenium-in-python
print("Please provide username")
uname = input()
print("Please provide password")
pword = input()

URL = "https://execaviation.vortexcms.com/vortex/flights.php"


# login code
driver.get("https://execaviation.vortexcms.com/vortex/")
driver.find_element("id", "username").send_keys(uname)
driver.find_element("id", "password").send_keys(pword)
driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div/div/form/div[1]").click()





vortexHTML = htmlGetter(driver, URL)

vortexTable = BeautifulSoup(vortexHTML, features="html5lib")


flights = dataFormatter(vortexTable)
flights.pop(0)
flights.pop(0)

# print("Arriving flights")
opsLog = []

for i in flights:
    #print(i)
    opsLog.append(makeOps(i[2], i[4], i[12], i[9], i[6], i[14]))

# printing formatted ops log
print("\n\n\nRC: \nLeads: \nStaff: \n\nStaff notes: \n\nEquipment notes: \n\n")

for i in opsLog:
    s = ""
    for j in i:
        s += j
    print(s)
    print()


