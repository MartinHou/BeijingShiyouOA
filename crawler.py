import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import csv
import sys


def get_date(old_date):
    return f'{old_date[:4]}-{old_date[4:6]}-{old_date[6:]}'


def get_currency_name(currency_file_path, currency_symbol):
    with open(currency_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == currency_symbol:
                return row[1]


def get_exchange_rate(dt, currency):
    print('Reaching BOC website...')
    driver.get("https://www.boc.cn/sourcedb/whpj/")
    print('BOC website reached')

    date_input = driver.find_element(By.NAME, 'nothing')
    date_input.send_keys(dt)
    print(f'date element changed: {date_input.get_attribute("value")}')

    currency_input = driver.find_element(By.NAME, 'pjname')
    select_obj = Select(currency_input)
    select_obj.select_by_value(currency)
    print('currency element changed')

    search_button = driver.find_element(By.XPATH, "//div[@class='invest_t']//input[@class='search_btn']")
    search_button.click()
    print('search button clicked')

    # wait for the table to load
    WebDriverWait(driver, 10, 1).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="BOC_main publish"]//tbody')))
    print('new table found')

    rate_table = driver.find_element(By.XPATH, '//div[@class="BOC_main publish"]//tbody')
    rows = rate_table.find_elements(By.TAG_NAME, "tr")
    if len(rows) > 1:
        return rows[1].find_elements(By.TAG_NAME, "td")[3].text


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 crawler.py YYYYMMDD currency_code")
        sys.exit(1)

    date = sys.argv[1]
    currency_code = sys.argv[2]
    if len(date) != 8:
        print('Invalid date, please input date in format of YYYYMMDD')
        sys.exit(1)
    date = get_date(date)
    print(f'Fetching {currency_code}, on {date}')

    # get currency name
    currency_name = get_currency_name('currencies.csv', currency_code)
    if currency_name is None:
        print(f'Currency not found: {currency_code}')
        sys.exit(1)
    print(f'Currency Name: {currency_name}')

    # anti-detection
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument("window-size=1920x1080")
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    firefox_options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Firefox(options=firefox_options)

    try:
        rate = get_exchange_rate(date, currency_name)
        print(f'Exchange Rate: {rate}')
        with open('result.txt', 'w') as f:
            f.write(f'{currency_code},{rate}')
    except Exception as e:
        print('Error occurred', e)
    finally:
        driver.quit()
