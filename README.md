# Crawler

Fetch currency exchange rates from BOA site and save it to a file.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

First, get symbol-currency mapping from the site.
```bash
python get_currency_map.py
```
Check if the mapping is correct and edit the file if necessary.

Then, run the crawler to get the result.

Follow this pattern: `python crawler.py <date> <currency_symbol>`

e.g. `python crawler.py 20240101 USD`
```bash
python crawler.py YYYYMMDD CURRENCY_SYMBOL
```

The result will be saved to `result.txt`.


