from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
import base64
from io import BytesIO
from PIL import Image
from .models import Location
from django.http import HttpRequest
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pymongo


# client = MongoClient("mongodb://localhost:27017/")
# db = client["maps"]
# colectie = db["CC"]
# #din baza de date trebuie citite, sa nu fie statice, in binar sa fie
# cale_imagini = [
#     "C:\\Users\\rusuv\\Desktop\\teza\\harta\\maps\\centru_civic\\aftar.jpg",
#     "C:\\Users\\rusuv\\Desktop\\teza\\harta\\maps\\centru_civic\\aula.jpg",
#     "C:\\Users\\rusuv\\Desktop\\teza\\harta\\maps\\centru_civic\\kruhnen.png",
#     "C:\\Users\\rusuv\\Desktop\\teza\\harta\\maps\\centru_civic\\temple.png"
# ]

# nume_imagini = ["Aftar Hours", "Aula UniTBv", "Kruhnen Musik Halle", "Temple"]

# def adauga_imagini_in_db():
#     for cale_imagine, nume_imagine in zip(cale_imagini, nume_imagini):
#         # Verifică dacă imaginea există deja în colecție
#         if colectie.find_one({"nume": nume_imagine}):
#             continue

#         with open(cale_imagine, "rb") as image_file:
#             # Decodifică imaginea și comprimă-o
#             imagine = Image.open(BytesIO(image_file.read()))
#             buffer = BytesIO()
#             imagine = imagine.convert('RGB')
#             imagine.save(buffer, format="JPEG")
#             content = buffer.getvalue()

#         colectie.insert_one({"nume": nume_imagine, "imagine": content})

# # Adaugă imaginile doar dacă nu există deja
# adauga_imagini_in_db()

# client.close()

def get_images(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["maps"]
    colectie = db["CC"]

    imagini = list(colectie.find({}, {'_id': 0}))

    for imagine in imagini:
        imagine['imagine'] = base64.b64encode(imagine['imagine']).decode('utf-8')

    client.close()

    return JsonResponse({'imagini': imagini})


def harta(request):
    locations = Location.objects.all()
    return render(request, 'map/afisareimag.html', {'locations': locations})


def streetview(request):
    locations = Location.objects.all()
    return render(request, 'map/streetview.html', {'locations': locations})
def aula(request: HttpRequest):
    url = 'https://www.unitbv.ro/stiri-si-evenimente.html'
    article_data = []
    base_url = 'https://www.unitbv.ro'

    client = MongoClient("mongodb://localhost:27017/")
    db = client["maps"]
    news_collection = db["Events"]

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('article', class_='item')

        for article in articles:
            title_element = article.find('h5', class_='item_title')
            description_element = article.find('div', class_='item_introtext')
            image_element = article.find('img')

            if title_element and description_element and image_element:
                title = title_element.text.strip()
                description = description_element.text.strip()
                image_url = urljoin(base_url, image_element['src'])
                article_url = urljoin(base_url, article.find('a')['href'])

                existing_article = news_collection.find_one({'article_url': article_url})
                if image_url and not existing_article:
                    article_data.append({
                        'title': title,
                        'article_url': article_url,
                        'image_url': image_url,
                        'description': description,
                    })

    # Insert the data into the MongoDB collection
    if article_data:
        news_collection.insert_many(article_data)

    # Retrieve data from MongoDB to display in the HTML template
    articole = news_collection.find()

    # Close the MongoDB connections
    client.close()
    articole_list = list(articole)

    return render(request, 'map/aula.html', {'articole': articole_list})
















def scrape_facebook():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")

    # Create the "maps" database if it doesn't exist
    db = client["maps"]

    # Create the "AH" collection if it doesn't exist
    collection = db["AH"]

    # Define the indexes for the collection
    collection.create_index([("data_eveniment", pymongo.TEXT), ("nume_eveniment", pymongo.TEXT)])

    # Facebook event URL
    url = "https://www.facebook.com/aftarhours/upcoming_hosted_events"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the GET request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the event elements
        evenimente = soup.find_all('div', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv x1s688f')

        # Loop through each event element
        for eveniment in evenimente:
            # Extract the event data
            data_eveniment = eveniment.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xg8j3zb').text.strip()
            nume_eveniment = eveniment.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xg8j3zb').text.strip()

            # Print the scraped data for debugging
            print("Data evenimentului:", data_eveniment)
            print("Numele evenimentului:", nume_eveniment)

            # Save the event data to MongoDB
            result = collection.insert_one({
                "data_eveniment": data_eveniment,
                "nume_eveniment": nume_eveniment
            })

            # Print the result of the insert operation for debugging
            print("Eveniment salvat in baza de date:", result.inserted_id)
    else:
        print("GET request failed with status code:", response.status_code)

    # Close the MongoDB connection
    client.close()

# Call the function to scrape Facebook events
scrape_facebook()