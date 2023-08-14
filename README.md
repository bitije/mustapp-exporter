# Mustapp Exporter to CSV.

Export your Must data to CSV. Must app scraper. 

## Installation

Python -> https://www.python.org/downloads/

Download `scrapy`. Enter in console:
```
$ python -m pip install scrapy
```

## Usage

### How to get your nickname?
Copy link to your profile, letters after `@` is your nickname.

Example: `https://mustapp.com/@username/`
nickname: `username`.

Go to directory where script is located then use it from here:
```
python main.py
```

You will get two .CSV files in the same directory:

- `want.csv` with columns: `Title`, `Year`.

- `watched.csv` with columns: `Title`, `Year`, `Rating10`, `WatchedDate`, `Review`.
