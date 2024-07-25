#!/usr/bin/env python3
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

day_of_week = {
    1: "Sunday",
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    7: "Saturday",
}


def main():
    html_doc: str

    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto("https://www.scaa.sc/index.php/seasonal-flight-schedule")
        html_doc = page.content()
        browser.close()

    soup = BeautifulSoup(html_doc, "html.parser")
    lines = soup.find_all("tr")
    tbl = []
    day = 0 # (eoea): first day of the week is Sunday, this counter gets incremented on the first pass below.

    for line in lines:
        tbl_row = {}
        html_txt = line.find_all("td")
        if html_txt:
            if (
                html_txt[0].text.strip() == "Flight Number"
                and html_txt[1].text.strip() == "From"
                and html_txt[2].text.strip() == "Arrival Time"
            ):
                day+=1
                continue

            tbl_row["Arrival_Day"] = day_of_week[day]
            tbl_row["Flight_Number"] = html_txt[0].text.strip()
            tbl_row["From"] = html_txt[1].text.strip()
            tbl_row["Arrival_Time"] = html_txt[2].text.strip()

            tbl.append(tbl_row)

    df = pd.DataFrame(tbl)

    df.to_csv("/tmp/skysc.csv", mode="w", index=False)
