# Libraries and dependencies
import csv
import requests
from bs4 import BeautifulSoup
import math
import time

# Function to scrape the homepage of an indexing website so as to obtain a 
# list of german provinces and the amount of ad agencies located there

def regional_totals(infile, outfile):
    try:
        with open(infile, "r") as in_csv, open(outfile, "w", newline='') as out_csv:
            csv_reader = csv.reader(in_csv, delimiter=",")
            csv_writer = csv.writer(out_csv, delimiter=",")
