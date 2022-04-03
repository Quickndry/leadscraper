# VirtualENV
# python -m pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup

def protoscraper(city, postcode):
    profile_url_list = []
    url = "https://www.druckereien.info/de/suche/ergebnis/13726/{}+{}/drucksachen/alle.html".format(postcode, city)
    page = requests.get(url)
    html_soup = BeautifulSoup(page.content, "html.parser")
    premium_profiles= html_soup.find_all("section", class_="premium_druckerei gainlayout")
    print("Premium Profile: ", premium_profiles[0]) #Print command to check extracted data
    for profile in premium_profiles:
        profile_details = profile.find(class_="details_leiste")
        profile_url_end = profile_details.find("a", "href")
        profile_url = "https://www.druckereien.info/" + str(profile_url_end)
        print("Profile URL: ", profile_url)
        profile_url_list.append(profile_url)
    standard_profiles= html_soup.find_all("section", class_="standard_druckerei gainlayout")
    print("Standard Profile: ", standard_profiles[0]) #Print command to check extracted data
    for profile in standard_profiles:
        profile_details = profile.find(class_="details_leiste")
        profile_url_end = profile_details.find("a", "href")
        profile_url = "https://www.druckereien.info/" + str(profile_url_end)
        print("Profile URL: ", profile_url)
        profile_url_list.append(profile_url)
    
    print("List of profile URL's: ", profile_url_list)
