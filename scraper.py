"""
A script to get csv file from henry hub gas prices.
"""
import csv
from urllib.parse import urljoin

import requests
import xlrd
from bs4 import BeautifulSoup


def main():
    # id = rngwhhd
    # day mark = D
    # week mark = W
    # so, rngwhhdD is daily data

    url = "https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    xls_link = soup.select_one("[href*='hist_xls']")

    xls_abs_url = urljoin(url, xls_link["href"])
    response = requests.get(xls_abs_url)

    workbook = xlrd.open_workbook(file_contents=response.content)
    sheet = workbook.sheet_by_name("Data 1")

    data = []
    for row in sheet.get_rows():
        if row[0].ctype == 3 : # date
            date = xlrd.xldate_as_datetime(row[0].value, 0).date().isoformat()
            price = row[1].value
            data.append([date, price])

    header = ['Date', 'Price']

    with open('daily_henry_hub_gas.csv', 'w') as dail_henry_hub:
        writer = csv.writer(dail_henry_hub)
        writer.writerow(header)
        writer.writerows(data)


if __name__ == "__main__":
    main()
