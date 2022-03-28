import json
from flask_cors import cross_origin
from flask import Flask, request


if __package__ is None or __package__ == '':
    from XP_Scraper.ScraperAPI import ScraperAPI
else:
    from .XP_Scraper.ScraperAPI import ScraperAPI


app = Flask(__name__)


@app.route('/api/v1/scrape', methods=['POST'])
@cross_origin()
def scrape_sites() -> dict:
    if request.method == 'POST':
        try:
            requestJSON = request.json

            responseJSON = {}
            if "scrapeRequests" in requestJSON:
                scrapeRequests = requestJSON["scrapeRequests"]

                # As it is, the request json isn't being verified,
                # This verification can be done here at the cost of having to iterate over the entire request json
                # Or within the scraperAPI as it is being loaded in to the custom json object.
                # IF you want to implement it here the you should probably extract the json building from the api and put it here as well.

                scraper = ScraperAPI()

                articlesJSON = json.loads(scraper.runSpiders(scrapeRequests))

                responseJSON['articles'] = articlesJSON

                return(responseJSON)
            else:
                return  "No scrape requests found", 400
        except: 
            return "Request Body invalid!", 400

    return request.json

