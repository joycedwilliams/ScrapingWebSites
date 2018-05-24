# Import dependencies
import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

import pymongo

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

database = client.surfs_db

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Create empy list
def scrape():
    browser = init_browser()
    locations = []
    location_urls = []
    water_temps = []
    air_temps = []
    
    # Id website to be scraped
    url = "https://www.surfline.com/surf-reports-forecasts-cams/costa-rica/3624060"
    browser.visit(url)

    surf_spots = database.surf_spots

    # Use Beautiful to parse the URL
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Scrape the locations from the website
    locations_soup = soup.find_all("h3", class_="sl-spot-details__name")
    for location_soup in locations_soup:
        locations.append(location_soup.get_text())
    
    # Scrape the URLs for the locations from the website
    locations_url_soup = soup.find_all("a", class_="sl-cam-list-link")
    for location_url_soup in locations_url_soup:
        location_urls.append("https://www.surfline.com" + location_url_soup.attrs['href'])
    
    # Print locations and their URLs for later use
    print(locations)
    print(location_urls)

    # Scrape the 2nd page to get the water and air temperatures
    for location_url in location_urls:
        browser.visit(location_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        # Get the water and air temperatures and add them to the list
        water_temp = soup.find_all("div", class_="sl-wetsuit-recommender__weather")[0].find_all('div', {'data-reactid':True})[0].get_text()
        air_temp = soup.find_all("div", class_="sl-wetsuit-recommender__weather")[0].find_all('div', {'data-reactid':True})[1].get_text()
        water_temps.append(water_temp)
        air_temps.append(air_temp)
    
    for index in range(len(locations)):
        spot = {
            "location":locations[index],
            "url":location_urls[index],
            "water_temp":water_temps[index],
            "air_temp":air_temps[index]            
        }
        surf_spots.insert(spot)

    print(water_temps)
    print(air_temps)
    
scrape()

    #listings["location"] = soup.find_all("h3",
    #   class_="sl-spot-details__name")
    #print(listings["location"][0].get_text())
    #code for main page
    #listings["location"] = soup.findall("h3", class_="sl-spot-details__name")

    #listings["location"] = [obj, obj.href, obj.get_text()]

    #'www.surfline.com'+obj.href
    
    #istings["Surf height"] = soup.findall("span", class_="quiver-surf-height")
    
    # code for individual reports
    #

