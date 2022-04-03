# Function that takes a csv file and filters the postcodes contained
# by a set of predetermined cities - confirmed to work 04/2022.
import csv
from more_itertools import unique_everseen

def filterpst(infile, duplfile, outfile, lst):
    try:
        with open(infile, "r") as in_csv, open(duplfile, "w", newline='') as dupl_csv:
            csv_reader = csv.reader(in_csv, delimiter=",")
            csv_writer = csv.writer(dupl_csv, delimiter=",")
            for row in csv_reader:
                if row[1] in lst:
                    if len(row[0]) < 5:
                        adaptedcode = "0" + str(row[0])
                        csv_writer.writerow([adaptedcode] + [row[1]])
                    else:
                        csv_writer.writerow([row[0]] + [row[1]])
        with open(duplfile, "r") as dupl, open(outfile, "w", newline='') as out_csv:
            out_csv.writelines(unique_everseen(dupl))
    except IOError:
        print("Error: cannot open file")



# Input for function
list_of_cities = [
    "Berlin",
            "Hamburg",
            "München",
            "Köln",
            "Frankfurt am Main",
            "Stuttgart",
            "Düsseldorf",
            "Dortmund",
            "Essen",
            "Leipzig",
            "Bremen",
            "Dresden",
            "Hannover",
            "Nürnberg",
            "Duisburg",
            "Bochum",
            "Wuppertal",
            "Bielefeld",
            "Bonn",
            "Münster",
            "Karlsruhe",
            "Mannheim",
            "Augsburg",
            "Wiesbaden",
            "Gelsenkirchen",
            "Mönchengladbach",
            "Braunschweig",
            "Chemnitz",
            "Kiel",
            "Aachen",
            "Halle",
            "Madgeburg",
            "Freiburg im Bresgau",
            "Krefeld",
            "Lübeck",
            "Oberhausen",
            "Erfurt",
            "Mainz",
            "Rostock",
            "Kassel",
            "Hagen",
            "Hamm",
            "Saarbrücken",
            "Mülheim an der Ruhr",
            "Potsdam",
            "Ludwigshafen am Rhein",
            "Oldenburg",
            "Leverkusen",
            "Osnabrück",
            "Solingen",
            "Heidelberg",
            "Herne",
            "Neuss",
            "Darmstadt",
            "Paderborn",
            "Regensburg",
            "Ingolstadt",
            "Würzburg",
            "Fürth",
            "Wolfsburg",
            "Offenbach am Main",
            "Ulm",
            "Heilbronn",
            "Pforzheim",
            "Göttingen",
            "Bottrop",
            "Trier",
            "Recklingshausen",
            "Reutlingen",
            "Bremerhaven",
            "Koblenz",
            "Bergisch Gladbach",
            "Jena",
            "Remscheid",
            "Erlangen",
            "Moers",
            "Siegen",
            "Hildesheim",
            "Salzgitter",
            "Kaiserlautern"]

filterpst("C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\PLZ_2021.csv",
          "C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\plz_duplicates.csv", "C:\\Users\\wazza\\OneDrive\\Documents\\GitHub\\leadscraper\\data\\plz_refined.csv", list_of_cities)
