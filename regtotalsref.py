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
    outlist = []
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
                        dict_storage = {}
                        profile_storage = profile.find("div", class_="row_adresse")
                        #print(profile_storage)
                        profile_string = list(profile_storage.findAll(text=True))
                        #print(profile_string, type(profile_string))
                        dict_storage["name"] = str(profile_string[1])
                        if dict_storage["name"] not in duplicate_checker:
                            duplicate_checker.append(dict_storage["name"])
                            dict_storage["adress"] = str(profile_string[2])[3:]
                            dict_storage["telephone"] = str(profile_string[5])[6:]
                            profile_string[3] = str(profile_string[3])[3:]
                            dict_storage["postcode"] = re.findall(r'-?\d+\.?\d*', profile_string[3])[0]
                            dict_storage["town"] = re.sub(r'-?\d+\.?\d*', '', profile_string[3])
                            url_storage = profile.find("a", class_="hl no_deco")
                            rough_url = url_storage.get("href")
                            dict_storage["profile url"] = "https://www.druckereien.info/" + str(rough_url)
                            outlist.append(dict_storage)
                            #shop_adress = str(profile_string[2])[3:]
                            #telephone_num = str(profile_string[5])[6:]
                            #print(profile_string[2], profile_string[3], telephone_num)
                            #profile_string[3] = str(profile_string[3])[3:]
                            #postcode = re.findall(r'-?\d+\.?\d*', profile_string[3])[0]
                            #town = re.sub(r'-?\d+\.?\d*', '', profile_string[3])
                            #print(postcode, type(postcode))
                            #print(town, type(town))
                            #print("profile name: ", profile_name, "type:", type(profile_name))
                            #print("Premium Profile Url: ", premium_profile_url)
                        
                    # Get standard profiles
                    standard_profiles = html_soup.findAll("section", class_="standard_druckerei gainlayout")
                    for profile in standard_profiles:
                        dict_storage = {}
                        profile_storage = profile.find("div", class_="row_adresse")
                        #print(profile_storage)
                        profile_string = list(profile_storage.findAll(text=True))
                        dict_storage["name"] = str(profile_string[1])
                        #name = str(profile_string[1])
                        if dict_storage["name"] not in duplicate_checker:
                            duplicate_checker.append(dict_storage["name"])
                            dict_storage["adress"] = str(profile_string[2])[3:]
                            dict_storage["postcode"] = re.findall(r'-?\d+\.?\d*', profile_string[3])[0]
                            dict_storage["town"] = re.sub(r'-?\d+\.?\d*', '', profile_string[3])
                            telephone_storage = profile.find("div", class_="row_features")
                            telephone_string = list(telephone_storage.findAll(text=True)
                            dict_storage["telephone"] = str(telephone_string[0])[6:])
                            url_storage = profile.find("a", class_="hl no_deco")
                            rough_url = url_storage.get("href")
                            dict_storage["profile url"] = "https://www.druckereien.info/" + str(rough_url)
                            outlist.append(dict_storage)
                    navbar = html_soup.find("span", class_="databrowser_noajax")
                    next_url_storage = navbar.find("a", class_="next")
                    next_url_rough = navbar.get("href")
                    next_url = "https://www.druckereien.info/" + str(next_url_rough)
                    print("Next URL: ", next_url)
                    pre_outlist = regional_totals(next_url, outfile, duplicate_checker)
                    final_outlist = outlist + pre_outlist
                    for dictionary in final_outlist:
                        csv_writer.writerow(dictionary["name"] + dictionary["adress"] + dictionary["postcode"] + dictionary["town"] + dictionary["telephone"] + dictionary["profile url"])
        except IOError:
            print("Error: cannot open file")
    else:
        page = requests.get(infile)
        html_soup = BeautifulSoup(page.content, "html.parser")
        premium_profiles = html_soup.findAll("section", class_="premium_druckerei gainlayout")
        for profile in premium_profiles:
            dict_storage = {}
            profile_storage = profile.find("div", class_="row_adresse")
            profile_string = list(profile_storage.findAll(text=True))
            dict_storage["name"] = str(profile_string[1])
            if dict_storage["name"] not in duplicate_checker:
                duplicate_checker.append(dict_storage["name"])
                dict_storage["adress"] = str(profile_string[2])[3:]
                dict_storage["telephone"] = str(profile_string[5])[6:]
                profile_string[3] = str(profile_string[3])[3:]
                dict_storage["postcode"] = re.findall(r'-?\d+\.?\d*', profile_string[3])[0]
                dict_storage["town"] = re.sub(r'-?\d+\.?\d*', '', profile_string[3])
                url_storage = profile.find("a", class_="hl no_deco")
                rough_url = url_storage.get("href")
                dict_storage["profile url"] = "https://www.druckereien.info/" + str(rough_url)
                outlist.append(dict_storage)

        standard_profiles = html_soup.findAll("section", class_="standard_druckerei gainlayout")
        for profile in standard_profiles:
            dict_storage = {}
            profile_storage = profile.find("div", class_="row_adresse")
            profile_string = list(profile_storage.findAll(text=True))
            dict_storage["name"] = str(profile_string[1])
            if dict_storage["name"] not in duplicate_checker:
                duplicate_checker.append(dict_storage["name"])
                dict_storage["adress"] = str(profile_string[2])[3:]
                dict_storage["postcode"] = re.findall(r'-?\d+\.?\d*', profile_string[3])[0]
                dict_storage["town"] = re.sub(r'-?\d+\.?\d*', '', profile_string[3])
                telephone_storage = profile.find("div", class_="row_features")
                telephone_string = list(telephone_storage.findAll(text=True)
                dict_storage["telephone"] = str(telephone_string[0])[6:])
                url_storage = profile.find("a", class_="hl no_deco")
                rough_url = url_storage.get("href")
                dict_storage["profile url"] = "https://www.druckereien.info/" + str(rough_url)
                outlist.append(dict_storage)
        navbar = html_soup.find("span", class_="databrowser_noajax")
        next_url_storage = navbar.find("a", class_="next")
        next_url_rough = navbar.get("href")
        next_url = "https://www.druckereien.info/" + str(next_url_rough)
        print("Next URL: ", next_url)
        pre_outlist = regional_totals(next_url, outfile, duplicate_checker)
        final_outlist = outlist + pre_outlist

regional_totals("C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\obsoletedata\\test.csv",
                "C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\shops_per_city.csv", [])
