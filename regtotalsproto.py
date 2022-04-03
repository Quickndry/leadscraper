# Libraries and dependencies
import csv
import requests
from bs4 import BeautifulSoup
import math

# Function where a list containing city names and postcodes
def regional_totals(infile, outfile):
    try:
        with open(infile, "r") as in_csv, open(outfile, "w", newline='') as out_csv:
            csv_reader = csv.reader(in_csv, delimiter="\t")
            csv_writer = csv.writer(out_csv, delimiter=",")
            header = ["City", "Total stores"]
            totals_dict = {}
            avg_totals_dict = {}
            for row in csv_reader:
                #print("row: ", row)
                #print("row[0]: ", row[0], "row[1]", row[1])
                if row[1] not in totals_dict:
                    totals_dict[row[1]] = []
                url = "https://www.druckereien.info/de/suche/ergebnis/13726/{}+{}/drucksachen/alle.html".format(
                    row[0], row[1])
                page = requests.get(url)
                html_soup = BeautifulSoup(page.content, "html.parser")
                #print("html_soup: ", html_soup)
                html_extract = html_soup.find("div", style="margin-top:30px;")
                #print("html_extract: ", html_extract)
                extract_list = html_extract.findAll("i")
                #print("extract_list", extract_list)
                total_stores_rough = str(extract_list[2])
                #print("total_stores_rough: ", total_stores_rough, "\nType: ", type(total_stores_rough) )
                total_stores = int(total_stores_rough[3:-4])
                #print("total_stores: ", total_stores)
                totals_dict[row[1]].append(total_stores)
            #print("totals_dict: ", totals_dict)
            for k in totals_dict:
                average_total = sum(totals_dict[k]) / len(totals_dict[k])
                avg_totals_dict[k] = math.ceil(average_total)
            #print("avg_totals_dict: ", avg_totals_dict)
            csv_writer.writerow(header)
            for k in avg_totals_dict:
                new_row = str(k) + "," + str(avg_totals_dict[k])
                csv_writer.writerow([new_row])
    except IOError:
        print("Error: cannot open file")


regional_totals("C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\test.csv",
                "C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\shops_per_city.csv")
