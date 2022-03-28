import { useCallback, useContext } from "react"
import { ArticlesContext } from "../interfaces/ArticlesContextData"

export const useArticlesManagement = () => {
	const { scrapeArticles } = useContext(ArticlesContext)

	const handleArticleScrape = useCallback((urls: string) => {
		scrapeArticles(urls)
	}, [scrapeArticles])

	return {
		handleArticleScrape
	}
}