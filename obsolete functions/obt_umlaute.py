# Function that takes two csv files and a list, to filter
# out data from one into the other according to content of 
# the list. 

# Dependencies
import csv

def umlaute(infile, outfile, lst):
    try:
        with open(infile, "r", encoding="utf8") as in_csv, open(outfile, "w", newline='', encoding='utf-8') as dupl_csv:
            csv_reader = csv.reader(in_csv, delimiter=",")
            csv_writer = csv.writer(dupl_csv, delimiter=",")
            for row in csv_reader:
                for umlaut in lst:
                    if umlaut in row[1]:
                        csv_writer.writerow([row[0]] + [row[1]])            
    except IOError:
        print("Error: cannot open file")


list_of_umlaute = ["ä", "ü", "ö", "Ä", "Ü", "Ö"]

umlaute("C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\plz_refined.csv", "C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\plz_umlaute.csv", list_of_umlaute)