# Mustapp Exporter to CSV.

Export your Must data to CSV. Must app scraper. 

## Requirements

- Python: https://www.python.org/downloads/

- Scrapy: `pip install scrapy`

## Usage

### TL;DR
To start script:
```
python main.py
```

### How to get your nickname?
Copy link to your profile, letters after `@` is your nickname.

Example: `https://mustapp.com/@username/`
nickname: `username`.


You will get two .CSV files:

- `want.csv` with columns: `Title`, `Year`.

- `watched.csv` with columns: `Title`, `Year`, `Rating10`, `WatchedDate`, `Review`.
