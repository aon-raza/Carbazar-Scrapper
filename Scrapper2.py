from bs4 import BeautifulSoup
import requests
import pandas as pd

searchString="honda-city"
url = "https://www.olx.com.pk/cars_c84/q-"+searchString.replace(" ", "-")

response = requests.get(url)
print(response)
data = response.text
# print(data)

soup = BeautifulSoup(data, 'html.parser')

models = soup.findAll("span", {"data-aut-id": "itemTitle"})

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
            "Link" : link,
            "Image" : image,
            "Price" : itemPrice,
            "Details" : itemDetails,
            "Title'" : itemTitle,
            "Location" : itemLocation
        }
        posts_dic[post_count] = [new_dic]

        print("\n Link:  "+link + "\nImage URL:  "+image+ "\n Item Price: "+itemPrice+ "\n Item Details: "+itemDetails+ "\n Item Title: "+itemTitle+ "\n Location: "+itemLocation)

post_df = pd.DataFrame.from_dict(posts_dic, orient = 'index')
print(post_df)
# post_df.to_csv('posts.csv')

post_df.to_json('posts.json')