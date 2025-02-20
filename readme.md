# IMDb Analyzer Desktop App

A desktop application built with [Eel](https://github.com/ChrisKnott/Eel) that allows you to calculate an user review score of any IMDb material.

- Uses BeautifulSoup to fetch data from IMDb.
- Uses Selenium (with a user-specified WebDriver) to scrape user reviews.
- Uses Hugging Face's Transformers (DistilBERT fine-tuned on SST-2) to compute the percentage of positive reviews. 
- Requires Torch, CUDA is recommended.
- A web-based interface (using Eel) with a two-column layout.
- Requires a chrome webdriver (https://developer.chrome.com/docs/chromedriver/downloads). Modify the config.py file with the path to your webdriver.
- Install packages from requirements.txt:

pip install -r requirements.txt

- Launch it by opening app.py
- The IMDb ID is the last part of an IMDb media link. For example, in https://www.imdb.com/title/tt0111161/ the ID is tt0111161.
- The app is slow for movies with many reviews since it uses Selenium to load them all.
- Calculates an user approval score based on amount of positive and negative reviews.
