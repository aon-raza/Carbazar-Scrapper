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


@app.route('/', methods=['GET'])
def home():
    url = "https://www.olx.com.pk/cars_c84/"

    response = requests.get(url)
    print(response)
    data = response.text
    # print(data)

    soup = BeautifulSoup(data, 'html.parser')

    # models = soup.findAll("span", {"data-aut-id": "itemTitle"})

    # for model in models:
    #     print(model.text)

    posts_dic = {}
    post_count = 0

    itemsList = soup.findAll("ul", {"data-aut-id": "itemsList"})

    for item in itemsList:
        itemBox = item.findAll("li", {"data-aut-id": "itemBox"})
        # print(itemBox)
        # print("\n ??????? \n")
        for links in itemBox:
            linkkk = links.find("a")
            link = linkkk.get("href") if linkkk.get("href") else "N/A"
            link = "https://www.olx.com.pk" + link

            imageee = linkkk.find("img")
            image = imageee.get("src") if imageee.get("src") else "N/A"

            itemPrice = linkkk.find("span", {"data-aut-id": "itemPrice"}).text
            itemDetails = linkkk.find("span", {"data-aut-id": "itemDetails"}).text
            itemTitle = linkkk.find("span", {"data-aut-id": "itemTitle"}).text
            itemLocation = linkkk.find("span", {"data-aut-id": "item-location"}).text

            post_count += 1
            new_dic = {
                "Link": link,
                "Image": image,
                "Price": itemPrice,
                "Details": itemDetails,
                "Title": itemTitle,
                "Location": itemLocation
            }
            # print(new_dic)
            posts_dic[post_count] = [new_dic]

    # return json.dumps(posts_dic)
    return posts_dic


@app.route('/search', methods=['GET'])
def Search():

    if 'query' in request.args:
        searchString = str(request.args['query']).lower()
    else:
        return "Error: No search query provided. Please specify a query."

    url = "https://www.olx.com.pk/cars_c84/q-"+searchString.replace(" ", "-")

    response = requests.get(url)
    print(response)
    data = response.text
    # print(data)

    soup = BeautifulSoup(data, 'html.parser')

    # models = soup.findAll("span", {"data-aut-id": "itemTitle"})

    # for model in models:
    #     print(model.text)

    posts_dic = {}
    post_count = 0

    itemsList = soup.findAll("ul", {"data-aut-id": "itemsList"})

    for item in itemsList:
        itemBox = item.findAll("li", {"data-aut-id": "itemBox"})
        # print(itemBox)
        # print("\n ??????? \n")
        for links in itemBox:
            linkkk = links.find("a")
            link = linkkk.get("href") if linkkk.get("href") else "N/A"
            link = "https://www.olx.com.pk" + link

            imageee = linkkk.find("img")
            image = imageee.get("src") if imageee.get("src") else "N/A"

            itemPrice = linkkk.find("span", {"data-aut-id": "itemPrice"}).text
            itemDetails = linkkk.find("span", {"data-aut-id": "itemDetails"}).text
            itemTitle = linkkk.find("span", {"data-aut-id": "itemTitle"}).text
            itemLocation = linkkk.find("span", {"data-aut-id": "item-location"}).text

            post_count += 1
            new_dic = {
                "Link": link,
                "Image": image,
                "Price": itemPrice,
                "Details": itemDetails,
                "Title": itemTitle,
                "Location": itemLocation
            }
            posts_dic[post_count] = [new_dic]

    # return json.dumps(posts_dic)
    return posts_dic



@app.route('/olxFilters', methods=['GET'])
def olxFilters():

    global KMDriven1, KMDriven2, price1, price2, year1, year2
    if 'query' in request.args:
        searchString = str(request.args['query']).lower()
    else:
        searchString = ""

    if 'price' in request.args:
        price = str(request.args['price'])
        if price != "-":
            array = price.split("-")
            price1 = array[0]
            price2 = array[1]
        else:
            price = ""
    else:
        price = ""

    if 'location' in request.args:
        location = str(request.args['location']).lower()
    else:
        location = ""

    if 'regCity' in request.args:
        regCity = str(request.args['regCity']).lower()
    else:
        regCity = ""

    if 'make' in request.args:
        make = str(request.args['make']).lower()
    else:
        make = ""

    if 'model' in request.args:
        model = str(request.args['model']).lower()
    else:
        model = ""

    if 'engineType' in request.args:
        engineType = str(request.args['engineType']).lower()
    else:
        engineType = ""

    if 'year' in request.args:
        year = str(request.args['year'])
        if year != "-":
            array = year.split("-")
            year1 = array[0]
            year2 = array[1]
        else:
            year = ""
    else:
        year = ""

    if 'KMDriven' in request.args:
        KMDriven = str(request.args['KMDriven'])
        if KMDriven != "":
            array = KMDriven.split(" - ")
            KMDriven1 = array[0]
            KMDriven2 = array[1]
        else:
            KMDriven = ""
    else:
        KMDriven = ""

    if 'condition' in request.args:
        condition = str(request.args['condition']).lower()
    else:
        condition = ""

    url = "https://www.olx.com.pk/cars_c84"
    if searchString != "":
        url = url + "/q-" + searchString.replace(" ", "-") + "?filter="
    else:
        url = url + "?filter="

    if make != "":
        if make == "suzuki" or make == "honda":
            url = url + "make_eq_cars-" + make + "%2"
            url = url.replace("cars_c84", make + "-cars_c84")
        else:
            url = url + "make_eq_" + make.replace(" ", "-") + "%2"
            url = url.replace("cars_c84", make.replace(" ", "-") + "-cars_c84")

    if KMDriven != "":
        url = url + "Cmileage_between_" + KMDriven1 + "_to_" + KMDriven2 + "%2"

    if condition != "":
        url = url + "Cnew_used_eq_" + condition + "%2"

    if engineType != "":
        url = url + "Cpetrol_eq_" + engineType + "%2"

    if price != "":
        url = url + "Cprice_between_" + price1 + "_to_" + price2 + "%2"

    if regCity != "":
        url = url + "Cregistration_city_eq_" + regCity.replace(" ", "") + "%2"

    if year != "":
        url = url + "Cyear_between_" + year1 + "_to_" + year2 + "%2"

    url = url[0:url.__len__()-2]
    print(url)

    # url = "https://www.olx.com.pk/honda-cars_c84/q-honda-city" \
    #       "?filter=make_eq_cars-honda%2" \
    #       "Cmileage_between_10000_to_1000000%2" \
    #       "Cpetrol_eq_petrol%2" \
    #       "Cprice_between_1000000_to_2000000%2" \
    #       "Cregistration_city_eq_lahore%2" \
    #       "Cyear_between_2001_to_2019%2" \

    response = requests.get(url)
    print(response)
    data = response.text
    # print(data)

    soup = BeautifulSoup(data, 'html.parser')

    # models = soup.findAll("span", {"data-aut-id": "itemTitle"})

    # for model in models:
    #     print(model.text)

    posts_dic = {}
    post_count = 0

    itemsList = soup.findAll("ul", {"data-aut-id": "itemsList"})

    for item in itemsList:
        itemBox = item.findAll("li", {"data-aut-id": "itemBox"})
        # print(itemBox)
        # print("\n ??????? \n")
        for links in itemBox:
            linkkk = links.find("a")
            link = linkkk.get("href") if linkkk.get("href") else "N/A"
            link = "https://www.olx.com.pk" + link

            imageee = linkkk.find("img")
            image = imageee.get("src") if imageee.get("src") else "N/A"

            itemPrice = linkkk.find("span", {"data-aut-id": "itemPrice"}).text
            itemDetails = linkkk.find("span", {"data-aut-id": "itemDetails"}).text
            itemTitle = linkkk.find("span", {"data-aut-id": "itemTitle"}).text
            itemLocation = linkkk.find("span", {"data-aut-id": "item-location"}).text

            post_count += 1
            new_dic = {
                "Link": link,
                "Image": image,
                "Price": itemPrice,
                "Details": itemDetails,
                "Title": itemTitle,
                "Location": itemLocation
            }
            posts_dic[post_count] = [new_dic]

    # return json.dumps(posts_dic)
    return posts_dic


@app.route('/pakWheelsHome', methods=['GET'])
def pakWheelsHome():
    i=0
    url = "https://www.pakwheels.com/used-cars/search/-/?page=1"

    posts_dic = {}
    post_count = 0

    while i < 1:

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
                    else:
                        rating = "N/A"

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
        searchString = str(request.args['query']).lower()
    else:
        return "Error: No search query provided. Please specify a query."

    url = "https://www.pakwheels.com/used-cars/search/-/?page=1&q="+searchString.replace(" ", "+")
    i=0
    posts_dic = {}
    post_count = 0

    while i < 1:

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
                    else:
                        rating = "N/A"

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


@app.route('/pakWheelsFilters', methods=['GET'])
def pakWheelsFilters():

    global KMDriven1, KMDriven2, price1, price2, year1, year2, engineCapacity1, engineCapacity2
    if 'query' in request.args:
        searchString = str(request.args['query']).lower()
    else:
        searchString = ""

    if 'price' in request.args:
        price = str(request.args['price'])
        if price != "-":
            array = price.split("-")
            price1 = array[0]
            price2 = array[1]
        else:
            price = ""
    else:
        price = ""

    if 'location' in request.args:
        location = str(request.args['location']).lower()
    else:
        location = ""

    if 'regCity' in request.args:
        regCity = str(request.args['regCity']).lower()
    else:
        regCity = ""

    if 'make' in request.args:
        make = str(request.args['make']).lower()
    else:
        make = ""

    if 'model' in request.args:
        model = str(request.args['model']).lower()
    else:
        model = ""

    if 'engineType' in request.args:
        engineType = str(request.args['engineType']).lower()
    else:
        engineType = ""

    if 'year' in request.args:
        year = str(request.args['year'])
        if year != "-":
            array = year.split("-")
            year1 = array[0]
            year2 = array[1]
        else:
            year = ""
    else:
        year = ""

    if 'KMDriven' in request.args:
        KMDriven = str(request.args['KMDriven'])
        if KMDriven != "":
            array = KMDriven.split(" - ")
            KMDriven1 = array[0]
            KMDriven2 = array[1]
        else:
            KMDriven = ""
    else:
        KMDriven = ""

    if 'transmission' in request.args:
        transmission = str(request.args['transmission']).lower()
    else:
        transmission = ""

    if 'color' in request.args:
        color = str(request.args['color']).lower()
    else:
        color = ""

    if 'engineCapacity' in request.args:
        engineCapacity = str(request.args['engineCapacity'])
        if engineCapacity != "-":
            array = engineCapacity.split("-")
            engineCapacity1 = array[0]
            engineCapacity2 = array[1]
        else:
            engineCapacity = ""
    else:
        engineCapacity = ""

    url = "https://www.pakwheels.com/used-cars/search/-"

    if make != "":
        url = url + "/mk_" + make.replace(" ", "-")

    if model != "":
        url = url + "/md_" + model.replace(" ", "-")

    if location != "":
        url = url + "/ct_" + location.replace(" ", "-")

    if regCity != "":
        url = url + "/rg_" + regCity.replace(" ", "-")

    if price != "":
        url = url + "/pr_" + price1 + "_" + price2

    if year != "":
        url = url + "/yr_" + year1 + "_" + year2

    if transmission != "":
        url = url + "/tr_" + transmission

    if engineType != "":
        url = url + "/eg_" + engineType

    if KMDriven != "":
        url = url + "/ml_" + KMDriven1 + "_" + KMDriven2

    if engineCapacity != "":
        url = url + "/ec_" + engineCapacity1 + "_" + engineCapacity2

    if color != "":
        url = url + "/cl_" + color

    url = url + "/?page=1"
    if searchString != "":
        url = url + "&q=" + searchString.replace(" ", "+")

    print(url)

    # url = "https://www.pakwheels.com/used-cars/search/-" \
    #       "/mk_honda" \
    #       "/md_city" \
    #       "/ct_lahore" \
    #       "/rg_lahore" \
    #       "/pr_1400000_2600000" \
    #       "/yr_2000_2019" \
    #       "/eg_petrol" \
    #       "/ml_40000_110000" \
    #       "/?page=2&q=honda+city"
    #
    # url = "https://www.pakwheels.com/used-cars/search/-/?page=1&q=" + searchString.replace(" ", "+")

    i=0
    posts_dic = {}
    post_count = 0
    # print(url)
    while i < 1:

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
                    else:
                        rating = "N/A"

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
        # next_url = soup.find("li", {"class": "next_page"})
        # next_url = next_url.find("a")
        # next_url = "https://www.pakwheels.com" + next_url.get("href") if next_url.get("href") else "N/A"
        # url = next_url

    return posts_dic


@app.route('/pkMotorsHome', methods=['GET'])
def pkMotorsHome():
    posts_dic = {}
    post_count = 0

    url = "https://www.pkmotors.com/used/car/p/10/0"

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

        title = soupInt.find("h1", {"class": "aboutinfobar"})
        if title is not None:
            title = soupInt.find("h1", {"class": "aboutinfobar"}).text  # 3
        else:
            title = ""

        price = soupInt.find("div", {"class": "itemdetprice"})
        if price is not None:
            price = soupInt.find("div", {"class": "itemdetprice"}).text  # 4
        else:
            price = ""

        SellerComments = soupInt.find("div", {"class": "itemspecbox"})
        if SellerComments is not None:
            SellerComments = SellerComments.find("h2").text
            SellerComments = str(SellerComments).replace("  ", "").replace("\n", "")  # 5
        else:
            SellerComments = ""

        otherAttributes = soupInt.find("div", {"class": "itemspecbox"})
        if otherAttributes is not None:
            otherAttributes = otherAttributes.findAll("ul", {"class": "speclisting"})
            singleAttributes = otherAttributes[1].findAll("div", {"class": "specbox2"})
        else:
            otherAttributes = ""

        Make = singleAttributes[1].text  # 6
        Model = singleAttributes[2].text  # 7
        Year = singleAttributes[3].text  # 8
        ExteriorColor = singleAttributes[4].text  # 9
        Mileage = singleAttributes[5].text  # 10
        RegistrationCity = singleAttributes[6].text  # 11
        Insurance = singleAttributes[7].text  # 12
        Transmission = singleAttributes[8].text  # 13

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
        if otherAttributes != "":
            post_count += 1
            posts_dic[post_count] = new_dic

    return posts_dic


@app.route('/pkMotorsSearch', methods=['GET'])
def pkMotorsSearch():

    if 'query' in request.args:
        searchString = str(request.args['query']).lower()
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

    i = 0
    for item in itemsList:
        i = i+1
        if i>10:
            break
        postLink = item.get("href") if item.get("href") else "N/A"  # 1

        response = requests.get(postLink)
        data = response.text

        soupInt = BeautifulSoup(data, 'html.parser')

        image = soupInt.find("div", {"id": "1"})
        if image is not None:
            image = image.find("img")
            image = image.get("src") if image.get("src") else "N/A"  # 2

        title = soupInt.find("h1", {"class": "aboutinfobar"})
        if title is not None:
            title = soupInt.find("h1", {"class": "aboutinfobar"}).text  # 3
        else:
            title = ""

        price = soupInt.find("div", {"class": "itemdetprice"})
        if price is not None:
            price = soupInt.find("div", {"class": "itemdetprice"}).text  # 4
        else:
            price = ""

        SellerComments = soupInt.find("div", {"class": "itemspecbox"})
        if SellerComments is not None:
            SellerComments = SellerComments.find("h2").text
            SellerComments = str(SellerComments).replace("  ", "").replace("\n", "")  # 5
        else:
            SellerComments = ""

        otherAttributes = soupInt.find("div", {"class": "itemspecbox"})
        if otherAttributes is not None:
            otherAttributes = otherAttributes.findAll("ul", {"class": "speclisting"})
            singleAttributes = otherAttributes[1].findAll("div", {"class": "specbox2"})
        else:
            otherAttributes = ""

        Make = singleAttributes[1].text  # 6
        Model = singleAttributes[2].text  # 7
        Year = singleAttributes[3].text  # 8
        ExteriorColor = singleAttributes[4].text  # 9
        Mileage = singleAttributes[5].text  # 10
        RegistrationCity = singleAttributes[6].text  # 11
        Insurance = singleAttributes[7].text  # 12
        Transmission = singleAttributes[8].text  # 13

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
        if otherAttributes != "":
            post_count += 1
            posts_dic[post_count] = new_dic

    return posts_dic


@app.route('/pkMotorsFilters', methods=['GET'])
def pkMotorsFilters():

    global KMDriven1, KMDriven2, price1, price2, year1, year2
    if 'query' in request.args:
        searchString = str(request.args['query']).lower()
    else:
        searchString = ""

    if 'price' in request.args:
        price = str(request.args['price'])
        if price != "-":
            array = price.split("-")
            price1 = array[0]
            price2 = array[1]
        else:
            price = ""
    else:
        price = ""

    if 'location' in request.args:
        location = str(request.args['location']).lower()
    else:
        location = ""

    if 'regCity' in request.args:
        regCity = str(request.args['regCity']).lower()
    else:
        regCity = ""

    if 'make' in request.args:
        make = str(request.args['make']).lower()
    else:
        make = ""

    if 'model' in request.args:
        model = str(request.args['model']).lower()
    else:
        model = ""

    if 'engineType' in request.args:
        engineType = str(request.args['engineType']).lower()
    else:
        engineType = ""

    if 'year' in request.args:
        year = str(request.args['year'])
        if year != "-":
            array = year.split("-")
            year1 = array[0]
            year2 = array[1]
        else:
            year = ""
    else:
        year = ""

    if 'KMDriven' in request.args:
        KMDriven = str(request.args['KMDriven'])
        if KMDriven != "":
            array = KMDriven.split(" - ")
            KMDriven1 = array[0]
            KMDriven2 = array[1]
        else:
            KMDriven = ""
    else:
        KMDriven = ""

    url = "https://www.pkmotors.com/used/car"

    if make != "":
        url = url + "/" + make

    if model != "":
        url = url + "/" + model

    if year != "":
        url = url + "/" + year2

    if location != "":
        url = url + "/" + location

    # if regCity != "":
    #     url = url + "/rg_" + regCity
    #
    # if price != "":
    #     url = url + "/pr_" + price1 + "_" + price2
    #
    # if engineType != "":
    #     url = url + "/eg_" + engineType
    #
    # if KMDriven != "":
    #     url = url + "/ml_" + KMDriven1 + "_" + KMDriven2

    # if searchString != "":
    #     url = url + "&q=" + searchString.replace(" ", "+")

    # url = "https://www.pkmotors.com/used/car" \
    #       "/honda" \
    #       "/city" \
    #       "/2016" \
    #       "/lahore"

    print(url)
    posts_dic = {}
    post_count = 0

    response = requests.get(url)
    # print(response)
    data = response.text
    # print(data)

    soup = BeautifulSoup(data, 'html.parser')

    itemsList = soup.findAll("a", {"class": "detailbtn"})

    i = 0
    for item in itemsList:
        i = i+1
        if i>10:
            break
        postLink = item.get("href") if item.get("href") else "N/A"  # 1

        response = requests.get(postLink)
        data = response.text

        soupInt = BeautifulSoup(data, 'html.parser')

        image = soupInt.find("div", {"id": "1"})
        if image is not None:
            image = image.find("img")
            image = image.get("src") if image.get("src") else "N/A"  # 2

        title = soupInt.find("h1", {"class": "aboutinfobar"})
        if title is not None:
            title = soupInt.find("h1", {"class": "aboutinfobar"}).text  # 3
        else:
            title = ""

        price = soupInt.find("div", {"class": "itemdetprice"})
        if price is not None:
            price = soupInt.find("div", {"class": "itemdetprice"}).text  # 4
        else:
            price = ""

        SellerComments = soupInt.find("div", {"class": "itemspecbox"})
        if SellerComments is not None:
            SellerComments = SellerComments.find("h2").text
            SellerComments = str(SellerComments).replace("  ", "").replace("\n", "")  # 5
        else:
            SellerComments = ""

        otherAttributes = soupInt.find("div", {"class": "itemspecbox"})
        if otherAttributes is not None:
            otherAttributes = otherAttributes.findAll("ul", {"class": "speclisting"})
            singleAttributes = otherAttributes[1].findAll("div", {"class": "specbox2"})
        else:
            otherAttributes = ""

        Make = singleAttributes[1].text  # 6
        Model = singleAttributes[2].text  # 7
        Year = singleAttributes[3].text  # 8
        ExteriorColor = singleAttributes[4].text  # 9
        Mileage = singleAttributes[5].text  # 10
        RegistrationCity = singleAttributes[6].text  # 11
        Insurance = singleAttributes[7].text  # 12
        Transmission = singleAttributes[8].text  # 13

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
        if otherAttributes != "":
            post_count += 1
            posts_dic[post_count] = new_dic

    return posts_dic


app.run(host='0.0.0.0', port=5000)
