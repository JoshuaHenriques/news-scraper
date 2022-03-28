from ScraperFlaskServer.backend import app

def test_scrape():
    """
    WHEN the '/api/v1/scrape' page is is posted to (POST)
    WITH a valid request object
    ASSERT that the response from the endpoint is 200
    """
    with app.test_client() as test_client:

        request = {
                    "scrapeRequests": [
                        {
                            "scraper": "www.reuters.com",
                            "urls": [
                                "https://www.reuters.com/lifestyle/box-office-the-batman-scores-128-million-second-biggest-pandemic-debut-2022-03-06/",
                                "https://www.reuters.com/business/finance/how-wall-street-star-cathie-wood-is-defying-her-doubters-2022-03-14/",
                                "https://www.reuters.com/business/oil-prices-slide-extending-last-weeks-decline-2022-03-14/"
                            ],
                            "create": "domain_name"
                        }
                    ]
                }

        response = test_client.post('/api/v1/scrape', json=request)
        assert response.status_code == 200