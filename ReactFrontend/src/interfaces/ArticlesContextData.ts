import { createContext } from "react"
import { Article } from "./Article"

export interface ArticlesContextData {
	articles: Article[]
	scrapeArticles: (urls: string) => void
}

export const articlesContextDefaultValue: ArticlesContextData = {
	articles: [],
	scrapeArticles: () => null 
}

export const ArticlesContext = createContext<ArticlesContextData>(articlesContextDefaultValue)