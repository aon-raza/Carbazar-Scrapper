from bs4 import BeautifulSoup
import requests
import pandas as pd
import flask
import json
from flask import request
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/pakWheelsHome', methods=['GET'])
def pakWheelsHome():
    i=0
    url = "https://www.pakwheels.com/used-cars/search/-/?page=1"

    posts_dic = {}
    post_count = 0

    while i < 10:

        response = requests.get(url)
        print(response)
        data = response.text
        # print(data)

        soup = BeautifulSoup(data, 'html.parser')

        itemsList = soup.findAll("ul", {"class": "search-results"})

        for item in itemsList:
            itemBox = item.findAll("li", {"class": "classified-listing"})
            for singleItem in itemBox:
                image = singleItem.find("img")
                if image is not None:
                    imageSrc = image.get("data-original") if image.get("data-original") else "N/A" #1
                    link = singleItem.find("a", {"class": "car-name"})

                    post_link = "https://www.pakwheels.com" + link.get("href") if link.get("href") else "N/A" #2
                    title = link.get("title") if link.get("title") else "N/A" #3

                    price = singleItem.find("div", {"class": "price-details"}).text #4
                    price = str(price).replace("\n", "")
                    ratingFake = singleItem.find("span", {"class": "auction-rating"})
                    if ratingFake is not None:
                        rating = ratingFake.text         #5

                    city = singleItem.find("ul", {"class": "search-vehicle-info"}).text  #6
                    city = str(city).replace("\n", "")
                    city = str(city).replace(" ", "")

                    otherDetails = str(singleItem.find("ul", {"class": "search-vehicle-info-2"}).text)
                    array = otherDetails.split("\n")

                    year = array[1]        #7
                    running = array[2]          #8
                    engineType = array[3]         #9
                    engineCapacity = array[4]           #10
                    transmission = array[5]        #11

                    post_count += 1
                    new_dic = {
                        "link": post_link,
                        "image": imageSrc,
                        "title": title,
                        "price": price,
                        "rating": rating,
                        "city": city,
                        "year": year,
                        "running": running,
                        "engineType": engineType,
                        "engineCapacity": engineCapacity,
                        "transmission": transmission
                    }
                    posts_dic[post_count] = new_dic
        i = i + 1
        next_url = soup.find("li", {"class": "next_page"})
        next_url = next_url.find("a")
        next_url = "https://www.pakwheels.com" + next_url.get("href") if next_url.get("href") else "N/A"
        url = next_url

    return posts_dic


@app.route('/pakWheelsSearch', methods=['GET'])
def pakWheelsSearch():

    if 'query' in request.args:
        searchString = str(request.args['query'])
    else:
        return "Error: No search query provided. Please specify a query."

    url = "https://www.pakwheels.com/used-cars/search/-/?page=1&q="+searchString.replace(" ", "+")
    i=0
    posts_dic = {}
    post_count = 0

    while i < 10:

        response = requests.get(url)
        print(response)
        data = response.text
        # print(data)

        soup = BeautifulSoup(data, 'html.parser')

        itemsList = soup.findAll("ul", {"class": "search-results"})

        for item in itemsList:
            itemBox = item.findAll("li", {"class": "classified-listing"})
            for singleItem in itemBox:
                image = singleItem.find("img")
                if image is not None:
                    imageSrc = image.get("data-original") if image.get("data-original") else "N/A" #1
                    link = singleItem.find("a", {"class": "car-name"})

                    post_link = "https://www.pakwheels.com" + link.get("href") if link.get("href") else "N/A" #2
                    title = link.get("title") if link.get("title") else "N/A" #3

                    price = singleItem.find("div", {"class": "price-details"}).text #4
                    price = str(price).replace("\n", "")
                    ratingFake = singleItem.find("span", {"class": "auction-rating"})
                    if ratingFake is not None:
                        rating = ratingFake.text         #5

                    city = singleItem.find("ul", {"class": "search-vehicle-info"}).text  #6
                    city = str(city).replace("\n", "")
                    city = str(city).replace(" ", "")

                    otherDetails = str(singleItem.find("ul", {"class": "search-vehicle-info-2"}).text)
                    array = otherDetails.split("\n")

                    year = array[1]        #7
                    running = array[2]          #8
                    engineType = array[3]         #9
                    engineCapacity = array[4]           #10
                    transmission = array[5]        #11

                    post_count += 1
                    new_dic = {
                        "link": post_link,
                        "image": imageSrc,
                        "title": title,
                        "price": price,
                        "rating": rating,
                        "city": city,
                        "year": year,
                        "running": running,
                        "engineType": engineType,
                        "engineCapacity": engineCapacity,
                        "transmission": transmission
                    }
                    posts_dic[post_count] = new_dic
        i = i + 1
        next_url = soup.find("li", {"class": "next_page"})
        next_url = next_url.find("a")
        next_url = "https://www.pakwheels.com" + next_url.get("href") if next_url.get("href") else "N/A"
        url = next_url

    return posts_dic


app.run()


#host='0.0.0.0', port=5000)
