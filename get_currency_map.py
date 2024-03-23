from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Firefox()


def scrape_currency_names():
    driver.get("https://www.11meigui.com/tools/currency")

    currency_table = driver.find_element(By.XPATH, '//table')
    rows = currency_table.find_elements(By.TAG_NAME, 'tr')

    currencies = []
    for row in rows[2:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) < 5:
            # print([cell.text.strip() for i, cell in enumerate(cells)])
            continue
        name = cells[1].text.strip()
        symbol = cells[4].text.strip()
        currencies.append([symbol, name])

    return currencies


def write_to_csv(currencies):
    with open('currencies.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'symbol'])
        writer.writerows(currencies)

try:
    currencies = scrape_currency_names()
    print(currencies)
    print(len(currencies))
    write_to_csv(currencies)
finally:
    driver.quit()
