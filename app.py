import eel
from scrape_reviews import scrape_reviews
from scrape_data import fetch_movie_details
from sentiment import analyze_reviews

eel.init("web")


@eel.expose
def get_movie_data(imdb_id):
    details = fetch_movie_details(imdb_id)
    return details


@eel.expose
def start_analysis(imdb_id):
    details = fetch_movie_details(imdb_id)
    reviews = scrape_reviews(imdb_id)
    _, pos_pct, _ = analyze_reviews(reviews)

    result = {
        "title": details["title"],
        "poster_url": details["poster_url"],
        "avg_rating": details["avg_rating"],
        "rating_count": details["rating_count"],
        "review_count": details["review_count"],
        "pos_pct": round(pos_pct, 1)
    }
    return result


if __name__ == "__main__":
    eel.start("index.html", size=(800, 600))
