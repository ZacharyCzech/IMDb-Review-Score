import requests
from bs4 import BeautifulSoup


def fetch_movie_details(imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/110.0.0.0 Safari/537.36")
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve page, status code {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1", {"data-testid": "hero-title-block__title"})
    if title_tag is None:
        title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "N/A"

    poster_url = "N/A"
    poster_container = soup.find("div", {"data-testid": "hero-media__poster"})
    if not poster_container:
        poster_container = soup.find("div", class_="poster")
    if poster_container:
        img_tag = poster_container.find("img")
        if img_tag and img_tag.get("src"):
            poster_url = img_tag["src"]
            if "._V1_" in poster_url:
                poster_url = poster_url.split("._V1_")[0] + "._V1_.jpg"

    rating_tag = soup.find("span", {"data-testid": "hero-rating-bar__aggregate-rating__score"})
    if rating_tag is None:
        rating_tag = soup.find("span", class_="sc-d541859f-1 imUuxf")
    avg_rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

    rating_count_div = soup.find("div", class_="sc-d541859f-3 dwhNqC")
    rating_count = rating_count_div.get_text(strip=True) if rating_count_div else "N/A"

    review_reference = soup.find("div", {"data-testid": "reviews-header"})
    review_count = "N/A"
    if review_reference:
        review_count_span = review_reference.find_next("span", class_="ipc-title__subtext")
        if review_count_span:
            review_count = review_count_span.get_text(strip=True)

    return {
        "title": title,
        "poster_url": poster_url,
        "avg_rating": avg_rating,
        "rating_count": rating_count,
        "review_count": review_count
    }