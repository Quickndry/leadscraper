# Libraries and dependencies
import csv
import requests
from bs4 import BeautifulSoup
import math
import time
import re

# Function that scrapes the total number of store profiles for each city & postcode pair searched for and adds
# it to a dictionary and list, which are then used to find the average number of store profiles per city. These
# are then written into target csv file.

def regional_totals(infile, outfile, duplicate_checker):
    if infile.startswith("C:\\"):
        try:
            with open(infile, "r") as in_csv, open(outfile, "w", newline='') as out_csv:
                csv_reader = csv.reader(in_csv, delimiter="\t") # add except rule, to check for other delimiter
                csv_writer = csv.writer(out_csv, delimiter=",")
                for row in csv_reader:
                    url = "https://www.druckereien.info/de/suche/ergebnis/536/{}+{}/drucksachen/alle.html".format(
                    row[0], row[1])
                    page = requests.get(url)
                    html_soup = BeautifulSoup(page.content, "html.parser")
                    # Get premium profiles
                    premium_profiles = html_soup.findAll("section", class_="premium_druckerei gainlayout")
                    #print("Premium Profiles: ", premium_profiles, "\nLength: ", len(premium_profiles))
                    for profile in premium_profiles:
                        profile_storage = profile.find("div", class_="row_adresse")
                        #print(profile_storage)
                        profile_string = list(profile_storage.findAll(text=True))
                        #print(profile_string, type(profile_string))
                        name = str(profile_string[1])
                        if name not in duplicate_checker:
                            shop_adress = str(profile_string[2])[3:]
                            telephone_num = str(profile_string[5])[6:]
                            #print(profile_string[2], profile_string[3], telephone_num)
                            profile_string[3] = str(profile_string[3])[3:]
                            postcode = re.findall(r'-?\d+\.?\d*', profile_string[3])[0]
                            town = re.sub(r'-?\d+\.?\d*', '', profile_string[3])
                            #print(postcode, type(postcode))
                            #print(town, type(town))

                            # Get profile url
                            url_storage = profile.find("a", class_="hl no_deco")
                            #print("profile name: ", profile_name, "type:", type(profile_name))
                            duplicate_checker.append(name)
                            rough_url = url_storage.get("href")
                            premium_profile_url = "https://www.druckereien.info/" + str(rough_url)
                            #print("Premium Profile Url: ", premium_profile_url)
                            adres_storage = profile.find("div", class_="row_adresse")


        except IOError:
            print("Error: cannot open file")
    else:
        pass


regional_totals("C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\obsoletedata\\test.csv",
                "C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\shops_per_city.csv", [])
