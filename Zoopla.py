# pluralsight.py
import time
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from xlwt import Workbook
import xlrd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent


def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    ua = UserAgent()
    userAgent = ua.random                                     #THIS IS FAKE AGENT IT WILL GIVE YOU NEW AGENT EVERYTIME
    print(userAgent)
    # add the argument and make the browser Headless.
   # chrome_options.add_argument("--headless")                    if you don't want to see the display on chrome just uncomment this


    chrome_options.add_argument(f'user-agent={userAgent}')
    #COMMENT THE LINE OF CODE BELOW IF YOU WANT NEW RANDOM AGENT EVERYTIME INSTEAD OF SAME AGENT EVERYTIME
   # chrome_options.add_argument(
    #    '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
    # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
    # For linux/Mac
   # driver = webdriver.Chrome(options = chrome_options)
    # For windows
    #chrome_options.add_argument("--log-level=3")
    #chrome_options.add_argument("--disable-notifications")
    #chrome_options.add_argument("--disable-infobars")
    #chrome_options.add_argument("start-maximized")
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
    return driver


def getCourses(driver, search_keyword):
    #driver.get(f"https://google.com")
    #time.sleep(4)
    #driver.find_element_by_xpath('//*[@id="CookiePolicyClose"]').click()
    #WebDriverWait(driver, 200).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'#topMenu > li:nth-child(1) > a.category-link')))
    #driver.find_element_by_xpath('//*[@id="ProductCardTemplate"]/div[8]/div[1]/div/div[2]/a').click()
    #search = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    #search.send_keys("Zoopla uk")
    #search.send_keys(Keys.ENTER)
    #WebDriverWait(driver, 3)
    #driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div[1]/a/h3').click()
    driver.get("https://www.zoopla.co.uk")
    WebDriverWait(driver, 200).until(
        expected_conditions.visibility_of_element_located((By.CLASS_NAME, "ui-button-secondary")))
    driver.find_element_by_class_name("ui-button-secondary").click()
     #def write_json(data, filename='OLX.json'):
     #  with open(filename, 'w') as f:
      #   json.dump(data, f, indent=4)

    #with open('OLX.json') as json_file:
     #  data = json.load(json_file)
                                                      #IF YOU EVER WANT TO CONVERT CODE TO JSON FILE UNCOMMENT CODE ABOVE

    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1',cell_overwrite_ok=True)
    print(" WORKSHEET CREATED SUCCESSFULLY!")
    # INITIALIZING THE COLOUMN NAMES NOW
    sheet1.write(0, 0, "Property Name")
    sheet1.write(0, 1, "Property Location")
    sheet1.write(0, 2, "Agent Name")
    sheet1.write(0, 3, "Agent Link")
    sheet1.write(0, 4, "Agent Phone")
    sheet1.write(0, 5, "Property Link")
    sheet1.write(0, 6, "Property Price")
    sheet1.write(0, 7, "Avg Market Price")
    sheet1.write(0, 8, "Market Place")
    wb.save('ZOOPLANEW.xls')
    WebDriverWait(driver, 20).until(
       expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="search-input-location"]')))
    search = driver.find_element_by_xpath('//*[@id="search-input-location"]')
    search.send_keys("Edinburgh")
   # for index in range(len(select.options)):
    #select.select_by_index(2)
    driver.find_element_by_xpath('//*[@id="search-submit"]').click()
    pon=1
    mi = 1
    for puy in range(41):
        print("**************PAGE: ", pon)
        pon=pon+1
        plot = driver.current_url
        print("MAIN PAGE LINK: ",plot)
        WebDriverWait(driver, 2)
        mainlink = "https://www.zoopla.co.uk"
        country = " ,Edinburgh"
        pagesoup = BeautifulSoup(driver.page_source, "html.parser")
        com = pagesoup.find("ul", {"class": "listing-results clearfix js-gtm-list"})
        container = com.findAll("li", {"class": "srp clearfix"})
        for contain in container:
            pan = contain.find("div", {"class": "listing-results-right clearfix"})
            link = contain.find('a', {"class": "listing-results-price text-price"}).get('href')
            link = mainlink + link
            print("PROPERTY LINK: " , link)
            driver.get(link)
            WebDriverWait(driver, 10)
            lice = driver.find_element_by_css_selector('#dp-sticky-element > article > div > p').text
            print("PROPERTY PRICE: " , lice)
            price = lice.replace('£', "")
            price = price.replace(',', "")
            place = driver.find_elements_by_class_name("ui-breadcrumbs__link")
            place = place[len(place) - 1].text
            print("LOCATION: " , place)
            place = place + country
            WebDriverWait(driver, 20).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,
                                                                   "#dp-sticky-element > article > h1")))
            try:
                property = driver.find_element_by_css_selector("#dp-sticky-element > article > h1").text
                location = driver.find_element_by_css_selector("#dp-sticky-element > article > h2").text
                agent = driver.find_element_by_css_selector(
                    "#dp-sticky-element > div > div.ui-agent > a > div.ui-agent__text > h4").text
                agentlink = driver.find_element_by_css_selector(
                    "#dp-sticky-element > div > div.ui-agent > a").get_attribute('href')
                phone = driver.find_element_by_css_selector(
                    "#dp-sticky-element > div > div.ui-agent > p > a").get_attribute('href')
                print("Property Name: ", property)
                print("Address: ", location)
                print("Agent: ", agent)
                print("Link Of Agent: ", agentlink)
                phone = phone.replace("tel:", "")
                print("Phone Of Agent: ", phone)
                sheet1.write(mi, 0, property)
                sheet1.write(mi, 1, location)
                sheet1.write(mi, 2, agent)
                sheet1.write(mi, 3, agentlink)
                sheet1.write(mi, 4, phone)
                sheet1.write(mi, 5, link)
                sheet1.write(mi, 6, price)
                sheet1.write(mi, 8, place)
                wb.save('ZOOPLANEW.xls')
                mi = mi + 1
            except Exception:
                print("UNABLE TO RETRIEVE")
                pass
            print("-------NEXT ENTRY--------")
        print("GOING TO MAIN PAGE LINK: ", plot)
        driver.get(plot)
        pon=str(pon)
        driver.find_element_by_link_text(pon).click()
        pon=int(pon)





# create the driver object.
search_keyword = "Web Scraping"
driver= configure_driver()
getCourses(driver, search_keyword)
# close the driver.
driver.close()















