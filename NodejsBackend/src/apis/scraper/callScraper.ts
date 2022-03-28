import { ScraperRequest } from "../../types/scraper/ScraperRequest"
import fetch from "node-fetch";

export const callScraper = async (scraperRequest: ScraperRequest) => {
	try {
		const res = await fetch('http://localhost:5000/api/v1/scrape', {
			method: "POST",
			body: JSON.stringify({
				scrapeRequests: scraperRequest
			}),
			headers: {
			"Access-Control-Allow-Origin": "*",
			"Content-type": "application/json"
			},
		})
		const data = await res.json()
		return data
	} catch(e) {
		console.log(e)
	}
}