import { Pool } from "pg";
import e, { Response, Request } from "express";
import { createRequestObj } from "../../util/scraper/createRequestObj";
import { ScraperRequest } from "../../types/scraper/ScraperRequest";
import { callScraper } from "../../apis/scraper/callScraper";
import {} from "../../apis/scraper/callScraper";
import {
  hasUrlBeenScraped,
  cacheScrapedArticles,
  retrieveCachedArticles,
} from "../../apis/database/dbAPI";
import { Article } from "../../types/entities/Article";

export const scrapeArticles = async (req: Request, res: Response) => {
  try {
    const urls: string[] = req.body.urls;
    const newUrls: string[] = [];
    const cachedUrls: string[] = [];

    const checkForCachedURLS = Promise.all(
      urls.map(async (url: string) => {
        if (await hasUrlBeenScraped(url)) {
          cachedUrls.push(url);
        } else {
          newUrls.push(url);
        }
      })
    );

    await checkForCachedURLS;

    // console.log(
    //   "Original List:\n",
    //   urls,
    //   "\n\ncached list:\n",
    //   cachedUrls,
    //   "\n\nnew list:\n",
    //   newUrls
    // );

    const returnData: Article[] = [];

    if (newUrls.length > 0) {
      const scraperRequest: ScraperRequest = createRequestObj(newUrls);
      const scrapedData: Article[] = (await callScraper(scraperRequest))[
        "articles"
      ];

      cacheScrapedArticles(scrapedData);

      scrapedData.map((article: Article) => {
        returnData.push(article);
      });
    }

    if (cachedUrls.length > 0) {
      const cachedData = await retrieveCachedArticles(cachedUrls);

      cachedData.map((article: any) => {
        returnData.push(article);
      });
    }

    res.setHeader("Content-Type", "application/json");
    res.json({ articles: returnData });
    res.end();
  } catch {
    res.end();
  }
};
