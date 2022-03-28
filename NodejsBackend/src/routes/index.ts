import { scrapeArticles } from "./scraper/scrapeArticles"
import { Router, Request, Response } from "express"


const route = Router()

route.post("/scrapeArticles", scrapeArticles)

export default route