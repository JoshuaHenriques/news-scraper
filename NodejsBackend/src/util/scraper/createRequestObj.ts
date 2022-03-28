import { ScraperRequest } from "../../types/scraper/ScraperRequest"
import { ScrapeUrl } from "../../types/scraper/ScrapeUrl"

export const createRequestObj = (urls: string[]): ScraperRequest => {

	const scraperRequest: ScraperRequest = []
	const groupUrls: any = {} 

	urls.forEach((url: any) => {
		const urlObj = new URL(url)
		let hostname = urlObj.hostname

		if (!hostname.match(/(www\.)/g)) {
			hostname = "www." + hostname
		}

		const hostArr = hostname.split(".")
		if (hostArr.length > 3) {
			hostArr.splice(1,1)
			hostname = hostArr.join(".")
		}


		if (groupUrls.hasOwnProperty(hostname)) {
			groupUrls[hostname].push(urlObj.href)
		}
		else {
			groupUrls[hostname] = [urlObj.href]
		}
	})

	Object.entries(groupUrls).forEach(([key, value]: any) => {
		const scrapeurl: ScrapeUrl = {
			scraper: key,
			urls: value
		}
		scraperRequest.push(scrapeurl)
	})

	return scraperRequest
}
