# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:39:44 2019

@author: Krishna, Abhigna, Lucy
"""

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import json

my_url = 'https://www.indeed.fr/Paris-(75)-Emplois-job-etudiant'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
csvFilePath = "ContractTypes.csv"
jsonFilePath = "ContractTypes.json"
arr = []

#Scraps and gets the Job Descriptions posted in the website
def jobDetails(page_soup):
    containers = page_soup.findAll("div", {"class": "jobsearch-SerpJobCard"})
    container = containers[0]
    filenm = "Jobs.csv"
    f = open(filenm, "w")
    headers = "Title, Company, Location \n"
    for container in containers:
        title = container.a["title"]
        companyContainer = container.findAll("div", {"class": "sjcl"})
        company = companyContainer[0].span.text.strip()
        summaryContainer = container.findAll("div", {"class": "summary"})
        summary = summaryContainer[0].text.strip()
        f.write(headers)
        f.write(title.replace(",", "|") + "," + company.replace(",", "|") + "," + summary.replace(",", "|") + "\n")
    csvfile = open('Jobs.csv', 'r')
    jsonfile = open('Jobs.json', 'w')
    fieldnames = ("title", "company", "summary")
    reader = csv.DictReader(csvfile, fieldnames)
    out = json.dumps([row for row in reader])
    jsonfile.write(out)
    f.close()

#Gets Roles of the needed Job profiles/Resumes
def getRoles():
    role_url = 'https://resumes.indeed.com/search?q=java&l=&searchFields=jt'
    uClient = uReq(role_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    searcher = page_soup.findAll("div", {"class": "rezemp-ResumeSearchCard"})
    f = open("Roles.csv", "w")
    for search in searcher:
        title = search.a["title"]
        f.write("Roles")
        f.write(title.replace(",", "|") + "\n")
    f.close()

#Gets the Contract type of set of available jobs fetched
def contractType(page_soup):
    contracts = page_soup.findAll("div", {"class": "rbsrbo"})
    f = open("ContractTypes.csv", "w")
    headers = "ContractType \n"
    for contract in contracts:
        # title = contract.a["title"]
        contContainer = contract.findAll("span", {"class": "rbLabel"})
        for cont in contContainer:
            contr = cont.text.strip()
            f.write(headers)
            f.write(contr.replace(",", "|") + "\n")

    f.close()

#Reads generated CSV file
with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    print(csvReader)
    for csvRow in csvReader:
        arr.append(csvRow)

print(arr)

# Write the data to a json file
with open(jsonFilePath, "w") as jsonFile:
    jsonFile.write(json.dumps(arr, indent=4))

if __name__ == "__main__":
    # getRoles()
    jobDetails(page_soup)
    contractType(page_soup)








