from bs4 import BeautifulSoup
import requests
import pandas as pd
import flask
import json
from flask import request
from flask_cors import CORS
# from selenium import webdriver


app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/pkMotorsHome', methods=['GET'])
def pkMotorsHome():
    posts_dic = {}
    post_count = 0

    url = "https://www.pkmotors.com/used/car/p/20/0"

    response = requests.get(url)
    # print(response)
    data = response.text
    # print(data)

    soup = BeautifulSoup(data, 'html.parser')

    itemsList = soup.findAll("a", {"class": "detailbtn"})

    for item in itemsList:
        postLink = item.get("href") if item.get("href") else "N/A"   # 1

        response = requests.get(postLink)
        data = response.text

        soupInt = BeautifulSoup(data, 'html.parser')

        image = soupInt.find("div", {"id": "1"})
        if image is not None:
            image = image.find("img")
            image = image.get("src") if image.get("src") else "N/A"   # 2

        title = soupInt.find("h1", {"class": "aboutinfobar"}).text  # 3
        price = soupInt.find("div", {"class": "itemdetprice"}).text  # 4

        SellerComments = soupInt.find("div", {"class": "itemspecbox"})
        SellerComments = SellerComments.find("h2").text
        SellerComments = str(SellerComments).replace("  ", "").replace("\n", "")  # 5

        otherAttributes = soupInt.find("div", {"class": "itemspecbox"})
        otherAttributes = otherAttributes.findAll("ul", {"class": "speclisting"})
        singleAttributes = otherAttributes[1].findAll("div", {"class": "specbox2"})

        Make = singleAttributes[1].text  # 6
        Model = singleAttributes[2].text  # 7
        Year = singleAttributes[3].text  # 8
        ExteriorColor = singleAttributes[4].text  # 9
        Mileage = singleAttributes[5].text  # 10
        RegistrationCity = singleAttributes[6].text  # 11
        Insurance = singleAttributes[7].text  # 12
        Transmission = singleAttributes[8].text  # 13

        post_count += 1
        new_dic = {
            "link": postLink,
            "image": image,
            "title": title,
            "price": price,
            "SellerComments": SellerComments,
            "Make": Make,
            "Model": Model,
            "Year": Year,
            "ExteriorColor": ExteriorColor,
            "Mileage": Mileage,
            "RegistrationCity": RegistrationCity,
            "Insurance": Insurance,
            "Transmission": Transmission
        }
        posts_dic[post_count] = new_dic

    return posts_dic


@app.route('/pkMotorsSearch', methods=['GET'])
def pkMotorsSearch():

    if 'query' in request.args:
        searchString = str(request.args['query'])
    else:
        return "Error: No search query provided. Please specify a query."

    url = "https://www.pkmotors.com/full-search/"+searchString.replace(" ", "-")
    posts_dic = {}
    post_count = 0

    response = requests.get(url)
    # print(response)
    data = response.text
    # print(data)

    soup = BeautifulSoup(data, 'html.parser')

    itemsList = soup.findAll("a", {"class": "detailbtn"})

    for item in itemsList:
        postLink = item.get("href") if item.get("href") else "N/A"  # 1

        response = requests.get(postLink)
        data = response.text

        soupInt = BeautifulSoup(data, 'html.parser')

        image = soupInt.find("div", {"id": "1"})
        if image is not None:
            image = image.find("img")
            image = image.get("src") if image.get("src") else "N/A"  # 2

        title = soupInt.find("h1", {"class": "aboutinfobar"}).text  # 3
        price = soupInt.find("div", {"class": "itemdetprice"}).text  # 4

        SellerComments = soupInt.find("div", {"class": "itemspecbox"})
        SellerComments = SellerComments.find("h2").text
        SellerComments = str(SellerComments).replace("  ", "").replace("\n", "")  # 5

        otherAttributes = soupInt.find("div", {"class": "itemspecbox"})
        otherAttributes = otherAttributes.findAll("ul", {"class": "speclisting"})
        singleAttributes = otherAttributes[1].findAll("div", {"class": "specbox2"})

        Make = singleAttributes[1].text  # 6
        Model = singleAttributes[2].text  # 7
        Year = singleAttributes[3].text  # 8
        ExteriorColor = singleAttributes[4].text  # 9
        Mileage = singleAttributes[5].text  # 10
        RegistrationCity = singleAttributes[6].text  # 11
        Insurance = singleAttributes[7].text  # 12
        Transmission = singleAttributes[8].text  # 13

        post_count += 1
        new_dic = {
            "link": postLink,
            "image": image,
            "title": title,
            "price": price,
            "SellerComments": SellerComments,
            "Make": Make,
            "Model": Model,
            "Year": Year,
            "ExteriorColor": ExteriorColor,
            "Mileage": Mileage,
            "RegistrationCity": RegistrationCity,
            "Insurance": Insurance,
            "Transmission": Transmission
        }
        posts_dic[post_count] = new_dic

    return posts_dic


app.run()


# host='0.0.0.0', port=5000
