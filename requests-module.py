import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def read_txt(textFile):
    try:
        with open(textFile,"r") as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    except FileNotFoundError:
        return []

def check_create_csv(filename,df):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Deleted file: {filename}")
    df.to_csv(filename,index=False)
    print(f"Created file: {filename}")

def make_requests(urls,fields):
    toExcelDf = pd.DataFrame()
    resDictList = []
    #go to website
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    for url in urls:
        response = requests.get(url,headers=headers)
        if response.status_code == 404:
            print("Not found...")
            continue

        elif response.status_code == 200:
            html_returned = response.text
            soup = BeautifulSoup(html_returned,"html.parser")
            resDict = {}

            for element in soup.select(".productDetailsTable_DataLabel"):
                #print(element.text+" : "+element.find_next_sibling('td').text)
                resDict[element.text]=  element.find_next_sibling('td').text.strip()

            resDictList.append(resDict)

        else:
            print("Status code {0}:".format(response.status_code))
            continue

    df = pd.DataFrame(resDictList)
    #write df to csv
    check_create_csv("Siemens Lookup.csv",df.filter(items=fields))


def main():
    #input handling
    #get attrs from txt File
    desiredInfo = read_txt("ItemAttrs.txt")
    #get all Part No.'s from txt File
    desiredPartNo = read_txt("PartNo.txt")
    #formulate urls
    urls = [f"https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/{part}" for part in desiredPartNo]
    make_requests(urls,desiredInfo)


if __name__=="__main__":
    main()




