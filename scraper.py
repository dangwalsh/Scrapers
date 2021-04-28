from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import path
from os import remove
import time
import csv

def write_to_file(name, data):
    if path.exists(name):
        response = input(
            'Would you like to (R)eplace or (A)ppend?\n').upper()
        if response == 'R':
            remove(name)
        else:
            data.pop(0)
    myfile = open(name,"a")
    for row in data:      
        myfile.write(row)
    myfile.close()

def get_table_data(data, office):
    if office == 'washingtondc':
        office = office[:-2]
    links = driver.find_elements_by_css_selector(
        'table >tbody >tr >.name >div:nth-child(1) >a')
    names = driver.find_elements_by_css_selector(
        'table >tbody >tr >.name >div:nth-child(1)')
    roles = driver.find_elements_by_css_selector(
        'table >tbody >tr >.name >div:nth-child(2)')
    studios = driver.find_elements_by_css_selector(
        'table >tbody >tr >.studio')
    ids = get_ids_from_links(links)
    for n in range(len(names)):
        row = (ids[n] + ',' + 
            names[n].text + ',' + 
            roles[n].text + ',' + 
            studios[n].text + ',' +
            office.capitalize() + '\n')
        data.append(row)

def get_ids_from_links(links):
    ids = []
    for link in links:
        href = link.get_attribute('href')
        id = href[-5:]
        ids.append(id)
    return ids

def get_button_class():
    return driver.find_element_by_class_name(
        'gensler-dynamictable-last').get_attribute('class')

office = ''
offices = [
    'atlanta', 
    'baltimore', 
    'charlotte', 
    'miami', 
    'philadelphia', 
    'raleigh', 
    'tampa', 
    'washingtondc']
bad_chars = [
    ';', 
    ':', 
    '!', 
    '*', 
    ' ', 
    '.']
data = ['Id,Name,Role,Studio,Office\n']

while not office in offices:
    office = input("Please enter the office name:\n").lower()
    office = ''.join(i for i in office if not i in bad_chars)

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(
    executable_path='drivers/chromedriver', 
    options=chrome_options)
driver.get(
    'http://' + office + '.web.gensler.com/office-information')
time.sleep(3)

get_table_data(data, office)
last_button_class = get_button_class()

while not 'disabled' in last_button_class:
    driver.find_element_by_class_name(
        'gensler-dynamictable-next').click()
    time.sleep(3)
    get_table_data(data, office)
    last_button_class = get_button_class()

filename = input("Enter the path for output:\n")

write_to_file(filename, data)

driver.close()

