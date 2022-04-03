# Libraries and dependencies
import csv
import requests
from bs4 import BeautifulSoup
import math
import time

# Function that scrapes the total number of store profiles for each city & postcode pair searched for and adds
# it to a dictionary and list, which are then used to find the average number of store profiles per city. These
# are then written into target csv file.
def regional_totals(infile, outfile):
    try:
        with open(infile, "r") as in_csv, open(outfile, "w", newline='') as out_csv:
            csv_reader = csv.reader(in_csv, delimiter=",")
            csv_writer = csv.writer(out_csv, delimiter=",")
            header = ["City", "Total stores"]
            totals_dict = {}
            avg_totals_dict = {}
            for row in csv_reader:
                if row[1] not in totals_dict:
                    totals_dict[row[1]] = []
                url = "https://www.druckereien.info/de/suche/ergebnis/13726/{}+{}/drucksachen/alle.html".format(
                    row[0], row[1])
                page = requests.get(url)
                html_soup = BeautifulSoup(page.content, "html.parser")
                html_extract = html_soup.find("div", style="margin-top:30px;")
                if html_extract != None:
                    extract_list = html_extract.findAll("i")
                    total_stores_rough = str(extract_list[2])
                    total_stores = int(total_stores_rough[3:-4])
                    totals_dict[row[1]].append(total_stores)
                    #time.sleep(1)
            for k in totals_dict:
                try:
                    average_total = sum(totals_dict[k]) / len(totals_dict[k])
                except ZeroDivisionError:
                    average_total = 0
                avg_totals_dict[k] = math.ceil(average_total)

            csv_writer.writerow(header)
            for k in avg_totals_dict:
                csv_writer.writerow([k] + [avg_totals_dict[k]])
    except IOError:
        print("Error: cannot open file")


regional_totals("C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\plz_umlaute.csv",
                "C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\shops_per_city.csv")
