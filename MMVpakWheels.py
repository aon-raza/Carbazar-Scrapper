import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.add_argument("--headless")
# driver = webdriver.Chrome("C:/Users/Syed Aon Raza/PycharmProjects/numberExtractor/chromedriver.exe", 1, options)

driver = webdriver.Chrome("C:/Users/Syed Aon Raza/PycharmProjects/numberExtractor/chromedriver.exe")

url = "https://www.pakwheels.com/used-cars/sell#"
driver.get(url)
time.sleep(2)

driver.find_element_by_id("car_selector").click()
time.sleep(2)

driver.find_element_by_id("model_year_2020").click()
time.sleep(2)

data_dic = ""
data_count = 0

make = driver.find_element_by_class_name("suzuki").click()
time.sleep(2)
modelsArray = driver.find_element_by_class_name("show")
modelsArray = modelsArray.find_elements_by_class_name("model")
i = 0
while i < 4:
    modelsArray[i].click()
    time.sleep(1)
    versionsArray = driver.find_elements_by_class_name("version")
    j = 0
    while j < versionsArray.__len__():
        version = str(versionsArray[j].text)
        if not version.__contains__(","):
            new_dic = {
                "make": "Suzuki",
                "model": modelsArray[i].text,
                "version": version
            }
            data_dic = data_dic + str(new_dic) + ",\n"
        j = j + 1
    i = i + 1


make = driver.find_element_by_class_name("toyota").click()
time.sleep(2)
modelsArray = driver.find_element_by_class_name("show")
modelsArray = modelsArray.find_elements_by_class_name("model")
i = 0
while i < 5:
    modelsArray[i].click()
    time.sleep(2)
    versionsArray = driver.find_elements_by_class_name("version")
    j = 0
    while j < versionsArray.__len__():
        if i == 0:
            version = versionsArray[j].find_element_by_tag_name("strong").text
            new_dic = {
                "make": "Toyota",
                "model": modelsArray[i].text,
                "version": version
            }
            data_dic = data_dic + str(new_dic) + ",\n"
            j = j + 1
        else:
            version = str(versionsArray[j].text)
            if not version.__contains__(","):
                new_dic = {
                    "make": "Toyota",
                    "model": modelsArray[i].text,
                    "version": version
                }
                data_dic = data_dic + str(new_dic) + ",\n"
            j = j + 1
    i = i + 1

make = driver.find_element_by_class_name("honda").click()
time.sleep(2)
modelsArray = driver.find_element_by_class_name("show")
modelsArray = modelsArray.find_elements_by_class_name("model")
i = 0
while i < 4:
    modelsArray[i].click()
    time.sleep(2)
    versionsArray = driver.find_elements_by_class_name("version")
    j = 0
    while j < versionsArray.__len__():
        if i == 1:
            version = versionsArray[j].find_element_by_tag_name("strong").text
            new_dic = {
                "make": "Honda",
                "model": modelsArray[i].text,
                "version": version
            }
            data_dic = data_dic + str(new_dic) + ",\n"
            j = j + 1
        else:
            version = str(versionsArray[j].text)
            if not version.__contains__(","):
                new_dic = {
                    "make": "Honda",
                    "model": modelsArray[i].text,
                    "version": version
                }
                data_dic = data_dic + str(new_dic) + ",\n"
            j = j + 1
    i = i + 1


make = driver.find_element_by_class_name("daihatsu").click()
time.sleep(2)
modelsArray = driver.find_element_by_class_name("show")
modelsArray = modelsArray.find_elements_by_class_name("model")
i = 0
while i < 5:
    modelsArray[i].click()
    time.sleep(1)
    versionsArray = driver.find_elements_by_class_name("version")
    j = 0
    while j < versionsArray.__len__():
        version = str(versionsArray[j].text)
        if not version.__contains__(","):
            new_dic = {
                "make": "Daihatsu",
                "model": modelsArray[i].text,
                "version": version
            }
            data_dic = data_dic + str(new_dic) + ",\n"
        j = j + 1
    i = i + 1


make = driver.find_element_by_class_name("nissan").click()
time.sleep(2)
modelsArray = driver.find_element_by_class_name("show")
modelsArray = modelsArray.find_elements_by_class_name("model")
i = 0
while i < 5:
    modelsArray[i].click()
    time.sleep(1)
    versionsArray = driver.find_elements_by_class_name("version")
    j = 0
    while j < versionsArray.__len__():
        version = str(versionsArray[j].text)
        if not version.__contains__(","):
            new_dic = {
                "make": "Nissan",
                "model": modelsArray[i].text,
                "version": version
            }
            data_dic = data_dic + str(new_dic) + ",\n"
        j = j + 1
    i = i + 1

print(data_dic)
